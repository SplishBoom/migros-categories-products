from Utilities import safeStart, safeStop
from Application import scrapper

if __name__ == "__main__" :

    safeStart()
    
    scrapper()
    
    safeStop()