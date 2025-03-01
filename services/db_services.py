import sqlite3
import logging
import os


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


def create_db() -> None:
    '''Функция создает базу данных'''
    connection = sqlite3.connect('./data/db/users.db')  # утанавливаем и создает базу данных
    cursor = connection.cursor()  # устанавливаем курсор

    # создаем таблицу
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (  
                id INTEGER PRIMARY KEY,
                tg_id TEXT NOT NULL,
                user_name TEXT,
                wb_id TEXT NOT NULL
    )''')  
    connection.commit()  # выполняем изменения(совершаем)
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
    

    connection.close()  # закрывает базу данных


if not os.path.isfile("./data/db/users.db"):  # если база данных пользователей не существует
    create_db()  # создает базу данных пользователей


print(all_datas())  # как инструмент разработчика. для просмотра содержимого базы данных
