from    selenium.webdriver.chrome.service  import Service
from    selenium.webdriver.chrome.options  import Options
from    selenium.webdriver.common.by       import By
from    selenium                           import webdriver
from   selenium.webdriver.common.action_chains import ActionChains
import  os
import bs4

from pprint import pprint


from Constants import *

class Web :

    def __init__(self, driver_path=CHROME_DRIVER_PATH, isHidden=False) :

        os.chmod(driver_path, 755)

        self.service = Service(executable_path=driver_path)
        self.options = Options()

        self.options.add_argument("--window-size=1920,1080")

        if isHidden :
            self.options.add_argument("--headless")
            
        self.browser = webdriver.Chrome(service=self.service, options=self.options)

        self.browser.maximize_window()

    def openWebPage(self,url) :
        self.browser.get(url)

    def terminate(self) :
        self.browser.quit()

    def createElement(self,xPath) :
        createdElement = None
        while (createdElement == None) :
            try :
                createdElement = self.browser.find_element(By.XPATH, xPath)
            except :
                continue
        return createdElement

    def clickOnElement(self, element) :
        while (True) :
            try :
                element.click()
                break
            except :
                continue

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