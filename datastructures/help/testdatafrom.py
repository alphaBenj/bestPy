# -*- coding: utf-8 -*-


class TestDataFrom():
    def __init__(self, data, hold_out, only_new):
        self.__data = data
        self.__hold_out = hold_out
        self.__only_new = only_new
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def data(self):
        return self.__data

    @property
    def hold_out(self):
        return self.__hold_out

    @property
    def only_new(self):
        return self.__only_new

    @property
    def number_of_cases(self):
        if not self.__has('number_of_cases'):
            self.__number_of_cases = len(self.__data)
        return self.__number_of_cases

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)