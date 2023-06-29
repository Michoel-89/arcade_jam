# db_utils.py
import sqlite3

def create_db_and_table():
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()

    # Create table
    c.execute('''
    CREATE TABLE scores
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    score INTEGER NOT NULL);''')

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()
def add_score(name, score):
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()

    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))

    conn.commit()
    conn.close()

def get_scores():
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()

    c.execute("SELECT * FROM scores")
    scores = c.fetchall()

    conn.close()

    return scores
