#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ..algorithms import TruncatedSVD
from ..datastructures import TrainTest
from .. import RecoBasedOn
from .. import Benchmark


class TestBenchmarkInitialization(ut.TestCase):

    def test_logs_and_raises_error_with_wrong_recommender(self):
        recommender = 'foo'
        log_msg = ['ERROR:root:Attempt to instantiate with incompatible'
                   ' recommender. Must be of type <RecoBasedOn>.']
        err_msg = 'Recommender must be of type <RecoBasedOn>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = Benchmark(recommender)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)


class TestBenchmark(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = TrainTest.from_csv(file)
        self.data.split(1)
        self.recommender = RecoBasedOn(self.data.train)
        self.benchmark = Benchmark(self.recommender)

    def test_has_method_against(self):
        self.assertTrue(hasattr(self.benchmark, 'against'))

    def test_method_against_is_callable(self):
        self.assertTrue(callable(self.benchmark.against))

    def test_has_no_attribute_score_without_test_data(self):
        self.assertFalse(hasattr(self.benchmark, 'score'))

    def test_error_on_setting_wrong_test_data_type(self):
        data = 'bar'
        log_msg = ['ERROR:root:Attempt to set incompatible type of test data.'
                   ' Must be <TestDataFrom>.']
        err_msg = 'Test data must be of type <TestDataFrom>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = self.benchmark.against(data)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_has_atrribute_score_with_test_data(self):
        benchmark = self.benchmark.against(self.data.test)
        self.assertTrue(hasattr(benchmark, 'score'))

    def test_cannot_set_attribute_score(self):
        benchmark = self.benchmark.against(self.data.test)
        with self.assertRaises(AttributeError):
            benchmark.score = 12.3

    def test_other_instances_do_not_get_score_without_own_test_data(self):
        other = Benchmark(self.recommender)
        benchmark = self.benchmark.against(self.data.test)
        self.assertFalse(hasattr(other, 'score'))

    def test_resets_recommender_only_new_to_true(self):
        log_msg = ['INFO:root:Resetting recommender to "pruning_old" because'
                   ' of test-data preference.']
        recommender = self.recommender.keeping_old
        with self.assertLogs(level=logging.INFO) as log:
            benchmark = Benchmark(recommender).against(self.data.test)
        self.assertEqual(log.output, log_msg)
        self.assertTrue(recommender.only_new)

    def test_resets_recommender_only_new_to_false(self):
        log_msg = ['INFO:root:Resetting recommender to "keeping_old" because'
                   ' of test-data preference.']
        self.data.split(1, False)
        recommender = RecoBasedOn(self.data.train).pruning_old
        with self.assertLogs(level=logging.INFO) as log:
            benchmark = Benchmark(recommender).against(self.data.test)
        self.assertEqual(log.output, log_msg)
        self.assertFalse(recommender.only_new)

    def test_score(self):
        benchmark = self.benchmark.against(self.data.test)
        self.assertAlmostEqual(benchmark.score, 0.08333333333333333)

    def test_changes_to_algorithm_settings_propagate_through_benchmark(self):
        data = self.data
        data.split(3)
        algorithm = TruncatedSVD()
        algorithm.number_of_factors = 2
        algorithm.binarize = True
        recommender = RecoBasedOn(data.train).using(algorithm)
        benchmark = Benchmark(recommender).against(data.test)
        before = benchmark.score
        algorithm.binarize = False
        after = benchmark.score
        self.assertNotEqual(before, after)


if __name__ == '__main__':
    ut.main()
