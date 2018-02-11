#!/usr/bin/python
#  -*- coding: utf-8 -*-

from unity.modules.configmodule import config
from unity.telegram.auth import auth_admin, auth_user
import unity.telegram.usermanagement as usermanagement
from telebot import types
import telebot

token =config().get('telegram','token')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
@auth_user(bot)
def start(message):
   bot.send_message(message.chat.id,'Стартовал')


@bot.message_handler(commands=["admin","админ","админка","админпанель"])
@auth_admin(bot)
def adminhanlder(message):
    message = bot.send_message(message.chat.id, 'Админпанель...')
    adminpanel(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    module,action,parameter=call.data.split(":")
    if module=='admin':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Админпанель...",
            reply_markup=None
        )
        adminpanel(call.message)
    if module=='user':
        usermanagement.callback(bot,call,module,action,parameter)

@auth_admin(bot)
def adminpanel(message):
    usermanagement.main(bot,message)

if __name__ == '__main__':
    bot.polling(none_stop=True)