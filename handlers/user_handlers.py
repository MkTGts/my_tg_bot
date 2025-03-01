import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.kyboards import main_kb
from lexicon.lexicon import LEXICON_RU
from data.config import status
from services.services import pars_wb
from services.db_services import create_db, verification_user, insert_user_to_db, set_wb_id



# инициализация логгера
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


router = Router()  # инициализация роутера


# хэндрел на команду старт
@router.message(Command(commands="start"))
async def process_command_start(message: Message):
    # проверка есть ли пользователь в базе и если нет, то занесение в базу
    if not verification_user(tg_id=message.from_user.id):
        insert_user_to_db((str(message.from_user.id), message.from_user.full_name, '0'))

    await message.answer(
        text=LEXICON_RU["/start"],
        reply_markup=main_kb
    )
    logger.info(f'Бота запуситл пользователь с id - {message.from_user.id}')


# хэндрел на команду /menu, которая выводит пользователю inline клавиатуры с основными функциями
@router.message(Command(commands="menu"))
async def process_command_menu(message: Message):

    await message.answer(
        text=LEXICON_RU["/menu"],
        reply_markup=main_kb
    )
    logger.info(f'Пользователь с id запросил меню - {message.from_user.id}')


# хэндлер на команду хелп
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(
        text=LEXICON_RU["/help"],
        reply_markup=main_kb
    )
    logger.info(f'Команду /help запустил пользователь с id - {message.from_user.id}')
    

# хэндлер на запуск парсера. в частонсти выставляется режим парсинга у пользователя 
@router.callback_query(F.data.in_("pres_pars"))
async def start_parser(callback: CallbackQuery):

    await callback.message.answer(
        text=LEXICON_RU["if_pars_wb"],  # просит юзера ввести id товара
    )
    logger.info(f'Парсер запустил пользователь с id - {callback.from_user.id}')  # запись в лог
    status.pars_mode = True # ставит статус парсинга в тру
    await callback.answer()


# хэндлер на запуск трэкера
@router.callback_query(F.data.in_("pres_tracker"))
async def start_parser(callback: CallbackQuery):
    # set_pars_mode(tg_id=str(callback.from_user.id))

    await callback.message.answer(
        text=LEXICON_RU["if_tracker_wb"],  # просит юзера ввести id товара
    )
    logger.info(f'Трэкер запустил пользователь с id - {callback.from_user.id}')  # запись в лог
    status.tracker_mode = True  # ставит статус трэкера в тру
    await callback.answer()



# хэндлер работы парсера 
@router.message(lambda x: x.text and x.text.isdigit() and 7 <= len(x.text) <= 10)  # проверка что id соответсвует требованию
async def working_parser(message: Message):


    if status.pars_mode :  # если установлен режим парсинга
        print(message.from_user.first_name)  # для меня. выводит имя пользователя в консоле

        pars_datas = pars_wb(str(message.text))  # результат парсинга по id заданному пользователем
        if pars_datas:
            response = pars_datas  # если данные собраны по id то возвращает результат парсинга
        else:
            response = LEXICON_RU["not_datas_to_id"]  # если данные собрать не удалось, то сообщает пользователю об этом

        await message.answer(
            text=response,  # возвращает результат парсинга
            parse_mode=None
        )
        status.pars_mode = False  # выключает режим парсинга
        logger.info(f'Отработал парсер у пользователя с id - {message.from_user.id}')  # лог запущенного парсера


    elif status.tracker_mode:  # если установлен режим трэкинга
        set_wb_id(tg_id=message.from_user.id, wb_id=message.text)  # добавляет в базу запрашиваемый id и прибавляет к чеслу раз парсинга

        await message.answer(
            text = f"Здесь будет работать режим трекинга для товара с id {message.text}"
        )
        status.tracker_mode = False  # выключается режим трэкинга
        logger.info(f'Отработал трэкинг у пользователя с id - {message.from_user.id}')


    else:  # если не включен ни один режим
        await message.answer(
            text=LEXICON_RU["not_mode"],
        )
        logger.info(f'Пользователь с id {message.from_user.id} ввел id товара, невключив режим')
