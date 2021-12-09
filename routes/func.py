from os import system, name
import datetime

def screen_clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def isstartingwithnumber(string):
    try:
        _ = int(string[0])
        return False
    except ValueError:
        return True

def epochtostr(e):
    i = datetime.datetime.fromtimestamp(int(e))
    return datetime.time.strptime(i, '%Y-%m-%dT%H:%M:%S')