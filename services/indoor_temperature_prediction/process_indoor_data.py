# getting the utils file here
import os, sys

import xbos_services_getter as xsg
import datetime
import pytz
import numpy as np
import pandas as pd
import itertools
from pathlib import Path
import pickle

# UNRELATED THOUGHTS: Should any preprocessing happen in outdoor temperatures microservice?
# YES. And there should be an option to preprocess in inddoor data service with a trained thermal model.

HEATING_ACTION = 1
COOLING_ACTION = 2


def store_data(data, building, zone, cache_name):
    data_dir = Path.cwd() / "services_data" / cache_name / building
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    file_path = data_dir / (zone + ".pkl")

    with open(str(file_path), "wb") as f:
        pickle.dump(data, f)


def load_data(building, zone, cache_name):
    data_dir = Path.cwd() / "services_data" / cache_name / building
    if not os.path.isdir(data_dir):
        return None

    file_path = data_dir / (zone + ".pkl")
    if not os.path.isfile(file_path):
        return None

    with open(str(file_path), "rb") as f:
        return pickle.load(f)


def _get_indoor_temperature_historic(stub, building, zone, start, end, window):
    loaded_data = load_data(building, zone, "indoor_temperature_historic_cache")
    err = xsg.check_data(loaded_data, start, end, window)
    if (loaded_data is not None) and (err is None):
        return loaded_data

    indoor_temperature = xsg.get_indoor_temperature_historic(stub, building, zone, start, end,
                                                             window)
    store_data(indoor_temperature, building, zone, "indoor_temperature_historic_cache")
    return indoor_temperature


def _get_action_historic(stub, building, zone, start, end, window):
    loaded_data = load_data(building, zone, "action_historic_cache")
    err = xsg.check_data(loaded_data, start, end, window)
    if (loaded_data is not None) and (err is not None):
        return loaded_data

    action_historic = xsg.get_actions_historic(stub, building, zone, start, end,
                                                             window)
    store_data(action_historic, building, zone, "action_historic_cache")
    return action_historic


def get_preprocessed_data(building, zone, start, end, window, raw_data_granularity="1m"):
    """Get training data to use for indoor temperature prediction.

    :param building: (str) building name
    :param zone: (str) zone name
    :param start: (datetime timezone aware)
    :param end: (datetime timezone aware)
    :param window: (str) the intervals in which to split data.
    :param raw_data_granularity: (str) the intervals in which to get raw indoor data.
    :return: pd.df index= start (inclusive) to end (not inclusive) with frequency given by window.
            col=["t_in", "action",  "t_out", "t_next", "occ", "action_duration", "action_prev",
            "temperature_zone_...", "dt"]. TODO explain meaning of each feature somewhere.

    """

    # get indoor temperature and action for current zone
    indoor_historic_stub = xsg.get_indoor_historic_stub()
    indoor_temperatures = _get_indoor_temperature_historic(indoor_historic_stub, building, zone, start, end,
                                                             raw_data_granularity)
    indoor_actions = _get_action_historic(indoor_historic_stub, building, zone, start, end, raw_data_granularity)

    # get indoor temperature for other zones.
    building_zone_names_stub = xsg.get_building_zone_names_stub()
    all_zones = xsg.get_zones(building_zone_names_stub, building)
    all_other_zone_temperature_data = {}
    for iter_zone in all_zones:
        if iter_zone != zone:
            all_other_zone_temperature_data[iter_zone] = _get_indoor_temperature_historic(indoor_historic_stub,
                                                                 building, iter_zone, start, end, window)

    # Preprocessing indoor data putting temperature and action data together.
    indoor_data = pd.concat([indoor_temperatures.to_frame(name="t_in"), indoor_actions.to_frame(name="action")], axis=1)
    preprocessed_data = preprocess_indoor_data(indoor_data, xsg.get_window_in_sec(window))
    if preprocessed_data is None:
        return None, "No data left after preprocessing."

    # get historic outdoor temperatures
    outdoor_historic_stub = xsg.get_outdoor_historic_stub()
    outdoor_historic_temperatures = xsg.get_outdoor_temperature_historic(outdoor_historic_stub, building, start, end, window)

    # getting occupancy
    # get occupancy
    occupancy_stub = xsg.get_occupancy_stub()
    occupancy = xsg.get_occupancy(occupancy_stub, building, zone, start, end, window)

    # add outdoor and occupancy and other zone temperatures
    preprocessed_data["t_out"] = [outdoor_historic_temperatures.loc[
                              idx: idx + datetime.timedelta(seconds=xsg.get_window_in_sec(window))].mean() for idx in
                                  preprocessed_data.index]

    preprocessed_data["occ"] = [occupancy.loc[
                              idx: idx + datetime.timedelta(seconds=xsg.get_window_in_sec(window))].mean() for idx in
                            preprocessed_data.index]

    for iter_zone, iter_data in all_other_zone_temperature_data.items():
        preprocessed_data["temperature_zone_" + iter_zone] = [
            iter_data.loc[idx: idx + datetime.timedelta(seconds=xsg.get_window_in_sec(window))].mean() for idx in
            preprocessed_data.index]

    # TODO check if we should drop nan values... or at least where they are coming from
    preprocessed_data = preprocessed_data.dropna(axis=0)

    return preprocessed_data, None


def convert_categorical_action(data, num_start, num_end, interval_thermal):
    """Converting the categorical action variable to dummy variables (one hot encoding). Takes into account for how
        long the action has been going.
        Motivation:

        We try to learn the first n+1 discrete timesteps (e.g. in 5 min intervals) of the
        infinite convolution of the response function. We assume that n+1th timestep gives us the steady-state solution.
        Similarly, we learn the n+1 discrete timesteps of the tail of a convolution of the
        response function which reached steady state at one point.

    :param data: pd.df with minimal columns = ["action_duration", "dt", "action", "action_prev"]
    :param num_start: (int) The timesteps to count since the current action has started.
    :param num_end: (int) The timesteps to count after the last action has ended.
    :param interval_thermal: (int) the seconds inbetween timesteps.
    :return: pd.df: data with added columns
        • action_heat/cool_i (indicating it's the ith timestep since heating/cooling has started),
        • action_prev_heat/cool_i (indicating that it's the ith timestep
        since the previous heating/cooling action has ended)

    """
    action_duration = data["action_duration"]
    dt = data["dt"]
    action = data["action"]
    previous_action = data["action_prev"]

    for iter_action, iter_num_start in itertools.product([HEATING_ACTION, COOLING_ACTION], list(range(num_start))):
        if HEATING_ACTION == iter_action:
            action_name = "heat"
        else:
            action_name = "cool"

        if iter_num_start != num_start - 1:
            data["action_" + action_name + "_" + str(iter_num_start)] = 1.0 * (
                        (action == iter_action) & (((action_duration - dt) // interval_thermal) == iter_num_start))
        else:
            data["action_" + action_name + "_" + str(iter_num_start)] = 1.0 * (
                        (action == iter_action) & (((action_duration - dt) // interval_thermal) >= iter_num_start))

    for iter_action, iter_num_end in itertools.product([HEATING_ACTION, COOLING_ACTION], list(range(num_end))):
        if HEATING_ACTION == iter_action:
            action_name = "heat"
        else:
            action_name = "cool"

        if iter_num_end != num_end - 1:
            data["action_prev_" + action_name + "_" + str(iter_num_end)] = 1.0 * ((previous_action == iter_action) & (
                        ((action_duration - dt) // interval_thermal) == iter_num_end))
        else:
            data["action_prev_" + action_name + "_" + str(iter_num_end)] = 1.0 * ((previous_action == iter_action) & (
                        ((action_duration - dt) // interval_thermal) >= iter_num_end))

    return data


def add_feature_last_temperature(data):
    """Adding a feature which specifies what the previous temperature was "dt" seconds before the current
    datasample. Since data does not need be continious, we need a loop.
    :param: pd.df with cols: "t_in", "dt" and needs to be sorted by time index.
    returns pd.df with cols "t_prev" added. """

    if data.shape[0] == 0:
        data["t_prev"] = []
        return data

    last_temps = []

    last_temp = None
    curr_time = data.index[0]
    for index, row in data.iterrows():

        if last_temp is None:
            last_temps.append(row["t_in"])  # so the feature will be zero instead
        else:
            last_temps.append(last_temp)

        if curr_time == index:
            last_temp = row["t_in"]
            curr_time += datetime.timedelta(seconds=row["dt"])
        else:
            last_temp = None
            curr_time = index + datetime.timedelta(seconds=row["dt"])

    data["t_prev"] = np.array(last_temps)
    return data


def indoor_data_cleaning(data):
    """Fixes up the data. Makes sure we count two stage as single stage actions, don't count float actions,
     fill's nan's in action_duration, sorts data by time index.
    :param data: pd.df col includes "action", "dt", "action_duration". "dt" and "action_duration"
    columns have string values. index should be timerseries.
    :return: cleaned data."""

    def f(x):
        if x == 0:
            return 0
        elif x == 2 or x == 5:
            return 2
        elif x ==1 or x == 3:
            return 1
        else:
            return -1

    data["action"] = data["action"].map(f)
    data = data[data["action"] != -1]

    # fill nans
    data = data.fillna(-1)  # set all nan values to negative one.
                            # Note: Previous action with -1 is counted as if no action happened before.

    data.sort_index()

    return data


def preprocess_indoor_data(indoor_data, interval):
    """Combines contigious data -- i.e. is contigious in time and has the same action.
    Every datapoint knows how many seconds ago the last change of action happened (action_duration)
    and knows what the last action was (action_prev).
    :param zone_data: pd col=("action", "t_in"), Index needs to be continuous in time.
    :param interval: float:seconds The maximum length in seconds of a grouped data block.
    :returns: {zone: pd.df columns: 'time' (datetime), 't_in' (float), 't_next' (float),
    'dt' (int), 'action' (float), 'action_prev' (float), 'action_duration' (int)}
    No nan values except potentially in action_prev column -- means that we don't know the last action.
    """

    if indoor_data.shape[0] == 0:
        return None

    data_list = []

    first_row = indoor_data.iloc[0]

    # init our variables.
    start_time = indoor_data.index[0]
    last_time = start_time  # last valid time. To account for temperatures which are nan values.

    curr_action = first_row["action"]
    start_temperature = first_row["t_in"]

    # last not None temperature.
    last_temperature = start_temperature

    # whether the current datablock is valid. (datablock is a contigious grouping of same action datapoints)
    is_valid_block = not (np.isnan(curr_action) or np.isnan(start_temperature))

    # setting action start/end counters.
    curr_action_start = start_time
    action_prev = np.nan  # Assume last action has been going on forever before current action.

    # start loop
    for index, row in indoor_data.iterrows():

        # if actions are None we just move on
        if np.isnan(curr_action) and np.isnan(row["action"]):
            continue

        # if action is the current action (we can assume that actions are valid, but starting temperatures may not be.)
        if curr_action == row["action"]:

            if not np.isnan(row["t_in"]):
                if index >= start_time + datetime.timedelta(seconds=interval):
                    # add datapoint and restart
                    if is_valid_block:
                        data_list.append({
                            'time': start_time,
                            't_in': start_temperature,
                            't_next': row["t_in"],
                            'dt': int((index - start_time).total_seconds()),
                            'action': curr_action,
                            'action_prev': action_prev,
                            'action_duration': int((index - curr_action_start).total_seconds())})

                    # restart fields
                    start_temperature = row["t_in"]
                    start_time = index
                    is_valid_block = not (np.isnan(curr_action) or np.isnan(start_temperature))

                # if not valid block but we have found a non-nan starting temperature, restart block
                if not is_valid_block:
                    start_temperature = row["t_in"]
                    start_time = index
                    is_valid_block = not (np.isnan(curr_action) or np.isnan(start_temperature))

                # remember last valid temperature with same action
                last_temperature = row["t_in"]
                last_time = index


            else:
                # if times match we set t_next to the last valid temperature and time
                if index >= start_time + datetime.timedelta(seconds=interval):
                    if is_valid_block:
                        data_list.append({
                            'time': start_time,
                            't_in': start_temperature,
                            't_next': last_temperature,
                            'dt': int((last_time - start_time).total_seconds()),
                            'action': curr_action,
                            'action_prev': action_prev,
                            'action_duration': int((last_time - curr_action_start).total_seconds())})

                    # restart fields. This will make it an invalid block
                    start_temperature = row["t_in"]
                    start_time = index
                    is_valid_block = not (np.isnan(curr_action) or np.isnan(start_temperature))

        # if action is not the current action
        else:
            if not np.isnan(row["t_in"]):
                if is_valid_block:
                    data_list.append({
                        'time': start_time,
                        't_in': start_temperature,
                        't_next': row["t_in"],
                        'dt': int((index - start_time).total_seconds()),
                        'action': curr_action,
                        'action_prev': action_prev,
                        'action_duration': int((index - curr_action_start).total_seconds())})
            else:
                if is_valid_block:
                    data_list.append({
                        'time': start_time,
                        't_in': start_temperature,
                        't_next': last_temperature,
                        'dt': int((last_time - start_time).total_seconds()),
                        'action': curr_action,
                        'action_prev': action_prev,
                        'action_duration': int((last_time - curr_action_start).total_seconds())})

            # restart the whole block.
            action_prev = curr_action
            curr_action_start = index

            curr_action = row["action"]
            start_temperature = row["t_in"]
            start_time = index

            last_temperature = row["t_in"]
            last_time = index

            is_valid_block = not (np.isnan(curr_action) or np.isnan(start_temperature))

    # add last datapoint
    if start_time != indoor_data.index[-1] and is_valid_block:
        data_list.append({
            "time": start_time,
            't_in': start_temperature,
            't_next': last_temperature,
            'dt': int((last_time - start_time).total_seconds()),
            'action': curr_action,
            'action_prev': action_prev,
            'action_duration': int((last_time - curr_action_start).total_seconds())})

    # if no datapoints could be created, we return None.
    if data_list == []:
        return None

    preprocessed_indoor_data = pd.DataFrame(data_list).set_index('time')

    return preprocessed_indoor_data


if __name__ == "__main__":
    import time
    bldg = "ciee"
    zone = "HVAC_Zone_Southzone"
    end = datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(hours=20)
    start = end - datetime.timedelta(days=5)

    getting_training_data_time = time.time()
    data = get_training_data(bldg, zone, start, end, "5m")
    print(data)
    print("Time to get training data:", time.time() - getting_training_data_time)

    # building = 'ciee'
    # zone = "HVAC_Zone_Northzone"
    #
    # end = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    # start = end - datetime.timedelta(hours=2)
    #
    # bw_client = Client()
    # bw_client.setEntityFromEnviron()
    # bw_client.overrideAutoChainTo(True)
    # hod_client = HodClient("xbos/hod", bw_client)
    # mdal_client = mdal.MDALClient("xbos/mdal")
    #
    # indoor = _get_raw_indoor_temperatures(building, zone, mdal_client, hod_client, start, end, "1m")
    # action = _get_raw_actions(building, zone, mdal_client, hod_client, start, end, "1m")
    # print(preprocess_thermal_data(indoor, action, 15))

    # ==== TESTS FOR PREPROCESSING ====
    # start = datetime.datetime(year=2018, month=5, day=1, hour=0, minute=0)
    #
    # # create test cases
    # test_cases = []
    #
    # tin = [np.nan, 2, 1]
    # action = [0, 1, 2]
    # test_cases.append([tin, action])
    #
    # tin = [1, np.nan, 2, 1]
    # action = [1, 0, 1, 2]
    # test_cases.append([tin, action])
    #
    # tin = []
    # action = []
    # test_cases.append([tin, action])
    #
    # tin = [-2]
    # action = [12]
    # test_cases.append([tin, action])
    #
    # tin = [1, 2, 3, 4, np.nan, 6, 7]
    # action = [0, 0, np.nan, 0, 0, 0, 0]
    # test_cases.append([tin, action])
    #
    # tin = [1, 2, 3, 4, np.nan, 6, 7]
    # action = [0, 0, np.nan, 0, 0, 2, 2]
    # test_cases.append([tin, action])
    #
    # tin = [np.nan, 2, 3, 4, np.nan, 6, 7]
    # action = [0, 0, np.nan, 0, 0, 2, 2]
    # test_cases.append([tin, action])
    #
    # tin = [1, 2, 3, 4, np.nan, 6, 7]
    # action = [np.nan, 0, np.nan, 0, 0, 2, 2]
    # test_cases.append([tin, action])
    #
    # action = [np.nan, 0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0, 0, 2, 2]
    # tin = list(range(len(action)))
    # test_cases.append([tin, action])
    #
    # tin = [1, np.nan, 3, 4, 5, 6, 7, 8, 9, 10]
    # action = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # test_cases.append([tin, action])
    #
    # for case in test_cases:
    #     tin = case[0]
    #     action = case[1]
    #     assert len(tin) == len(action)
    #     end = start + datetime.timedelta(minutes=len(tin) - 1)
    #
    #     test_data = pd.DataFrame(index=pd.date_range(start, end, freq="1T"), data={"t_in": tin, "action": action})
    #     print(test_data)
    #     print("processed", _preprocess_thermal_data(test_data, 5))
    #     print("")
    # # ==== END ====

