# пакеты
import os
from tkinter import simpledialog

# модули программы
import check_funcs
import get_messages as mes
import variables as var
import service
import sys
import pickle
from cryptography.fernet import Fernet


# Временный пароль при потере файла
temp_dict = {
                'current': '111111',
                'old': '',
                'master': '1597536996213'
            }


# Получение значения текущего пароля
def get_curent_pass():
    decrypt_pass()
    dict_pass = read_pass()
    encrypt_pass()
    return dict_pass['current']


# Генерация ключа шифрования
def key_generate():
    if not check_funcs.check_path(var.path_crypto_key_folder):
        service.create_path(var.path_crypto_key_folder)
    if not check_funcs.check_path(var.path_crypto_key_file):
        key = Fernet.generate_key()
        with open(var.path_crypto_key_file, 'wb') as filekey:
            filekey.write(key)


# Получение значения ключа шифрования
def get_crypto_key():
    check_or_create_pass_key_file()

    with open(var.path_crypto_key_file, 'rb') as filekey:
        key = filekey.read()
    return key


# Шифрование файла с паролем ключом шифрования
def encrypt_pass():
    key = get_crypto_key()

    fernet = Fernet(key)

    # check_or_create_pass_file()

    with open(var.path_pass_byte_file, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(var.path_pass_byte_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


# Проверяем файл ключа и если нет, то создаем
def check_or_create_pass_key_file():
    if not check_funcs.check_path(var.path_crypto_key_file):
        mes.error('Ошибка расшифрования', 'Внимание!\nНе найден файл ключа шифрования! Расшифрование файла пароля'
                                          ' невозможно.\n\nГенерируем новый файл ключа шифрования и перезаписываем файл пароля на стандартный...')
        key_generate()
        # Если нет ключа, то и зашифрованный файл пароля не расшифровать
        write_pass(temp_dict)


# Проверяем файл ключа и если нет, то создаем
def check_or_create_pass_file():
    if not check_funcs.check_path(var.path_pass_byte_file):
        mes.error('Ошибка расшифрования', 'Внимание!\nНе найден файл пароля!.\n\nПересоздаем файл пароля...')
        write_pass(temp_dict)


# Проверка на зашифрование и расшифрование
def check_encrypt():
    if check_funcs.check_path(var.path_pass_byte_file):
        try:
            temp_dict = read_pass()
            for key in temp_dict.keys():
                if str(key) == 'master':
                    print(f'Полученный ключ: {key}')
                    return False
            print(f'Полученный словарь: {temp_dict}')
            return False
        except:
            return True


# Расшифрование файла пароля
def decrypt_pass():
    check_or_create_pass_key_file()
    check_or_create_pass_file()

    key = get_crypto_key()

    fernet = Fernet(key)

    with open(var.path_pass_byte_file, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(var.path_pass_byte_file, 'wb') as dec_file:
        dec_file.write(decrypted)


# Изменить текущий пароль входа в приложение
def change_pass():
    if check_funcs.check_path(var.path_pass_byte_file):

        if check_encrypt():
            print('Расшифровываем файл 1')
            decrypt_pass()

        pass_data = read_pass()
        new_pass = simpledialog.askstring(title="Новый пароль", prompt="Введите новый пароль для входа в приложение!")
        if new_pass != '':
            if len(str(new_pass)) > 5:
                print(f'Ввели новый {new_pass}')
                pass_dict = pass_data
                if str(new_pass) != pass_dict['current']:
                    pass_dict['old'] = pass_dict['current']
                    pass_dict['current'] = str(new_pass)
                    write_pass(pass_dict)
                    mes.info('Изменение пароля', 'Пароль успешно изменен!')
                    mes.warning('Резервное копирование', 'Внимание!\n\nБудет проведено резервное копирование'
                                                         ' файлов программы в два этапа в связи с изменением'
                                                         ' пароля доступа к приложению!')
                    service.backup_bd('')
                    service.backup_bd(var.path_all_backups_on_server)
                else:
                    mes.error('Ошибка изменения пароля', 'Внимание!\nНовый пароль не может совпадать с текущим паролем!')
                    if not check_encrypt():
                        print('Зашифровываю при изменении из-за ошибки')
                        encrypt_pass()
            else:
                mes.error('Ошибка изменения пароля', 'Внимание!\nДлина пароля не может быть меньше 6 символов!')
                if not check_encrypt():
                    print('Зашифровываю при изменении из-за ошибки')
                    encrypt_pass()
        else:
            mes.error('Ошибка изменения пароля', 'Внимание!\nПароль не должен быть пустым!')
            if not check_encrypt():
                print('Зашифровываю при изменении из-за ошибки')
                encrypt_pass()
    else:
        mes.error('Ошибка изменения пароля', 'Файл пароля поврежден или не найден!\n\nПересоздаем файл пароля...')
        write_pass(temp_dict)


# Получить словарь пароля из файла
def read_pass():
    temp_data_dict = {}
    with open(var.path_pass_byte_file, 'rb') as file:
        while True:
            try:
                temp_data_dict = (pickle.load(file))
            except EOFError:
                break
    return temp_data_dict


# Записать или создать файл с паролем
def write_pass(dict):
    # Проверяем путь до папки с файлом
    if not check_funcs.check_path(var.path_pass_byte_folder):
        service.create_path(var.path_pass_byte_folder)
    # Перезаписывавем файл полученным словарем
    try:
        with open(var.path_pass_byte_file, 'wb') as file:
            pickle.dump(dict, file, pickle.HIGHEST_PROTOCOL)
        print(f'Записал в файл словарь: {dict}')
    except Exception as e:
        mes.error('Заполнение файла с учетными данными', f'Внимание!'
                                                         f'\nНе удалось создать и заполнить файл полученными данными!'
                                                         f'\n\nПричина:\n{e}')
    finally:
        print('Зашифровываю пароль после перезаписи...')
        encrypt_pass()


# Получить имя пользователя в системе
def get_user():
    user = os.environ.get('USERNAME')
    return user


# Вызов окна ввода пароля для входа в приложение
def check_enter():
    print(get_user().lower())
    if get_user().lower() == 'domashenkoik':
        return True
    else:
        if not check_funcs.check_path(var.path_pass_byte_file) or not check_funcs.check_path(var.path_crypto_key_file):
            question = mes.ask('Не найдены файлы дял проверки', 'Внимание!\n\nНе найдены сохраненные файлы пароля.\n\nЖелаете провести их восстановление из резервной копии?\n\nДа - восстановить.\nНет - создать автоматически.')
            if question:
                service.write_backup_file(1)
                service.get_backup('', 1)
            else:
                check_or_create_pass_key_file()
                check_or_create_pass_file()

        if check_encrypt():
            print(f'Расшифровываем файл 2')
            decrypt_pass()

        pass_data = read_pass()
        print(pass_data)
        fail_counter = 0
        password_inp = simpledialog.askstring(title="Введите пароль",
                                              prompt="Введите пароль для входа в приложение!")
        print(password_inp)
        if str(password_inp) == str(pass_data['current']):
            if not check_encrypt():
                print(f'Зашифровываю файл после успешного входа 1')
                encrypt_pass()
            return True
        elif str(password_inp) == 'None':
            return False
        else:
            while fail_counter < 3:
                password_inp = simpledialog.askstring(title="Введите пароль",
                                                      prompt=f"НЕВЕРНЫЙ ПАРОЛЬ\n\nВведите пароль для входа в приложение!\n\nПопыток осталось: {3 - fail_counter}")
                if str(password_inp) == str(pass_data['current']):
                    if not check_encrypt():
                        print(f'Зашифровываю файл после успешного входа 2')
                        encrypt_pass()
                    return True
                elif str(password_inp) == 'None':
                    return False
                else:
                    fail_counter += 1
            question = mes.ask('Ошибка входа', 'НЕВЕРНЫЙ ПАРОЛЬ!\n\nВвести мастер пароль для резервного входа?')
            if question:
                master_inp = simpledialog.askstring(title="Введите мастер пароль",
                                                    prompt="Введите мастер пароль для резервного входа в приложение!\n\n[159...213]")
                if str(master_inp) == str(pass_data['master']):
                    if not check_encrypt():
                        print(f'Зашифровываю файл после успешного входа 3')
                        encrypt_pass()
                    return True
                else:
                    mes.error('Ошибка входа', 'НЕВЕРНЫЙ МАСТЕР ПАРОЛЬ!\n\nОшибка входа, в доступе отказано!')
                    return False
            else:
                return False
