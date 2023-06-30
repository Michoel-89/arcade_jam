import subprocess
import time
import sqlite3

subprocess.call(['python', './snake_ascii.py'])

def create_db():
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS player_score
        (name TEXT, score INTEGER);
    ''')

    conn.commit()
    conn.close()

def get_user_details():
    print("Hello, welcome to the snake game!")
    name = input("Whats was your name again: ")
    city = input("Please, enter your city: ")
    return name, city

def store_name(name):
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()

    c.execute("SELECT score FROM player_score WHERE name = ?", (name,))
    result = c.fetchone()

    if result is None:
        c.execute("INSERT INTO player_score (name, score) VALUES (?, ?)", (name, 0))

    conn.commit()
    conn.close()

def run_game_script(name):
    subprocess.call(['python', 'snake/snake_cli.py', name])

def merge_snake_scores():
    # Connect to the SQLite databases
    conn_all_scores = sqlite3.connect('all_scores.db')
    conn_snake_scores = sqlite3.connect('snake_game.db')
    cursor_all_scores = conn_all_scores.cursor()
    cursor_snake_scores = conn_snake_scores.cursor()

    # Execute the SQL statement to delete old table
    cursor_all_scores.execute("DROP TABLE IF EXISTS all_scores")

    # Commit the changes of deleting the table
    conn_all_scores.commit()

    # Create a new table to store all scores
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS all_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE COLLATE NOCASE,
        trivia_score INTEGER,
        tictactoe_score DECIMAL,
        snake_score INTEGER
    )
    '''
    cursor_all_scores.execute(create_table_query)

    # Select the scores from the snake_scores table
    select_snake_scores_query = '''
    SELECT name, score FROM player_score
    '''
    snake_scores = cursor_snake_scores.execute(select_snake_scores_query).fetchall()

    # Insert or update the scores from the snake_scores table into the all_scores table
    # If the same username exists, the DO UPDATE clause updates the snake_score value instead of inserting a new row
    merge_snake_scores_query = '''
    INSERT INTO all_scores (username, snake_score) VALUES (?, ?)
    ON CONFLICT (username) DO UPDATE SET snake_score = excluded.snake_score
    '''
    cursor_all_scores.executemany(merge_snake_scores_query, snake_scores)

    

    # Commit the changes
    conn_all_scores.commit()

    # Close the connections
    conn_all_scores.close()
    conn_snake_scores.close()

def main():
    name, city = get_user_details()
    store_name(name)
    print(f'\033[1;34mThanks {name} from {city}, let\'s start the game now.\033[0m')
    time.sleep(5)
    run_game_script(name)
    merge_snake_scores()

if __name__ == "__main__":
    create_db()
    main()

print()  # Add line break
print()  # Add line break
def continue_playing():
    print('Press "enter" to return to main menu or "q" to quit')
    answer = input("Do you want to keep playing? ")
    if(answer == ''):
        print(f'Returning to the main menu...')
        time.sleep(3)  # Wait for 3 seconds
        subprocess.call(['python', './main_cli.py'])
    if(answer == 'q'):
        print('Exiting Arcade JAM...')
        quit()
continue_playing()

# import subprocess
# import time
# import sqlite3

# def create_db():
#     conn = sqlite3.connect('snake_game.db')
#     c = conn.cursor()

#     c.execute('''
#         CREATE TABLE IF NOT EXISTS player_score
#         (name TEXT, score INTEGER);
#     ''')

#     conn.commit()
#     conn.close()

# def get_user_details():
#     print("Hello, welcome to the snake game!")
#     name = input("Whats was your name again: ")
#     city = input("Please, enter your city: ")
#     return name, city

# def store_name(name):
#     conn = sqlite3.connect('snake_game.db')
#     c = conn.cursor()

#     c.execute("SELECT score FROM player_score WHERE name = ?", (name,))
#     result = c.fetchone()

#     if result is None:
#         c.execute("INSERT INTO player_score (name, score) VALUES (?, ?)", (name, 0))

#     conn.commit()
#     conn.close()

# def run_game_script(name):
#     subprocess.call(['python', 'snake/snake_cli.py', name])

# def merge_snake_scores():
#     # Connect to the SQLite databases
#     conn_all_scores = sqlite3.connect('all_scores.db')
#     conn_snake_scores = sqlite3.connect('snake_game.db')
#     conn_trivia_scores = sqlite3.connect('trivia_scores.db')
#     conn_tictactoe_scores = sqlite3.connect('tictactoe_scores.db')

#     cursor_all_scores = conn_all_scores.cursor()
#     cursor_snake_scores = conn_snake_scores.cursor()
#     cursor_trivia_scores = conn_trivia_scores.cursor()
#     cursor_tictactoe_scores = conn_tictactoe_scores.cursor()

#     # Execute the SQL statement to delete old table
#     cursor_all_scores.execute("DROP TABLE IF EXISTS all_scores")

#     # Commit the changes of deleting the table
#     conn_all_scores.commit()

#     # Create a new table to store all scores
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS all_scores (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE COLLATE NOCASE,
#         trivia_score INTEGER,
#         tictactoe_score DECIMAL,
#         snake_score INTEGER
#     )
#     '''
#     cursor_all_scores.execute(create_table_query)

#     # Select the scores from the snake_scores table
#     select_snake_scores_query = '''
#     SELECT name, score FROM player_score
#     '''
#     snake_scores = cursor_snake_scores.execute(select_snake_scores_query).fetchall()

#     # Insert or update the scores from the snake_scores table into the all_scores table
#     # If the same username exists, the DO UPDATE clause updates the snake_score value instead of inserting a new row
#     merge_snake_scores_query = '''
#     INSERT INTO all_scores (username, snake_score) VALUES (?, ?)
#     ON CONFLICT (username) DO UPDATE SET snake_score = excluded.snake_score
#     '''
#     cursor_all_scores.executemany(merge_snake_scores_query, snake_scores)

#     # Select the scores from the trivia_scores table
#     select_trivia_scores_query = '''
#     SELECT username, trivia_score FROM trivia_scores
#     '''
#     trivia_scores = cursor_trivia_scores.execute(select_trivia_scores_query).fetchall()

#     # Insert the scores from the trivia_scores table into the all_scores table
#     # If the same username exists, the DO UPDATE clause updates the trivia_score value instead of inserting a new row
#     merge_trivia_scores_query = '''
#     INSERT INTO all_scores (username, trivia_score) VALUES (?, ?)
#     ON CONFLICT (username) DO UPDATE SET trivia_score = excluded.trivia_score
#     '''
#     cursor_all_scores.executemany(merge_trivia_scores_query, trivia_scores)

#     # Select the scores from the tictactoe_scores table
#     select_tictactoe_scores_query = '''
#     SELECT player_name, player_win_percentage FROM tic_tac_toe
#     '''
#     tictactoe_scores = cursor_tictactoe_scores.execute(select_tictactoe_scores_query).fetchall()

#     # Insert or update the scores from the tictactoe_scores table into the all_scores table
#     # If the same username exists, the DO UPDATE clause updates the tictactoe_score value instead of inserting a new row
#     merge_tictactoe_scores_query = '''
#     INSERT INTO all_scores (username, tictactoe_score) VALUES (?, ?)
#     ON CONFLICT (username) DO UPDATE SET tictactoe_score = excluded.tictactoe_score
#     '''
#     cursor_all_scores.executemany(merge_tictactoe_scores_query, tictactoe_scores)

#     # Commit the changes
#     conn_all_scores.commit()

#     # Close the connections
#     conn_all_scores.close()
#     conn_snake_scores.close()
#     conn_trivia_scores.close()
#     conn_tictactoe_scores.close()

# def main():
#     create_db()
#     name, city = get_user_details()
#     store_name(name)
#     print(f'\033[1;34mThanks {name} from {city}, let\'s start the game now.\033[0m')
#     time.sleep(5)
#     run_game_script(name)
#     merge_snake_scores()
#     subprocess.call(['python', 'main_cli.py'])

# if __name__ == "__main__":
#     main()
