import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from dotenv import find_dotenv, load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from services import hand
from keyboard import cards, suits, new_hand, deck

from lang import _

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


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот для рассчета вероятности самой сильной покерной руки. "
                         "Выберите свои карты из предложенных:", reply_markup=new_hand())


# Обработчик выбора новой раздачи
@dp.message_handler(lambda message: message.text == "Новая раздача")
async def choose_new_hand(message: types.Message):
    await ChooseCard.first_card.set()
    await message.answer('Выберите первую карту:', reply_markup=cards())


# Обработчик выбора первой карты
@dp.callback_query_handler(lambda c: c.data.startswith('card '), state=ChooseCard.first_card)
async def first_card(callback_query: CallbackQuery, state: ChooseCard):
    async with state.proxy() as data:
        data['first_card'] = callback_query.data.replace('card ', '')
        await ChooseCard.next()
        await callback_query.message.answer('Выберите масть для первой карты:', reply_markup=suits())


# Обработчик выбора масти для первой карты
@dp.callback_query_handler(lambda c: c.data.startswith('suit '), state=ChooseCard.first_suit)
async def first_suit(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        first_card_value = data.get('first_card', '')
        first_suit = callback_query.data.split()[-1]
        data['first_card'] = first_card_value + first_suit

    await ChooseCard.next()
    await callback_query.message.answer('Выберите вторую карту:', reply_markup=cards())


# Обработчик выбора второй карты
@dp.callback_query_handler(lambda c: c.data.startswith('card '), state=ChooseCard.second_card)
async def second_card(callback_query: CallbackQuery, state: ChooseCard):
    async with state.proxy() as data:
        data['second_card'] = callback_query.data.replace('card ', '')
        await ChooseCard.next()
        await callback_query.message.answer('Выберите масть для второй карты:', reply_markup=suits())


# Обработчик выбора масти для второй карты
@dp.callback_query_handler(lambda c: c.data.startswith('suit '), state=ChooseCard.second_suit)
async def second_suit(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        second_card_value = data.get('second_card', '')
        second_suit = callback_query.data.split()[-1]
        if data['first_card'] != second_card_value + second_suit:
            data['second_card'] = second_card_value + second_suit
        else:
            await callback_query.message.answer("Эта карта уже выбрана. Выберите другую.", reply_markup=suits())
            return

    await ChooseCard.next()
    await callback_query.message.answer('Выберите этап игры:', reply_markup=deck())


# Обработчик выбора этапа игры (Flop, Turn, River) и вывод результата
@dp.callback_query_handler(lambda c: c.data.startswith('deck '), state=ChooseCard.deck)
async def select_deck(callback_query: CallbackQuery, state: ChooseCard):
    async with state.proxy() as data:
        step = callback_query.data.replace('deck', '')
        data['deck'] = step

    result = await hand(state)

    await callback_query.message.answer(f"Лучшая вероятная комбинация для этапа {_(step.strip())}:\n{_(result)}",
                                        reply_markup=new_hand())
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
