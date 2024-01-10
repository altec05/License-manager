import os
from pathlib import Path


# Проверка на пустоту каталога
def empty_or_not(path):
    return next(os.scandir(path), None)


# Проверка запрашиваемого пути
def check_path(ch_path):
    if os.path.exists(ch_path):
        return True
    else:
        return False


# Проверка строки на числа
def check_digit(row):
    if row.isdigit():
        return True
    else:
        return False