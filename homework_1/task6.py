# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
# программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

import chardet

if __name__ == "__main__":
    with open("test_file.txt", "rb") as file:
        data = file.read()
        encoding = chardet.detect(data)["encoding"]
        print(f'кодировка файла: {encoding}')
        print('*'*50)
    with open("test_file.txt", "r", encoding="UTF-8") as file:
        for line in file:
            print(line)


