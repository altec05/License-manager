import os

# временные глобальные переменные
id_value = ''
name_value = ''
serial_number_value = ''
count_value = ''
date_of_purchase_value = ''
place_of_use_value = ''
date_of_use_value = ''

# переменная для копирования
temp_value = ''
# перменная дял сортировки
temp_sort = 0

# пути для функций и БД
path_default = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
path_db = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents', 'Licenses manager', 'db')
