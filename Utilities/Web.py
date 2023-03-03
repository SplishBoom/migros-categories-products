from    selenium.webdriver.chrome.service  import Service
from    selenium.webdriver.chrome.options  import Options
from    selenium.webdriver.common.by       import By
from    selenium                           import webdriver
import  os

from Constants import CHROME_DRIVER_PATH

class Web :

    def __init__(self, driver_path=CHROME_DRIVER_PATH, isHidden=False) :

        os.chmod(driver_path, 755)

        self.service = Service(executable_path=driver_path,)
        self.options = Options()

        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])

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