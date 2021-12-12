from os import system, name
import datetime

def screen_clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
