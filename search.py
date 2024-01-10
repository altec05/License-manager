# пакеты
import tkinter as tk
import sqlite3

# модули программы
import License_db as db
import get_messages as mes
from variables import path_db
import table_win


# Функция поиска по строке
def search_for_row(frame, row):
    def sort_list(non_sorted):
        name_id_list = []
        sorted_list = []
        sorted_name_id_list = []
        id_counter = 0
        # Получаем элементы и их порядковый id
        for item in non_sorted:
            name_id_list.append((item[1], id_counter))
            id_counter += 1
        # Сортируем по имени
        sorted_name_id_list = sorted(name_id_list)
        # Получаем элементы по порядковым номерам из отсортированного списка
        for item in sorted_name_id_list:
            sorted_list.append(non_sorted[item[1]])
        return sorted_list

    def show_results(results):
        data = (row for row in results)

        for widget in frame.winfo_children():
            widget.destroy()

        table = table_win.Table(frame, headings=('ID', 'Название', 'Серийный номер', 'Шт.', 'Дата получения',
                                                 'Место установки', 'Дата установки'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        mes.info('Результаты поиска', f'Найдено подходящих записей: {len(results)}')

    def get_results(find_sub_row, where_find, step):
        db1 = sqlite3.connect(path_db + '/Licenses.sqlite',
                              detect_types=sqlite3.PARSE_DECLTYPES |
                                           sqlite3.PARSE_COLNAMES)
        cursor = db1.cursor()
        print(where_find)
        need_find = ''
        if step == 1:
            # По Названию
            need_find = str(find_sub_row).title()
        elif step == 2:
            # По серийному номеру
            need_find = str(find_sub_row).upper()
        elif step == 3:
            # По месту установки
            need_find = str(find_sub_row).capitalize()
        # Общий поиск
        sql_search_query = f"""SELECT * FROM licenses WHERE {where_find} LIKE '%{need_find}%' ORDER BY name ASC"""
        print(sql_search_query)
        cursor.execute(sql_search_query)
        finded_rows = cursor.fetchall()
        print(finded_rows)
        result = list()
        data = ()
        for row in finded_rows:
            result.append(row)
        db1.close()
        return result

    def find_sub_row_in_bd(find_sub_row):
        for widget in frame.winfo_children():
            widget.destroy()

        if db.check_db_silent():
            send_data = list()
            first_search = get_results(find_sub_row, 'name', 1)
            second_search = get_results(find_sub_row, 'serial_number', 2)
            third_search = get_results(find_sub_row, 'place_of_use', 3)
            if len(first_search) > 0:
                send_data += first_search
            if len(second_search) > 0:
                send_data += second_search
            if len(third_search) > 0:
                send_data += third_search
            # Очищаем результаты от повторений по id
            for row in send_data:
                # Ищем все индексы вхождений id в список
                indeces = [i for i in range(len(send_data)) if send_data[i] == row]
                rev_indxs = list()
                # Если больше 1 раза id
                if len(indeces) > 1:
                    # Переворачиваем индексы для удаления без смещений с конца к началу
                    for i in indeces[::-1]:
                        rev_indxs.append(i)
                    # Удаляем по индексу из списка
                    for i in rev_indxs[:len(rev_indxs)-1]:
                        print(f'Удаляем {send_data[i]} по {i}')
                        del send_data[i]
            send_data.sort()
            return send_data
        else:
            mes.error('Поиск в БД', 'Ошибка: таблица не существует!')

    if row != '':
        find_row = str(row)
        show_results(sort_list(find_sub_row_in_bd(find_row)))