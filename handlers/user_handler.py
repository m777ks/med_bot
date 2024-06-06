from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from tabulate import tabulate
from lexicon.lexicon_ru import LEXICON_RU
from functions.patients import PatientManager
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from datetime import datetime

router = Router()

# Создаем экземпляр класса PatientManager для управления пациентами
patient_manager = PatientManager()


# Определяем состояние машины для сбора информации о пациенте
class Form(StatesGroup):
    name = State()  # Состояние для имени пациента
    birthdate = State()  # Состояние для даты рождения пациента


# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.name)  # Устанавливаем состояние на ввод имени
    await message.reply(LEXICON_RU['start'])


# Обработчик ввода имени пациента
@router.message(StateFilter(Form.name))
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Сохраняем введенное имя
    await state.set_state(Form.birthdate)  # Переходим к следующему состоянию
    await message.reply(LEXICON_RU['birthdate'])


# Обработчик ввода даты рождения пациента
@router.message(StateFilter(Form.birthdate))
async def process_birthdate(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    birthdate = message.text

    response = patient_manager.add_patient(name, birthdate)
    if "Пациент успешно добавлен." in response:
        await message.reply(response)
        await state.clear()  # Завершаем состояние машины состояний
    else:
        await message.reply(response + f'\nПожалуйста, введите данные снова.\nВведите имя пациента:')
        await state.set_state(Form.name)  # Возвращаемся к состоянию ввода имени


# Обработчик команды /today
@router.message(Command(commands='today'))
async def cmd_today(message: Message):
    patients = patient_manager.get_today_patients()
    if patients:
        # Создаем таблицу
        table = [(p[0], p[1]) for p in patients]
        response = tabulate(table, headers=["Имя", "Дата рождения"], tablefmt="pretty")
    else:
        response = "Сегодня нет пациентов."
    await message.reply(f"<pre>{response}</pre>", parse_mode='HTML')


# Обработчик команды /weekly
@router.message(Command(commands='weekly'))
async def cmd_weekly(message: Message):
    counts = patient_manager.get_weekly_patient_counts()
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    # Создаем таблицу
    table = [(days[int(day)], count) for day, count in counts.items()]
    response = tabulate(table, headers=["День", "Количество пациентов"], tablefmt="pretty")

    await message.reply(f"<pre>{response}</pre>", parse_mode='HTML')
