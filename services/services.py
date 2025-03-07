import random
from requests import get
import sqlite3



class ParsWB:
    '''Класс обращается к карточке товара WB и собирает данные по API.
    Возвращает шаблонные данные в формате строки в формате строки.'''

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
        if response["data"]["products"]:
            self.price: str = str(response["data"]["products"][0]["sizes"][0]["price"]["total"])   # цена товара
            self.price_for_track = int(self.price[:-2])  # возвращает цены в инте для трэгинга цен
            self.name: str = response["data"]["products"][0]["name"]  # наименование
            self.rating: str = str(response["data"]["products"][0]['reviewRating'])  # рейтинг 
            self.feedbacks: str = str(response["data"]["products"][0]["feedbacks"])  # количество отзывов
            self.description: str = self.card_description()  # описание товара из карточки
            self.urls_images: list = self.card_images()  # ссылки на изображения
            return True
        else: 
            return False


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
    


async def checking_price(old_price: int, new_price: int):
    '''Асинхронная функция провереят стала ли цена ниже.
    На вход принимает старую цену и новую. Возвращает булево значение.'''
    if new_price < old_price:
        pass
    else:
        return False


            
    
class Tracking:
    def __init__(self, tg_id: str, username: str, wb_id: str, stop_price: int=0) -> None:
        self.wb_id: str = wb_id  # подаваемый id товара 
        self.tg_id: str = tg_id  # tr id пользователя
        self.stop_price = stop_price  # цена при которой отправляется оповещение пользователю
        self.username: str = username

        pars = ParsWB(id_card=wb_id)  # создание объекта парсера
        pars.datas_card()  # выполняется процесс парсинга товара
        self.product_name: str = pars.name  # имя товара
        self.new_price: str = pars.price_for_track  # новая цена товара



    def _create_db(self) -> None:
        '''Функция создает базу данных'''
        connection = sqlite3.connect('./data/db/_users.db')  # утанавливаем и создает базу данных
        cursor = connection.cursor()  # устанавливаем курсор
        
        # создает таблицу пользователей
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (  
                    user_id INTEGER PRIMARY KEY,
                    tg_id INTEGER UNIQUE, 
                    username TEXT NOT NULL
        )''')  
        connection.commit()  # выполняем изменения(совершаем)

        # создает таблицу товаров
        cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id INTEGER PRIMARY KEY,
                        wb_id TEXT UNIQUE, 
                        product_name TEXT NOT NULL,
                        price INTEGER,
                        stop_price Integer
        )''')
        connection.commit()  # выполняем изменения(совершаем)

        # создает таблицу подписок
        cursor.execute('''CREATE TABLE IF NOT EXISTS Subscriptions (
                    sub_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    product_id INTERGER,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )''')
        connection.commit()  # выполняем изменения(совершаем)

        connection.close()  # закрываем соединение



    def _insert_user_to_db(self) -> None:  
        '''Функция заносит пользователя в базу данных, только если его еще нет в ней
        И добавлеяет товар к пользователю.
        На вход принимает кортеж значений (tg_id, username)'''
        connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
        cursor = connection.cursor()  # устанавливаем курсор

        cursor.execute('INSERT OR IGNORE INTO Users (tg_id, user_name) VALUES(?, ?)',  # (?, ?) заносится пользователь если нет в таблице 
                    (self.tg_id, self.username)) 
        connection.commit()  # применяем изменения

        connection.close()  # закрываем соединение



    def _insert_wb_id_to_db(self) -> None:
        '''Метод вставляет товар в таблицу, если его там еще нет'''
        connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
        cursor = connection.cursor()  # устанавливаем курсор


        cursor.execute('INSERT OR IGNORE INTO Products (wb_id, product_name, price, stop_price) VALUES(?, ?, ?, ?)',  # (?, ?) заносится товар если нет в таблице 
                    (self.wb_id, self.product_name, self.new_price, self.stop_price)) 
        connection.commit()  # применяем изменения

        connection.close()  # закрываем соединение

        

    def _tables_ids(self) -> None:
        '''Метод достает табличные id пользователя и товара из таблиц'''
        connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
        cursor = connection.cursor()  # устанавливаем курсор

        cursor.execute('SELECT user_id FROM Users WHERE tg_id = ?', (self.tg_id, ))
        self.user_id = cursor.fetchall()[0][0]  # достает user_id пользователя в таблице

        cursor.execute('SELECT product_id FROM Products WHERE wb_id = ?', (self.wb_id, ))
        self.user_id = cursor.fetchall()[0][0]  # достает product_id товара в таблице

        connection.close()  # закрываем соединение



    def _search_old_price(self) -> int | None:
        '''Метод достает цену которая записана для товара в таблице.'''
        connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
        cursor = connection.cursor()  # устанавливаем курсор

        cursor.execute('SELECT price, stop_price FROM Products WHERE wb_id = ?', (self.wb_id, ))
        self.old_price = cursor.fetchall()[0[0]]
        self.stop_price = cursor.fetchall()[0][1]
        

        connection.close()  # закрываем соединение



    def _replace_price(self) -> None:
        '''Метод заменяет цену в таблицы на новую'''
        connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
        cursor = connection.cursor()  # устанавливаем курсор

        cursor.execute('UPDATE Products SET price = ? WHERE wb_id = ?', (self.new_price, self.wb_id))

        connection.commit()  # применяем изменения
        connection.close()  # закрываем соединение

        

    def check_price(self) -> None: 
        '''Метод сравниванивает новую цену с ценой записанной в таблице. 
        Если цена новая ниже, записывает ее в таблицу'''
        self._search_old_price()  #  метод достающий цену из таблицы

        if self.new_price <= self.stop_price:  # если новый цена ниже или равна ожидаемой цене оповещаем пользователя об этом
            pass  # доделать механизм
        else:  
            if self.new_price < self.old_price:  # если новая цена ниже той что есть в таблице - переписываем в таблице
                self._replace_price() 
            else:  # если новая цена выше имеющейся или искомой цены ничего не делаем
                return None  # тут тоже наверное доделать механизм


        
        




    






def pars_wb(id_card: str):
    resp = ParsWB(id_card=id_card)
    if resp.datas_card():
        res = f"Наименование товара: {resp.name}\nЦена товара: {resp.price[:-2]} руб.\nРейтинг товвара: {resp.rating}\nКоличество отзывов: {resp.feedbacks}\n\nСсылки на изображение:\n{'\n'.join(resp.urls_images)}\n\nОписание товара: {resp.description}"
    else:
        res = None
    return res




'''
resp = ParsWB(id_card=str(110291183))
resp.datas_card()
print(int(resp.price[:-2]) > 4000)'''


