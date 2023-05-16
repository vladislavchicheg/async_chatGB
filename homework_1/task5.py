# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
# байтовового в строковый тип на кириллице.
import subprocess

import chardet as chardet
if __name__ == "__main__":
    sites = ['yandex.ru', 'youtube.com']


    def show_site_ping_result(domain, count):
        site_ping = subprocess.Popen(("ping", domain), stdout=subprocess.PIPE)
        i = 0
        for line in site_ping.stdout:
            if i > count:
                break
            result = chardet.detect(line)
            print(result)
            line = line.decode(result['encoding']).encode('utf-8')
            print(line.decode('utf-8'))
            i += 1
        print("*" * 50)


    for site in sites:
        show_site_ping_result(site, 3)
