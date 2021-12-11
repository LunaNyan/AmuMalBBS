import routes.main_articles as main_articles
import routes.func as func
import routes.texteditor as texteditor
import math
import time

def a_comments(db, cfg, article):
    page = 1
    attention = ""
    while True:
        ctrk = main_articles.read_comment(db, article[0])
        ctrk.reverse()
        pages = math.ceil(len(ctrk) / 10)
        c1 = (page - 1) * 10
        ctrkp = ctrk[c1:c1+10]
        nx = len(ctrk) - ((page - 1) * 10)
        func.screen_clear()
        print("댓글 목록 (총 " + str(len(ctrk)) + "개)")
        print(article[1])
        print("----------")
        if len(ctrk) == 0:
            print("작성된 댓글이 없습니다.")
        else:
            for c in ctrkp:
                d = time.localtime(int(c[2]))
                d = time.strftime('%Y-%m-%d %H:%M:%S', d)
                print("#" + str(nx) + " : " + c[0] + " - " + d)
                print("\t" + c[1])
                nx -= 1
        print("----------")
        if attention != "":
            print(attention)
        print("페이지 " + str(page) + " / " + str(pages))
        print("1페이지 이동(<, >), 처음 페이지로(<<), 마지막 페이지로(>>), 특정 페이지로 이동(P[페이지]), 댓글 작성(W), 뒤로가기(B)")
        i = input(cfg.get("config", "username") + "> ")
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
        elif i.upper() == "B":
            break
        elif i.upper() == "W":
            usn = cfg.get("config", "username")
            print("취소(@X)")
            username = input("작성자 이름 입력 (" + usn + ") : ")
            if username.upper() == "@X":
                attention = "댓글 작성을 취소하였습니다."
                continue
            if username == "":
                username = usn
            content = input("내용 입력 : ")
            if content.upper() == "@X":
                attention = "댓글 작성을 취소하였습니다."
                continue
            main_articles.write_comment_once(db, article[0], username, content)
            db.commit()
            continue
        else:
            attention = ""
            continue

def a_reader(db, cfg, article):
    content = main_articles.read_article(db, article[0])
    attention = ""
    while True:
        func.screen_clear()
        d = time.localtime(int(article[3]))
        d = time.strftime('%Y-%m-%d %H:%M:%S', d)
        print(article[1])
        print("작성자 : " + article[2] + ", 작성 일시 : " + d)
        print("----------")
        print(content)
        print("----------")
        if attention != "":
            print(attention)
        print("목록으로(B), 댓글 보기(C), 수정하기(E), 삭제하기(D)")
        i = input(cfg.get("config", "username") + "> ")
        if i.upper() == "B":
            break
        elif i.upper() == "C":
            a_comments(db, cfg, article)
            db.commit()
            continue
        elif i.upper() == "E":
            attention = "TODO"
            continue
        elif i.upper() == "D":
            i = input("정말로 삭제하시겠습니까? (Y/N) : ")
            if i == "Y" or i == "y":
                db.remove_section(article[0])
                db.commit()
                break
            else:
                continue
        else:
            attention = ""
            continue

def a_list(db, cfg):
    page = 1
    attention = ""
    # 게시물 리스트
    while True:
        al = main_articles.list_articles(db)
        al.reverse()
        pages = math.ceil(len(al) / 10)
        func.screen_clear()
        print(cfg.get("config", "db_title") + " (게시물 총 " + str(len(al)) + "개)\n----------")
        c = (page - 1) * 10
        trk = al[c:c+10]
        nx = len(al) - ((page - 1) * 10)
        if len(al) == 0:
            print("작성된 게시물이 없습니다.")
        else:
            for k in trk:
                d = time.localtime(int(k[3]))
                d = time.strftime('%Y-%m-%d %H:%M:%S', d)
                print("#" + str(nx) + "\t" + k[1] + "\n\t작성자 : " + k[2] + ", 작성 일시 : " + d)
                nx -= 1
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
        elif i.startswith("P") or i.startswith("p"):
            try:
                t = i.replace("P", "")
                t = t.replace("p", "")
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
        elif i.startswith("R") or i.startswith("r"):
            try:
                t = i.replace("R", "")
                t = t.replace("r", "")
                if int(t) <= 0 or int(t) > len(al):
                    attention = "존재하지 않는 게시물 번호입니다."
                    continue
                else:
                    al2 = al
                    al2.reverse()
                    art = al2[int(t) - 1]
                    a_reader(db, cfg, art)
                    continue
            except ValueError:
                attention = "R[게시물 번호] 형태로 입력해 주십시오. (예시 : R1)"
                continue
        elif i.upper() == "W":
            usn = cfg.get("config", "username")
            title = input("게시물 제목 입력 : ")
            username = input("작성자 이름 입력 (" + usn + ") : ")
            if username == "":
                username = usn
            t = texteditor.editor(title)
            main_articles.write_article(db, title, username, t)
            continue
        elif i.upper() == "X":
            break
        else:
            attention = ""
            continue
