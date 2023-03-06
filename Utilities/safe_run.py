"""
This script is used for execution safety of the program.
"""

from    Constants   import connect_urls, CONNECTION_TEST_URL, CHROME_DRIVER_DOWNLOAD_URL, CHROME_DRIVER_DOWNLOAD_PARTITION
from    Constants   import CHROME_DRIVER_PATH, CACHED_FOLDER_LIST, PRE_EXISTING_CHECKLIST
from    bs4         import BeautifulSoup
from    sys         import platform
import  requests
import  colorama
import  zipfile
import  shutil
import  os
import  io
import  re

def _get_chrome_version() -> str:
    """
    Private Method, that gets the chrome version.
    @Params:
        - None
    @Return:
        - str : Chrome version.
    """

    def _extract_version_folder() -> str:
        """
        Private Method, that extracts the chrome version from the folder.
        @Params:
            - None
        @Return:
            - str : Chrome version.
        """
        # Check if the Chrome folder exists in the x32 or x64 Program Files folders.
        for i in range(2):
            path = 'C:\\Program Files' + (' (x86)' if i else '') +'\\Google\\Chrome\\Application'
            if os.path.isdir(path):
                paths = [f.path for f in os.scandir(path) if f.is_dir()]
                for path in paths:
                    filename = os.path.basename(path)
                    pattern = '\d+\.\d+\.\d+\.\d+'
                    match = re.search(pattern, filename)
                    if match and match.group():
                        # Found a Chrome version.
                        return match.group(0)
        return None
    
    def _extract_version_registry(output) -> str:
        """
        Private Method, that extracts the chrome version from the registry.
        @Params:
            - None
        @Return:
            - str : Chrome version.
        """
        try:
            google_version = ''
            for letter in output[output.rindex('DisplayVersion    REG_SZ') + 24:]:
                if letter != '\n':
                    google_version += letter
                else:
                    break
            return(google_version.strip())
        except TypeError:
            return
        
    version = None
    install_path = None

    try:
        if platform == "linux" or platform == "linux2":
            # linux
            install_path = "/usr/bin/google-chrome"
        elif platform == "darwin":
            # OS X
            install_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
        elif platform == "win32":
            # Windows...
            try:
                # Try registry key.
                stream = os.popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
                output = stream.read()
                version = _extract_version_registry(output)
            except Exception as ex:
                # Try folder path.
                version = _extract_version_folder()
    except Exception as ex:
        pass

    version = os.popen(f"{install_path} --version").read().strip('Google Chrome ').strip() if install_path else version

    if version is None:
        print(colorama.Fore.RED, f"***LOG: Chrome not detected, terminating application !", colorama.Fore.RESET)
        exit()

    return version

def _load_chrome_driver() -> None:
    """
    Private Method, that loads the chrome driver.
    @Params:
        - None
    @Return:
        - None
    """
    
    version_base = _get_chrome_version()

    version_base = version_base.split(".")[0]

    download_page_response = requests.get(CHROME_DRIVER_DOWNLOAD_URL)

    parsed_page = BeautifulSoup(download_page_response.text, "html.parser")

    all_versions = parsed_page.find_all("a", class_="XqQF9c")

    for current_version in all_versions :

        if current_version.text.split(" ")[1].startswith(version_base) :
            official_version = current_version.text.split(" ")[1]
            break       

    file_download_url = connect_urls(CHROME_DRIVER_DOWNLOAD_PARTITION["base"], official_version, CHROME_DRIVER_DOWNLOAD_PARTITION["args"])

    download_response = requests.get(file_download_url)
    zipFile = zipfile.ZipFile(io.BytesIO(download_response.content))
    zipFile.extractall("Sources")

def _check_internet_connection() -> bool :
    """
    Private Method, that checks if the internet connection is available.
    @Params:
        - None
    @Return:
        - bool : True if internet connection is available, False otherwise.
    """
    try :
        requests.get(CONNECTION_TEST_URL)
        return True
    except :
        return False

def safeStart() -> None:
    """
    Public Method, that checks if the program can be started.
    @Params:
        - None
    @Return:
        - None
    """

    print()

    for path in PRE_EXISTING_CHECKLIST :
        if not os.path.exists(path) :
            if os.path.splitext(path)[1] == "" :
                print(colorama.Fore.RED, f"***LOG: The folder {path} was not found, creating...", colorama.Fore.RESET)
                os.mkdir(path)
            else :
                print(colorama.Fore.RED, f"***LOG: The file {path} was not found, creating...", colorama.Fore.RESET)
                with open(path, "w") as f :
                    f.write("")

    print(colorama.Fore.GREEN, "***LOG: Pre-Existing-Checklist approved, continuing...", colorama.Fore.RESET)

    if not _check_internet_connection() :
        print(colorama.Fore.RED, "***LOG: No internet connection found, terminating application...", colorama.Fore.RESET)
        exit()
    else :
        print(colorama.Fore.GREEN, "***LOG: Internet connection found, continuing...", colorama.Fore.RESET)

    if not os.path.exists(CHROME_DRIVER_PATH) :
        print(colorama.Fore.RED, "***LOG: Chrome driver not found, downloading...", colorama.Fore.RESET)
        _load_chrome_driver()
    else :
        print(colorama.Fore.GREEN, "***LOG: Chrome driver found, continuing...", colorama.Fore.RESET)

    print(colorama.Fore.YELLOW, "***LOG: Application started successfully !", colorama.Fore.RESET)

def safeStop() -> None:
    """
    Public Method, that checks if the program can be stopped.
    @Params:
        - None
    @Return:
        - None
    """

    projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for folder in CACHED_FOLDER_LIST :
        folderPath = os.path.join(projectDir, folder)
        for root, dirs, files in os.walk(folderPath):
            for dir in dirs :
                if dir == "__pycache__" :
                    print(colorama.Fore.BLUE, f"***LOG: Cache cleared -> ./{folder}...", colorama.Fore.RESET)
                    shutil.rmtree(os.path.join(root, dir))

    print(colorama.Fore.YELLOW, "***LOG: Application closed successfully !", colorama.Fore.RESET)
    
    exit()