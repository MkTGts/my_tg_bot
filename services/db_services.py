import sqlite3
import logging
import os
from services.services import ParsWB


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


def _create_db() -> None:
    '''Функция создает базу данных'''
    connection = sqlite3.connect('./data/db/_users.db')  # утанавливаем и создает базу данных
    cursor = connection.cursor()  # устанавливаем курсор
    
    # создает таблицу пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (  
                user_id INTEGER PRIMARY KEY,
                tg_id INTEGER, 
                username TEXT NOT NULL
    )''')  
    connection.commit()  # выполняем изменения(совершаем)

    # создает таблицу товаров
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                    product_id INTEGER PRIMARY KEY,
                    wb_id TEXT UNIQUE, 
                    product_name TEXT NOT NULL,
                    price INTEGER
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
    logger.info("Создана база данных users.db")



def _insert_user_to_db(val: tuple[str, str]) -> None:  
    '''Функция заносит пользователя в базу данных, только если его еще нет в ней
    И добавлеяет товар к пользователю.
    На вход принимает кортеж значений (tg_id, username)'''
    connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
    cursor = connection.cursor()  # устанавливаем курсор

    cursor.execute('INSERT INTO Users (tg_id, user_name) VALUES(?, ?)',  # (?, ?) заносится пользователь если нет в таблице 
                 val) 
    connection.commit()  # применяем изменения
    connection.close()  # закрываем соединение

    logger.info(f"Пользователь с id {val[0]} и именем {val[1]} добавлен в базу user.db")



def _insert_product(wb_id: str) -> None:
    '''Функция вставляет в базу товаров новый товар, если его в базе еще нет.'''
    flag = False

    pars = ParsWB(id_card=wb_id)  # создание объекта парсера
    pars.datas_card()  # выполняется процесс парсинга товара
    product_name = pars.name  # имя товара
    new_price = pars.price_for_track  # новая цена товара

    connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
    cursor = connection.cursor()  # устанавливаем курсор
    cursor.execute('SELECT price FROM Products WHERE wb_id = ?', (wb_id))  # достает значения цены
    lst = cursor.fetchall()[0][0]  # присваивает полученные значения   

    if lst:  # если значение цены для данного товара есть в базе
        flag = False  # ничего делать не нужно
        pass
        old_price = lst[0][0]  # цена из сохраненная в таблице
        if new_price < old_price:  # если новая цена ниже цены записанной в таблице
            pass
        else:  # если новая цена выше записанной в таблице
            flag = False  # ничего делать не нужно
            
    else:  # если данного товара нет в таблице
        cursor.execute('INSERT OR IGNORE INTO Products (wb_id, product_name, price) VALUES(?, ?, ?, ?)',
                    (wb_id, ))
        flag = True
    

    connection.commit()  # применяем изменения
    connection.close()  # закрываем соединение



def fixet_product_price(wb_id: str) -> None:
    connection = sqlite3.connect('./data/db/_users.db')  # подключаемся к базе данных
    cursor = connection.cursor()  # устанавливаем курсор

    pars = ParsWB(id_card=wb_id)
    pars.datas_card()
    product_name = pars.name
    new_price = pars.price_for_track

    connection.commit()  # применяем изменения
    connection.close()  # закрываем соединение
















_create_db()
connection = sqlite3.connect('./data/db/_users.db')  # утанавливаем и создает базу данных
cursor = connection.cursor()  # устанавливаем курсор

#cursor.execute('INSERT INTO Users (username) VALUES(?)', ('Manka',)) # (?, ?) ставится что бы потом по шаблону подать кортеж
                

#cursor.execute('INSERT INTO Products (product_name, current_price, previous_price) VALUES(?, ?, ?)',  ('Korm', 1500, 1700))# (?, ?) ставится что бы потом по шаблону подать кортеж


#cursor.execute('INSERT INTO Subscriptions (user_id, product_id) VALUES(?, ?)', (3, 1))

#cursor.execute('INSERT INTO Products (product_name, current_price, previous_price) VALUES(?, ?, ?)', ('Keyboard', 5000, 5000))
#cursor.execute('INSERT INTO Subscriptions (user_id, product_id) VALUES(?, ?)', (1, 4))



connection.commit()             

cursor.execute('''SELECT user_id FROM Users WHERE username = 'Maksim';
                SELECT product_id FROM Products WHERE product_name = "Keyboard"
''')

#cursor.execute('SELECT * FROM Products')
#cursor.execute('''SELECT Products.current_price, Products.previous_price FROM Products
#               JOIN Subscriptions ON Products.product_id = Subscriptions.product_id
#               JOIN Users ON Users.user_id = Subscriptions.user_id
#               WHERE Users.username = 'Maksim'
#               ''')
lst = cursor.fetchall()
connection.close()
print(lst)




def create_db() -> None:
    '''Функция создает базу данных'''
    connection = sqlite3.connect('./data/db/users.db')  # утанавливаем и создает базу данных
    cursor = connection.cursor()  # устанавливаем курсор

    # создаем таблицу пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (  
                id INTEGER PRIMARY KEY,
                tg_id TEXT NOT NULL,
                user_name TEXT,
                wb_id TEXT NOT NULL
    )''')  
    connection.commit()  # выполняем изменения(совершаем)

    # создаем таблицу id товаров
    cursor.execute('''CREATE TABLE IF NOT EXISTS Id_wb (
                id INTEGER PRIMARY KEY,
                wb_id INTEGER, 
                FOREIGN KEY (wb_id) REFERENCES Users(wb_id)
    )''')
    connection.commit()

    connection.close()  # закрываем соединение
    logger.info("Create database users.db")


def insert_user_to_db(val: tuple[str, str, str]) -> None:  
    '''Функция заносит пользователя в базу данных, только если его еще нет в ней
    На вход принимает кортеж значений (tg_id, user_name, wb_id)'''
    con = sqlite3.connect('./data/db/users.db')  # подключаемся к базе данных
    curs = con.cursor()  # устанавливаем курсор

    curs.execute('INSERT INTO Users (tg_id, user_name, wb_id) VALUES(?, ?, ?)',  # (?, ?) ставится что бы потом по шаблону подать кортеж
                 val)  # val должен быть кортежем

    con.commit()  # применяем изменения
    con.close()  # закрываем соединение

    logger.info(f"Пользователь с id {val[0]} добавлен в базу user.db")


def verification_user(tg_id: str) -> bool: 
    '''Проверяет есть ли пользователь с таким id в базе данных'''
    connect = sqlite3.connect('./data/db/users.db')
    curs = connect.cursor()

    curs.execute('''SELECT tg_id
                 FROM Users
                WHERE tg_id = ?''',
                (tg_id, ) )
    
    lst = curs.fetchall()
    connect.close()

    return bool(lst)



def all_datas() -> bool:
    '''Возвращает все содержимое базы данных. просто чтобы можно было в консоле посмотреть содержимое базы'''
    connect = sqlite3.connect('./data/db/users.db')
    curs = connect.cursor()

    curs.execute('''SELECT *
                 FROM Users''')
    
   # curs.execute('SELECT * FROM Id_wb')
    
    lst = curs.fetchall()
    connect.close()

    return lst


def set_wb_id(tg_id: str, wb_id:str): 
    '''Функция сохраняет запрашиваемые wb_id
    Записывает просто как стороку в которой через запятую идут все значения.
    Хорошо бы оптимизировать как нибудь'''
    # достает список id и добавляет к нему новый
    connection = sqlite3.connect('./data/db/users.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT wb_id
                 FROM Users
                WHERE tg_id = ?''',
                (tg_id, ) )
    lst = cursor.fetchall()  # все запрашиваемые пользователем id
    if lst:
        res = lst[0][0] + f", {wb_id}"  # все запрашиваемые пользователем id плюс новый через запятую
        cursor.execute('UPDATE Users SET wb_id = ? WHERE tg_id = ?', (res, tg_id))  # запись значения в базу данных
        connection.commit()
        connection.close()



    

    connection.close()  # закрывает базу данных


if not os.path.isfile("./data/db/users.db"):  # если база данных пользователей не существует
    create_db()  # создает базу данных пользователей


def oke_lesgo():
    connection = sqlite3.connect('./data/db/users.db')
    cursor = connection.cursor()
    #cursor.execute('''SELECT *
    #               FROM Id_wb''')
    '''CREATE TABLE IF NOT EXISTS Users (  
                    id INTEGER PRIMARY KEY,
                    tg_id TEXT NOT NULL,
                    user_name TEXT,
                    wb_id TEXT NOT NULL
        )'''
    cursor.execute('INSERT INTO Users (tg_id, user_name, wb_id) VALUES (?, ?, ?)', ('123', 'mktgs', '321'))
    connection.commit()
    connection.close()

#print(all_datas())  # как инструмент разработчика. для просмотра содержимого базы данных
