# coding=utf-8

import telebot
from telebot import types
import os
from flask import Flask, request

from instapaper import Instapaper

import messages

bot = telebot.TeleBot(os.environ['telegram_token'])

instapaper = None

server = Flask(__name__)

data = []



@bot.message_handler(commands=['start'])
def start(message):
    global instapaper
    instapaper = Instapaper(message.chat.id) if not instapaper else instapaper

    global data
    data = []

    markup = types.ReplyKeyboardHide()

    bot.send_message(message.chat.id, messages.hello, reply_markup=markup)

    if not instapaper.is_authorized():
        bot.send_message(message.chat.id, messages.auth_first)


@bot.message_handler(commands=['auth'])
def ask_for_data(message):
    global instapaper
    instapaper = Instapaper(message.chat.id) if not instapaper else instapaper

    global data
    data = []

    if instapaper.is_authorized():
        bot.send_message(message.chat.id, messages.auth_warning, parse_mode='Markdown', reply_markup=types.ReplyKeyboardHide())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton('Auth')

    markup.add(btn)

    text = "Send me your *Email* or *Username* and *Password, if you have one*:"
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['add'])
def ask_for_url(message):
    global instapaper
    instapaper = Instapaper(message.chat.id) if not instapaper else instapaper

    global data
    data = []

    if not instapaper.is_authorized():
        bot.send_message(message.chat.id, messages.auth_requirement, parse_mode='Markdown', reply_markup=types.ReplyKeyboardHide())
        
        return None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton('Add')

    markup.add(btn)

    text = "Send me *URL*:"
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(content_types=['text'], regexp='Auth|Add')
def act(message):
    markup = types.ReplyKeyboardHide()

    if message.text == 'Auth':
        status_code = instapaper.auth(*data)
    else:
        status_code = instapaper.add(*data)

    if status_code == 200:
        text = "You are successfully authorized."

    elif status_code == 201:
        text = "URL has been successfully added."

    elif status_code == 403:
        text = "Invalid username or password. Please try again: /auth."

    else: # status_code == 500
        text = "The service encountered an error. Please try again later."

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_data(message):
    data.append(message.text)


@server.route("/bot", methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="{}/bot".format(os.environ['app_url']))
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

# bot.polling()