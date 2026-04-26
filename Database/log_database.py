#===================================================================================================================================================
#                                                  Logs Database                                                                                   #
#===================================================================================================================================================


# Libraries

import sqlite3

import threading

from datetime import datetime

# database lock (semaphore)

db_lock = threading.Lock() 

# Create Database

def create_database():

    conn = sqlite3.connect("./Database/Honeypot_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS attemps (

            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT,
            ip          TEXT,
            username    TEXT,
            password    TEXT,
            accepted    INTEGER
        )
    """)

    conn.commit()
    conn.close()


# Insert data into the Database

def log_attempt(ip, username, password, accepted):

    with db_lock:
        conn = sqlite3.connect("./Database/log_database")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attemps (timestamp, ip, username, password, accepted)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.datetime.now().isoformat(), ip, username, password, int(accepted)))

        conn.commit()
        conn.close()




