import os

def connect_pathes(*pathes):
    return os.path.join(*pathes)

PRE_EXISTING_CHECKLIST = ["Sources", "Data Export"]
CHROME_DRIVER_PATH = connect_pathes("Sources", "chromedriver.exe")
CACHED_FOLDER_LIST = ["Constants", "Utilities"]
CHROME_DRIVER_APPLICATION_DISPATCH = "Scripting.FileSystemObject"