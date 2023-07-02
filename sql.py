import sqlite3


def table_checker(con,cursor):
    try:
        cursor.execute("SELECT * FROM datas")
        dlist = cursor.fetchall()
    except sqlite3.OperationalError:  
        cursor.execute('''CREATE TABLE datas (
                                    start_date TEXT NOT NULL,
                                    finish_date TEXT NOT NULL,
                                    exe TEXT NOT NULL,
                                    title TEXT NOT NULL,
                                    path TEXT NOT NULL,
                                    duration TEXT NOT NULL,
                                    ip TEXT NOT NULL,
                                    computer_name TEXT NOT NULL,
                                    mouse TEXT NOT NULL,
                                    keyboard TEXT NOT NULL,
                                    url TEXT NOT NULL,
                                    user TEXT NOT NULL,
                                    company TEXT NOT NULL,
                                    client_id TEXT NOT NULL)''')

    con.commit()

def add_row(con,cursor,q):
    a= q.pop(0)
    cursor.executemany("INSERT INTO datas VALUES (?,?,?,?,?,?,?,?,?,?)", [a])
    con.commit()
    return q    