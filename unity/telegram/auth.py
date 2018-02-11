#!/usr/bin/python3.6
#  -*- coding: utf-8 -*-

from unity.model import users
from telebot import types

def auth_user(bot):
    def decorator(function):
        def wrapper(message, **kwargs):
            if not users.get(id=message.chat.id):
                access_denied(message=message,bot=bot)
            elif users.get(id=message.chat.id)['role']=='pending':
                bot.send_message(message.chat.id, 'Заявка на рассмотрении.')
            elif users.get(id=message.chat.id)['role'] not in ['user','admin']:
                bot.send_message(message.chat.id, 'Заявка на рассмотрении.')
            else:
                function(message, **kwargs)
        return wrapper
    return decorator

def auth_admin(bot):
    def decorator(function):
        def wrapper(message, **kwargs):
            if not users.get(id=message.chat.id):
                access_denied(message=message,bot=bot,registerbutton=False)
            elif not users.get(id=message.chat.id)['role']=='admin':
                access_denied(message=message,bot=bot,registerbutton=False)
            else:
                function(message, **kwargs)
        return wrapper
    return decorator

def access_denied(bot,message,registerbutton=True):
    markup=types.ReplyKeyboardRemove()
    if registerbutton:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1, resize_keyboard=True)
        button = types.KeyboardButton("Запрос на доступ")
        markup.add(button)
    reply = bot.send_message(message.chat.id, 'Доступ запрещен.', reply_markup=markup)
    bot.register_next_step_handler(reply, lambda message: request_access(message, bot=bot))

def request_access(message,bot):
    types.ReplyKeyboardRemove()
    if message.text=='Запрос на доступ' and not users.get(id=message.from_user.id):
        description = "{} {}".format(message.chat.first_name, message.chat.last_name)
        users.add(
            id=message.chat.id,
            username=message.chat.username,
            description=description,
            phone='',
            role='pending')
        for user in users.get(role='admin'):
            bot.send_message(user['id'], 'Новая заявка на доступ от {0} ({1})'.format(description,message.chat.username))
        bot.send_message(message.chat.id, 'Заявка отправлена на рассмотрение.')