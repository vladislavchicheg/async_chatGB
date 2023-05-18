# Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
# сохранение данных в файле YAML-формата. Для этого:
# a. Подготовить данные для записи в виде словаря, в котором первому ключу
# соответствует список, второму — целое число, третьему — вложенный словарь, где
# значение каждого ключа — это целое число с юникод-символом, отсутствующим в
# кодировке ASCII (например, €);
# b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
# При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
# также установить возможность работы с юникодом: allow_unicode = True;
# c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
# с исходными.

import yaml


def dump_data(data, file_name):
    with open(file_name, "w") as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def load_data(file_name):
    with open(file_name) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


if __name__ == "__main__":
    file_name = 'task3.yaml'
    incoming_data = {'items': ['computer', 'printer', 'keyboard', 'mouse'],
                     'items_count': 4,
                     'prices': {'computer': '1000\u20ac',
                                'printer': '300\u20ac',
                                'keyboard': '50\u20ac',
                                'mouse': '7\u20ac'}
                     }

    dump_data(incoming_data, file_name)
    output_data = load_data(file_name)
    print(output_data)
    if output_data == incoming_data:
        print('Данные идеентичны')
    else:
        print('Данные различются')
