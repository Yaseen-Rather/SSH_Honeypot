#===================================================================================================================================================
#                                                  Logs Database
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


create_database()


