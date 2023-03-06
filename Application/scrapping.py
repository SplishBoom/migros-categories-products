from Utilities import Web, By, progressBar
import json
from Constants import OUTPUT_JSON_FILE_PATH, OUTPUT_EXCEL_FILE_PATH, OUTPUT_CSV_FILE_PATH, connect_pathes
import colorama
import pandas as pd
import time
import multiprocessing
from pprint import pprint
import os
from datetime import datetime
import platform

import concurrent.futures


class Scrapper :

    def __init__(self) -> None:
        
        self.category_mapping = {}

        self._retrieve_category_list()

        start = datetime.now()

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.category_mapping)) as executor:
            for name, link in self.category_mapping.items():
                executor.map(self._retrieve_sub_category_list, [name], [link])
        
        src_fldr_path = connect_pathes("Temporary")

        checked_folders = []
        for folder in os.listdir(src_fldr_path):
            checked_folders.append(folder)

        for name, link in self.category_mapping.items():
            if name not in checked_folders:
                print("Category " + name + " was not finalized in pool, starting again !")
                self._retrieve_sub_category_list(name, link)

        product_list_dataframe = pd.DataFrame(columns=["name", "type", "link", "cat_1", "cat_2", "cat_3", "cat_4", "cat_5", "cat_6", "cat_7", "cat_8", "cat_9", "cat_10"])

        for folder in os.listdir(src_fldr_path):
            for file in os.listdir(connect_pathes(src_fldr_path, folder)):
                if file.endswith(".xlsx"):
                    # use concat method to add new dataframe to existing dataframe
                    product_list_dataframe = pd.concat([product_list_dataframe, pd.read_excel(connect_pathes(src_fldr_path, folder, file))], ignore_index=True)

        product_list_dataframe.to_excel(OUTPUT_EXCEL_FILE_PATH, index=False)

        catalog_navigation = {}

        for folder in os.listdir(src_fldr_path):
            for file in os.listdir(connect_pathes(src_fldr_path, folder)):
                if file.endswith(".json"):
                    with open(connect_pathes(src_fldr_path, folder, file), "r", encoding="utf-8") as f:
                        catalog_navigation.update(json.load(f))

        with open(OUTPUT_JSON_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog_navigation, f, indent=4, ensure_ascii=False)

        end = datetime.now()
        print("Total time: " + str(end - start))
            
    def _retrieve_category_list(self) :

        client = Web()

        web_page_link = "https://www.migros.com.tr/"

        client.open_web_page(web_page_link)

        pop_up_deleter = client.create_element("//*[@id=\"header-money-discounts\"]")
        client.click_on_element(pop_up_deleter)

        pop_up_deleter = client.create_element("/html/body/sm-root/div/fe-product-cookie-indicator/div/div/button[1]")
        client.click_on_element(pop_up_deleter)

        catagories_element = client.create_element("//*[@id=\"header-wrapper\"]/div[3]/div/div")
        client.click_on_element(catagories_element)

        all_category_elements = client.create_element("//*[@id=\"header-wrapper\"]/div[3]/div[1]/div[2]/div[1]").find_elements(By.TAG_NAME, "a")

        exceptions = ("Tüm İndirimli Ürünler", "Sadece Migros'ta")
        for current_catogory_element in all_category_elements :
            category_name = current_catogory_element.text
            category_link = current_catogory_element.get_attribute("href")

            if category_name not in exceptions :
                self.category_mapping[category_name] = category_link

    def _retrieve_sub_category_list(self, name, link) :

        print("Category " + name + " has been started.")

        temporary_navigation = []
        navigation_catalog = {}
        products_list = []
        typo_list = []
        product_browser = Web()
        typo_browser = Web()

        def _update_catalog(addition_list):
            refenence_var = navigation_catalog
            for item in addition_list:
                if item not in refenence_var:
                    refenence_var[item] = {}
                refenence_var = refenence_var[item]

        def _get_products(category_cats, category_link, category_product_count) :

            product_browser.open_web_page(category_link)

            category_cats = category_cats + [None] * (10 - len(category_cats))

            if category_product_count > 30 :
                latest_page_move = product_browser.create_element("//*[@id=\"pagination-button-last\"]/span[2]")
                product_browser.click_on_element(latest_page_move)
                time.sleep(1)
                last_page = product_browser.browser.current_url.split("=")[-1]
                product_browser.open_web_page(category_link)
            else :
                last_page = 1

            for i in range(1, int(last_page)+1):
                products = product_browser.create_element("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[2]/div[4]").find_elements(By.TAG_NAME, "sm-list-page-item")

                for product in products:
                    splitted_name = product.text.split("\n")
                    name = splitted_name[0] if not splitted_name[0].startswith("%") else splitted_name[2]
                    link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                    products_list.append([name, link, *category_cats])

                if category_product_count > 30 and i != int(last_page):
                    latest_page_move = product_browser.create_element("//*[@id=\"pagination-button-next\"]")
                    product_browser.click_on_element(latest_page_move)

        def _top_down_research(name, browser) :

            temporary_navigation.append(name)

            category_list = browser.create_element("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[1]/sm-product-filters-desktop/div/div[2]/div[2]").find_elements(By.TAG_NAME, "div")
            if len(category_list) == 1:
                last_element_name = category_list[0].text[0:category_list[0].text.find("(")].strip()
                owner_name = name
                if last_element_name == owner_name :
                    current_path = temporary_navigation
                else :
                    current_path = temporary_navigation + [last_element_name]
                print(current_path)
                _update_catalog(current_path)

                last_elements_procudt_count = category_list[0].text[category_list[0].text.find("(")+1:category_list[0].text.find(")")]
                last_elements_link = category_list[0].find_element(By.TAG_NAME, "a").get_attribute("href")

                _get_products(current_path, last_elements_link, int(last_elements_procudt_count))
                
                return
                
            counter = 0
            while counter < len(category_list) : 
                try :
                    current_sub_category = browser.create_element("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[1]/sm-product-filters-desktop/div/div[2]/div[2]").find_elements(By.TAG_NAME, "div")[counter]
                    sub_catagory_name = current_sub_category.text[0:current_sub_category.text.find("(")].strip()
                    sub_catagory_link = current_sub_category.find_element(By.TAG_NAME, "a").get_attribute("href")
                except :
                    counter = counter + 1
                    continue
                browser.open_web_page(sub_catagory_link)
                _top_down_research(sub_catagory_name, browser)
                counter = counter + 1
                browser.go_back()
                temporary_navigation.pop()

        def _get_types(category_name, category_link) :

            def get_typos() :

                browser = typo_browser

                time.sleep(1)
                filters = browser.create_element("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[1]/sm-product-filters-desktop/div")

                ng_stars = filters.find_elements(By.CLASS_NAME, "ng-star-inserted")

                typos_container = None
                for ng_star in ng_stars :
                    try :
                        if ng_star.find_element(By.CLASS_NAME, "subtitle-1").text == "Türü" :
                            typos_container = ng_star
                    except :
                        continue

                if typos_container is None :
                    return
                
                typos = typos_container.find_elements(By.CLASS_NAME, "ng-star-inserted")

                return typos

            def _get_typod_products(category_product_count, category_link, typo) :

                product_browser = typo_browser

                if category_product_count > 30 :
                    latest_page_move = product_browser.create_element("//*[@id=\"pagination-button-last\"]")
                    product_browser.click_on_element(latest_page_move)
                    time.sleep(1)
                    url = product_browser.browser.current_url
                    last_page = url[url.find("sayfa=")+6:url.find("&")]
                    product_browser.open_web_page(category_link)
                else :
                    last_page = 1

                for i in range(1, int(last_page)+1):
                    products = product_browser.create_element("/html/body/sm-root/div/main/sm-product/article/sm-list/div/div[4]/div[2]/div[4]").find_elements(By.TAG_NAME, "sm-list-page-item")

                    for product in products:
                        splitted_name = product.text.split("\n")
                        name = splitted_name[0] if not splitted_name[0].startswith("%") else splitted_name[2]
                        typo_list.append([name, typo])

                    if category_product_count > 30 and i != int(last_page):
                        latest_page_move = product_browser.create_element("//*[@id=\"pagination-button-next\"]")
                        product_browser.click_on_element(latest_page_move)

            browser = typo_browser

            browser.open_web_page(category_link)

            pop_up_deleter = browser.create_element("/html/body/sm-root/div/fe-product-cookie-indicator/div/div/button[1]")
            browser.click_on_element(pop_up_deleter)
            
            try :
                typo_count = len(get_typos())
            except :
                print("No typo for " + category_name + " category")
                return

            for current_typo_no in range(typo_count) :

                browser.open_web_page(category_link)

                typo = get_typos()[current_typo_no]

                text = typo.text
                typos_name = text[0:text.find("(")-1]
                typos_product_count = text[text.find("(")+1:text.find(")")]
                typo_link = typo.find_element(By.CLASS_NAME, "mdc-checkbox")
                typo_link.click()

                _get_typod_products(int(typos_product_count), category_link, typos_name)

        client = Web()
        client.open_web_page(link)

        pop_up_deleter = client.create_element("/html/body/sm-root/div/fe-product-cookie-indicator/div/div/button[1]")
        client.click_on_element(pop_up_deleter)

        _top_down_research(name, client)

        _get_types(name, link)

        typo_browser.terminate_client()
        product_browser.terminate_client()
        client.terminate_client()

        merged_list = []

        for l1 in products_list:
            is_matched = False
            for l2 in typo_list:
                if l1[0] == l2[0]:
                    _type = l2[1]
                    l1.insert(1, _type)
                    merged_list.append(l1)
                    is_matched = True
                    break
            if not is_matched:
                l1.insert(1, None)
                merged_list.append(l1)

        os.makedirs(connect_pathes("Temporary", name), exist_ok=True)

        json_output_path = connect_pathes("Temporary", name, name + ".json")
        with open(json_output_path, "w", encoding="utf-8") as json_file:
            json.dump(navigation_catalog, json_file, ensure_ascii=False, indent=4)

        product_list_data_frame = pd.concat([pd.DataFrame([row], columns=["name", "type", "link", "cat_1", "cat_2", "cat_3", "cat_4", "cat_5", "cat_6", "cat_7", "cat_8", "cat_9", "cat_10"]) for row in merged_list], ignore_index=True)
        csv_output_path = connect_pathes("Temporary", name, name + ".csv")
        product_list_data_frame.to_csv(csv_output_path, index=False)
        excel_output_path = connect_pathes("Temporary", name, name + ".xlsx")
        product_list_data_frame.to_excel(excel_output_path, index=False)

        print("Category " + name + " has been processed. And the results are saved in " + connect_pathes("Temporary", name))