#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from operator import itemgetter
from .traintestbase import TrainTestBase, TestDataFrom, FileFrom
from .useritemmatrix import UserItemMatrix


class TrainTest(TrainTestBase):
    def __init__(self, n_rec, n_err, unique, trans):
        super().__init__(n_rec, n_err, unique, trans)
        self.__unique = self._TrainTestBase__unique
        self.__transactions = self._TrainTestBase__transactions

    def split(self, hold_out=5, only_new=True):
        self.__check_boolean_type_of(only_new)
        hold_out = self.__checked_for_type_and_range_of(hold_out)
        keep = {user: items
                for user, items in self.__unique.items()
                if len(items) >= hold_out}
        last_unique_items_of = {user: self.__last(unique_items)[:hold_out]
                                for user, unique_items in keep.items()}
        test = {user: self.__items_from(last_transactions)
                for user, last_transactions in last_unique_items_of.items()}
        if only_new:
            train = (';'.join((timestamp, user, item))
                     for timestamp, user, item in self.__transactions
                     if user in keep.keys()
                     and item not in test[user])
        else:
            train = (';'.join((timestamp, user, item))
                     for timestamp, user, item in self.__transactions
                     if user in keep.keys()
                     and (item, timestamp) not in last_unique_items_of[user])
        self.__test = TestDataFrom(test, hold_out, only_new)
        TrainTest.test = property(lambda self: self.__test)
        self.__train = UserItemMatrix.from_csv(FileFrom(train))
        TrainTest.train = property(lambda self: self.__train)

    def __check_boolean_type_of(self, only_new):
        if not isinstance(only_new, bool):
            log.error('Attempt to set "only_new" to non-boolean type.')
            raise TypeError('Flag "only_new" can only be True or False!')

    def __checked_for_type_and_range_of(self, hold_out):
        if not isinstance(hold_out, int):
            log.error('Attempt to set "hold_out" to non-integer type.')
            raise TypeError('Parameter "hold_out" must be an integer!')
        if hold_out < 1:
            log.warning('Attempt to set hold_out < 1. Resetting to 1.')
            hold_out = 1
        if hold_out > self.max_hold_out:
            log.warning('Hold_out > meaningful maximum of {0}.'
                        ' Resetting to {0}.'.format(self.max_hold_out))
            hold_out = self.max_hold_out
        return hold_out

    def __last(self, unique):
        return sorted(unique.items(), key=itemgetter(1), reverse=True)

    def __items_from(self, last_transactions):
        return set(tuple(zip(*last_transactions))[0])
