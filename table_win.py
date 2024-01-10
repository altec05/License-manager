import tkinter as tk
from tkinter import ttk
import sqlite3
import License_db as db

import variables as var
from variables import path_db
import get_messages as mes


# класс таблицы с её свойствами и созданием
class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        # выбор ячейки
        def selectItem(event):
            curItem = table.item(table.focus())
            col = table.identify_column(event.x)
            # print(event)
            # print(f'curItem {curItem}')
            if curItem['values'] != '':
                if col == '#1':
                    cell_value = curItem['values'][0]
                elif col == '#2':
                    cell_value = curItem['values'][1]
                elif col == '#3':
                    cell_value = curItem['values'][2]
                elif col == '#4':
                    cell_value = curItem['values'][3]
                elif col == '#5':
                    cell_value = curItem['values'][4]
                elif col == '#6':
                    cell_value = curItem['values'][5]
                elif col == '#7':
                    cell_value = curItem['values'][6]
                if cell_value != '':
                    var.temp_value = cell_value

        # выбор строки
        def item_selected(event):
            for selected_item in table.selection():
                item = table.item(selected_item)
                record = item['values']
                var.id_value = record[0]
                var.name_value = record[1]
                var.serial_number_value = record[2]
                var.count_value = record[3]
                var.date_of_purchase_value = record[4]
                var.place_of_use_value = record[5]
                var.date_of_use_value = record[6]
                temp = [record[0], record[1]]
                var.list_del_values.append(temp)

        table = ttk.Treeview(self, show="headings", selectmode="extended")
        table["columns"] = headings
        table["displaycolumns"] = headings
        # столбцы
        for head in headings:
            if 'ID' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_id(parent))
                table.column(head, anchor=tk.CENTER, width=1)
            elif 'Название' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_name(parent))
                table.column(head, anchor=tk.W, width=1)
            elif 'Серийный номер' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_sn(parent))
                table.column(head, anchor=tk.CENTER, width=30)
            elif 'Шт.' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_count(parent))
                table.column(head, anchor=tk.CENTER, width=30)
            elif 'Дата получения' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_dop(parent))
                table.column(head, anchor=tk.CENTER, width=30)
            elif 'Место установки' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_pou(parent))
                table.column(head, anchor=tk.W, width=30)
            elif 'Дата установки' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_dou(parent))
                table.column(head, anchor=tk.CENTER, width=30)
            else:
                table.heading(head, text=head, anchor=tk.CENTER)
                table.column(head, anchor=tk.CENTER, width=30)
            
        # строки
        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrollYtable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrollYtable.set)
        scrollYtable.pack(side=tk.RIGHT, fill=tk.Y)
        # бинды по клику
        table.bind('<<TreeviewSelect>>', item_selected)
        table.bind("<Button-1>", selectItem)

        table.pack(expand=tk.YES, fill=tk.BOTH)
        
        
# сортировки по убыванию и возрастанию
def sort_id(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 1 or var.back_to_sort == False and var.temp_sort != 1 or var.back_to_sort == True and var.temp_sort != 1:
        head = 'ID ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM licenses ORDER BY id ASC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=(head, 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 1
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 2 or var.back_to_sort == False and var.temp_sort != 2:
        head = 'ID v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM licenses ORDER BY id DESC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=(head, 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 2
        var.back_to_sort = False


def sort_name(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 3 or var.back_to_sort == False and var.temp_sort != 3 or var.back_to_sort == True and var.temp_sort != 3:
        head = 'Название ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY name ASC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', head, 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 3
        var.back_to_sort = False
        print(f"var {var.temp_sort}")
    elif var.back_to_sort == True and var.temp_sort == 4 or var.back_to_sort == False and var.temp_sort != 4:
        head = 'Название v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY name DESC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', head, 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 4
        var.back_to_sort = False


def sort_sn(frame):
    print(var.back_to_sort, var.temp_sort)
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 5 or var.back_to_sort == False and var.temp_sort != 5 or var.back_to_sort == True and var.temp_sort != 5:
        head = 'Серийный номер ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY serial_number ASC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', head, 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 5
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 6 or var.back_to_sort == False and var.temp_sort != 6:
        head = 'Серийный номер v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY serial_number DESC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', head, 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 6
        var.back_to_sort = False
    print(var.back_to_sort, var.temp_sort)


def sort_count(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 7 or var.back_to_sort == False and var.temp_sort != 7 or var.back_to_sort == True and var.temp_sort != 7:
        head = 'Шт. ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY count ASC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', head, 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 7
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 8 or var.back_to_sort == False and var.temp_sort != 8:
        head = 'Шт. v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY count DESC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', head, 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 8
        var.back_to_sort = False


def sort_dop(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 9 or var.back_to_sort == False and var.temp_sort != 9 or var.back_to_sort == True and var.temp_sort != 9:
        head = 'Дата получения ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_purchase ASC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', head,
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 9
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 10 or var.back_to_sort == False and var.temp_sort != 10:
        head = 'Дата получения v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_purchase DESC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', head,
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 10
        var.back_to_sort = False


def sort_pou(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 11 or var.back_to_sort == False and var.temp_sort != 11 or var.back_to_sort == True and var.temp_sort != 11:
        head = 'Место установки ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY place_of_use ASC")
                data = (row for row in cursor.fetchall())

            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  head, 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 11
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 12 or var.back_to_sort == False and var.temp_sort != 12:
        head = 'Место установки v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY place_of_use DESC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  head, 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 12
        var.back_to_sort = False


def sort_dou(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 13 or var.back_to_sort == False and var.temp_sort != 13 or var.back_to_sort == True and var.temp_sort != 13:
        head = 'Дата установки ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_use ASC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', head), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 13
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 14 or var.back_to_sort == False and var.temp_sort != 14:
        head = 'Дата установки v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_use DESC")
                data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', head), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 14
        var.back_to_sort = False
