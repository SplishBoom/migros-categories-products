from Utilities import Web, By
from pprint import pprint

from Constants import *

def retrieve_main_categories() :

    client = Web(isHidden=True)

    main_url = "https://www.migros.com.tr/"

    client.openWebPage(main_url)

    dummy = client.createElement("//*[@id=\"header-money-discounts\"]")
    client.clickOnElement(dummy)

    dummy = client.createElement("/html/body/sm-root/div/fe-product-cookie-indicator/div/div/button[1]")
    client.clickOnElement(dummy)

    catagories_element = client.createElement("//*[@id=\"header-wrapper\"]/div[3]/div/div")
    client.clickOnElement(catagories_element)

    all_category_elements = client.createElement("//*[@id=\"header-wrapper\"]/div[3]/div[1]/div[2]/div[1]").find_elements(By.TAG_NAME, "a")

    category_link_map = {}
    exceptions = ("Tüm İndirimli Ürünler", "Sadece Migros'ta")
    for current_catogory_element in all_category_elements :
        category_name = current_catogory_element.text
        category_link = current_catogory_element.get_attribute("href")

        if category_name not in exceptions :
            category_link_map[category_name] = category_link

    client.terminate()

    return category_link_map

pprint(retrieve_main_categories())