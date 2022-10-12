import json


put = 'Burger King'

#Добаление в путь
def update_pss(value):
    global put
    put=put+'|'+value

def delete():
    global put
    put_list=put.split('|')
    put= '|'.join(put_list[:-1])
    print(put)
#Рестораны
def get_rests():
    with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        rests=list(fcc_data.keys())
        return rests
#Категории
def get_cats(rest):
    with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        cats= list(fcc_data[rest]['cats'].keys())
        return cats
#Товары из категорий
def get_products():
    global put
    with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        path = put.split('|')
        products = list(fcc_data[path[0]]['cats'][path[1]].keys())
        return products

def main():
    global put
    with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        path = put.split('|')
        if len(path) == 1:
            cats= list(fcc_data[path[0]]['cats'].keys())
            return cats
        elif len(path) == 2:
            products = list(fcc_data[path[0]]['cats'][path[1]].keys())
            return products
        elif len(path) == 3:
            description = []
            for i in list(fcc_data[path[0]]['cats'][path[1]][path[2]].values()):
                description.append(i)
            return description


def delete_all():
    global put
    put_list=put.split('|')
    put= 'Burger King'
    print(put)







    




#Описание продукта
#Цена продукта
#Каллории продукта