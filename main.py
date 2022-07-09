# пакеты
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


# очистка фрейма, содержащего таблицу для её обновления
def clear_frame():
    for widget in f3.winfo_children():
        widget.destroy()


def create_table():
    db.create_db()
    clear_frame()
    reload()


def delete_table():
    db.del_licenses()
    clear_frame()


# если таблица существует, то сбрасываем временные переменные и показываем таблицу
def reload():
    if db.check_db():
        var.temp_sort = 0
        var.id_value = ''
        show_table()


# отркываем новое окно создания и сворачиваем главное окно
def hide_win():
    if db.check_db():
        add.new_lic(root)
        var.id_value = ''
        reload()
        root.withdraw()


# удалить выбранную запись
def delete_id():
    question = messagebox.askokcancel(title='Удаление записи', message=f'Вы уверены, что хотите удалить запись '
                                                                       f'№{var.id_value} "{var.name_value}"?')
    if question:
        print(var.id_value)
        if db.del_id(var.id_value):
            var.id_value = ''
        else:
            var.id_value = ''
        reload()


def clear_table():
    if db.clear_db():
        reload()
    else:
        reload()


def edit_table():
    if var.id_value != '':
        data = [var.id_value, var.name_value, var.serial_number_value, var.count_value, var.date_of_purchase_value,
                var.place_of_use_value, var.date_of_use_value]
        edit_lic.edit_value(root, data)
        root.withdraw()
    else:
        pass


# копируем серийный номер выделенной записи
def copy_lic():
    ms.info('Копирование записи', f'Серийный номер записи № {var.id_value} скопирован.')
    reload()
    root.clipboard_clear()
    root.clipboard_append(var.serial_number_value)
    var.id_value = ''


# копируем выбранную ячейку
def copy_lic_col():
    if var.temp_value != '':
        ms.info('Копирование ячейки', f'Значение "{var.temp_value}" скопировано.')
        reload()
        root.clipboard_clear()
        root.clipboard_append(var.temp_value)
        # var.id_value = ''
        var.temp_value = ''
    else:
        ms.warning('Копирование ячейки', f'Значение не скопировано так как ячейка пуста.\nЕсли ячейка не пуста, '
                                         f'то просто нажмите после этого уведолмения на ячейку ещё раз.')


# изменение записи по двойному клику
def edit_table_ev(event):
    if var.id_value != '':
        data = [var.id_value, var.name_value, var.serial_number_value, var.count_value, var.date_of_purchase_value,
                var.place_of_use_value, var.date_of_use_value]
        print(f'data перед отправкой: {data}')
        edit_lic.edit_value(root, data)
        root.withdraw()
    else:
        pass


# сортировки по убыванию и возрастанию
def sort_id():
    clear_frame()
    if var.temp_sort != 1:
        head = 'ID ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY id ASC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=(head, 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 1
    else:
        head = 'ID v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY id DESC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=(head, 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 2


def sort_name():
    clear_frame()
    if var.temp_sort != 3:
        head = 'Название ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY name ASC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', head, 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 3
        print(f"var {var.temp_sort}")
    else:
        head = 'Название v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY name DESC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', head, 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 4


def sort_sn():
    clear_frame()
    if var.temp_sort != 5:
        head = 'Серийный номер ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY serial_number ASC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', head, 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 5
    else:
        head = 'Серийный номер v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY serial_number DESC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', head, 'Шт.', 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 6


def sort_count():
    clear_frame()
    if var.temp_sort != 7:
        head = 'Шт. ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY count ASC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', head, 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 7
    else:
        head = 'Шт. v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY count DESC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', head, 'Дата получения',
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 8


def sort_dop():
    clear_frame()
    if var.temp_sort != 9:
        head = 'Дата получения ^'
        clear_frame()
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_purchase ASC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', head,
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 9
    else:
        head = 'Дата получения v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_purchase DESC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', head,
                                                  'Место установки', 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 10


def sort_pou():
    clear_frame()
    if var.temp_sort != 11:
        head = 'Место установки ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY place_of_use ASC")
                data = (row for row in cursor.fetchall())

            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  head, 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 11
    else:
        head = 'Место установки v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY place_of_use DESC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  head, 'Дата установки'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 12


def sort_dou():
    clear_frame()
    if var.temp_sort != 13:
        head = 'Дата установки ^'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_use ASC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', head), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 13
    else:
        head = 'Дата установки v'
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                            sqlite3.PARSE_COLNAMES) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY date_of_use DESC")
                data = (row for row in cursor.fetchall())
            table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                  'Место установки', head), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 14


# показать таблицу, бинды действий, меню на пкм
def show_table():
    def check_id_value(event):
        id_value = var.id_value
        do_popup(event, id_value)

    def do_popup(event, id_value):
        if id_value == '':
            # Контекстное меню на пкм
            m = Menu(root, tearoff=0)
            m.add_command(label="Добавить лицензию", command=hide_win)

            m.add_separator()
            main_sort = Menu(m, tearoff=0)
            sort_menu = Menu(main_sort, tearoff=0)
            m.add_cascade(label="Сортировать", menu=sort_menu)
            sort_menu.add_command(label="ID", command=sort_id)
            sort_menu.add_command(label="Название", command=sort_name)
            sort_menu.add_command(label="Серийный номер", command=sort_sn)
            sort_menu.add_command(label="Количество", command=sort_count)
            sort_menu.add_command(label="Дата получения", command=sort_dop)
            sort_menu.add_command(label="Место установки", command=sort_pou)
            sort_menu.add_command(label="Дата установки", command=sort_dou)

            m.add_separator()
            m.add_command(label="Обновить", command=reload)
        else:
            # Контекстное меню на лкм по записи и пкм
            m = Menu(root, tearoff=0)
            m.add_command(label="Добавить лицензию", command=hide_win)
            m.add_command(label="Редактировать выбранную запись", command=edit_table)
            m.add_command(label="Удалить выбранную запись", command=delete_id)
            m.add_separator()
            main_sort = Menu(m, tearoff=0)
            sort_menu = Menu(main_sort, tearoff=0)
            m.add_cascade(label="Сортировать", menu=sort_menu)
            sort_menu.add_command(label="ID", command=sort_id)
            sort_menu.add_command(label="Название", command=sort_name)
            sort_menu.add_command(label="Серийный номер", command=sort_sn)
            sort_menu.add_command(label="Количество", command=sort_count)
            sort_menu.add_command(label="Дата получения", command=sort_dop)
            sort_menu.add_command(label="Место установки", command=sort_pou)
            sort_menu.add_command(label="Дата установки", command=sort_dou)
            m.add_separator()
            m.add_command(label="Копировать серийный номер", command=copy_lic)
            m.add_command(label="Копировать данные ячейки", command=copy_lic_col)
            m.add_separator()
            m.add_command(label="Обновить", command=reload)

        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    root.bind("<Button-3>", check_id_value)
    root.bind("<Double-Button-1>", edit_table_ev)

    clear_frame()

    if db.check_db():
        data = ()
        with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM licenses ORDER BY id")
            data = (row for row in cursor.fetchall())

        table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                              'Место установки', 'Дата установки'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        mes.error('Вывод таблицы', 'Таблица не существует!')


root = Tk()
root.title('Менеджер лицензий')
root.geometry('1150x600+300+200')
root.resizable(True, True)
root.minsize(500, 300)

main_menu = Menu(root)
root.config(menu=main_menu, bg="#F1EEE9")

# Взаимодействие с таблицей из БД
table_menu = Menu(main_menu, tearoff=0)
table_menu.add_command(label="Очистить таблицу", command=clear_table)
table_menu.add_command(label="Создать таблицу", command=create_table)
table_menu.add_command(label="Удалить таблицу", command=delete_table)
table_menu.add_command(label="Проверить существование таблицы", command=db.check_db)
main_menu.add_cascade(label="База данных", menu=table_menu)

f3 = Frame(root, bg='#73777B')
f3.pack(fill=BOTH, expand=True, padx=10, pady=10)
# обновляем таблицу при открытии программы
reload()

root.mainloop()
