import sqlite3, asyncio

from config import admins


db = sqlite3.connect("users.db")
sql = db.cursor()



async def createDB():

    sql.execute("""CREATE TABLE IF NOT EXISTS users(
                id TEXT,
                rate TEXT,
                bal INT,
                nick TEXT,
                exp INT,
                verif INT,
                adm INT
    )""")

    sql.execute("""CREATE TABLE IF NOT EXISTS beats(
                msg_id TEXT,
                proj_id TEXT,
                ath_id TEXT,
                sell INT,
                full INT,
                commerc INT,
                read INT
    )""")

    sql.execute("""CREATE TABLE IF NOT EXIXST bot(
                stop INT
    )""")

    db.commit()
    return True

async def check(id):
    sql.execute("SELECT * FROM users WHERE id= ?", (id,))
    if sql.fetchone() is None:
        return False
    return True


async def reg(id, name):
    sql.execute("SELECT * FROM users WHERE id= ?", (id,))
    if sql.fetchone() is None:
        #id TEXT, rate INT, bal INT, nick TEXT, exp INT, verif INT, adm INT
        if id in admins:
            sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (id, "Новичок", 10000, name, 0, 100, 100,))
            db.commit()
            return "ADMIN"
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (id, "Новичок", 0, name, 0, 0, 0,))
        db.commit()
        return "USER"


async def regbeat(msg_id, proj_id, ath_id, full, commerc, read, price):

    sql.execute("INSERT INTO beats VALUES (?, ?, ?, ?, ?, ?, ?)", (msg_id, proj_id, ath_id, 1, full, commerc, read,))
    db.commit()

    return True