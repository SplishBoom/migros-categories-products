"""
Script to store all the urls used in the project. ("Note: this is not exactly achieved yet !")
"""

def connect_urls(*urls) -> str:
    """
    Public Method, that connects the urls.
    @Params:
        - urls : (Required) : Urls to be connected.
    @Return:
        - str : Connected urls.
    """
    return "/".join(urls)

CHROME_DRIVER_DOWNLOAD_URL = "https://chromedriver.chromium.org/downloads"
CONNECTION_TEST_URL = "https://www.google.com"
CHROME_DRIVER_DOWNLOAD_PARTITION = {"base":"https://chromedriver.storage.googleapis.com", "args":"chromedriver_win32.zip"}