#!/usr/bin/python
# -*- coding: utf-8 -*-

from unity.modules.configmodule import config
import logging
import inspect
import telebot

token =config().get('telegram','token')
logchatid =config().get('telegram','logchatid')

def loginfo(message):
    mod = inspect.getmodule(inspect.stack()[1][0])
    telebot.TeleBot(token).send_message(logchatid, "[{}]\nINFO: {}".format(mod,message))
    logging.info(message)