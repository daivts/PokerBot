from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def cards():
    markup = InlineKeyboardMarkup()

    values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    row1 = [InlineKeyboardButton(value, callback_data=f"card {value}") for value in values[:7]]
    row2 = [InlineKeyboardButton(value, callback_data=f"card {value}") for value in values[7:]]

    markup.row(*row1)
    markup.row(*row2)

    return markup


def suits():
    markup = InlineKeyboardMarkup(row_width=2)
    suits = ['♠', '♥', '♣', '♦']
    suit_mapping = {
        '♠': 's',
        '♥': 'h',
        '♣': 'c',
        '♦': 'd'
    }

    for suit in suits:
        letter = suit_mapping.get(suit, suit)  # Получаем соответствующий символ масти
        markup.add(InlineKeyboardButton(suit, callback_data=f"suit {suit} {letter}"))

    return markup


def new_hand():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Новая раздача")

    return markup


def deck():
    markup = InlineKeyboardMarkup(row_width=2)
    decks = ['Flop', 'Tern', 'River']
    for deck in decks:
        markup.add(InlineKeyboardButton(deck, callback_data=f"deck {deck}"))

    return markup
