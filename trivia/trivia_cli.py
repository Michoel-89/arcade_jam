import sqlite3
import random
from trivia_questions import questions

# Connect to the SQLite database
conn_trivia_scores = sqlite3.connect('trivia/trivia_scores.db')
cursor_trivia_scores = conn_trivia_scores.cursor()

# # Delete old table
# cursor.execute("DROP TABLE IF EXISTS trivia_scores")

# # Commit the changes of the table
# conn_trivia_scores.commit()

# Create a new table to store the all scores
create_table_query = '''
CREATE TABLE IF NOT EXISTS trivia_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE COLLATE NOCASE,
    trivia_score INTEGER
)
'''
cursor_trivia_scores.execute(create_table_query)

# def print_highest_score(player_name):
#     # Query the database for the highest score of the specified player
#     cursor.execute("SELECT MAX(trivia_score) FROM trivia_scores WHERE username COLLATE NOCASE = ?", (player_name,))
#     highest_score = cursor.fetchone()[0]

#     if highest_score is not None:
#         print(f"Highest score for {player_name}: {highest_score}")
#     else:
#         print("No past scores found for the player.")

# # Prompt the player to enter their name
# player_name = input("Enter your username: ")

# Retrieve player_name entered in main_cli.py
with open("player_name.txt", "r") as file:
    player_name = file.read()

# # Call the function to print the highest score for the player
# print_highest_score(player_name)

print()  # Print a blank line for separation

# Prompt the player to select a category
category_num = 1
print('Choose from the following categories:')
for category in questions['trivia categories']:
    print(f"{category_num}. {questions['trivia categories'][category_num - 1]}")
    category_num += 1
category_selection = input("Select a category (1-4): ")

# Show questions from the selected category
while category_selection not in [1, 2, 3, 4]:
    if category_selection.isdigit() and 1 <= int(category_selection) <= 4:
        category_selection = int(category_selection)
        selected_category = questions['trivia categories'][category_selection-1]
    else:
        print("Invalid input. Enter a number 1-4.")
        category_selection = input("Select a category (1-4): ")

print()  # Print a blank line for separation

# Shuffle the questions
random.shuffle(questions[selected_category])

# Initialize variables to track score and question number
score = 0
question_num = 1

# Iterate through each question, limited to 5 questions
total_num_questions = 5
for question in questions[selected_category][:total_num_questions]:
    print(f"Question {question_num}: {question['question']}")

    # Shuffle the answer options
    random.shuffle(question['options'])
    
    # Print the answer options
    for i, option in enumerate(question['options']):
        print(f"{i+1}. {option}")
    
    # Get the player's answer
    player_answer = input("Enter your answer (1-4): ")
    
    # Validate the answer
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    NC='\033[0m' # No Color

    while player_answer not in [1, 2, 3, 4]:
        if player_answer.isdigit() and 1 <= int(player_answer) <= 4:
            player_answer = int(player_answer)
            if question['options'][player_answer-1] == question['answer']:
                print(f"{GREEN}Correct!{NC}")
                score += 1
            else:
                print(f"{RED}Wrong!{NC} The correct answer is: {question['answer']}")
        else:
            print("Invalid input. Enter a number 1-4.")
            player_answer = input("Enter your answer (1-4): ")
            
    print()  # Print a blank line for separation
    
    # Increment the question number
    question_num += 1

# Check if the username exists in the table (case-insensitive)
check_username_query = "SELECT * FROM trivia_scores WHERE username COLLATE NOCASE = ?"
cursor_trivia_scores.execute(check_username_query, (player_name,))
existing_user = cursor_trivia_scores.fetchone()

if existing_user:
    # Username already exists, check if the new score is higher
    if score > existing_user[2]:
        # Update the score for the existing username
        update_score_query = "UPDATE trivia_scores SET trivia_score = ? WHERE username COLLATE NOCASE = ?"
        cursor_trivia_scores.execute(update_score_query, (score, player_name))
        conn_trivia_scores.commit()
else:
    # Username doesn't exist, insert a new row
    insert_score_query = "INSERT INTO trivia_scores (username, trivia_score) VALUES (?, ?)"
    cursor_trivia_scores.execute(insert_score_query, (player_name, score))
    conn_trivia_scores.commit()

# Print the final score
print(f"Quiz complete! Your score is: {score}/{total_num_questions}")
import sqlite3


# Connect to the SQLite databases
conn_all_scores = sqlite3.connect('all_scores.db')
conn_tictactoe_scores = sqlite3.connect('games.db')

# Set the connection to use case-insensitive collation
cursor_all_scores = conn_all_scores.cursor()
cursor_trivia_scores = conn_trivia_scores.cursor()
cursor_tictactoe_scores = conn_tictactoe_scores.cursor()

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
    tictactoe_score DECIMAL
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
SELECT player_name, player_win_percentage FROM tic_tac_toe
'''
tictactoe_scores = cursor_tictactoe_scores.execute(select_tictactoe_scores_query).fetchall()

# Insert or update the scores from the tictactoe_scores table into the all_scores table
# If the same username exists, the DO UPDATE clause updates the tictactoe_score value instead of inserting a new row
merge_tictactoe_scores_query = '''
INSERT INTO all_scores (username, tictactoe_score) VALUES (?, ?)
ON CONFLICT (username) DO UPDATE SET tictactoe_score = excluded.tictactoe_score
'''
cursor_all_scores.executemany(merge_tictactoe_scores_query, tictactoe_scores)

# Commit the changes
conn_all_scores.commit()

# Close the connections
conn_all_scores.close()
conn_trivia_scores.close()
conn_tictactoe_scores.close()

# Return to main menu
import time
import subprocess

print()  # Add line break
print()  # Add line break
print(f'Returning to the main menu...')

time.sleep(5)  # Wait for 5 seconds

subprocess.call(['python', './main_cli.py'])