import locale
from tkinter import *
import sqlite3
from variables import path_db
import get_messages as mes
import datetime
import get_messages as ms
import variables as var
import re
import service

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def edit_value(root, data, root_func):
    # проверка наличия обязательных полей
    def check_entry():
        if e_name.get() != '' and e_sn.get() != '':
            return True
        else:
            return False

    # Проверка формата кол-ва
    def check_count():
        if e_count.get().isdigit() or e_count.get() == '':
            return True
        else:
            return False

    # проверка формата даты
    def check_data():
        temp = '-'
        place = [2, 5]

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
            if [m.start() for m in re.finditer('-', n_clear2)] == place:
                if len(digit2) == 8:
                    if temp in e_date_of_purchase.get():
                        if clear2.isdigit():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
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

    # очистка глобальных переменных
    def clear_var():
        var.id_value = ''
        var.name_value = ''
        var.serial_number_value = ''
        var.count_value = ''
        var.date_of_purchase_value = ''
        var.place_of_use_value = ''
        var.date_of_use_value = ''

    # очистка полей ввода после отправки записи
    def clear_entry():
        e_name.delete(0, END)
        e_sn.delete(0, END)
        e_count.delete(0, END)
        e_date_of_purchase.delete(0, END)
        e_place.delete(0, END)
        e_date_of_use.delete(0, END)

    # заполнение полей ввода при открытии редактирования записи
    def fill_entry():
        def get_true_format(data):
            day = data[8:10]
            month = data[4:7]
            year = data[0:4]
            temp = day + month + '-' + year
            return temp
        print(f'fill data: {data}')
        e_name.insert(0, data[1])
        e_sn.insert(0, data[2])
        e_count.insert(0, data[3])
        if data[4] != '':
            date_op = datetime.datetime.strptime(get_true_format(data[4]), "%d-%m-%Y").strftime("%d-%m-%Y")
        else:
            date_op = ''
        e_date_of_purchase.insert(0, str(date_op))
        e_place.insert(0, data[5])
        if data[6] != '':
            date_ou = datetime.datetime.strptime(get_true_format(data[6]), "%d-%m-%Y").strftime("%d-%m-%Y")
        else:
            date_ou = ''
        e_date_of_use.insert(0, str(date_ou))

    # считать данные из полей ввода
    def get_data():
        name = e_name.get()
        serial_number = service.check_rus(e_sn.get())
        if e_count.get() == '':
            count = 1
        else:
            count = e_count.get()
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
        send_data = (name, serial_number, count, send_date_of_purchase, place_of_use, send_date_of_use)
        return send_data

    # отправить введенные данные
    def confirm():
        if check_data():
            if check_count():
                print(f'data: {data}')
                id_value = data[0]
                send_data = get_data()
                db = sqlite3.connect(path_db + '/Licenses.sqlite')
                cursor = db.cursor()
                print(f'send_data: {send_data}')
                sql_update_query = """UPDATE licenses SET name = ?, serial_number = ?, count = ?, date_of_purchase = ?, 
                place_of_use = ?, date_of_use = ? WHERE id = ?"""
                query_data = (send_data[0], send_data[1], send_data[2], send_data[3], send_data[4], send_data[5], id_value)
                cursor.execute(sql_update_query, query_data)

                changes = db.total_changes
                cursor.close()

                db.commit()
                if changes > 0:
                    mes.info("Обработка лицензии", "Лицензия успешно обновлена!\nДля отображения изменений обновите "
                                                   "таблицу.")
                else:
                    mes.warning("Обработка лицензии",
                                "Лицензия не обновлена так как серийный номер уже существует в таблице!")
                db.close()
                clear_var()
                edit_lic_closing_with_reload()
            else:
                ms.error('Валидация значений', 'Ошибка формата количества!\nЗначение должно быть числом!')
        else:
            ms.error('Валидация значений', 'Ошибка формата даты!\nИспользуйте формат дд-мм-гггг')

    # закртие окна и разворачивание главного окна
    def edit_lic_closing_no_reload():
        var.id_value = ''
        var.back_to_sort = True
        edit.destroy()
        root.deiconify()

    # закртие окна и разворачивание главного окна
    def edit_lic_closing_with_reload():
        var.id_value = ''
        var.back_to_sort = True
        edit.destroy()
        root.deiconify()
        root_func()

    edit = Tk()
    edit.title('Редактор лицензий')
    edit.geometry('600x300+300+200')
    edit.resizable(True, False)
    edit.minsize(600, 300)
    edit.protocol("WM_DELETE_WINDOW", edit_lic_closing_no_reload)

    main_menu = Menu(edit)
    edit.config(menu=main_menu)

    f1 = Frame(edit)
    f1.pack(fill=X, padx=10, pady=10)

    f2 = Frame(edit)
    f2.pack(fill=X, padx=10, pady=10)

    f3 = Frame(edit)
    f3.pack(fill=X, padx=10, pady=10)

    f4 = Frame(edit)
    f4.pack(fill=X, padx=10, pady=10)

    f5 = Frame(edit)
    f5.pack(fill=X, padx=10, pady=10)

    f6 = Frame(edit)
    f6.pack(fill=X, padx=10, pady=10)

    f7 = Frame(edit)
    f7.pack(fill=X, padx=10, pady=10)

    label1 = Label(f1, text='Название: ', font="Verdana 12", width=25, anchor=W)
    label1.pack(side=LEFT)

    e_name = Entry(f1, font="Verdana 9")
    e_name.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label2 = Label(f2, text='Серийный номер: ', font="Verdana 12", width=25, anchor=W)
    label2.pack(side=LEFT)

    e_sn = Entry(f2, font="Verdana 9")
    e_sn.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label3 = Label(f3, text='Шт.: ', font="Verdana 12", width=26, anchor=W)
    label3.pack(side=LEFT)

    e_count = Entry(f3, font="Verdana 9")
    e_count.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label3 = Label(f4, text='Дата получения (дд-мм-гггг): ', font="Verdana 12", width=25, anchor=W)
    label3.pack(side=LEFT)

    e_date_of_purchase = Entry(f4, font="Verdana 9")
    e_date_of_purchase.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label4 = Label(f5, text='Место установки: ', font="Verdana 12", width=25, anchor=W)
    label4.pack(side=LEFT)

    e_place = Entry(f5, font="Verdana 9")
    e_place.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label5 = Label(f6, text='Дата установки (дд-мм-гггг): ', font="Verdana 12", width=25, anchor=W)
    label5.pack(side=LEFT)

    e_date_of_use = Entry(f6, font="Verdana 9")
    e_date_of_use.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    btn_confirm = Button(f7, font="Verdana 9", bg="#fca311", text='Принять', command=confirm, padx=10, pady=5)
    btn_confirm.pack(side=LEFT)

    # заполянем поля при открытии формы
    fill_entry()