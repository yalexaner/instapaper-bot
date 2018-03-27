# coding=utf-8

import telebot
from telebot import types
import os
from flask import Flask, request

import requests
import pickle

from config import telegram_token, app_url
import messages

bot = telebot.TeleBot(telegram_token)

server = Flask(__name__)

url = 'https://www.instapaper.com/api/'

method = {
    'auth': url + 'authenticate'
}

user = {
    'username': None,
    'password': None    
}

with open('users.pkl', 'rb') as file:
    users = pickle.load(file)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, messages.hello)

    if message.chat.id not in users:
        bot.send_message(message.chat.id, messages.auth)


@bot.message_handler(commands=['auth'])
def ask_for_data(message):
    global user
    user['username'] = None
    user['password'] = None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton('DONE')

    markup.add(btn)

    bot.send_message(message.chat.id, "Send me your *Login* and *Password*:", parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'DONE')
def auth(message):
    markup = types.ReplyKeyboardHide()

    response = requests.get(method['auth'], params=user)

    if response.status_code == 200:
        bot.send_message(message.chat.id, 'You are successfully authorized.', reply_markup=markup)

        users[message.chat.id] = (user['username'], user['password'])

        with open('users.pkl', 'wb') as file:
            pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)

    elif response.status_code == 403:
        bot.send_message(message.chat.id, 'Invalid username or password. Try again: /auth', reply_markup=markup)

    else: # status_code == 500
        bot.send_message(message.chat.id, 'The service encountered an error. Please try again later.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_data(message):
    if not user['username']:
        user['username'] = message.text
    else:
        user['password'] = message.text


@server.route("/bot", methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="{}/bot".format(app_url))
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

# bot.polling()