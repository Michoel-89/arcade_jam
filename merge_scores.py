import sqlite3

# Connect to the SQLite databases
conn_all_scores = sqlite3.connect('all_scores.db')
conn_trivia_scores = sqlite3.connect('trivia/trivia_scores.db')
conn_tictactoe_scores = sqlite3.connect('tictactoe/tictactoe_scores.db')

cursor_all_scores = conn_all_scores.cursor()
cursor_trivia_scores = conn_trivia_scores.cursor()
cursor_tictactoe_scores = conn_tictactoe_scores.cursor()

# Execute the SQL statement to delete old table
cursor_all_scores.execute("DROP TABLE IF EXISTS all_scores")

# Commit the changes of deleting the table
conn_all_scores.commit()

# Create a new table to store the all scores
create_table_query = '''
CREATE TABLE all_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    trivia_score INTEGER,
    tictactoe_score INTEGER
)
'''
cursor_all_scores.execute(create_table_query)

# Select the scores from the trivia_scores table
select_trivia_scores_query = '''
SELECT username, trivia_score FROM trivia_scores
'''
trivia_scores = cursor_trivia_scores.execute(select_trivia_scores_query).fetchall()

# Insert the scores from the trivia_scores table into the all_scores table
# If the same username exists, the DO UPDATE clause updates the trivia_score value instead of inserting a new row
merge_trivia_scores_query = '''
INSERT INTO all_scores (username, trivia_score) VALUES (?, ?)
ON CONFLICT (username) DO UPDATE SET trivia_score = excluded.trivia_score
'''
cursor_all_scores.executemany(merge_trivia_scores_query, trivia_scores)

# Select the scores from the tictactoe_scores table
select_tictactoe_scores_query = '''
SELECT username, tictactoe_score FROM tictactoe_scores
'''
tictactoe_scores = cursor_tictactoe_scores.execute(select_tictactoe_scores_query).fetchall()

# Insert or update the scores from the tictactoe_scores table into the all_scores table
# If the same username exists, the DO UPDATE clause updates the tictactoe_score value instead of inserting a new row
merge_tictactoe_scores_query = '''
INSERT INTO all_scores (username, tictactoe_score) VALUES (?, ?)
ON CONFLICT (username) DO UPDATE SET tictactoe_score = excluded.tictactoe_score
'''
cursor_all_scores.executemany(merge_tictactoe_scores_query, tictactoe_scores)

# If the username exists, show the highest scores for each game
def print_highest_score(player_name):
    # Query the database for the highest scores of the specified player
    cursor_all_scores.execute("SELECT MAX(trivia_score), MAX(tictactoe_score) FROM all_scores WHERE username=?", (player_name,))
    highest_scores = cursor_all_scores.fetchone()
    highest_trivia_score = highest_scores[0]
    highest_tictactoe_score = highest_scores[1]

    if highest_trivia_score is not None:
        print(f"Highest trivia score for {player_name}: {highest_trivia_score}")
    else:
        print("No past trivia scores found for the player.")

    if highest_tictactoe_score is not None:
        print(f"Highest tictactoe score for {player_name}: {highest_tictactoe_score}")
    else:
        print("No past tictactoe scores found for the player.")

# Prompt the player to enter their name
player_name = input("Enter your username: ")

# Call the function to print the highest score for the player
print_highest_score(player_name)

print()  # Print a blank line for separation

# Commit the changes and close the connections
conn_all_scores.commit()
conn_all_scores.close()
conn_trivia_scores.close()
conn_tictactoe_scores.close()