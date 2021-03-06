import routes.func as func

def setuponce(db):
    print("초기 설정을 진행합니다.")
    db.add_section("config")
    # DB name
    while True:
        dbn = input("데이터베이스 파일 이름(기본값 : db) : ")
        if dbn == "":
            dbn = "db"
            db.set("config", "db_path", "db")
            break
        else:
            db.set("config", "db_path", dbn)
            break
    # DB title
    while True:
        dbt = input("데이터베이스 제목(기본값 : 아무말) : ")
        if dbt == "":
            dbt = "아무말"
            break
        else:
            break
    # User name
    while True:
        ui = input("기본 사용자 이름(기본값 : amumal) : ")
        if ui == "":
            db.set("config", "username", "amumal")
            break
        else:
            db.set("config", "username", ui)
            break
    # DB Backup
    while True:
        da = input("애플리케이션 실행 전에 데이터베이스 백업(Y/N) (기본값 : Y) : ")
        if da == "Y" or da == "y":
            db.set("config", "backup_db", "1")
            break
        elif da == "N" or da == "n":
            db.set("config", "backup_db", "0")
            break
        elif da == "":
            db.set("config", "backup_db", "1")
            break
        else:
            print("Y 또는 N으로 응답하여 주십시오.\n중도 취소를 원하시는 경우 Ctrl+C를 눌러 주십시오.")
            continue
    print("초기 설정을 완료하였습니다.")
    with open("amumal.cfg", 'w') as configfile:
        db.write(configfile)
    return [dbn, dbt]