from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api =''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
inl = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ], resize_keyboard=True
)
but = KeyboardButton(text='Рассчитать')
but1 = KeyboardButton(text='Информация')
button = KeyboardButton(text='Купить')


kb.row(but)
kb.insert(but1)
kb.add(button)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
@dp.message_handler(commands=['start'])
async def start_message(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('photo/D3.jpg', 'rb') as img1:
        await message.answer(f'Название: Product1 |'
                             f' Описание: Витамин Д3 для вашей радости |'
                             f' Цена: {1 * 100}')
        await message.answer_photo(img1)
    with open('photo/fe.jpg', 'rb') as img2:
        await message.answer( f'Название: Product2 |'
                                       f' Описание: Витамин Железо для борьбы с анемией |'
                                       f' Цена: {2 * 100}')
        await message.answer_photo(img2)
    with open('photo/kl.jpg', 'rb') as img3:
        await message.answer(f'Название: Product3 |'
                                           f' Описание: Коллаген для здоровой кожи, волос и ногтей |'
                                           f' Цена: {3 * 100}')
        await message.answer_photo(img3)
    with open('photo/zn.jpg', 'rb') as img4:
        await message.answer(f'Название: Product4 |'
                                               f' Описание: Цинк в сезон простуд для иммунитета |'
                                               f' Цена: {4 * 100}')
        await message.answer_photo(img4)
        await message.answer("Выберите продукт для покупки:", reply_markup=inl)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес в килограммах:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=int(message.text))
    await message.answer('Укажите свой пол М или Ж')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories (message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    if data["gender"] == 'Ж':
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) - 161
    else:
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) + 5

    await message.answer(f"Ваша норма калорий в день составляет- {calories}")
    await message.answer('Спасибо, что воспользовались ботом')
    await state.finish()
@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)


