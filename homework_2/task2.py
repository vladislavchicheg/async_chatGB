# Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
# информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
# этого:
# a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
# (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
# должна предусматривать запись данных в виде словаря в файл orders.json. При
# записи данных указать величину отступа в 4 пробельных символа;
# b. Проверить работу программы через вызов функции write_order_to_json() с передачей
# в нее значений каждого параметра.
import json


def get_all_orders(filename="orders.json"):
    with open(filename) as file:
        return json.load(file)


def write_order_to_json(item, quantity, price, buyer, date, filename="orders.json"):
    orders = get_all_orders(filename)
    order = {"item": item,
             "quantity": quantity,
             "price": price,
             "buyer": buyer,
             "date": date}
    orders["orders"].append(order)
    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)


if __name__ == "__main__":
    order_1 = ["Playstation 5", 1, 50000, "Vasya", "19/05/2023"]
    order_2 = ["Xbox X", 6, 60000, "Petya", "19/05/2023"]
    write_order_to_json(*order_1)
    write_order_to_json(*order_2)

    orders = get_all_orders()
    print(orders)
