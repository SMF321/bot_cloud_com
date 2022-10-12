import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains


options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://eda.yandex.ru/Dubna')
time.sleep(5)

element = driver.find_element(By.XPATH, "//*[@id='root']/div/header/div/div[1]/div/div[2]/div/button")
element.click()
time.sleep(5)

element = driver.find_element(By.CLASS_NAME, "UIPopupList_option")
element.click()
time.sleep(3)
# element = driver.find_elements(By.CLASS_NAME, "input[class='UiKitUiKitIcon_m UiKitUiKitIcon_root AppAddressInput_closeIcon']").click()
time.sleep(3)
element = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div/div/div/div[1]/div[2]/div/div/div[1]/input")[0].click()
time.sleep(3)

for i in range(30):
    ActionChains(driver)\
            .key_down(Keys.BACKSPACE)\
            .key_up(Keys.BACKSPACE)\
            .perform()

element = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div/div/div/div[1]/div[2]/div/div/div[1]/input")[0].send_keys('2-й сектор, 21')
time.sleep(3)
element = driver.find_elements(By.XPATH, "//*[@id='react-autowhatever-1--item-0']/span")[0]
element.click()
time.sleep(3)
element = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div/div[1]/div[2]/button")
# print(element)
element.click()
time.sleep(3)
driver.execute_script("window.scrollTo(0, 400)") 
time.sleep(3)
urls = driver.find_elements(By.XPATH,"//*[@id='root']/div/div/div[1]/div/div/div/div[5]/div/div/div/div[2]/ul/li")
test = {}
test['name_restorant'] = {}
for elem in range(len(urls)):
    # driver.execute_script("window.scrollTo(0, 50)") 
    name = driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/div/div[5]/div/div/div/div[2]/ul/li[{elem + 1}]/div/a/div/div[2]/h3")
    print(name.text)
    # test['name_restorant'] = name.text
    time_dost = driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/div/div[5]/div/div/div/div[2]/ul/li[{elem + 1}]/div/a/div/div[1]/div/div[2]")
    if time_dost.text == '':
        time_dost = driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/div/div[5]/div/div/div/div[2]/ul/li[{elem + 1}]/div/a/div/div[1]/div[2]/div[1]")
        print(time_dost.text)
        # test[name.text]['time'] = time_dost.text
    else:
        print(time_dost.text)
        # test[name.text]['time'] = time_dost.text
    element = driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/div/div[5]/div/div/div/div[2]/ul/li[{elem + 1}]/div/a")
    print(element.get_attribute("href"))
    # test[name.text]['link'] = element.get_attribute("href")
    
    test['name_restorant'][name.text] = dict( {'link':element.get_attribute("href"),'time':time_dost.text})

print(test)

for i in range(len(list(test['name_restorant'].values()))):
    driver.get(list(test['name_restorant'].values())[i]['link'])
    time.sleep(3)

    try:
        if driver.find_element(By.CLASS_NAME,"ModalSurge_button"):
            cli = driver.find_element(By.CLASS_NAME,"ModalSurge_button")
            cli.click()
    except:
        pass
    skroll = 200
    driver.execute_script(f"window.scrollTo(0, {skroll})")
    categoris = driver.find_elements(By.CLASS_NAME,"RestaurantMenu_category")
    for i in range(len(categoris)):
        cat = driver.find_elements(By.CLASS_NAME, f"RestaurantMenu_catName")
        print(cat[i].text)
        eda = driver.find_elements(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/section/div[2]/div[{i+1}]/div/div/div")
        
        # //*[@id="root"]/div/div/div[1]/div/div/section/div[2]/div[1]/div/div
        # //*[@id="root"]/div/div/div[1]/div/div/section/div[2]/div[1]/div/div/div[1]
        # //*[@id="root"]/div/div/div[1]/div/div/section/div[2]/div[2]/div/div/div[1]
        # //*[@id="root"]/div/div/div[1]/div/div/section/div[2]/div[1]/div/div/div[1]/div/div[2]/div[2]
        # //*[@id="root"]/div/div/div[1]/div/div/section/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]
        # //*[@id="root"]/div/div/div[1]/div/div/section/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]
        
        for x in range(len(eda)):
            skroll += 130
            driver.execute_script(f"window.scrollTo(0, {skroll})")
            name_eda = driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/section/div[2]/div[{i+1}]/div/div/div[{x+1}]/div/div[2]/div[2]")
            print(name_eda.text)
            ActionChains(driver).move_to_element(name_eda).perform()

    


# element = driver.find_element(By.XPATH, "//*[@id='category_6328befb61f48636df9ec7b0']")
# # print(element)
# element.click()
# time.sleep(3)

# # ActionChains(driver)\
# #         .key_down(Keys.ENTER)\
# #         .key_up(Keys.ENTER)\
# #         .perform()
# # time.sleep(3)



# urls = driver.find_elements(By.CLASS_NAME,"menu-categories__item")

# for elem in urls:
#     print(elem.get_attribute("id"))

# clickable = driver.find_element(By.CLASS_NAME, "menu-categories__label")
# ActionChains(driver)\
#     .click_and_hold(clickable)\
#     .perform()
# time.sleep(3)


