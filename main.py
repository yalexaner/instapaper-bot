# coding=utf-8

import telebot
from telebot import types
import os
from flask import Flask, request

import requests
import pickle

import messages

bot = telebot.TeleBot(os.environ['telegram_token'])

server = Flask(__name__)

url = 'https://www.instapaper.com/api/'

method = {
    'auth': url + 'authenticate',
    'add' : url + 'add'
}

command = None

user = {
    'username': None,
    'password': None
}

data = {
    'url': None
}

with open('users.pkl', 'rb') as file:
    users = pickle.load(file)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardHide()

    bot.send_message(message.chat.id, messages.hello, reply_markup=markup)

    if message.chat.id not in users:
        bot.send_message(message.chat.id, messages.auth)


@bot.message_handler(commands=['auth', 'add'])
def ask_for_data(message):
    global command
    command = message.text[1:]

    global user
    user['username'], user['password'] = users.get(message.chat.id, (None, None))

    if command == 'auth' and user['username'] != None:
        bot.send_message(message.chat.id, messages.auth_warning, parse_mode='Markdown')

        user['username'], user['password'] = (None, None)

    if command == 'add' and user['username'] == None:
        bot.send_message(message.chat.id, messages.auth_requirement, parse_mode='Markdown')
        return None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton('DONE')

    markup.add(btn)

    if command == 'auth':
        text = "Send me your *Login* and *Password*:"
    else:
        text = "Send me *URL*:"

    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'DONE')
def act(message):
    markup = types.ReplyKeyboardHide()

    response = requests.get(method[command], params={**user, **data})

    if response.status_code == 200:
        text = "You are successfully authorized."

        users[message.chat.id] = (user['username'], user['password'])

        with open('users.pkl', 'wb') as file:
            pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)

    elif response.status_code == 201:
        text = "URL has been successfully added to your Instapaper account."

    elif response.status_code == 403:
        text = "Invalid username or password. Try again: /auth."

    else: # status_code == 500
        text = "The service encountered an error. Please try again later."

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_data(message):
    if not user['username']:
        user['username'] = message.text
    elif not user['password']:
        user['password'] = message.text
    else:
        data['url'] = message.text


@server.route("/bot", methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="{}/bot".format(os.environ['app_url']))
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

# bot.polling()