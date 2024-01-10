import os
import sqlite3
import get_messages as mes
import variables as var


# создать таблицу в БД
def create_db():
    db = sqlite3.connect(var.path_db + '/Licenses.sqlite')
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
        mes.info('Создание таблицы', 'Таблица создана!')

    except Exception as e:
        db.close()
        mes.error('Создание таблицы', f'Ошибка создания таблицы!\n\nОшибка:\n[{e}]')
    finally:
        db.close()


# очистить таблицу в БД
def clear_db():
    db = sqlite3.connect(var.path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM licenses")
        db.commit()
        db.close()
        mes.info('Очистка таблицы', 'Таблица очищена!')
        return True
    except Exception as e:
        db.close()
        mes.error('Очистка таблицы', 'Ошибка очистки таблицы!')
        return False
    finally:
        db.close()


# проверка существования записи в БД
def check_id(id_check):
    db = sqlite3.connect(var.path_db + '/Licenses.sqlite')
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
    except Exception as e:
        db.close()
        mes.error('Поиск значения в таблице', 'Ошибка поиска значения!')
    finally:
        db.close()


# удалить запись в БД
def del_id(id_value):
    db = sqlite3.connect(var.path_db + '/Licenses.sqlite')
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
                # mes.info('Удаление записи', 'Запись успешно удалена!')
                return True
            except Exception as e:
                var.id_value = ''
                mes.error('Удаление записи', f'Ошибка удаления записи!\n\nОшибка: [{e}]')
                db.close()
                return False
            finally:
                db.close()
        else:
            var.id_value = ''
            mes.error('Поиск значения в таблице', 'Введенный ID не зарегистрирован!')
    else:
        mes.error('Поиск значения в таблице', 'Для удаления выберите значение из таблицы!')


# удалить таблицу из БД
def del_licenses():
    db = sqlite3.connect(var.path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("DROP TABLE licenses")
        db.commit()
        db.close()
        mes.info('Удаление таблицы', 'Таблица успешно удалена!')
    except Exception as e:
        db.close()
        mes.error('Удаление таблицы', f'Ошибка удаления таблицы!\n\nОшибка: [{e}]')
    finally:
        db.close()


# проверка пути для файла БД
def create_path():
    try:
        os.makedirs(var.path_db, exist_ok=True)
    except Exception as e:
        mes.error('Создание пути для Базы данных', f'Ошибка создания пути!\n\nОшибка: [{e}]')


# Проверка существования таблицы без уведомлений
def check_db_silent():
    db = sqlite3.connect(var.path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM licenses")
        res = cursor.fetchall()
        db.close()
        return True
    except:
        db.close()
        return False
    finally:
        db.close()


# Проверить существование таблицы и выдать уведомление
def check_db_and_mes():
    if check_db():
        mes.info('Проверка таблицы', 'Таблица существует!')


# проверка на существование таблицы
def check_db():
    db = sqlite3.connect(var.path_db + '/Licenses.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM licenses")
        res = cursor.fetchall()
        db.close()
        return True
    except Exception as e:
        db.close()
        mes.error('Проверка таблицы', 'Таблица не существует!')
        return False
    finally:
        db.close()
