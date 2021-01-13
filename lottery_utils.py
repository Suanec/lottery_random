# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'lynne'
# Created by lynne on 2021/1/13.

import os
import sys
import json
import requests
import time
import logging
from logging.handlers import RotatingFileHandler

KEY_COMPONENT_NAME = "lottery_randperm"
KEY_COMPONENT_FNAME = "lottery_randperm"
time_suffix = time.strftime('_%Y%m%d_%s', time.localtime( float( time.time() )))
logger_file_name = "./lynne_{LOG_FNAME}.log".format(LOG_FNAME=KEY_COMPONENT_FNAME)

def logger_time_fmt():
    return '%Y/%m/%d %H:%M:%S %a'

def wei_logger(_cls_name = "logger_helper",
               _log_level = logging.INFO):
    _format_str = '[%(levelname)s] : %(asctime)s %(filename)s[line:%(lineno)d]  %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=_format_str,
                        filename=logger_file_name,
                        datefmt=logger_time_fmt())

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console_formatter = logging.Formatter(_format_str)
    console.setFormatter(console_formatter)

    rotating_file_handler = RotatingFileHandler(logger_file_name, maxBytes=1024 * 1024 * 50, backupCount=5)
    rotating_file_handler.setLevel(logging.DEBUG)
    rotating_file_handler.setFormatter(console_formatter)

    logger = logging.getLogger(_cls_name)
    logger.addHandler(console)
    logger.addHandler(rotating_file_handler)
    logger.debug('%s logger init success!!' % _cls_name)
    return logger

logger = wei_logger(KEY_COMPONENT_FNAME)

def logger_fmt_component(_msg = ""):
    logger_fmt = [KEY_COMPONENT_NAME]
    if(isinstance(_msg, list)):
        logger_fmt += _msg
    else:
        logger_fmt.append(_msg)
    return " : ".join( logger_fmt )
