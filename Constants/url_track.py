def connect_urls(*urls):
    return "/".join(urls)

CHROME_DRIVER_DOWNLOAD_URL = "https://chromedriver.chromium.org/downloads"
CONNECTION_TEST_URL = "https://www.google.com"
CHROME_DRIVER_DOWNLOAD_PARTITION = {"base":"https://chromedriver.storage.googleapis.com", "args":"chromedriver_win32.zip"}