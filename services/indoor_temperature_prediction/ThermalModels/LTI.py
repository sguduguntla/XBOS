
import numpy as np
import pandas as pd
import itertools

import os, sys
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
xbos_services_path = os.path.dirname(os.path.dirname(os.path.dirname(FILE_PATH)))
sys.path.append(xbos_services_path)
import utils3 as utils
from ParentThermalModel import ParentThermalModel

from scipy.optimize import curve_fit


def get_window_in_sec(s):
    """Returns number of seconds in a given duration or zero if it fails.
       Supported durations are seconds (s), minutes (m), hours (h), and days(d)."""
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return float(s[:-1]) * seconds_per_unit[s[-1]]
    except:
        return 0


# following model also works as a sklearn model.
class LTI(ParentThermalModel):
    # how many coefficient we want to learn for start and end for each action. HYPERPARAMETER
    NUM_START = 4
    NUM_END = 4

    TWO_STAGES = False

    def __init__(self, interval_thermal, thermal_precision=0.05, learning_rate=0.00001):
        '''
        :param interval_thermal: The minutes the thermal model learns to predict for. The user is responsible to ensure
                                that the data the model receives for training is as specified.
        :param thermal_precision: the closest multiple of which to round to.
        '''

        self._params = None
        self._params_coeff_order = None  # first part of _params is coeff part
        self._params_bias_order = None  # the rest is bias part.
        self._filter_columns = None  # order of columns by which to filter when predicting and fitting data.

        self.thermal_precision = thermal_precision
        self.learning_rate = learning_rate  # TODO evaluate which one is best.

        # Set the parent variables
        super(LTI, self).__init__(thermal_precision, interval_thermal)

    # thermal model function
    def _func(self, X, *params):
        """The polynomial with which we model the thermal model.
        :param X: np.array with row order (Tin, action, Tout, dt, rest of zone temperatures). Is also compatible
                    with pd.df with columns ('t_in', 'action', 't_out', 'dt', "zone_temperatures")
        :param *coeff: the coefficients for the thermal model.
                Should be in order: self._prams_coeff_order, self._params_bias_order
        """
        if isinstance(X, pd.DataFrame):
            X = X[self._filter_columns].T.as_matrix()
        elif not isinstance(X, np.ndarray):
            raise Exception("_func did not receive a valid datatype. Expects pd.df or np.ndarray")

        if not params:
            try:
                getattr(self, "_params")
            except AttributeError:
                raise RuntimeError("You must train classifier before predicting data!")
            params = self._params

        coeffs = params[:len(self._params_coeff_order)]
        biases = params[len(self._params_bias_order):]

        features = self._features(X)
        Tin, action = X[0], X[1]

        action_filter = self._filter_actions(X)
        features_biases = (features - biases) * action_filter

        return Tin + features_biases.dot(np.array(coeffs))

    def _features(self, X):
        """Returns the features we are using as a matrix.
        :param X: A matrix with row order (Tin, action, Tout, dt, rest of zone temperatures, previous_action, action_duration)
        :return np.matrix. each column corresponding to the features in the order of self._param_order"""

        Tin, action, previous_action, action_duration, Tout, dt, zone_temperatures = X[0], X[1], X[2], X[3], X[4], X[5], X[6:]
        features = []

        if not LTI.TWO_STAGES:
            NUM_ACTIONS = 2  # heating and cooling
            features += [Tin for _ in range(NUM_ACTIONS*LTI.NUM_START + NUM_ACTIONS*LTI.NUM_END)]
        else:
            raise NotImplementedError("Two stage thermal model is not implemented.")

        features.append(Tin - Tout)  # outside temperature influence.
        features.append(Tin)  # overall bias (no action)

        for zone_temp in zone_temperatures:
            features.append(Tin - zone_temp)
        return np.array(features).T

    def _filter_actions(self, X):
        """Returns a matrix of _features(X) shape to filter features according to actions.
        :param X: A matrix with row order: Tin, action, Tout, dt, rest of zone temperatures.
        :return np.matrix. each column corresponding to whether to use the features in the order of self._param_order"""
        num_data = X.shape[1]

        action, previous_action, action_duration, dt, zone_temperatures = X[1], X[2], X[3], X[5], X[6:]

        # setting action filter according to convolution properties.
        action_filter = []
        for iter_action, iter_num_start in itertools.product([utils.HEATING_ACTION, utils.COOLING_ACTION], list(range(LTI.NUM_START))):
            if iter_num_start != LTI.NUM_START - 1:
                action_filter += [(action == iter_action) & (((action_duration - dt) // self.interval_thermal) == iter_num_start)]
            else:
                action_filter += [(action == iter_action) & (((action_duration - dt) // self.interval_thermal) >= iter_num_start)]

        for iter_action, iter_num_end in itertools.product([utils.HEATING_ACTION, utils.COOLING_ACTION], list(range(LTI.NUM_END))):
            if iter_num_end != LTI.NUM_END - 1:
                action_filter += [(previous_action == iter_action) & (((action_duration - dt) // self.interval_thermal) == iter_num_end)]
            else:
                action_filter += [(previous_action == iter_action) & (((action_duration - dt) // self.interval_thermal) >= iter_num_end)]

        action_filter += [np.ones(num_data),  # tout
                         np.ones(num_data)]  # bias/no action

        # other zones
        for _ in zone_temperatures:
            action_filter.append(np.ones(num_data))

        action_filter = np.array(action_filter).T
        return action_filter

    def fit(self, X, y):
        """Needs to be called to initally fit the model. Will set self._params to coefficients.
        Will refit the model if called with new data.
        :param X: pd.df with columns ('t_in', 'action', 'previous_action', 'action_duration', 't_out', 'dt') and all zone temperature where all have
        to begin with "zone_temperature_" + "zone name"
        :param y: the labels corresponding to the data. As a pd.dataframe
        :return self
        """

        # set column order
        zone_col = X.columns[["zone_temperature_" in col for col in X.columns]]
        filter_columns = ['t_in', 'action', 'previous_action', 'action_duration', 't_out', 'dt'] + list(zone_col)
        self._filter_columns = filter_columns

        # set parameter order
        if not LTI.TWO_STAGES:
            actions_order = [act + "_" + "start" + "_" + str(num) for act, num in itertools.product(["heating", "cooling"], list(range(LTI.NUM_START)))]
            actions_order += [act + "_" + "end" + "_" + str(num) for act, num in itertools.product(["heating", "cooling"], list(range(LTI.NUM_END)))]

            self._params_coeff_order = actions_order + ['t_out', 'no_action'] + list(zone_col)
            self._params_bias_order = actions_order + ['t_out', 'no_action'] + list(zone_col)
        else:
            raise NotImplementedError("Two stage thermal model is not implemented.")

        # fit the data.
        popt, pcov = curve_fit(self._func, X[filter_columns].T.as_matrix(), y.as_matrix(),
                               p0=np.ones(len(
                                   self._params_coeff_order) + len(self._params_bias_order)))
        self._params = np.array(popt)

        return self

    def update_fit(self, X, y):
        raise NotImplementedError("Online Learning is not implemented.")



if __name__ == '__main__':
    pass

