import datetime
import random

def list_articles(db):
    s = db.sections()
    truck = []
    for i in s:
        truck.append([i, db.read_b64(i, "title"), db.read_b64(i, "author"), db.read_b64(i, "datetime")])
    return truck

def read_article(db, id):
    return db.read_b64(id, "content")

def write_article(db, title, username, content):
    dt = datetime.datetime.now()
    dt = int(dt.timestamp())
    aid = str(dt) + "_" + str(random.randint(0, 9999))
    db.add_section(aid)
    db.write_b64(aid, "title", title)
    db.write_b64(aid, "author", username)
    db.write_b64(aid, "datetime", str(dt))
    db.write_b64(aid, "content", content)
    db.commit()
