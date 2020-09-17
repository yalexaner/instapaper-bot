import enum
from enum import Enum

from telebot import types


class State(Enum):
    IDLE = enum.auto
    GET_USERNAME = enum.auto
    GET_PASSWORD = enum.auto
    ADD_URL = enum.auto
    ADDING_MODE = enum.auto


def get_one_button_markup_with_text(text):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text))

    return markup


def get_action_choices_markup():
    markup = types.ReplyKeyboardMarkup()
    add_urls_btn = types.KeyboardButton('Add urls')
    go_to_adding_mode_btn = types.KeyboardButton('Go to Adding mode')
    see_help_msg_btn = types.KeyboardButton('See help message')
    auth_btn = types.KeyboardButton('Authorize')
    markup.row(add_urls_btn, auth_btn)
    markup.row(go_to_adding_mode_btn)
    markup.row(see_help_msg_btn)

    return markup
