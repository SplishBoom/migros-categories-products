from Utilities import Web, By
from pprint import pprint
import time

"""name = "Bebek"
link = "https://www.migros.com.tr/bebek-c-9"

client = Web(isHidden=False)
client.openWebPage(link)
dummy = client.createElement("/html/body/sm-root/div/fe-product-cookie-indicator/div/div/button[1]")
client.clickOnElement(dummy)


dd = {name : {}}
sub_categories = client.createElement("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[1]/sm-product-filters-desktop/div/div[2]/div[2]").find_elements(By.TAG_NAME, "div")
for current_sub_category in sub_categories :
    sub_catagory_name = current_sub_category.text[0:current_sub_category.text.find("(")].strip()
    sub_catagory_link = current_sub_category.find_element(By.TAG_NAME, "a").get_attribute("href")
    sub_category_product_count = current_sub_category.text[current_sub_category.text.find("(")+1:current_sub_category.text.find(")")]
    dd[name][sub_catagory_name] = {}"""

ALL = {"Bebek" : {}}

temp = []
def fnc(name, client) :

    temp.append(name)

    category_list = client.createElement("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[1]/sm-product-filters-desktop/div/div[2]/div[2]").find_elements(By.TAG_NAME, "div")
    if len(category_list) == 1:

        last_element_name = category_list[0].text[0:category_list[0].text.find("(")].strip()
        owner_name = name
        if last_element_name == owner_name :
            print("/".join(temp))
        else :
            print("/".join(temp) + "/" + last_element_name)

        return

    counter = 0

    while counter < len(category_list) : 

        current_sub_category = client.createElement("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[1]/sm-product-filters-desktop/div/div[2]/div[2]").find_elements(By.TAG_NAME, "div")[counter]

        sub_catagory_name = current_sub_category.text[0:current_sub_category.text.find("(")].strip()
        sub_catagory_link = current_sub_category.find_element(By.TAG_NAME, "a").get_attribute("href")
        sub_category_product_count = current_sub_category.text[current_sub_category.text.find("(")+1:current_sub_category.text.find(")")]
        
        client.openWebPage(sub_catagory_link)

        fnc(sub_catagory_name, client)

        counter = counter + 1

        client.browser.back()
        temp.pop()
    


name = "Bebek"
link = "https://www.migros.com.tr/bebek-c-9"
client = Web(isHidden=False)
client.openWebPage(link)
dummy = client.createElement("/html/body/sm-root/div/fe-product-cookie-indicator/div/div/button[1]")
client.clickOnElement(dummy)

fnc(name, client)