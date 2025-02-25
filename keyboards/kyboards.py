from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


'''# создание кнопока в ответ на поедложение начать игру
button_pars = KeyboardButton(
    text=LEXICON_RU["but_pars_wb"]
    )

# инициализация биледра 
main_kb_builder = ReplyKeyboardBuilder()
main_kb_builder.row(button_pars, width=1)

main_kb = main_kb_builder.as_markup(  # создание клавиатуры начать игру да нет
    one_time_keyboard=True,
    resize_keyboard=True
)'''



# кнопка начала парсинга
button_pars = InlineKeyboardButton(
    text=LEXICON_RU["but_pars_wb"],
    callback_data="pres_pars"
)

# кнопка начала трэкинга
but_tracker = InlineKeyboardButton(
    text=LEXICON_RU["but_tracker_wb"],
    callback_data="pres_tracker"
)

# создание инлайн-клавиатуры
main_kb = InlineKeyboardMarkup(
    inline_keyboard=[[button_pars],
                     [but_tracker]]
)






