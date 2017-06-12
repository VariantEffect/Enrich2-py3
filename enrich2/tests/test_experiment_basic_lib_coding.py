#  Copyright 2016-2017 Alan F Rubin
#
#  This file is part of Enrich2.
#
#  Enrich2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Enrich2 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Enrich2.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from copy import deepcopy

from ..experiment.experiment import Experiment
from .methods import HDF5TestComponent
from .utilities import DEFAULT_STORE_PARAMS
from .utilities import load_config_data, update_cfg_file

CFG_FILE = "basic_experiment_coding.json"
CFG_DIR = "data/config/experiment/"
READS_DIR = "data/reads/experiment/"
RESULT_DIR = "data/result/experiment/"

DRIVER = "runTest"
LIBTYPE = 'basic'
CODING_STR = "c"
FILE_EXT = 'pkl'
FILE_SEP = ''


class TestExperimentBasicLibWLSScoringCompleteNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'WLS'
        logr = 'complete'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibWLSScoringFullNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'WLS'
        logr = 'full'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibWLSScoringWTNormC(unittest.TestCase):
    def setUp(self):
        scoring = 'WLS'
        logr = 'wt'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibOLSScoringCompleteNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'OLS'
        logr = 'complete'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibOLSScoringFullNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'OLS'
        logr = 'full'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibOLSScoringWTNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'OLS'
        logr = 'wt'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibRatiosScoringCompleteNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'ratios'
        logr = 'complete'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibRatiosScoringFullNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'ratios'
        logr = 'full'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibRatiosScoringWTNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'ratios'
        logr = 'wt'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibCountsScoringCompleteNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'counts'
        logr = 'complete'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibCountsScoringFullNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'counts'
        logr = 'full'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibCountsScoringWTNormC(unittest.TestCase):

    def setUp(self):
        scoring = 'counts'
        logr = 'wt'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibSimpleScoringCompleteNormC(unittest.TestCase):
    def setUp(self):
        scoring = 'simple'
        logr = 'complete'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibSimpleScoringFullNormC(unittest.TestCase):
    def setUp(self):
        scoring = 'simple'
        logr = 'full'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()


class TestExperimentBasicLibSimpleScoringWTNormC(unittest.TestCase):
    def setUp(self):
        scoring = 'simple'
        logr = 'wt'
        cfg = load_config_data(CFG_FILE, CFG_DIR)
        cfg = update_cfg_file(cfg, scoring, logr)
        params = deepcopy(DEFAULT_STORE_PARAMS)
        file_prefix = '{}_{}_{}_{}'.format(LIBTYPE, CODING_STR, scoring, logr)

        self.general_test_component = HDF5TestComponent(
            store_constructor=Experiment, cfg=cfg, file_prefix=file_prefix,
            result_dir=RESULT_DIR, file_ext=FILE_EXT, file_sep=FILE_SEP,
            save=False, params=params, verbose=False)
        self.general_test_component.setUp()

    def tearDown(self):
        self.general_test_component.tearDown()

    def test_all_hdf5_dataframes(self):
        self.general_test_component.runTest()
        
        
if __name__ == "__main__":
    unittest.main()
