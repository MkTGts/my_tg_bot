from environs import Env
from dataclasses import dataclass



@dataclass
class TgBot:
    bot_token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            bot_token=env("BOT")
        )
    )



@dataclass
class Status:
    pars_mode: dict  # режим парсинга
    tracker_mode: dict  # режим трэкинга цен на товары


status = Status(
    pars_mode={},
    tracker_mode={}
                )

