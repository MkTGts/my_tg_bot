import logging
from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU


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


router = Router()  # подключение роутера

# хэндлер для сообщений не подходящих не под какуб категорию
@router.message()
async def other_all_mess(message: Message):
    await message.answer(
        text=LEXICON_RU["other"]
    )
    logger.info(f'Other command user id - {message.from_user.id}')