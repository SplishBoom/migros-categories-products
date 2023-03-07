"""
This program is a web scrapper that scrapes the web for the latest products & typos & links through the Migros Sanal Market website.

@Authors :
    - <3 THE MIRMIR <3

******************************************************************************
******************************************************************************
**** ██               ██  ██  ██████    ██               ██  ██  ██████   ****
**** ████           ████  ██  █   ███   ████           ████  ██  █   ███  ****
**** ██  ██       ██  ██  ██  █████     ██  ██       ██  ██  ██  █████    ****
**** ██    ██   ██    ██  ██  ██   ██   ██    ██   ██    ██  ██  ██   ██  ****
**** ██      ███      ██  ██  ██    ██  ██      ███      ██  ██  ██    ██ ****
******************************************************************************
******************************************************************************

@Since : 
    - 3/6/2023

@Contact :
    - memise@mef.edu.tr
    - yildizah@mef.edu.tr
"""

from Utilities   import safeStart, safeStop
from Application import Scrapper

if __name__ == "__main__" :

    safeStart()
    
    Scrapper()
    
    safeStop()