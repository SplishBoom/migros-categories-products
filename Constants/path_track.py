import os

def connect_pathes(*pathes):
    return os.path.join(*pathes)

PRE_EXISTING_CHECKLIST = ["Temporary", "Sources", "Data Export"]
OUTPUT_JSON_FILE_PATH = connect_pathes("Data Export", "catalog.json")
CHROME_DRIVER_PATH = connect_pathes("Sources", "chromedriver.exe")
CACHED_FOLDER_LIST = ["Application", "Constants", "Utilities"]
CHROME_DRIVER_APPLICATION_DISPATCH = "Scripting.FileSystemObject"
OUTPUT_EXCEL_FILE_PATH = connect_pathes("Data Export", "products.xlsx")
OUTPUT_CSV_FILE_PATH = connect_pathes("Data Export", "products.csv")
