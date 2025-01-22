import random
from requests import get
from lexicon.lexicon import LEXICON_RU


class ApiWB:
    def __init__(self, id_card):
        self.id_card = id_card


    @staticmethod   
    def gett(url: str):
        return get(
            url=url
        ).json()


    def get_api_wb(self) -> None:
        url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1586360&spp=30&hide_dtype=10&ab_testing=false&nm={self.id_card}"
        response = __class__.gett(url=url)
        self.price = str(response["data"]["products"][0]["sizes"][0]["price"]["total"]) 
        self.name = response["data"]["products"][0]["name"] 
        self.rating = str(response["data"]["products"][0]['reviewRating'])  
        self.feedbacks = str(response["data"]["products"][0]["feedbacks"]) 


    def get_api_wb_description(self) -> None:
        for i in range(1, 100):
            num = str(i).rjust(2, "0")
            url = f'https://basket-{num}.wbbasket.ru/vol{self.id_card[:-5]}/part{self.id_card[:-3]}/{self.id_card}/info/ru/card.json'
            if get(url=url).status_code == 200:
                response = __class__.gett(url=url)
                self.num = num
                self.description: str = response['description']
                return None


    def get_image(self):
        self.urls_images = []
        for i in range(1, 100):
            url=f"https://basket-{self.num}.wbbasket.ru/vol{self.id_card[:-5]}/part{self.id_card[:-3]}/{self.id_card}/images/big/{i}.webp"
            resp = get(
                url=url
            )
            if get(url=url).status_code == 200:
                self.urls_images.append(url)
            else:
                return None


    def __call__(self, *args, **kwds):
        self.get_api_wb()
        self.get_api_wb_description()
        self.get_image()



def pars_wb(id_card: str):
    resp = ApiWB(id_card=id_card)
    resp()
    res = f"Наименование товара: {resp.name}\nЦена товара: {resp.price[:-2]} руб.\nРейтинг товвара: {resp.rating}\nКоличество отзывов: {resp.feedbacks}\n\nСсылки на изображение:\n{'\n'.join(resp.urls_images)}\n\nОписание товара: {resp.description}"
    return res