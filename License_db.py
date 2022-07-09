import os
import sqlite3
import get_messages
from variables import path_db, path_default
import variables as var


# создать таблицу в БД
def create_db():
    db = sqlite3.connect(path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    create_path()

    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            serial_number TEXT NOT NULL UNIQUE,
            count INTEGER,
            date_of_purchase DATE,
            place_of_use TEXT,
            date_of_use DATE
            )
            ''')
        db.commit()
        db.close()
        get_messages.info('Создание таблицы', 'Таблица создана!')

    except:
        db.close()
        get_messages.error('Создание таблицы', 'Ошибка создания таблицы!')


# очистить таблицу в БД
def clear_db():
    db = sqlite3.connect(path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM licenses")
        db.commit()
        db.close()
        get_messages.info('Очистка таблицы', 'Таблица очищена!')
        return True
    except:
        db.close()
        get_messages.error('Очистка таблицы', 'Ошибка очистки таблицы!')
        return False


# проверка существования записи в БД
def check_id(id_check):
    db = sqlite3.connect(path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        sql_check_id_query = """SELECT * FROM licenses WHERE id = ?"""
        cursor.execute(sql_check_id_query, (id_check,))
        count = cursor.fetchall()
        if len(count) > 0:
            db.close()
            return True
        else:
            db.close()
            return False
    except:
        db.close()
        get_messages.error('Поиск значения в таблице', 'Ошибка поиска значения!')


# удалить запись в БД
def del_id(id_value):
    db = sqlite3.connect(path_db + '/Licenses.sqlite')
    cursor = db.cursor()
    if id_value != '':
        if check_id(id_value):
            try:
                del_ID = id_value
                sql_update_query = """DELETE FROM licenses WHERE id = ?"""
                cursor.execute(sql_update_query, (del_ID,))
                db.commit()
                db.close()
                var.id_value = ''
                get_messages.info('Удаление записи', 'Запись успешно удалена!')
                return True
            except:
                var.id_value = ''
                get_messages.error('Удаление записи', 'Ошибка удаления записи!')
                db.close()
                return False
        else:
            var.id_value = ''
            get_messages.error('Поиск значения в таблице', 'Введенный ID не зарегистрирован!')
    else:
        get_messages.error('Поиск значения в таблице', 'Для удаления выберите значение из таблицы!')


# удалить таблицу из БД
def del_licenses():
    db = sqlite3.connect(path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("DROP TABLE licenses")
        db.commit()
        db.close()
        get_messages.info('Удаление таблицы', 'Таблица успешно удалена!')
    except:
        db.close()
        get_messages.error('Удаление таблицы', 'Ошибка удаления таблицы!')


# проверка пути дял файла БД
def create_path():
    try:
        os.mkdir(path_default)
    except FileExistsError:
        pass
    finally:
        try:
            os.mkdir(path_default + '/Licenses manager')
        except FileExistsError:
            pass
        finally:
            try:
                os.mkdir(path_default + '/Licenses manager' + '/db/')
            except FileExistsError:
                pass


# проверка на существование таблицы
def check_db():
    db = sqlite3.connect(path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM licenses")
        res = cursor.fetchall()
        db.close()
        return True
    except:
        db.close()
        get_messages.error('Проверка таблицы', 'Таблица не существует!')
        return False
