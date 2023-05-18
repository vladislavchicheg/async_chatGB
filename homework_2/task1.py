# Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
# определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
# «отчетный» файл в формате CSV. Для этого:
# a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
# данными, их открытие и считывание данных. В этой функции из считанных данных
# необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
# каждого параметра поместить в соответствующий список. Должно получиться четыре
# списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
# функции создать главный список для хранения данных отчета — например, main_data
# — и поместить в него названия столбцов отчета в виде списка: «Изготовитель
# системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
# столбцов также оформить в виде списка и поместить в файл main_data (также для
# каждого файла);
# b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
# функции реализовать получение данных через вызов функции get_data(), а также
# сохранение подготовленных данных в соответствующий CSV-файл;
# c. Проверить работу программы через вызов функции write_to_csv().
import csv
import re

from chardet import detect

files_array = ["info_1.txt", "info_2.txt", "info_3.txt"]
columns = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]


def decode_file(file_name):
    with open(file_name, "rb") as file:
        data = file.read()
        decode_data = data.decode(encoding=detect(data)['encoding'])
    return decode_data


def get_regular_ex(characteristic: str):
    return f"({characteristic}:)\\s+(.+)"


def get_data(files_array, columns):
    main_data = {}
    for column in columns:
        main_data[column] = []

    for file_name in files_array:
        file_data = decode_file(file_name)
        for column in columns:
            match = re.search(get_regular_ex(column), file_data)
            main_data[column].append(match[2].strip())
    return main_data


def write_to_csv(csv_file, files_array, columns):
    data = get_data(files_array, columns)
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = list(data.keys())
        writer.writerow(headers)
        for idx in range(len(data[headers[0]])):
            item = []
            for head in headers:
                item.append(data[head][idx])
            writer.writerow(item)


if __name__ == "__main__":
    write_to_csv('task1.csv', files_array, columns)
