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

