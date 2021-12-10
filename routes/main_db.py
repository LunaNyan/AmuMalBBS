import configparser
import base64
import shutil

db = configparser.ConfigParser()
db_path = ""
initialized = False

# DB file actions
def initialize(filename):
    global db_path, initialized
    db_path = filename
    db.read(filename)
    initialized = True

def commit():
    if initialized:
        with open(db_path, 'w') as configfile:
            db.write(configfile)
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

def copy(to_name):
    if initialized:
        commit()
        shutil.copy(db_path, to_name)
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

# DB I/O department
def read_raw(section, key):
    if initialized:
        return db.get(section, key)
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

def read_b64(section, key):
    if initialized:
        return str(base64.b64decode(db.get(section, key)).decode('utf-8'))
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

def write_raw(section, key, value):
    if initialized:
        db.set(section, key, value)
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

def write_b64(section, key, value):
    if initialized:
        e = base64.b64encode(value.encode('utf-8'))
        e = str(e).replace("b'", "")
        e = e.replace("'", "")
        db.set(section, key, e)
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

# etc
def sections():
    if initialized:
        return db.sections()
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

def add_section(section):
    if initialized:
        return db.add_section(section)
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")

def remove_section(section):
    if initialized:
        return db.remove_section(section)
    else:
        raise NameError(
            "DB I/O module is not initialized. you may have to initialize DB module with 'main_db.initialize(filename)'.")