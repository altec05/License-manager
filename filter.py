# пакеты
from tkinter import ttk
from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox

# модули программы
import License_db as db
import add_lic as add
import get_messages as mes
import variables as var
from variables import path_db
import table_win
import edit_lic
import get_messages as ms
import service


# Вывод по метке
def show_only_for_filter(event, frame, filter_value, show_table):
    def show_filtered(filtered_items_list):
        if len(filtered_items_list) > 0:
            data = (row for row in filtered_items_list)

            for widget in frame.winfo_children():
                widget.destroy()

            table = table_win.Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                     'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            mes.info('Фильтр по факту установки', f'Записей, с запрашиваемым фильтром: {len(filtered_items_list)}')
        else:
            mes.warning("Фильтр по факту установки", "Не найдено записей с запрашиваемым фильтром.")

    def find_by_filter(query):
        print(f'query:\n{query}')
        if db.check_db_silent():
            db1 = sqlite3.connect(path_db + '/Licenses.sqlite')
            cursor = db1.cursor()
            sql_filter_query = query
            # sql_update_query = """SELECT * FROM licenses WHERE place_of_use IS NOT NULL OR place_of_use != ''"""
            cursor.execute(sql_filter_query)
            filtered_items = cursor.fetchall()
            items_list = list()
            for item in filtered_items:
                items_list.append(item)
            db1.close()
            return items_list
        else:
            mes.error('Фильтр записей', 'Ошибка: таблица не существует!')
    query = ''
    if filter_value == 'Все':
        show_table()
    elif filter_value == 'Установлены':
        query = """SELECT * FROM licenses WHERE place_of_use != ''"""
        show_filtered(find_by_filter(query))
    elif filter_value == 'Не установлены':
        query = """SELECT * FROM licenses WHERE place_of_use = ''"""
        show_filtered(find_by_filter(query))
    else:
        mes.error('Фильтр записей', f'Ошибка: неизвестный фильтр {filter_value}!')
