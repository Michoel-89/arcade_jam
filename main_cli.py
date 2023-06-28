import sqlite3

# Connect to the SQLite databases
conn_all_scores = sqlite3.connect('all_scores.db')
conn_trivia_scores = sqlite3.connect('trivia/trivia_scores.db')
conn_tictactoe_scores = sqlite3.connect('games.db')

# Set the connection to use case-insensitive collation
cursor_all_scores = conn_all_scores.cursor()
cursor_trivia_scores = conn_trivia_scores.cursor()
cursor_tictactoe_scores = conn_tictactoe_scores.cursor()

# If the username exists, show the highest scores for each game
def print_highest_score(player_name):
    # Query the database for the highest scores of the specified player (case-insensitive)
    cursor_all_scores.execute("SELECT MAX(trivia_score), MAX(tictactoe_score) FROM all_scores WHERE username COLLATE NOCASE=?", (player_name,))
    highest_scores = cursor_all_scores.fetchone()
    highest_trivia_score = highest_scores[0]
    highest_tictactoe_score = highest_scores[1]

    if highest_trivia_score is not None:
        print(f"Highest trivia score for {player_name}: {highest_trivia_score}/5")
    else:
        print("No past trivia scores found for the player.")

    if highest_tictactoe_score is not None:
        print(f"Tic tac toe win percentage for {player_name}: {highest_tictactoe_score:.2f}%")
    else:
        print("No past tictactoe scores found for the player.")

# Prompt the player to enter their name
player_name = input("Enter your username: ")

# Same player_name to txt file for use in other programs
with open("player_name.txt", "w") as file:
    file.write(player_name)          

# Call the function to print the highest score for the player
print_highest_score(player_name)

print()  # Print a blank line for separation




# import click
from pick import pick
import subprocess
title = 'Please choose a game: '
options = ['Tic tac toe', 'Trivia', 'Snake']
# the pick function returns a tuple with 2 elements the option and the index, 
# here we store those 2 elements in variables
option, index = pick(options, title)
if index == 0:  # Tic tac toe option
    subprocess.call(['python', 'tic_tac_toe/tic_tac_toe.py'])  # Replace 'tic_tac_toe.py' with the actual filename

elif index == 1:  # Trivia option
    subprocess.call(['python', 'trivia/trivia_cli.py'])
elif index == 2:  # Trivia option
    subprocess.call(['python', 'snake/snake_cli.py'])
# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Enter your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo(f"Hello {name}!")


# if __name__ == '__main__':
#     hello()


# Close the connections
conn_all_scores.close()
conn_trivia_scores.close()
conn_tictactoe_scores.close()