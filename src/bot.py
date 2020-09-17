# coding=utf-8

import os

from flask import Flask, request
from telebot import TeleBot, types

from src import messages, utils
from src.instapaper import Instapaper

bot = TeleBot(os.environ['telegram_token'])

# user data for Instapaper
instapaper = Instapaper()

# current state
state = utils.State.IDLE

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    instapaper.user_id = message.chat.id

    if instapaper.is_authorized():
        # creating action buttons
        msg_text = messages.authorized_hello
        markup = utils.get_action_choices_markup()
    else:
        # creating button for authentication
        msg_text = messages.unauthorized_hello
        markup = utils.get_one_button_markup_with_text("OK. Let's do it")

    bot.send_message(message.chat.id, msg_text, reply_markup=markup)


@bot.message_handler(regexp="OK. Let's do it")
def start_authorizing(message):
    ask_for_username(message.chat.id)


def ask_for_username(user_id):
    global state
    state = utils.State.GET_USERNAME

    bot.send_message(user_id, messages.username_request, parse_mode='Markdown',
                     reply_markup=types.ReplyKeyboardRemove)


@bot.message_handler(content_types=['text'], func=lambda: state.action == utils.State.GET_USERNAME)
def get_username(message):
    instapaper.username = message.text
    ask_for_password(message.chat.id)


def ask_for_password(chat_id):
    global state
    state = utils.State.GET_PASSWORD

    bot.send_message(chat_id, messages.password_request, parse_mode='Markdown',
                     reply_markup=types.ReplyKeyboardRemove)


@bot.message_handler(content_types=['text'], func=lambda: state.action == utils.State.GET_PASSWORD)
def get_password(message):
    instapaper.password = message.text
    authorize(message.chat.id)


def authorize(chat_id):
    global state
    state = utils.State.IDLE

    instapaper.auth()

    markup = utils.get_one_button_markup_with_text("OK. Let's start then")
    bot.send_message(chat_id, messages.authorized, reply_markup=markup)


@bot.message_handler(regexp="OK. Let's start then")
def finish_authorization(chat_id):
    markup = utils.get_action_choices_markup()
    bot.send_message(chat_id, messages.finish_authorization, reply_markup=markup)


@bot.message_handler(commands=['auth'])
def ask_for_data(message):
    global instapaper
    instapaper = Instapaper(message.chat.id) if not instapaper else instapaper

    data.clear()

    global command
    command = message.text

    if instapaper.is_authorized():
        bot.send_message(message.chat.id, messages.auth_warning, parse_mode='Markdown',
                         reply_markup=types.ReplyKeyboardHide())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton('Auth')

    markup.add(btn)

    text = "Send me your *Email* or *Username* and *Password, if you have one*:"
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['add'])
def ask_for_url(message):
    global instapaper
    instapaper = Instapaper(message.chat.id) if not instapaper else instapaper

    data.clear()

    global command
    command = message.text

    if not instapaper.is_authorized():
        bot.send_message(message.chat.id, messages.auth_requirement, parse_mode='Markdown',
                         reply_markup=types.ReplyKeyboardHide())

        return None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = types.KeyboardButton('Add')

    markup.add(btn)

    text = "Send me *URL*:"
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['adding_mode'])
def adding_mode(message):
    global instapaper
    instapaper = Instapaper(message.chat.id) if not instapaper else instapaper

    data.clear()

    global command
    command = message.text

    text = "Send me urls (each one in a separate message) and I'll be saving them."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['cancel'])
def cancel(message):
    markup = types.ReplyKeyboardHide()

    data.clear()

    global command
    command = None

    text = "Canceled. What are we going to do next?"
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(content_types=['text'], regexp='Auth|Add')
def act(message):
    markup = types.ReplyKeyboardHide()

    status_codes = []

    msg = {
        200: "You are successfully authorized.",
        201: "URL has been successfully added.",
        403: "Invalid username or password. Please try again: /auth.",
        500: "The service encountered an error. Please try again later."
    }

    if message.text == 'Auth':
        status_codes.append(instapaper.auth(*data))

    else:
        for url in data:
            status_codes.append(instapaper.add(url))

    data.clear()

    for status_code in status_codes:
        bot.send_message(message.chat.id, msg[status_code], reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_data(message):
    data.append(message.text)

    if command == '/adding_mode':
        act(message)


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
