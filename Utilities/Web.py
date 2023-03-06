"""
This script is used for handling web browser operations.
"""

from    selenium.webdriver.chrome.service   import Service
from    selenium.webdriver.chrome.options   import Options
from    selenium.webdriver.common.by        import By
from    Constants                           import CHROME_DRIVER_PATH
from    selenium                            import webdriver
import  os

class Web :
    """
    Class, that initializes and overrides selenium webdriver.
    """

    def __init__(self, driver_path=CHROME_DRIVER_PATH, isHidden=True) -> None:
        """
        Constructor, that initializes selenium browser.
        @Params:
            - driver_path : (Optional) : Path to the chrome driver.
            - isHidden    : (Optional) : If true, browser will be hidden.
        @Return:
            - None
        """

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

    def open_web_page(self,url) -> None:
        """
        Public Class Method, that opens a web page.
        @Params:
            - None
        @Return:
            - None
        """
        self.browser.get(url)

    def go_back(self) -> None:
        """
        Public Class Method, that goes back to the previous page.
        @Params:
            - None
        @Return:
            - None
        """
        self.browser.back()

    def terminate_client(self) -> None:
        """
        Public Class Method, that terminates the browser.
        @Params:
            - None
        @Return:
            - None
        """
        self.browser.quit()

    def create_element(self,xPath) -> None:
        """
        Public Class Method, that creates an element. With certain quarantees likewise the loop.
        @Params:
            - xPath : (Required) : Path to the element.
        @Return:
            - None
        """
        createdElement = None
        while (createdElement == None) :
            try :
                createdElement = self.browser.find_element(By.XPATH, xPath)
            except :
                continue
        return createdElement

    def click_on_element(self, element) -> None:
        """
        Public Class Method, that clicks on an element. With certain quarantees likewise the loop.
        @Params:
            - element : (Required) : Element to be clicked.
        @Return:
            - None
        """
        while (True) :
            try :
                element.click()
                break
            except :
                continue