from tkinter.messagebox import QUESTION
from typing import final
from requests import delete
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,  distinct
import random
import json

from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
import os

# from utils.db_api.NLP_model import *
engine = db.create_engine(f'sqlite:///utils/db_api/DB.sqlite')
connection = engine.connect()
metadata = db.MetaData()

# Таблица Макса
Friends = db.Table('Friends', metadata,
                   autoload=True, autoload_with=engine)
#
Order = db.Table('Order', metadata,
                 autoload=True, autoload_with=engine)



class FuncM():
    # Пример записи данных id и username в таблицу макса
    def POST(id1, username1):
        a = db.select([Friends.columns.id])
        list_id = []
        for i in connection.execute(a).fetchall():
            list_id.append(i[0])
        if str(id1) in list_id:
            pass
        else:
            query = db.insert(Friends).values(id=id1, Username=username1,
                                              Friends_id='',  id_reminder='')
            ResultProxy = connection.execute(query)

# Пример чтения данных username по id из таблицы макса
    def GET(id):
        a = db.select([Friends.columns.Username]).where(
            Friends.columns.id == id)
        list_username = []
        for row in connection.execute(a).fetchall():
            list_username.append(row[0])
        return list_username

    def GET_ID():
        a = db.select([Friends.columns.id])
        list_id = []
        for row in connection.execute(a).fetchall():
            list_id.append(row[0])
        return list_id

# Пример обновления данных в таблице макса
    def UPDATE(id, username):
        query = db.update(Friends).values(
            Username=username)
        query = query.where(Friends.columns.id == id)
        ResultProxy = connection.execute(query)
# Добваление дня напоминания


# Добавление друзей


    def Friends(id1, username):
        list_id = []
        list_fr = []
        # айди потенциального друга
        a = db.select([Friends.columns.id]).where(
            Friends.columns.Username == username)
        # список друзей
        b = db.select([Friends.columns.Friends_id]).where(
            Friends.columns.id == id1)
        for row in connection.execute(a).fetchall():
            list_id.append(row[0])
        for row in connection.execute(b).fetchall():
            list_fr.append(row[0])
        if (list_fr[0] == ''):
            query = db.update(Friends).values(
                Friends_id=list_id[0]
            )
        else:
            query = db.update(Friends).values(
                Friends_id=list_fr[0]+','+list_id[0]
            )

        query = query.where(Friends.columns.id == id1)
        ResultProxy = connection.execute(query)


# Удаление друзей


    def delete_friends(id1, username):
        list_id = []
        a = db.select([Friends.columns.id]).where(
            Friends.columns.Username == username)
        for row in connection.execute(a).fetchall():
            list_id.append(row[0])
        list_id_fr = []
        b = db.select([Friends.columns.Friends_id]).where(
            Friends.columns.id == id1)
        for row in connection.execute(b).fetchall():
            list_id_fr = row[0].split(',')
        list_id_fr.remove(list_id[0])
        str_id_fr = ','.join(list_id_fr)
        query = db.update(Friends).values(
            Friends_id=str_id_fr
        )
        query = query.where(Friends.columns.id == id1)
        ResultProxy = connection.execute(query)


# Запрос друзей


    def get_friends(id1):
        list_id = []
        a = db.select([Friends.columns.Friends_id]).where(
            Friends.columns.id == id1)
        for row in connection.execute(a).fetchall():
            list_id = row[0].split(',')
        return list_id

    def get_friends_smart(id1):
        a = db.select([Friends.columns.Friends_id]).where(
            Friends.columns.id == id1)
        frnds = connection.execute(a).fetchall()[0][0].split(',')
        b = db.select(Order.columns.id)
        frnds_ =[]
        for i in connection.execute(b).fetchall():
            frnds_.append(i[0])

        return list(set(frnds) - set(frnds_))

# Запрос имени по id

    def get_username_by_id(username):
        str_id = ''
        a = db.select([Friends.columns.id]).where(
            Friends.columns.Username == username)
        for row in connection.execute(a).fetchall():
            str_id = row[0]
        return str_id

    def get_username_by_id1(id1):
        str_id = ''
        a = db.select([Friends.columns.Username]).where(
            Friends.columns.id == id1)
        for row in connection.execute(a).fetchall():
            str_id = row[0]
        return str_id


class My_Order():
    # Добавление/изменение ресторана
    def POST_REST(id1, link1):
        list_id = FuncM.get_friends_smart(id1)
        print(list_id)
        if id1 in list_id:
            query = db.update(Order).where(Order.columns.id == id1).values(
                id=id1, link=link1, preminary_link='', final_link='', default=link1)
            ResultProxy = connection.execute(query)
        else:
            query_id1 = query = db.insert(Order).values(
                    id=id1, link=link1, preminary_link='', final_link='', default=link1)
            ResultProxy = connection.execute(query_id1)
            for id in list_id:
                query = db.insert(Order).values(
                    id=id, link=link1, preminary_link='', final_link='', default=link1)
                ResultProxy = connection.execute(query)
    #Шаг вперед
    def POST_PATH(id1,link1):
        a = db.select([Order.columns.link]).where(Order.columns.id == id1)
        link = connection.execute(a).fetchall()[0]
        query = db.update(Order).where(Order.columns.id == id1).values(
                id=id1, link=link[0]+'|'+link1)
        ResultProxy = connection.execute(query)
    #ШАг назад
    def DEL_PATH(id1):
        a = db.select([Order.columns.link]).where(Order.columns.id == id1)
        link = connection.execute(a).fetchall()[0][0]
        link =  '|'.join(link.split('|')[:-1])
        query = db.update(Order).where(Order.columns.id == id1).values(
                link=link)
        ResultProxy = connection.execute(query)
    #zУдалить всё из пути до ресторана
    def DEL_PATH_REST(id1):
        a = db.select([Order.columns.default]).where(Order.columns.id == id1)
        link = connection.execute(a).fetchall()[0][0]
        query = db.update(Order).where(Order.columns.id == id1).values(
                link=link)
        ResultProxy = connection.execute(query)

    #Добавление заказа в корзину
    def POST_PRELIMINARY(id1):
        a = db.select([Order.columns.link]).where(Order.columns.id == id1)
        b = db.select([Order.columns.preminary_link]).where(Order.columns.id == id1)
        link = connection.execute(a).fetchall()[0]
        print(link)
        pr_link = connection.execute(b).fetchall()[0]
        print(pr_link)
        if pr_link[0]=='':
            query=db.update(Order).where(Order.columns.id == id1).values(
                    preminary_link=link[0])
            ResultProxy = connection.execute(query)
        elif link[0] != pr_link[0]:
            query = db.update(Order).where(Order.columns.id == id1).values(
                id=id1, preminary_link=pr_link[0]+','+link[0])
            ResultProxy = connection.execute(query)
        else:
            query = db.update(Order).where(Order.columns.id == id1).values(
                id=id1, link=link[0], preminary_link=link[0], final_link='')
            ResultProxy = connection.execute(query)

    #Получить список продуктов из корзины
    def GET_PR(id1):
        b = db.select([Order.columns.preminary_link]).where(Order.columns.id == id1)
        pr_link = connection.execute(b).fetchall()[0]
        pr_link = pr_link[0].split(',')
        products_list=[]
        for i in pr_link:
            products_list.append(i.split('|')[-1])
        return products_list
    #Удалить один продукт из корзины
    def DEL_PRODUCT(id1, product):
        b = db.select([Order.columns.preminary_link]).where(Order.columns.id == id1)
        pr_link = connection.execute(b).fetchall()[0]
        pr_link = pr_link[0].split(',')
        for index,path in enumerate(pr_link):
            if product in path:
                pr_link.pop(index)
                break
        query = db.update(Order).where(Order.columns.id == id1).values(
                preminary_link=','.join(pr_link))
        ResultProxy = connection.execute(query)

    #Добавление в финальный заказ
    def POST_FINAL(id1):
        a = db.select([Order.columns.preminary_link]).where(Order.columns.id == id1)
        link = connection.execute(a).fetchall()[0]
        print(link)
        query = db.update(Order).where(Order.columns.id == id1).values(
                id=id1, final_link=link[0])
        ResultProxy = connection.execute(query)


    # Удаление последнего заказа из корзины
    def DEL_PR(id1):
        a = db.select([Order.columns.preminary_link]).where(Order.columns.id == id1)
        link = connection.execute(a).fetchall()[0][0]
        link = link.split(',')[:-1]
        query = db.update(Order).where(Order.columns.id == id1).values(
                preliminary_link=link[0])
        ResultProxy = connection.execute(query)

    #Удаление финального заказа
    def DEL_FINAL(id1):
        query = db.update(Order).where(Order.columns.id == id1).values(
                final_link='')
        ResultProxy = connection.execute(query)



    def main(id1):
        with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
            fcc_data = json.load(fcc_file)
            a = db.select([Order.columns.link]).where(Order.columns.id == id1)
            link = connection.execute(a).fetchall()[0]
            path = link[0].split('|')
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

    def getListProducts(id1):
        with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
            fcc_data = json.load(fcc_file)
            a = db.select([Order.columns.link]).where(Order.columns.id == id1)
            link = connection.execute(a).fetchall()[0]
            path = link[0].split('|')
            products = list(fcc_data[path[0]]['cats'][path[1]].keys())
            return products

    def delString(id1):
        query = db.update(Order).where(Order.columns.id == id1).values(
                id='', link='', preminary_link='', final_link='', default='')
        ResultProxy = connection.execute(query)

    def getLinkRest(rest):
        with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
            fcc_data = json.load(fcc_file)
            return fcc_data[rest]['link']

    def getPrice(id1):
        with open('utils/json/delivery.json', 'r', encoding='UTF-8') as fcc_file:
            fcc_data = json.load(fcc_file)
            a = db.select([Order.columns.preminary_link]).where(Order.columns.id == id1)
            link = connection.execute(a).fetchall()[0][0]
            link = link.split(',')
            price=0
            for i in link:
                path = i.split('|')
                price+=int(fcc_data[path[0]]['cats'][path[1]][path[2]]['price'][0:-2])
            return price

class ZAKAZ():

    def get_products_info(driver,name, menu_list,rest, cat):
        item = menu_list.find_elements(By.CLASS_NAME,"menu-product__info-item")
        items = list(map(lambda x: x.text, item))   
        descriptions = menu_list.find_elements(By.CLASS_NAME,"menu-product__description")
        srs_list = get_img(menu_list, driver, rest, cat)
        desc=[]
        try:
            for index,i in enumerate(item):
                ActionChains(driver).move_to_element(i).perform()
                print(descriptions[index].get_attribute('textContent'))
                desc.append(descriptions[index].get_attribute('textContent'))
                btn=  menues_list[index].find_elements(By.CLASS_NAME,"menu-product__btn")
                btn.click()
        except:
            desc.append('')
        print(desc)
        prices = menu_list.find_elements(By.CLASS_NAME,"menu-product__price")
        prices = list(map(lambda x: x.text, prices))
        index = 0
        for key,i in name.items():
            name[key] = {'item': items[index],
                        'price': prices[index],
                        'description': desc[index+1],
                        'rep_img': srs_list[index]
                        }
            index+=1

    def get_products(driver,element,rest,list_info):
        menues_list = driver.find_elements(By.CLASS_NAME,"vendor-menu__section")
        index = 0
        for key,i in element.items():
            titles = menues_list[index].find_elements(By.CLASS_NAME,"menu-product__title")
            element[key] = dict.fromkeys(list(map(lambda x: x.text,titles)))
            time.sleep(5)
            if titles == list_info[:-1]:
                ZAKAZ.get_products_info(driver, element[key], menues_list[index],rest, key)
                index+=1

    def get_categories(rests,driver,list_info):
        for key,i in rests.items():
            if key == list_info[1]:
                print(rests)
                print(key)
                print(rests[key]['link'])
                driver.get(rests[key]['link'])
                time.sleep(3)
                    # try:
                    # if len(list(driver.find_element(By.CLASS_NAME,"popup__overlay"))) == 0:
                # btn = driver.find_element(By.CLASS_NAME,"popup__close-button")
                # btn.click()
                cats_elem = driver.find_elements(By.CLASS_NAME,"vendor-categories__item")
                cats = dict.fromkeys(list(map(lambda x: x.text, cats_elem)))
                ZAKAZ.get_products(driver, cats, key,list_info)
                rests[key]['cats'] = cats
            else:
                continue

    def get_restaurant(address, URL, driver, list_info):
        driver.get("https://www.delivery-club.ru/moscow")
        time.sleep(3)
        elem = driver.find_element(By.CLASS_NAME,"address-input__location")
        elem.click()
        input_el = driver.find_element(By.CLASS_NAME, 'address-suggest__search-input').send_keys(address)
        time.sleep(3)
        ActionChains(driver)\
                .key_down(Keys.ENTER)\
                .key_up(Keys.ENTER)\
                .perform()
        time.sleep(3)
        urls = driver.find_elements(By.CLASS_NAME,"vendor-item__link")
        names = driver.find_elements(By.CLASS_NAME,"vendor-item__title-text")
        times = driver.find_elements(By.CLASS_NAME,"vendor-item__delivery-time")
        prices = driver.find_elements(By.CLASS_NAME,"vendor-item__info-item")
        restaurants =dict.fromkeys(list(map(lambda x: x.text, names)))
        index=0
        for key,i in restaurants.items():
            if key== list_info[0]:
                restaurants[key]={'link':urls[index].get_attribute("href"),
                                'time':times[index].text,
                                'minprice':prices[index].text,
                                }
                index+=1
        return restaurants

    def main(value):
        address='Московская область, Дубна, садовое товарищество Заря, 2-й сектор, 33 \n'
        URL_TEMPLATE = "https://www.delivery-club.ru/moscow?addressSuggestOpened=1"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        list_info = value.split('|')
        rests = ZAKAZ.get_restaurant(address, URL_TEMPLATE, driver,list_info)
        ZAKAZ.get_categories(rests,driver,list_info)
        print(rests)

# print(My_Order.getPrice('1234'))
# FuncM.get_friends_smart('962483958')
# ZAKAZ.main('Burger King|Популярные|Воппер')
# def get_img(menu_list, driver, rest, cat):
#         images = menu_list.find_elements(By.CLASS_NAME,"menu-product__img")
#         time.sleep(3)
#         imgs=[]
#         for i in images:
#             imgs.append(i.get_attribute("data-src"))
#         names = download_img(imgs, rest, cat)
#         time.sleep(3)
#         return names
    
# def download_img(imgs, rest, cat ):
#         # rep = "D:/Пользователь/User/GitHub/zona/"+cat+'/'+rest+'/'
#     images_path = 'images'
#     if not os.path.exists(images_path):
#         os.mkdir(images_path)

#     names = []
#     for src in imgs:
#         try:
#             index = random.randint(0, 2000)
#             name = images_path + f"/{index}.jpg"
#             print(src)
#                 # name = f'{index}.jpg'
#             p = requests.get(src)
#             out = open(name, "wb")
#             out.write(p.content)
#             out.close()
#                 # urllib.request.urlretrieve(src, rep+name)
#             names.append(name)
#         except:
#             name=''
#             names.append(name)

#     return names
        
# def get_products(driver,element,rest):
#     menues_list = driver.find_elements(By.CLASS_NAME,"vendor-menu__section")
#     index = 0
#     for key,i in element.items():
#         titles = menues_list[index].find_elements(By.CLASS_NAME,"menu-product__title")
#         element[key] = dict.fromkeys(list(map(lambda x: x.text,titles)))
#         get_products_info(driver, element[key], menues_list[index],rest, key)
#         index+=1

# def get_products_info(driver,name, menu_list,rest, cat):
#     item = menu_list.find_elements(By.CLASS_NAME,"menu-product__info-item")
#     items = list(map(lambda x: x.text, item))   
#     descriptions = menu_list.find_elements(By.CLASS_NAME,"menu-product__description")
#     srs_list = get_img(menu_list, driver, rest, cat)
#     desc=[]
#     try:
#         for index,i in enumerate(item):
#             ActionChains(driver).move_to_element(i).perform()
#             print(descriptions[index].get_attribute('textContent'))
#             desc.append(descriptions[index].get_attribute('textContent'))
#     except:
#         desc.append('')
#     print(desc)
#     prices = menu_list.find_elements(By.CLASS_NAME,"menu-product__price")
#     prices = list(map(lambda x: x.text, prices))
#     index = 0
#     for key,i in name.items():
#         name[key] = {'item': items[index],
#                     'price': prices[index],
#                     'description': desc[index+1],
#                     'rep_img': srs_list[index]
#                     }
#         index+=1


# def get_categories(rests,driver):
#     for key,i in rests.items():
#         driver.get(rests[key]['link'])
#         time.sleep(3)
#         try:
#             # if len(list(driver.find_element(By.CLASS_NAME,"popup__overlay"))) == 0:
#             #     btn = driver.find_element(By.CLASS_NAME,"icon__svg")
#             #     btn.click()
#             btn = driver.find_element(By.CLASS_NAME,"popup__close-button")
#             btn.click()
#         except:
#             cats_elem = driver.find_elements(By.CLASS_NAME,"vendor-categories__item")
#             cats = dict.fromkeys(list(map(lambda x: x.text, cats_elem)))
#             get_products(driver, cats, key)
#             rests[key]['cats'] = cats
            


    # def get_product(id1):
    #     a = db.select([Order.columns.id])
    #     list_id = []
    #     for i in connection.execute(a).fetchall():
    #         list_id.append(i[0])
    #     if str(id1) in list_id:
    #         b = db.select([Order.columns.link]).where(Order.columns.id == id1)
    #     c = db.select([Delivery.columns.info])
    #     prdct = c[str(b)]
    #     ResultProxy = connection.execute(query)

    # def get_aim(id1):
    #     str_id = ''
    #     a = db.select([Friends.columns.Aim]).where(
    #         Friends.columns.id == id1)
    #     for row in connection.execute(a).fetchall():
    #         str_id = row[0]
    #     return str_id

    # def get_feedback(id1):
    #     a = db.select(Friends.columns.feedback).where(Friends.columns.id == id1)
    #     list_feedback = []
    #     for row in connection.execute(a).fetchall():
    #         list_feedback = row[0].split('&')
    #     return list_feedback
