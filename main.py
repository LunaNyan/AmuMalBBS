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
                db.initialize("db/" + dbp + ".dat")
                break
            else:
                print("존재하지 않는 데이터베이스 파일입니다.")
                i = input("새로 생성할까요? (Y/N) : ")
                if i == "Y" or i == "y":
                    pf = open("db/" + di + ".dat", "w")
                    pf.write("")
                    pf.close()
                    # DB title
                    db.initialize("db/" + di + ".dat")
                    dbt = input("데이터베이스 제목(기본값 : 아무말) : ")
                    db.add_section("metadata")
                    if dbt == "":
                        db.write_b64("metadata", "db_title", "아무말")
                    else:
                        db.write_b64("metadata", "db_title", dbt)
                    db.commit()
                    cnf.set("config", "db_path", di)
                    break
                else:
                    continue
        else:
            db.initialize("db/" + dbp + ".dat")
            break
    #if cnf.get("config", "backup_db") == "1":
    #    db.copy("db/" + dbp + "_backup.dat")

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
    db.add_section("metadata")
    db.write_b64("metadata", "db_title", sonce[1])
    db.commit()

# Call main UI
with open("amumal.cfg", 'w') as configfile:
    cnf.write(configfile)
ui.a_list(db, cnf)