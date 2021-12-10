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
    dbp = cnf.get("config", "db_path")
    while True:
        di = input("DB 경로 (최근 : " + dbp + ") : ")
        if di != "":
            if os.path.exists("db/" + di + ".dat"):
                dbp = di
                cnf.set("config", "db_path", di)
                break
            else:
                print("존재하지 않는 데이터베이스 파일입니다.")
                i = input("새로 생성할까요? (Y/N) : ")
                if i == "Y" or i == "y":
                    pf = open("db/" + di + ".dat", "w")
                    pf.write("")
                    pf.close()
                else:
                    continue
        else:
            break
    db.initialize("db/" + dbp + ".dat")
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

# Call main UI
ui.a_list(db, cnf)