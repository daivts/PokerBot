import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from dotenv import find_dotenv, load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from services import hand

from keyboard import cards, suits, new_hand, deck

load_dotenv(find_dotenv())

storage = MemoryStorage()
bot = Bot(os.environ.get("TOKEN"))
dp = Dispatcher(bot, storage=storage)


class ChooseCard(StatesGroup):
    first_card = State()
    first_suit = State()
    second_card = State()
    second_suit = State()
    deck = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот для рассчета вероятности самой сильной покерной руки. "
                         "Выберите свои карты из предложенных:", reply_markup=new_hand())


@dp.message_handler(lambda message: message.text in ["Новая раздача"])
async def choose(message: types.Message):
    await ChooseCard.first_card.set()
    await message.answer('Choose first card', reply_markup=cards())


@dp.callback_query_handler(lambda c: c.data.startswith('card '), state=ChooseCard.first_card)
async def first_card(callback_query: CallbackQuery, state: ChooseCard):
    async with state.proxy() as data:
        data['first_card'] = callback_query.data.replace('card ', '')
        await ChooseCard.next()
        await callback_query.message.answer('Выберите масть для первой карты:', reply_markup=suits())


# @dp.callback_query_handler(lambda c: c.data.startswith('suit '), state=ChooseCard.first_suit)
# async def first_suit(callback_query: CallbackQuery, state: ChooseCard):
#     async with state.proxy() as data:
#         data['first_suit'] = callback_query.data.split()[-1]
#         await ChooseCard.next()
#         await callback_query.message.answer('Choose second card:', reply_markup=cards())
@dp.callback_query_handler(lambda c: c.data.startswith('suit '), state=ChooseCard.first_suit)
async def first_suit(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # Retrieve the value of first_card from the data dictionary
        first_card_value = data.get('first_card', '')

        # Get the selected suit for the first card
        first_suit = callback_query.data.split()[-1]

        # Store the combined value of the first card in the data dictionary
        data['first_card'] = first_card_value + first_suit

    await ChooseCard.next()
    await callback_query.message.answer('Choose second card:', reply_markup=cards())


@dp.callback_query_handler(lambda c: c.data.startswith('card '), state=ChooseCard.second_card)
async def second_card(callback_query: CallbackQuery, state: ChooseCard):
    async with state.proxy() as data:
        data['second_card'] = callback_query.data.replace('card ', '')
        await ChooseCard.next()
        await callback_query.message.answer('Выберите масть для vtoroy карты:', reply_markup=suits())


@dp.callback_query_handler(lambda c: c.data.startswith('suit '), state=ChooseCard.second_suit)
async def second_suit(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # Retrieve the value of second_card from the data dictionary
        second_card_value = data.get('second_card', '')

        # Get the selected suit for the second card
        second_suit = callback_query.data.split()[-1]

        # Store the combined value of the second card in the data dictionary
        data['second_card'] = second_card_value + second_suit

    await ChooseCard.next()
    await callback_query.message.answer('Choose etap:', reply_markup=deck())


@dp.callback_query_handler(lambda c: c.data.startswith('deck '), state=ChooseCard.deck)
async def second_suit(callback_query: CallbackQuery, state: ChooseCard):
    async with state.proxy() as data:
        data['deck'] = callback_query.data.replace('deck ', '')

    await hand(state)

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
