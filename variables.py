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
# переменная для сортировки
temp_sort = 0
back_to_sort = False

# Список для удаления нескольких записей
list_del_values = list()

# Переменная для хранения текущих значений в таблице
data_value = list()

# # пути для функций и БД
# path_default = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
# path_db = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents', 'Licenses manager', 'db')

# Пути для конфига и БД
# path_default = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
path_db = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер лицензий\База данных"

# Пароль для входа в приложение
path_pass_byte_folder = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер лицензий\База данных\config"
path_pass_byte_file = os.path.join(path_pass_byte_folder, 'pass.pkl')

# Пути для резервного копирования
path_server_backup = r'\\192.168.15.4\Soft\Программирование\Py\Менеджер лицензий\Резервная копия БД'
path_all_backups_on_server = r"\\192.168.15.4\Soft\Программирование\Py\Резервные копии\Менеджер лицензий"

# Файл для операции резервного восстановления
path_start_backup_txt_folder = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер лицензий\База данных\config"
path_start_backup_txt_file = os.path.join(path_start_backup_txt_folder, 'backup_need_status.txt')

# Путь файла ключа шифрования
path_crypto_key_folder = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер лицензий\База данных\config"
path_crypto_key_file = os.path.join(path_crypto_key_folder, 'crypto_key.key')

# Путь до файла с выгруженными данными
path_xlsx_out = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер лицензий\База данных\licenses.xlsx"

# Путь до файла с изменениями версий
path_changes = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер лицензий\ПО Менеджер лицензий\Менеджер лицензий\change_log.txt"
