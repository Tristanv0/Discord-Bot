import sqlite3

class Economy:
    def __init__(self, database_path):
        # Connecting to the database
        self.conn = sqlite3.connect(database_path)
        self.c = self.conn.cursor()

        # Creating a table
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    guild TEXT,
                    username TEXT,
                    balance REAL,
                    bank REAL
                )
            ''')
        self.conn.commit()

    def insert_user(self, guild, username, balance, bank):
        self.c.execute('INSERT INTO users (guild, username, balance, bank) VALUES (?, ?, ?, ?)', (guild, username, balance, bank))
        self.conn.commit()

    def get_user_balance(self, guild, username):
        try:
            self.c.execute('SELECT balance FROM users WHERE guild = ? AND username = ?', (guild, username))
            balance = self.c.fetchone()
            if balance:
                return balance[0]
            else:
                return None
        except sqlite3.Error as e:
            print("Error retrieving user balance:", e)
            return None

    #placing bet
    def update_user_balance(self, guild, username, amount):        #amount = amount to subtract by
        self.c.execute('SELECT balance FROM users WHERE guild = ? AND username = ?', (guild, username))
        balance = self.c.fetchone()

        if balance:
            new_balance = balance[0] - amount
            self.c.execute('UPDATE users SET balance = ? WHERE guild = ? AND username = ?', (new_balance, guild, username))
            self.conn.commit()
        else:
            print("User not found in the database.")

    #update user balance according to winning or work pay
    def user_winning(self, guild, username, amount):         #amount = amount to add by
        self.c.execute('SELECT balance FROM users WHERE guild = ? AND username = ?', (guild, username))
        balance = self.c.fetchone()
        
        if balance:
            new_balance = balance[0] + amount
            self.c.execute('UPDATE users SET balance = ? WHERE guild = ? AND username = ?', (new_balance, guild, username))
            self.conn.commit()
        else:
            print("User not found in the database.")
        
    def get_user_bank(self, guild, username):
        self.c.execute('SELECT bank FROM users WHERE guild = ? AND username = ?', (guild, username))
        bank = self.c.fetchone()
        if bank:
            return bank[0]
        else:
            return None

    def deposit(self, guild, username, amount):
        self.c.execute('SELECT bank FROM users WHERE guild = ? AND username = ?', (guild, username))
        bank = self.c.fetchone()
        self.c.execute('SELECT balance FROM users WHERE guild = ? AND username = ?', (guild, username))
        balance = self.c.fetchone()
        
        if bank and balance:
            new_balance = balance[0] - amount
            self.c.execute('UPDATE users SET balance = ? WHERE guild = ? AND username = ?', (new_balance, guild, username))
            new_bank = bank[0] + amount
            self.c.execute('UPDATE users SET bank = ? WHERE guild = ? AND username = ?', (new_bank, guild, username))                
            self.conn.commit()
        else:
            print("User not found in the database.")
                
    def withdraw(self, guild, username, amount):
        self.c.execute('SELECT bank FROM users WHERE guild = ? AND username = ?', (guild, username))
        bank = self.c.fetchone()
        self.c.execute('SELECT balance FROM users WHERE guild = ? AND username = ?', (guild, username))
        balance = self.c.fetchone()
        
        if bank and balance:
            new_bank = bank[0] - amount
            self.c.execute('UPDATE users SET bank = ? WHERE guild = ? AND username = ?', (new_bank, guild, username))
            new_balance = balance[0] + amount
            self.c.execute('UPDATE users SET balance = ? WHERE guild = ? AND username = ?', (new_balance, guild, username))                
            self.conn.commit()
        else:
            print("User not found in the database.")

    def close_connection(self):    
        self.conn.close()
