#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ...algorithms import MostPopular
from ...datastructures import UserItemMatrix


class TestMostPopular(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = UserItemMatrix.from_csv(file)
        self.algorithm = MostPopular()

    def test_binarize_type(self):
        log_msg = ['ERROR:root:Attempt to set "binarize" to non-boolean type.']
        err_msg = 'Attribute "binarize" must be True or False!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.algorithm.binarize = 'foo'
        self.assertEqual(log.output, log_msg)

    def test_binarize_true(self):
        self.algorithm.binarize = True
        self.assertTrue(self.algorithm.binarize)

    def test_binarize_false(self):
        self.algorithm.binarize = False
        self.assertFalse(self.algorithm.binarize)

    def test_has_attribute_operating_on(self):
        self.assertTrue(hasattr(self.algorithm, 'operating_on'))

    def test_attribute_operating_on_is_callable(self):
        self.assertTrue(callable(self.algorithm.operating_on))

    def test_has_attribute_has_data(self):
        self.assertTrue(hasattr(self.algorithm, 'has_data'))

    def test_has_data_false(self):
        self.assertFalse(self.algorithm.has_data)

    def test_has_data_true(self):
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_without_data(self):
        with self.assertRaises(AttributeError):
            self.algorithm.has_data = 'foz'
        self.assertFalse(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_with_data(self):
        self.algorithm = self.algorithm.operating_on(self.data)
        with self.assertRaises(AttributeError):
            self.algorithm.has_data = 'john'
        self.assertTrue(self.algorithm.has_data)

    def test_data_type(self):
        log_msg = ['ERROR:root:Attempt to set incompatible data type.'
                  ' Must be <UserItemMatrix>']
        err_msg = 'Data must be of type <UserItemMatrix>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.algorithm.operating_on('bar')
        self.assertEqual(log.output, log_msg)

    def test_no_attribute_for_one_after_wrong_data_type(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(TypeError):
                _ = self.algorithm.operating_on('baz')
        self.assertFalse(hasattr(self.algorithm, 'for_one'))

    def test_no_attribute_for_one_without_data(self):
        self.assertFalse(hasattr(self.algorithm, 'for_one'))

    def test_has_attribute_for_one_with_data(self):
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(hasattr(self.algorithm, 'for_one'))

    def test_recommendation_binarized(self):
        target = 3
        should_be = [0.03225806451612903, 0.03225806451612903,
                     1.0,        1.0,        1.0,        1.0,
                     0.06451612903225806, 0.03225806451612903,
                     0.03225806451612903, 0.03225806451612903,
                     0.03225806451612903, 0.03225806451612903,
                     0.03225806451612903, 0.03225806451612903,
                     0.03225806451612903, 0.03225806451612903,
                     0.03225806451612903, 0.03225806451612903,
                     0.03225806451612903, 0.03225806451612903,
                     0.03225806451612903, 0.03225806451612903,
                     0.03225806451612903]
        self.algorithm.binarize = True
        self.algorithm = self.algorithm.operating_on(self.data)
        actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_recommendation_not_binarized(self):
        target = 5
        should_be = [0.02, 0.02, 0.12, 0.06, 0.04, 0.02, 1.0, 10.0, 10.0, 0.02,
                     0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 1.0,
                     1.0, 1.0, 1.0]
        self.algorithm.binarize = False
        self.algorithm = self.algorithm.operating_on(self.data)
        actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_binarized_recommendation_does_not_change(self):
        target = 1
        self.algorithm.binarize = True
        self.algorithm = self.algorithm.operating_on(self.data)
        before = self.algorithm.for_one(target).copy().tolist()
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after = self.algorithm.for_one(target).tolist()
        self.assertListEqual(before, after)

    def test_non_binarized_recommendation_does_not_change(self):
        target = 2
        self.algorithm.binarize = False
        self.algorithm = self.algorithm.operating_on(self.data)
        before = self.algorithm.for_one(target).copy().tolist()
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after = self.algorithm.for_one(target).tolist()
        self.assertListEqual(before, after)

    def test_binarized_data_does_not_change(self):
        target = 1
        before_col = self.data.matrix_by_col.copy().todense().tolist()
        before_row = self.data.matrix_by_row.copy().todense().tolist()
        before_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        before_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.algorithm.binarize = True
        self.algorithm = self.algorithm.operating_on(self.data)
        recommendation = self.algorithm.for_one(target)
        after_col = self.data.matrix_by_col.copy().todense().tolist()
        after_row = self.data.matrix_by_row.copy().todense().tolist()
        after_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        after_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.assertListEqual(before_col, after_col)
        self.assertListEqual(before_row, after_row)
        self.assertListEqual(before_boolcol, after_boolcol)
        self.assertListEqual(before_boolrow, after_boolrow)

    def test_non_binarized_data_does_not_change(self):
        target = 2
        before_col = self.data.matrix_by_col.copy().todense().tolist()
        before_row = self.data.matrix_by_row.copy().todense().tolist()
        before_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        before_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.algorithm.binarize = False
        self.algorithm = self.algorithm.operating_on(self.data)
        recommendation = self.algorithm.for_one(target)
        after_col = self.data.matrix_by_col.copy().todense().tolist()
        after_row = self.data.matrix_by_row.copy().todense().tolist()
        after_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        after_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.assertListEqual(before_col, after_col)
        self.assertListEqual(before_row, after_row)
        self.assertListEqual(before_boolcol, after_boolcol)
        self.assertListEqual(before_boolrow, after_boolrow)


if __name__ == '__main__':
    ut.main()
