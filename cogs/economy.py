import sqlite3
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the filename of your SQLite database
database_filename = 'economy_database.db'  # Adjust this to your actual filename

# Combine the script directory with the database filename
database_path = os.path.join(script_directory, database_filename)

class Economy:
    def __init__(self, database_path):
        # Connecting to database
        self.conn = sqlite3.connect(database_path)
        self.c = self.conn.cursor()

        # Creating a table
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    balance REAL,
                    bank REAL
                )
            ''')
        self.conn.commit()

        # Insert user data
    def insert_user(self, username, balance, bank):
        self.c.execute('INSERT INTO users (username, balance, bank) VALUES (?, ?, ?)', (username, balance, bank))  # Fixed typo 'NSERT'
        self.conn.commit()

        # Get user balance
    def get_user_balance(self, username):
        self.c.execute('SELECT balance FROM users WHERE username = ?', (username,))
        balance = self.c.fetchone()
        if balance:
            return balance[0]
        else:
            return None

        # Get user bank balance
    def get_user_bank(self, username):
        self.c.execute('SELECT bank FROM users WHERE username = ?', (username,))
        bank = self.c.fetchone()
        if bank:
            return bank[0]
        else:
            return None

        # Close the database connection (ideally, this should be handled in your bot's shutdown process)
    def close_connection(self):    
        self.conn.close()
