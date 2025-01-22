import logging
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.kyboards import main_kb
from lexicon.lexicon import LEXICON_RU
from services.services import pars_wb
from services.db_services import create_db, verification_user, insert_datas, set_pars_mode, verification_mode, set_wb_id



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
        insert_datas(("false", str(message.from_user.id), '0', 0, ))

    await message.answer(
        text=LEXICON_RU["/start"],
        reply_markup=main_kb
    )
    logger.info(f'Start bot user id - {message.from_user.id}')


# хэндлер на команду хелп
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(
        text=LEXICON_RU["/help"],
        reply_markup=main_kb
    )
    logger.info(f'Help bot user id - {message.from_user.id}')
    

# хэндлер на запуск парсера. в частонсти выставляется режим парсинга у пользователя 
@router.message(F.text == LEXICON_RU["but_pars_wb"])
async def start_parser(message: Message):
    set_pars_mode(tg_id=str(message.from_user.id))

    await message.answer(
        text=LEXICON_RU["if_pars_wb"],  # просит юзера ввести id товара
    )
    logger.info(f'Start parser user id - {message.from_user.id}')  # запись в лог


# хэндлер работы парсера
@router.message(lambda x: x.text and x.text.isdigit() and len(x.text) == 9)  # проверка что id соответсвует требованию
async def working_parser(message: Message):
    if verification_mode(str(message.from_user.id)):  # если установлен режим парсинга
        set_wb_id(tg_id=message.from_user.id, wb_id=message.text)  # добавляет в базу запрашиваемый id и прибавляет к чеслу раз парсинга

        await message.answer(
            text=pars_wb(message.text)  # возвращает результат парсинга
        )
        set_pars_mode(tg_id=str(message.from_user.id), var="false")  # закрывает режим парсинга wb
        logger.info(f'Working parser user id - {message.from_user.id}')  # лог запущенного парсера
    else:
        await message.answer(
            text=LEXICON_RU["not_pars_mode"],
        )

