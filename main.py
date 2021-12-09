# Init
import routes.main_db as db
import routes.main_ui as ui
import routes.setuponce
import os
import configparser

# Load Config
cnf = configparser.ConfigParser()
if os.path.exists("amumal.cfg"):
    cnf.read("amumal.cfg")
    db.initialize("db/" + cnf.get("config", "db_path") + ".dat")
else:
    # Make Config file
    pf = open("amumal.cfg", "w")
    pf.write("")
    pf.close()
    # Call Basic Setup Tool
    sonce = routes.setuponce.setuponce(cnf)
    # Make DB file
    pf = open("db/" + sonce[0] + ".dat", "w")
    pf.write("")
    pf.close()
    db.initialize("db/" + sonce[0] + ".dat")

ui.a_list(db, cnf)