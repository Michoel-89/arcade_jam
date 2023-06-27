import sqlite3
import random
from trivia_questions import questions

# Connect to the SQLite database
conn = sqlite3.connect('trivia_scores.db')
cursor = conn.cursor()

# Create a table to store trivia scores if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS trivia_scores
             (username text, trivia_score int)''')

def print_highest_score(player_name):
    # Query the database for the highest score of the specified player
    cursor.execute("SELECT MAX(trivia_score) FROM trivia_scores WHERE username=?", (player_name,))
    highest_score = cursor.fetchone()[0]

    if highest_score is not None:
        print(f"Highest score for {player_name}: {highest_score}")
    else:
        print("No past scores found for the player.")

# Prompt the player to enter their name
player_name = input("Enter your username: ")

# Call the function to print the highest score for the player
print_highest_score(player_name)

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

# Store the user's score in the database
cursor.execute("INSERT INTO trivia_scores VALUES (?, ?)", (player_name, score))
conn.commit()

# Print the final score
print(f"Quiz complete! Your score is: {score}/{total_num_questions}")

# def delete_all_scores():
#     # Execute an SQL statement to delete all records from the "trivia_scores" table
#     cursor.execute("DELETE FROM trivia_scores")
#     conn.commit()
#     print("All scores have been deleted.")

# # Call the function to delete all scores
# delete_all_scores()

# # Execute the SQL statement to delete an old table called "scores"
# cursor.execute("DROP TABLE IF EXISTS scores")

# # Commit the changes of the table
# conn.commit()

# Close the database connection
conn.close()