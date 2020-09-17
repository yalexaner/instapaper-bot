from telebot import types

from src import messages


def get_auth_suggestion():
    message = messages.unauthorized_hello

    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("OK. Let's do it"))

    return message, markup


def get_action_choices():
    message = messages.authorized_hello

    markup = types.ReplyKeyboardMarkup()
    add_urls_btn = types.KeyboardButton('Add urls')
    go_to_adding_mode_btn = types.KeyboardButton('Go to Adding mode')
    see_help_msg_btn = types.KeyboardButton('See help message')
    auth_btn = types.KeyboardButton('Authorize')
    markup.row(add_urls_btn, auth_btn)
    markup.row(go_to_adding_mode_btn)
    markup.row(see_help_msg_btn)

    return message, markup
