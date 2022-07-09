import tkinter as tk
from tkinter import ttk

import variables as var


# класс таблицы с её свойствами и созданием
class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        # выбор ячейки
        def selectItem(event):
            curItem = table.item(table.focus())
            col = table.identify_column(event.x)
            print(event)
            print(f'curItem {curItem}')
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

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
        # столбцы
        for head in headings:
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
