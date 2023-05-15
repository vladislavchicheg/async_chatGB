# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
# строкового представления в байтовое и выполнить обратное преобразование (используя
# методы encode и decode).

if __name__ == "__main__":
    word_list = [
        "разработка",
        "администрирование",
        "protocol",
        "standard"
    ]

    for word in word_list:
        encode_word = word.encode(encoding="UTF-8")
        reverse_decode_word = encode_word.decode(encoding="UTF-8")
        print(f'слово: "{word}"; байтовое представление: {encode_word}; обратно преобразованное: {reverse_decode_word}')
