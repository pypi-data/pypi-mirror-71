import unittest
from datetime import date

import numpy as np
import pandas as pd
from dateutil import relativedelta

from table_data_reader import TableParameterLoader, ParameterRepository, growth_coefficients
import pint


class CSVParameterLoaderTestCase(unittest.TestCase):

    def test_parameter_getvalue_exp(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_v2.csv', table_handler='csv').load_into_repo(sheet_name='Sheet1',
                                                                                                 repository=repository)
        p = repository.get_parameter('a')

        settings = {'sample_size': 3, 'times': pd.date_range('2016-01-01', '2017-01-01', freq='MS'),
                    'sample_mean_value': False, 'use_time_series': True}
        val = p(settings)

        n = val.mean(level='time').mean()
        assert n > 0.7

    def test_parameter_getvalue_exp_units(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_v2.csv', table_handler='csv').load_into_repo(sheet_name='Sheet1',
                                                                                                 repository=repository)
        p = repository.get_parameter('a')

        settings = {'sample_size': 3, 'times': pd.date_range('2016-01-01', '2017-01-01', freq='MS'),
                    'sample_mean_value': False, 'use_time_series': True, 'with_pint_units': True}
        val = p(settings)
        series = val.pint.m
        n = series.mean(level='time').mean()
        assert n > 0.7


class PandasCSVParameterLoaderTestCase(unittest.TestCase):

    def test_parameter_getvalue_exp(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_v2.csv', table_handler='pandas').load_into_repo(sheet_name='Sheet1',
                                                                                                    repository=repository)
        p = repository.get_parameter('a')

        settings = {'sample_size': 3, 'times': pd.date_range('2016-01-01', '2017-01-01', freq='MS'),
                    'sample_mean_value': False, 'use_time_series': True, 'with_pint_units': True}
        val = p(settings)
        series = val.pint.m
        n = series.mean(level='time').mean()
        assert n > 0.7


class ExcelParameterLoaderTestCase(unittest.TestCase):

    def test_parameter_getvalue_exp(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_v2.xlsx', table_handler='openpyxl').load_into_repo(sheet_name='Sheet1',
                                                                                                   repository=repository)
        p = repository.get_parameter('a')

        settings = {'sample_size': 3, 'times': pd.date_range('2016-01-01', '2017-01-01', freq='MS'),
                    'sample_mean_value': False, 'use_time_series': True, 'with_pint_units': True}
        val = p(settings)
        series = val.pint.m
        n = series.mean(level='time').mean()
        print(n)
        assert n > 0.7

    def test_parameter_getvalue_linear(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_v2.xlsx', table_handler='openpyxl').load_into_repo(sheet_name='Sheet1',
                                                                                                   repository=repository)
        p = repository.get_parameter('b')

        settings = {'sample_size': 3, 'times': pd.date_range('2010-01-01', '2010-12-01', freq='MS'),
                    'sample_mean_value': False, 'use_time_series': True, 'with_pint_units': True}
        val = p(settings)
        series = val.pint.m
        n = series.mean(level='time').mean()
        assert n > 0.7

    def test_parameter_getvalue_mean(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_v2.xlsx', table_handler='openpyxl').load_into_repo(sheet_name='Sheet1',
                                                                                                   repository=repository)
        p = repository.get_parameter('a')

        settings = {'sample_size': 3, 'times': pd.date_range('2010-01-01', '2010-12-01', freq='MS'),
                    'sample_mean_value': True, 'use_time_series': True, 'with_pint_units': True}
        val = p(settings)
        series = val.pint.m
        n = series.mean(level='time').mean()

        assert n > 0.7

    def test_column_order(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(
            sheet_name='shuffle_col_order',
            repository=repository)

        p = repository.get_parameter('z')
        assert p.name == 'z'
        assert p.tags == 'x'

    def test_choice_single_param(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('choice_var')
        assert p() == .9

    def test_choice_two_params(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('a')
        assert p() in [1, 2]

    def test_multiple_choice(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('multiple_choice')
        assert p() in [1, 2, 3]

    def test_choice_time(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx',
                             times=pd.date_range('2009-01-01', '2015-05-01', freq='MS'), size=10
                             ).load_into_repo(sheet_name='Sheet1', repository=repository)

        p = repository.get_parameter('choice_var')
        val = p()
        # print(val)
        assert (val == .9).all()

    def test_choice_two_params_with_time(self):
        loader = TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx',
                                      times=pd.date_range('2009-01-01', '2009-03-01', freq='MS'), size=10)
        repository = ParameterRepository()
        loader.load_into_repo(sheet_name='Sheet1', repository=repository)
        tag_param_dict = repository.find_by_tag('user')
        keys = tag_param_dict.keys()
        print(keys)
        assert 'a' in keys
        repository['a']()

        print(tag_param_dict['a'])

    def test_uniform(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('b')
        val = p()
        assert (val >= 2) & (val <= 4)

    def test_uniform_time(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx',
                             times=pd.date_range('2009-01-01', '2015-05-01', freq='MS'), size=10
                             ).load_into_repo(sheet_name='Sheet1', repository=repository)
        p = repository.get_parameter('b')
        val = p()
        print(val)
        print(type(val))

        assert (val >= 2).all() & (val <= 4).all()

    def test_uniform_mean(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('b')

        val = p({'sample_mean_value': True, 'sample_size': 5})

        print(val)
        assert (val == 3).all()

    def test_uniform_mean_growth(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('uniform_dist_growth')

        val = p({'sample_mean_value': True, 'sample_size': 5, 'use_time_series': True,
                 'times': pd.date_range('2009-01-01', '2010-01-01', freq='MS'), 'with_pint_units': True})

        val = val.pint.m

        assert (val >= 3).all()

    def test_parameter_getvalue_with_settings_mean(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('uniform_dist_growth')

        settings = {'sample_size': 1, 'sample_mean_value': True, 'use_time_series': True,
                    'times': pd.date_range('2009-01-01', '2010-01-01', freq='MS'), 'with_pint_units': True}
        val = p(settings)
        val = val.pint.m
        print(val)
        n = np.mean(val)
        assert n > 0.7

    def test_triagular(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx').load_into_repo(sheet_name='Sheet1',
                                                                                               repository=repository)
        p = repository.get_parameter('c')

        res = p()

        assert (res < 10.) & (res > 3.)

    def test_triagular_time(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test_excelparameterloader.xlsx',
                             times=pd.date_range('2009-01-01', '2015-05-01', freq='MS'), size=10
                             ).load_into_repo(sheet_name='Sheet1', repository=repository)

        p = repository.get_parameter('c')

        res = p()

        assert (res < 10.).all() & (res > 3.).all()

    def test_triangular_timeseries(self):
        repository = ParameterRepository()
        TableParameterLoader(filename='./tests/test.xlsx').load_into_repo(sheet_name='Sheet1', repository=repository)

        p = repository.get_parameter('c')

        settings = {
            'use_time_series': True,
            'times': pd.date_range('2009-01-01', '2015-05-01',
                                   freq='MS'),
            'sample_size': 10, 'with_pint_units': True
            # 'cagr': 0,
            # 'sample_mean_value': True
        }

        res = p(settings)
        res = res.pint.m
        print(res)
        assert (res < 10.).all() & (res > 3.).all()


if __name__ == '__main__':
    unittest.main()


class TestCAGRCalculation(unittest.TestCase):
    def test_identitical_month(self):
        """
        If start and end are identical, we expect an array of one row of ones of sample size

        :return:
        """
        samples = 3
        alpha = 1  # 100 percent p.a.
        ref_date = date(2009, 1, 1)
        start_date = date(2009, 1, 1)
        end_date = date(2009, 1, 1)

        a = growth_coefficients(start_date, end_date, ref_date, alpha, samples)
        assert np.all(a == np.ones((samples, 1)))

    def test_one_year(self):
        """
        If start and end are one month apart, we expect an array of one row of ones of sample size for the ref month
        and one row with CAGR applied

        :return:
        """
        samples = 3
        alpha = 1  # 100 percent p.a.
        ref_date = date(2009, 1, 1)
        start_date = date(2009, 1, 1)
        end_date = date(2010, 1, 1)

        a = growth_coefficients(start_date, end_date, ref_date, alpha, samples)
        print(a)
        assert np.all(a[0] == np.ones((samples, 1)))
        assert np.all(a[1] == np.ones((samples, 1)) * pow(1 + alpha, 1. / 12))

    def test_one_year(self):
        """
        If start and end are one month apart, we expect an array of one row of ones of sample size for the ref month
        and one row with CAGR applied

        :return:
        """
        samples = 3
        alpha = 0.5  # 100 percent p.a.
        ref_date = date(2009, 1, 1)
        start_date = date(2009, 1, 1)
        end_date = date(2010, 1, 1)

        a = growth_coefficients(start_date, end_date, ref_date, alpha, samples)
        print(a)
        assert np.all(a[0] == np.ones((samples, 1)))
        assert np.all(a[1] == np.ones((samples, 1)) * pow(1 + alpha, 1. / 12))

    def test_negative_growth(self):
        """
        If start and end are one month apart, we expect an array of one row of ones of sample size for the ref month
        and one row with CAGR applied

        :return:
        """
        samples = 3
        alpha = -0.1  # 100 percent p.a.
        ref_date = date(2009, 1, 1)
        start_date = date(2009, 1, 1)
        end_date = date(2010, 1, 1)
        a = growth_coefficients(start_date, end_date, ref_date, alpha, samples)
        print(a)
        assert np.all(a[0] == np.ones((samples, 1)))
        assert np.all(a[-1] == np.ones((samples, 1)) * 1 + alpha)

    def test_refdate_after_start(self):
        """
        If the ref date is greater than the start, we expect an array of one row of ones of sample size for the ref month
        and rows with (1-CAGR)^t applied

        :return:
        """
        samples = 3
        alpha = 0.1  # 10 percent p.a.
        ref_date = date(2009, 2, 1)
        start_date = date(2009, 1, 1)
        end_date = date(2009, 2, 1)

        a = growth_coefficients(start_date, end_date, ref_date, alpha, samples)
        assert a.shape == (2, samples)
        # first row has negative coefficients
        assert np.all(a[0] == np.ones((samples, 1)) * pow(1 - alpha, 1. / 12))
        # second row has ref values
        assert np.all(a[-1] == np.ones((samples, 1)))

    def test_refdate_between_start_and_end(self):
        """
        If the ref date is greater than the start, we expect an array of one row of ones of sample size for the ref month
        and rows with (1-CAGR)^t applied

        :return:
        """
        samples = 3
        alpha = 0.1  # 10 percent p.a.
        ref_date = date(2009, 3, 1)
        start_date = date(2009, 1, 1)
        end_date = date(2009, 6, 1)

        delta = relativedelta.relativedelta(end_date, start_date)
        total_months = delta.months + delta.years * 12 + 1

        ref_delta = relativedelta.relativedelta(ref_date, start_date)
        ref_row_idx = ref_delta.months + ref_delta.years * 12

        a = growth_coefficients(start_date, end_date, ref_date, alpha, samples)
        # print a

        assert a.shape == (total_months, samples)
        # the ref_row_idx has all ones
        assert np.all(a[ref_row_idx] == np.ones((samples, 1)))
        # the row before ref_row_idx has negative coefficients
        assert np.all(a[ref_row_idx - 1] == np.ones((samples, 1)) * pow(1 - alpha, 1. / 12))
        # the row after ref_row_idx has positive coefficients
        assert np.all(a[ref_row_idx + 1] == np.ones((samples, 1)) * pow(1 + alpha, 1. / 12))

        # the last row has positive coefficients
        assert np.all(a[-1] == np.ones((samples, 1)) * pow(1 + alpha, float(total_months - 1 - ref_row_idx) / 12))
