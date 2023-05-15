# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
# байтовом типе.

if __name__ == "__main__":
    word_list = [
        'attribute',
        'класс',
        'функция',
        'type'
    ]
    error_words = [];

    for word in word_list:
        try:
            print(f'Слово "{word}" в байтовом типе -  {bytes(word, "ascii")}')
        except UnicodeEncodeError:
            error_words.append(word)

    if  error_words:
        print(f'слова "{", ".join(error_words)}" невозможно записать в байтовом типе');