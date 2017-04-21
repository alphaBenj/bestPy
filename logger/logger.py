#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log


def write_log_to(file, log_level=30):
    color = '\033[33m[{0}]\033[34m{1}\033[0m|\033[32m{2}\033[0m: {3}'
    log_entry_format = color.format('%(levelname)-8s',
                                    '%(module)-15s',
                                    '%(funcName)-15s',
                                    '%(message)s')
    log.basicConfig(filename=file,
                    filemode='w',
                    level=round(log_level, -1),
                    format=log_entry_format)
