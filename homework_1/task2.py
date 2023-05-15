# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.

if __name__ == "__main__":
    word_list = [b"class", b"function", b"method"]
    for word in word_list:
        print(type(word), word, len(word))
