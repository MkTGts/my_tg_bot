import random
from requests import get
from lexicon.lexicon import LEXICON_RU


class ApiWB:
    def __init__(self, id_card):
        self.id_card = id_card


    @staticmethod   
    def get_api(url: str):
        '''Делает гет на api wb'''
        return get(
            url=url
        ).json()


    def datas_card(self) -> None:
        '''Собирает данные из карточки товара.'''
        url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1586360&spp=30&hide_dtype=10&ab_testing=false&nm={self.id_card}"
        response = __class__.get_api(url=url)  # делает гет
        self.price = str(response["data"]["products"][0]["sizes"][0]["price"]["total"])   # цена товара
        self.name = response["data"]["products"][0]["name"]  # наименование
        self.rating = str(response["data"]["products"][0]['reviewRating'])  # рейтинг 
        self.feedbacks = str(response["data"]["products"][0]["feedbacks"])  # количество отзывов
        self.urls_images = self.card_images()  # ссылки на изображения
        self.description = self.card_description()  # описание товара из карточки


    def card_description(self) -> str:
        '''Достает описание товара из карточки и узнает номер баскета циклом
        номера баскета для api запросов непонятно по какому принципу присваиваются,
        пожтому просто делает гет на ссылки с баскетами от 1 условно до 99,
        пока не вернется статус код 200'''
        for i in range(1, 100):  # идет цикл
            num = str(i).rjust(2, "0")  # форматирует в номер баскета в двузначный вид
            url = f'https://basket-{num}.wbbasket.ru/vol{self.id_card[:-5]}/part{self.id_card[:-3]}/{self.id_card}/info/ru/card.json'
            if get(url=url).status_code == 200:  # если статус код 200 то сохраняет номер баскета и делает запрос к апи
                response = __class__.get_api(url=url)
                self.num = num
                description: str = response['description']
                break
        return description


    def card_images(self) -> list:
        '''Проходит циклом от 1 до 100. Пока статус код возвращается 200 собирает ссылки на изображения'''
        urls_images = []
        for i in range(1, 100): 
            url=f"https://basket-{self.num}.wbbasket.ru/vol{self.id_card[:-5]}/part{self.id_card[:-3]}/{self.id_card}/images/big/{i}.webp"
            resp = get(
                url=url
            )
            if get(url=url).status_code == 200:
                urls_images.append(url)
            else:
                break
        return urls_images
            
    






def pars_wb(id_card: str):
    resp = ApiWB(id_card=id_card)
    resp.datas_card()
    res = f"Наименование товара: {resp.name}\nЦена товара: {resp.price[:-2]} руб.\nРейтинг товвара: {resp.rating}\nКоличество отзывов: {resp.feedbacks}\n\nСсылки на изображение:\n{'\n'.join(resp.urls_images)}\n\nОписание товара: {resp.description}"
    return res