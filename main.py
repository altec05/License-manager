# пакеты
from tkinter import ttk
from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox
import os

# модули программы
import License_db as db
import add_lic as add
import check_funcs
import get_messages as mes
import variables as var
from variables import path_db
import table_win
import edit_lic
import get_messages as ms
import service
import filter
import search
import login


def open_changes():
    if check_funcs.check_path(var.path_changes):
        os.system(fr"explorer.exe {var.path_changes}")
    else:
        mes.error('Открытие файла', 'Файл с изменениями не найден!')


def export_data():
    result = service.export_data_to_xlsx()
    if result == True:
        mes.info('Экспорт данных', 'Экспорт данных на сервер успешно выполнен!\n\nСейчас откроется папка с документом.')
        # По завершению открываем папку с полученными файлами
        os.system(
            fr"explorer.exe {var.path_xlsx_out.replace(os.path.basename(var.path_xlsx_out), '')}")
    else:
        mes.warning('Экспорт данных', f'Экспорт данных на сервер не выполнен!\n\nПричина:\n{result}.')


def clear_filter():
    combobox_filter.current(0)
    combobox_filter.set('Все')


# Поиск по Названию, СЕРИЙНОМУ НОМЕРУ и Месту установки
def search_for_row():
    row = e_search.get()
    search.search_for_row(f3, row)
    clear_filter()


# Вывод значений по фильтру
def filter_items(event):
    filter_value = combobox_filter.get()
    filter.show_only_for_filter(event, f3, filter_value, show_table)


# Изменить пароль для входа в приложение
def edit_pass():
    login.change_pass()


# Запуск резервного копирования файлов БД
def start_backup():
    mes.info('Резервное копирование', 'Внимание!\nРезервное копирование будет проведено в два этапа в разные'
                                      ' расположения на сервере!')
    service.backup_bd('')
    service.backup_bd(var.path_all_backups_on_server)


def root_closing():
    login.check_or_create_pass_key_file()
    login.check_or_create_pass_file()
    if not login.check_encrypt():
        print('Зашифровываю перед выходом из программы...')
        login.encrypt_pass()
    root.destroy()
    root.quit()


def first_backup():
    service.write_backup_file(1)
    service.get_backup(root_closing, 1)


# Запуск резервного копирования файлов БД
def get_backup():
    clear_frame()
    service.get_backup(root_closing, 0)
    show_table()


# очистка фрейма, содержащего таблицу для её обновления
def clear_frame():
    for widget in f3.winfo_children():
        widget.destroy()


def create_table():
    result = ''
    if db.check_db_silent():
        reuslt = mes.ask('Создание таблицы', 'Внимание!\nТаблицы уже существует, действительно хотите пересоздать её, что приведет к потере имеющихся данных?')
        if reuslt:
            db.del_licenses()
            db.create_db()
            clear_frame()
            reload()
        else:
            mes.warning('Создание таблицы', 'Операция отменена пользователем!')
    else:
        db.create_db()
        clear_frame()
        reload()


def delete_table():
    if db.check_db():
        db.del_licenses()
        clear_frame()


# если таблица существует, то сбрасываем временные переменные и показываем таблицу
def reload():
    if db.check_db():
        # var.temp_sort = 0
        var.id_value = ''
        var.list_del_values.clear()
        show_table()


# если таблица существует, то сбрасываем временные переменные и показываем таблицу
def full_reload():
    if db.check_db():
        var.temp_sort = 0
        var.id_value = ''
        var.list_del_values.clear()
        var.back_to_sort = False
        show_table()
        clear_filter()


# отркываем новое окно создания и сворачиваем главное окно
def hide_win():
    if db.check_db():
        add.new_lic(root, reload)
        root.withdraw()
        clear_filter()


# удалить выбранную запись
def delete_id():
    question = ''
    items = ''
    if len(var.list_del_values) > 1:
        print(f'Список элементов на удаление: {var.list_del_values}')
        print(f'Отсортированный список элементов на удаление: {var.list_del_values.sort()}')
        if len(var.list_del_values) > 2 or len(var.list_del_values) == 2 and var.list_del_values[0][0] == var.list_del_values[1][0]:
            for item in var.list_del_values:
                indexes = [i for i in range(len(var.list_del_values)) if var.list_del_values[i] == item]
                print(f'Элемент: {item} и индексы: {item}')
                print(item, indexes)
                rev_indxs = indexes[::-1]
                print(rev_indxs)
                rev_indxs = rev_indxs[0:len(rev_indxs)-1]
                print(rev_indxs)
                for ind in rev_indxs:
                    print(f'Удаляем {var.list_del_values[ind]} по {ind}')
                    del var.list_del_values[ind]

        for item in var.list_del_values:
            row = '№ ' + str(item[0]) + ' "' + str(item[1]) + '"\n'
            items += row

        question = messagebox.askokcancel(title='Удаление записей', message=f'Вы уверены, что хотите удалить указанные записи?:\n'
                                                                           f'{items}')
        if question:
            print(var.list_del_values)
            error_flag = False
            for item in var.list_del_values[::-1]:
                if not db.del_id(item[0]):
                    error_flag = True
            if not error_flag:
                mes.info('Удаление записей', 'Записи успешно удалены!')
            var.id_value = ''
            var.list_del_values.clear()
            reload()
        else:
            var.id_value = ''
            var.list_del_values.clear()
            print(var.list_del_values)
    else:
        question = messagebox.askokcancel(title='Удаление записи', message=f'Вы уверены, что хотите удалить запись '
                                                                       f'№ {var.id_value} "{var.name_value}"?')
        if question:
            print(var.id_value)
            if db.del_id(var.id_value):
                var.id_value = ''
                mes.info('Удаление записи', 'Запись успешно удалена!')
            else:
                var.id_value = ''
            reload()
        else:
            var.id_value = ''


def clear_table():
    result = ''
    if db.check_db_silent():
        reuslt = mes.ask('Очистка таблицы',
                         'Внимание!\nВы действительно хотите очистить таблицу, что приведет к потере имеющихся данных?')
        if reuslt:
            if db.clear_db():
                reload()
            else:
                reload()
        else:
            mes.warning('Очистка таблицы', 'Операция отменена пользователем!')
    else:
        db.check_db()


def edit_table():
    if var.id_value != '':
        data = [var.id_value, var.name_value, var.serial_number_value, var.count_value, var.date_of_purchase_value,
                var.place_of_use_value, var.date_of_use_value]
        edit_lic.edit_value(root, data, reload)
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
        edit_lic.edit_value(root, data, reload)
        root.withdraw()
    else:
        pass


def sort_id():
    table_win.sort_id(f3)
    clear_filter()


def sort_name():
    table_win.sort_name(f3)
    clear_filter()


def sort_sn():
    table_win.sort_sn(f3)
    clear_filter()


def sort_count():
    table_win.sort_count(f3)
    clear_filter()


def sort_dop():
    table_win.sort_dop(f3)
    clear_filter()


def sort_pou():
    table_win.sort_pou(f3)
    clear_filter()


def sort_dou():
    clear_frame()
    table_win.sort_dou(f3)
    clear_filter()


# показать таблицу, бинды действий, меню на пкм
def show_table():
    def check_id_value(event):
        id_value = var.id_value
        do_popup(event, id_value)

    def do_popup(event, id_value):
        var.back_to_sort = False
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
            m.add_command(label="Удалить выбранные записи", command=delete_id)
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
            m.add_command(label="Обновить", command=full_reload)

        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    root.bind("<Button-3>", check_id_value)
    root.bind("<Double-Button-1>", edit_table_ev)

    # clear_frame()
    print(f'var.temp_sort = {var.temp_sort}', var.back_to_sort)
    if var.temp_sort != 0:
        clear_frame()
        clear_filter()
        sort = var.temp_sort
        if var.back_to_sort == True:
            if sort == 1 or sort == 2:
                sort_id()
                var.back_to_sort = False
            elif sort == 3 or sort == 4:
                sort_name()
                var.back_to_sort = False
            elif sort == 5 or sort == 6:
                sort_sn()
                var.back_to_sort = False
            elif sort == 7 or sort == 8:
                sort_count()
                var.back_to_sort = False
            elif sort == 9 or sort == 10:
                sort_dop()
                var.back_to_sort = False
            elif sort == 11 or sort == 12:
                sort_pou()
                var.back_to_sort = False
            elif sort == 13 or sort == 14:
                sort_dou()
                var.back_to_sort = False
        else:
            clear_frame()
            if db.check_db():
                data = ()
                with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM licenses ORDER BY id DESC")
                    data = (row for row in cursor.fetchall())
                    cursor.close()

                table = table_win.Table(f3, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                      'Место установки', 'Дата установки'), rows=data)
                table.pack(expand=tk.YES, fill=tk.BOTH)
            else:
                mes.error('Вывод таблицы', 'Таблица не существует!')
    else:
        clear_frame()
        if db.check_db():
            data = ()
            with sqlite3.connect(path_db + '/Licenses.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM licenses ORDER BY id DESC")
                data = (row for row in cursor.fetchall())
                cursor.close()

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
root.protocol("WM_DELETE_WINDOW", root_closing)

main_menu = Menu(root)
root.config(menu=main_menu, bg="#F1EEE9")

# Взаимодействие с таблицей из БД
table_menu = Menu(main_menu, tearoff=0)
table_menu.add_command(label="Очистить таблицу", command=clear_table)
table_menu.add_command(label="Создать таблицу", command=create_table)
table_menu.add_command(label="Удалить таблицу", command=delete_table)
table_menu.add_command(label="Проверить существование таблицы", command=db.check_db_and_mes)
main_menu.add_cascade(label="База данных", menu=table_menu)

# Вспомогательные функции
service_menu = Menu(main_menu, tearoff=0)
service_menu.add_command(label="Провести резервное копирование БД на сервер", command=start_backup)
service_menu.add_command(label="Восстановить БД из резервной копии", command=first_backup)
service_menu.add_command(label="Изменить пароль входа в приложение", command=edit_pass)
service_menu.add_command(label="Экспорт данных", command=export_data)
main_menu.add_cascade(label="Сервис", menu=service_menu)

# Версия
version_menu = Menu(main_menu, tearoff=0)
version_menu.add_command(label="Версия: 1.2")
version_menu.add_command(label="Изменения", command=open_changes)
main_menu.add_cascade(label="О программе", menu=version_menu)

status = service.check_backup_status()
if status == 'True':
    print(status)
    get_backup()

# Проверка входа перед выводом данных
root.withdraw()
if not login.check_enter():
    root_closing()
else:
    root.deiconify()

    f1 = Frame(root)
    f1.pack(fill=X, padx=10, pady=10)

    f3 = Frame(root, bg='#73777B')
    f3.pack(fill=BOTH, expand=True, padx=10, pady=10)

    languages = ['Все', 'Установлены',  'Не установлены']
    # по умолчанию будет выбран первый элемент из languages
    languages_var = StringVar(value=languages[0])

    label = ttk.Label(f1, text='Фильтр по: ')
    label.pack(side=LEFT)

    combobox_filter = ttk.Combobox(f1, textvariable=languages_var, values=languages, takefocus=0)
    combobox_filter['state'] = 'readonly'
    combobox_filter.pack(side=LEFT)

    btn_start_search = Button(f1, font="Helvetica 9", bg="white", text='Найти', command=search_for_row, padx=10, pady=5)
    btn_start_search.pack(side=RIGHT)

    e_search = Entry(f1, font="Helvetica 9", width=50, state=NORMAL)
    e_search.pack(padx=10, ipady=2, side=RIGHT)

    combobox_filter.bind("<<ComboboxSelected>>", filter_items)

    print(status)
    # обновляем таблицу при открытии программы
    reload()

    root.mainloop()
