import routes.main_articles as main_articles
import routes.func as func
import math

def a_reader(db, cfg, article):
    content = main_articles.read_article(db, article[0])
    attention = ""
    while True:
        func.screen_clear()
        print(article[1])
        print("작성자 : " + article[2] + ", 작성 일자 " + func.epochtostr(article[3])+ "\n----------")
        print(content)
        print("----------")
        if attention != "":
            print(attention)
        print("목록으로(P), 수정하기(E), 삭제하기(D)")
        i = input(cfg.get("config", "username") + "> ")
        if i == "P":
            break
        elif i == "E":
            attention = "TODO"
            continue
        elif i == "D":
            attention = "TODO"
            continue
        else:
            attention = ""
            continue

def a_list(db, cfg):
    al = main_articles.list_articles(db)
    page = 1
    pages = math.ceil(len(al) / 10)
    attention = ""
    # 게시물 리스트
    while True:
        func.screen_clear()
        print(cfg.get("config", "db_title") + " (게시물 총 " + str(len(al)) + "개)\n----------")
        c = (page - 1) * 10
        trk = al[c:c+10]
        nx = 10 + ((page - 1) * 5)
        for k in trk:
            print("#" + str(nx) + "\t" + k[1] + "\n\t작성자 : " + k[2] + ", 작성 일자 " + func.epochtostr(k[3]))
            nx += 1
        print("----------")
        if attention != "":
            print(attention)
        print("페이지 " + str(page) + " / " + str(pages))
        print("1페이지 이동(<, >), 처음 페이지로(<<), 마지막 페이지로(>>), 특정 페이지로 이동(P[페이지]), 게시물 읽기(R[번호]), 게시물 쓰기(W), 종료(X)")
        i = input(cfg.get("config", "username") + "> ")
        # Command Parser
        if i == "<":
            if page == 1:
                attention = "맨 처음 페이지입니다."
                continue
            else:
                page -= 1
                attention = ""
                continue
        elif i == ">":
            if page == pages:
                attention = "맨 마지막 페이지입니다."
                continue
            else:
                page += 1
                attention = ""
                continue
        elif i == "<<":
            page = 1
            attention = ""
            continue
        elif i == ">>":
            page = pages
            attention = ""
            continue
        elif i.startswith("P"):
            try:
                t = i.replace("P", "")
                if int(t) >= pages or int(t) <= 0:
                    attention = "잘못된 페이지 번호입니다."
                    continue
                else:
                    page = int(t)
                    attention = ""
                    continue
            except ValueError:
                attention = "P[페이지 번호] 형태로 입력해 주십시오. (예시 : P1)"
                continue
        elif i.startswith("R"):
            try:
                t = i.replace("R", "")
                if int(t) <= 0 or int(t) >= len(al):
                    attention = "존재하지 않는 게시물 번호입니다."
                    continue
                else:
                    art = al[int(t) - 1]
                    a_reader(db, cfg, art)
                    continue
            except ValueError:
                attention = "R[게시물 번호] 형태로 입력해 주십시오. (예시 : R1)"
                continue
        elif i == "W":
            attention = "TODO"
            continue
        elif i == "X":
            break
        else:
            attention = ""
            continue
