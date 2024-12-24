import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        secures a connection with database and stores it in the variable conn
        """
        self.conn = sqlite3.connect("venmo.db", check_same_thread=False)
        self.create_user_table() 
    
    def create_user_table(self):
        """
        Using SQL, creates a users table 
        """
        self.conn.execute("""

        CREATE TABLE IF NOT EXISTS users(
                          
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name  TEXT NOT NULL,
                          username TEXT NOT NULL,
                          balance INTEGER NOT NULL DEFAULT 0
                
        );""")

    def delete_user_table(self):
        """
        Using SQL, deletes user table 
        """
        self.conn.execute(""" DROP TABLE IF EXISTS users; """)

    def get_all_users(self):
        """
        Using SQL, returns all users
        """
        cursor = self.conn.execute(""" SELECT * FROM users """)
        users = [] 
        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users 
    
     
    
    def insert_user_table(self, name, username, balance=None):
        """
        Using SQL, inserts user to users table 
        """
        if balance is None:
            cursor = self.conn.execute("""
                INSERT INTO users(name, username) VALUES (?, ?);                   
            """, (name, username))
        else:
            cursor = self.conn.execute("""
                INSERT INTO users(name, username, balance) VALUES (?, ?, ?);                   
            """, (name, username, balance))
        
        self.conn.commit() 

        return cursor.lastrowid
    
    def get_user_by_id(self, user_id):
        """
        Using SQL, gets a specific user by id
        """
        cursor = self.conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        
        for row in cursor:
            return ({"id": row[0], "name": row[1], "username": row[2], "balance": row[3] if len(row) > 3 else 0})
        return None 
    
    def delete_user_by_id(self, user_id):
        """
        Using SQL, deletes specific user 
        """
        self.conn.execute("""
                          
            DELETE FROM users WHERE id = ?

        """, (user_id, ))
        self.conn.commit() 

    def update_user_balance(self, user_id, new_balance):
        """
        Using SQL, updates senders and receivers balance 
        """
        self.conn.execute("""
            UPDATE users SET balance = ? WHERE id = ?

        """, (new_balance, user_id))

        self.conn.commit()

    
    
     




# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
