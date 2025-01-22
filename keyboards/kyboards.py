from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


# создание кнопока в ответ на поедложение начать игру
button_pars = KeyboardButton(text=LEXICON_RU["but_pars_wb"])

# инициализация биледра 
main_kb_builder = ReplyKeyboardBuilder()
main_kb_builder.row(button_pars, width=1)

main_kb = main_kb_builder.as_markup(  # создание клавиатуры начать игру да нет
    one_time_keyboard=True,
    resize_keyboard=True
)










