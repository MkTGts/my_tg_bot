from environs import Env
from dataclasses import dataclass


'''STATUS: dict = {
    "pars_mode": {},
    "tracker_mode": {}
}'''


@dataclass
class Status:
    pars_mode: dict
    tracker_mode: dict



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


status = Status(
    pars_mode={},
    tracker_mode={}
                )



