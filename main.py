from Utilities import safeStart, safeStop
from Application import Scrapper

if __name__ == "__main__" :

    safeStart()
    
    app = Scrapper()
    
    safeStop()