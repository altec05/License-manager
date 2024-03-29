import locale
from tkinter import *
import sqlite3
import re

import check_funcs
import variables as var
from variables import path_db
import get_messages as mes
import datetime
import get_messages as ms
import service

try:
    locale.setlocale(locale.LC_ALL, 'ru-RU.UTF-8')
except Exception as e:
    mes.error('Ошибка локали', f'Обнаружена ошибка локали:\n\n{[e]}')


def new_lic(root, root_func):
    # проверка наличия обязательных полей
    def check_entry():
        if e_name.get() != '' and e_sn.get() != '':
            return True
        else:
            return False

    # проверка формата даты
    def check_data():
        temp = '-'
        place = [2, 5]
        print(e_date_of_purchase.get())
        if e_date_of_use.get() != '' and e_date_of_purchase.get() != '':  # если есть оба поля
            n_clear1 = e_date_of_use.get()
            n_clear2 = e_date_of_purchase.get()
            clear1 = n_clear1.replace('-', '')
            clear2 = n_clear2.replace('-', '')
            digit1 = ''.join([i for i in n_clear1 if i.isdigit()])
            digit2 = ''.join([i for i in n_clear2 if i.isdigit()])
            if [m.start() for m in re.finditer('-', n_clear1)] == place and [m.start() for m in re.finditer('-',
                                                                                                             n_clear2)] == place:
                if len(digit1) == 8 and len(digit2) == 8:
                    if temp in e_date_of_use.get() and temp in e_date_of_purchase.get():
                        if clear1.isdigit() and clear2.isdigit():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        elif e_date_of_purchase.get() != '':  # если есть поле получено
            n_clear2 = e_date_of_purchase.get()
            clear2 = n_clear2.replace('-', '')
            digit2 = ''.join([i for i in n_clear2 if i.isdigit()])
            print([m.start() for m in re.finditer('-', n_clear2)])
            if [m.start() for m in re.finditer('-', n_clear2)] == place:
                if len(digit2) == 8:
                    if temp in e_date_of_purchase.get():
                        if clear2.isdigit():
                            return True
                        else:
                            print(f"Числа {clear2}")
                            return False
                    else:
                        print(f"Поиск {temp} в {e_date_of_purchase.get()}")
                        return False
                else:
                    print(f"Длина {len(digit2)}")
                    return False
            else:
                print(f"Места {[m.start() for m in re.finditer('-', n_clear2)]}")
                return False
        elif e_date_of_use.get() != '':  # если есть поле установлено
            n_clear1 = e_date_of_use.get()
            clear1 = n_clear1.replace('-', '')
            digit1 = ''.join([i for i in n_clear1 if i.isdigit()])
            if [m.start() for m in re.finditer('-', n_clear1)] == place:
                if len(digit1) == 8:
                    if temp in e_date_of_use.get():
                        if clear1.isdigit():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:  # если нет ни одного
            return True

    # Очистка полей ввода после отправки записи
    def clear_entry():
        e_sn.delete(0, END)
        e_count.delete(0, END)
        e_place.delete(0, END)
        e_date_of_use.delete(0, END)

    # Полная очистка полей ввода после отправки записи
    def clear_entry_full():
        e_name.delete(0, END)
        e_sn.delete(0, END)
        e_count.delete(0, END)
        e_date_of_purchase.delete(0, END)
        e_place.delete(0, END)
        e_date_of_use.delete(0, END)


    # считать данные из полей ввода
    def get_data():
        name = e_name.get()
        name[0].capitalize()
        serial_number = service.check_rus(e_sn.get())

        count = ''
        if e_count.get() != '':
            if check_funcs.check_digit(str(e_count.get())):
                count = int(e_count.get())
            else:
                mes.error('Проверка данных', 'Кол-во должно быть целым числом!')
                return False
        else:
            count = 1
        if e_date_of_purchase.get() != '':
            date_of_purchase = datetime.datetime.strptime(e_date_of_purchase.get(), "%d-%m-%Y")
            send_date_of_purchase = date_of_purchase.date()
        else:
            send_date_of_purchase = ''
        place_of_use = e_place.get()
        if e_date_of_use.get() != '':
            date_of_use = datetime.datetime.strptime(e_date_of_use.get(), "%d-%m-%Y")
            send_date_of_use = date_of_use.date()
        else:
            send_date_of_use = ''

        data = (name, serial_number, count, send_date_of_purchase, place_of_use, send_date_of_use)
        return data

    # отправить введенные данные
    def confirm():
        if check_data():
            if check_entry():
                data = get_data()
                if data != False:
                    db = sqlite3.connect(path_db + '/Licenses.sqlite')
                    cursor = db.cursor()

                    cursor.execute(
                        "INSERT OR IGNORE INTO licenses (name, serial_number, count, date_of_purchase, place_of_use, "
                        "date_of_use) "
                        "VALUES(?, ?, ?, ?, ?, ?)", data)
                    changes = db.total_changes

                    db.commit()
                    if changes > 0:
                        mes.info("Обработка лицензии",
                                 "Лицензия успешно добавлена в таблицу!\nДля отображения изменений "
                                 "обновите таблицу.")
                        clear_entry()
                    else:
                        mes.warning("Обработка лицензии",
                                    "Лицензия не добавлена так как уже зарегистрирована в таблице!")
                    db.close()
                    var.id_value = ''
            else:
                ms.error('Валидация значений', 'Заполните обязательные поля!')

        else:
            ms.error('Валидация значений', 'Ошибка формата даты!\nИспользуйте формат дд-мм-гггг')

    # закртие окна и разворачивание главного окна
    def add_lic_closing():
        var.id_value = ''
        var.back_to_sort = True
        add.destroy()
        root.deiconify()
        root_func()

    def clear():
        clear_entry_full()

    add = Tk()
    add.title('Добавление лицензий')
    add.geometry('600x300+300+200')
    add.resizable(True, False)
    add.minsize(600, 300)
    add.protocol("WM_DELETE_WINDOW", add_lic_closing)

    main_menu = Menu(add)
    add.config(menu=main_menu)

    f1 = Frame(add)
    f1.pack(fill=X, padx=10, pady=10)

    f2 = Frame(add)
    f2.pack(fill=X, padx=10, pady=10)

    f3 = Frame(add)
    f3.pack(fill=X, padx=10, pady=10)

    f4 = Frame(add)
    f4.pack(fill=X, padx=10, pady=10)

    f5 = Frame(add)
    f5.pack(fill=X, padx=10, pady=10)

    f6 = Frame(add)
    f6.pack(fill=X, padx=10, pady=10)

    f7 = Frame(add)
    f7.pack(fill=X, padx=10, pady=10)

    label1 = Label(f1, text='Название: ', font="Verdana 12", width=25, anchor=W)
    label1.pack(side=LEFT)

    label1_1 = Label(f1, text='*', font="Verdana 12", foreground='red', width=1)
    label1_1.pack(side=LEFT)

    e_name = Entry(f1, font="Verdana 9")
    e_name.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label2 = Label(f2, text='Серийный номер: ', font="Verdana 12", width=25, anchor=W)
    label2.pack(side=LEFT)

    label2_1 = Label(f2, text='*', font="Verdana 12", foreground='red', width=1)
    label2_1.pack(side=LEFT)

    e_sn = Entry(f2, font="Verdana 9")
    e_sn.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label3 = Label(f3, text='Шт.: ', font="Verdana 12", width=26, anchor=W)
    label3.pack(side=LEFT)

    e_count = Entry(f3, font="Verdana 9")
    e_count.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label4 = Label(f4, text='Дата получения (дд-мм-гггг): ', font="Verdana 12", width=26, anchor=W)
    label4.pack(side=LEFT)

    e_date_of_purchase = Entry(f4, font="Verdana 9")
    e_date_of_purchase.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label5 = Label(f5, text='Место установки: ', font="Verdana 12", width=26, anchor=W)
    label5.pack(side=LEFT)

    e_place = Entry(f5, font="Verdana 9")
    e_place.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label6 = Label(f6, text='Дата установки (дд-мм-гггг): ', font="Verdana 12", width=26, anchor=W)
    label6.pack(side=LEFT)

    e_date_of_use = Entry(f6, font="Verdana 9")
    e_date_of_use.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    btn_clear_e = Button(f7, font="Verdana 9", bg="#CFCFCF", text='Очистить', command=clear, padx=10, pady=5)
    btn_clear_e.pack(side=LEFT)

    btn_confirm = Button(f7, font="Verdana 9", bg="#fca311", text='Принять', command=confirm, padx=10, pady=5)
    btn_confirm.pack(side=RIGHT)
