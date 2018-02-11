#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser

def config():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    return config