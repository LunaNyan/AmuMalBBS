import datetime
import random

def list_articles(db):
    s = db.sections()
    truck = []
    for i in s:
        if i == "metadata":
            pass
        else:
            truck.append([i, db.read_b64(i, "title"), db.read_b64(i, "author"), db.read_b64(i, "datetime")])
    return truck

def read_article(db, id):
    return db.read_b64(id, "content")

def read_comment(db, id):
    # read comments from article object
    ca = db.read_b64(id, "comment_author")
    cc = db.read_b64(id, "comment_content")
    cd = db.read_b64(id, "comment_datetime")
    # comment list is empty => return empty list
    if ca == "":
        return []
    else:
        # make accessible list
        # split with "✦"
        ca = ca.split("✦")
        cc = cc.split("✦")
        cd = cd.split("✦")
        # make comments truck
        trk = []
        tn = 0
        tl = len(ca) - 1
        while tl >= tn:
            trk.append([ca[tn], cc[tn], cd[tn]])
            tn += 1
        return trk

def save_comment(db, id, trk):
    ta = ""
    tc = ""
    td = ""
    for c in trk:
        ta += c[0] + "✦"
        tc += c[1] + "✦"
        td += c[2] + "✦"
    db.write_b64(id, "comment_author", ta[:-1])
    db.write_b64(id, "comment_content", tc[:-1])
    db.write_b64(id, "comment_datetime", td[:-1])

def write_comment_once(db, id, author, content):
    trk = read_comment(db, id)
    dt = datetime.datetime.now()
    dt = int(dt.timestamp())
    trk.append([author, content, str(dt)])
    save_comment(db, id, trk)

def write_article(db, title, username, content, comments=None):
    dt = datetime.datetime.now()
    dt = int(dt.timestamp())
    aid = str(dt) + "_" + str(random.randint(0, 9999))
    db.add_section(aid)
    db.write_b64(aid, "title", title)
    db.write_b64(aid, "author", username)
    db.write_b64(aid, "datetime", str(dt))
    db.write_b64(aid, "content", content)
    if comments == None:
        db.write_b64(aid, "comment_author", "")
        db.write_b64(aid, "comment_content", "")
        db.write_b64(aid, "comment_datetime", "")
    else:
        pass
    db.commit()

def edit_article(aid, content):
    db.write_b64(aid, "content", content)
    db.commit()
