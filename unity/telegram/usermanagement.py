#!/usr/bin/python
#  -*- coding: utf-8 -*-

from unity.model import users
from telebot import types

def main(bot,message,newline=False):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for user in users.get():
        keyboard.add(types.InlineKeyboardButton(text="{} ({})".format(user['username'],user['description']), callback_data="user:show:{0}".format(user['id'])))
    keyboard.add(types.InlineKeyboardButton(text="Назад",callback_data="admin:main:"))
    if newline:
        message = bot.send_message(message.chat.id, 'Управление пользователями')
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text='Управление пользователями',
        reply_markup=keyboard
    )

def callback(bot,call,module,action,parameter):
    if module=="user" and parameter:
        user=users.get(id=parameter)
        if not user:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Ошибка: пользователь не найден!"
            )
            main(bot,call.message,True)
        if action=="show":
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            if user['role']=='user':
                keyboard.add(types.InlineKeyboardButton(text="Отключить",callback_data="user:disable:{0}".format(user['id'])))
            elif user['role']=='disabled':
                keyboard.add(types.InlineKeyboardButton(text="Включить",callback_data="user:enable:{0}".format(user['id'])))
            elif user['role']=='pending':
                keyboard.add(types.InlineKeyboardButton(text="Дать доступ",callback_data="user:makeuser:{0}".format(user['id'])))
            keyboard.add(types.InlineKeyboardButton(text="Назад",callback_data="user:list:"))
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="{0} ({1}) [{2}]".format(user['username'],user['description'],user['role']),
                reply_markup=keyboard
            )
        elif action=="disable":
            users.set(id=user['id'],role='disabled')
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Пользователь {} отключен".format(user['username'])
            )
            main(bot,call.message,True)
        elif action=="enable":
            users.set(id=user['id'],role='user')
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Пользователь {} включен".format(user['username'])
            )
            main(bot,call.message,True)
        elif action=="makeuser":
            users.set(id=user['id'],role='user')
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Пользователю {} предоставлен доступ к боту".format(user['username'])
            )
            main(bot,call.message,True)
    if module=="user" and action=="list":
        main(bot=bot,message=call.message)
