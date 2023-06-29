from create_table import Game, session


# Initialize the board the underscore is not being used it's just there as a placeholder
board = [" " for _ in range(9)]
# board looks like this after creation [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] a list of empty strings
''' 
Function to print the board: it runs 3 times when i is 0 it prints the line 0, 1, 2
when i is 1 it prints the line 3,4,5 and when i is 2 it prints the line 6,7,8
 '''
def print_board():
    print("-------------")
    for i in range(3):
        print("|", board[i * 3], "|", board[i * 3 + 1], "|", board[i * 3 + 2], "|")
        print("-------------")

# Function to check if the board is full: the condition returns true if there are no empty strings on the board
def is_board_full():
    return " " not in board

# Function to check if a player has won
def check_winner(symbol):
    # Check rows (the step is set to 3 so i will be 0,3,6) if the symbol for each is the same return true
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == symbol:
            return True

    # Check columns (the index of i will be 1,2,3)
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == symbol:
            return True

    # Check diagonals pretty straightforward
    if board[0] == board[4] == board[8] == symbol or board[2] == board[4] == board[6] == symbol:
        return True

    return False

# Function to make a move
def make_move(player_name, symbol):
    print("It's your turn", player_name + ".")
    while True:
        move = input("Enter your move (1-9): ")
        ''' 
        note: the value stored in move is a str therefore we must convert it to an int for the moves to work.
        the isdigit methods returns true if the value is a str with the value of 0-9
        the if statement checks if the input is a digit 1-9 and whether the board location is an empty string
        if it is it changes it to the current symbol x or o if not it prints invalid move
        (notice although the board has the digits 0-8 we accept inputs 1-9 and subtract 1 each time)

        '''
        if move.isdigit() and 1 <= int(move) <= 9 and board[int(move) - 1] == " ":
            board[int(move) - 1] = symbol
            break
        else:
            print("Invalid move. Try again.")

''' 
Main game loop:
1: prints the board
2: saves both players names to variables
3: assigns player1 to X and player2 to O
4: runs a loop which executes player 1's move and checks if it won, if yes the program returns player 1 as the winner,
if not it checks if the board is full, if yes it returns It's a tie, if there's no tie it executes player 2's move and 
checks if it won, if yes the program returns player 2 as the winner,
if not it checks if the board is full, if yes it returns It's a tie,
if all 4 conditions were didn't cause a break the loop will run again and again until one of the conditions is met.
'''

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print_board()
    # player1_name = input("Enter name for Player 1: ")
    with open("player_name.txt", "r") as file:
        player1_name = file.read()
    print(f'Hello {player1_name}, you are Player 1.')
    player2_name = input("Enter name for Player 2: ")
    player1 = 'X'
    player2 = 'O'
    
    # Retrieve the game for player 1 from the database saves the player to the game1 variable
    game1 = session.query(Game).filter_by(player_name=player1_name).first()
    
    # Create a new game for player 1 if it doesn't exist uses the Game constructor to create a new player
    if game1 is None:
        game1 = Game(player_name=player1_name, player_wins=0, player_losses=0, player_draws=0, player_win_percentage=0)
        session.add(game1)
    
    # Retrieve the game for player 2 from the database saves the player to the game2 variable
    game2 = session.query(Game).filter_by(player_name=player2_name).first()
    
    # Create a new game for player 2 if it doesn't exist uses the Game constructor to create a new player
    if game2 is None:
        game2 = Game(player_name=player2_name, player_wins=0, player_losses=0, player_draws=0, player_win_percentage=0)
        session.add(game2)
    
    while True:
        make_move(player1_name, player1)
        print_board()
        if check_winner(player1):
            print("Player", player1_name, "wins!\nPlayer", player2_name, "loses.")
            # Update player 1's wins and player 2's losses
            game1.player_wins += 1
            game2.player_losses += 1
            game1.player_win_percentage = (game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100
            game2.player_win_percentage = (game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100
            session.commit()
            print(f"Stats for {player1_name}:\n  Wins: {game1.player_wins},\n  Losses: {game1.player_losses},\n  draws: {game1.player_draws},\n  Win percentage: {(game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100:.2f}%.")
            print(f"Stats for {player2_name}:\n  Wins: {game2.player_wins},\n  Losses: {game2.player_losses},\n  draws: {game2.player_draws},\n  Win percentage: {(game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100:.2f}%.")
            break
        elif is_board_full():
            print("It's a tie!")
            # Update both players' draws
            game1.player_draws += 1
            game2.player_draws += 1
            game1.player_win_percentage = (game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100
            game2.player_win_percentage = (game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100
            session.commit()
            print(f"Stats for {player1_name}:\n  Wins: {game1.player_wins},\n  Losses: {game1.player_losses},\n  draws: {game1.player_draws},\n  Win percentage: {(game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100:.2f}%.")
            print(f"Stats for {player2_name}:\n  Wins: {game2.player_wins},\n  Losses: {game2.player_losses},\n  draws: {game2.player_draws},\n  Win percentage: {(game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100:.2f}%.")
            break
        make_move(player2_name, player2)
        print_board()
        if check_winner(player2):
            print("Player", player2_name, "wins!\nPlayer", player1_name, "loses.")
            # Update player 2's wins and player 1's losses
            game2.player_wins += 1
            game1.player_losses += 1
            game1.player_win_percentage = (game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100
            game2.player_win_percentage = (game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100
            session.commit()
            print(f"Stats for {player1_name}:\n  Wins: {game1.player_wins},\n  Losses: {game1.player_losses},\n  draws: {game1.player_draws},\n  Win percentage: {(game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100:.2f}%.")
            print(f"Stats for {player2_name}:\n  Wins: {game2.player_wins},\n  Losses: {game2.player_losses},\n  draws: {game2.player_draws},\n  Win percentage: {(game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100:.2f}%.")
            break
        elif is_board_full():
            print("It's a tie!")
            # Update both players' draws
            game1.player_draws += 1
            game2.player_draws += 1
            game1.player_win_percentage = (game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100
            game2.player_win_percentage = (game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100
            session.commit()
            print(f"Stats for {player1_name}:\n  Wins: {game1.player_wins},\n  Losses: {game1.player_losses},\n  draws: {game1.player_draws},\n  Win percentage: {(game1.player_wins/(game1.player_wins + game1.player_losses + game1.player_draws)) * 100:.2f}%.")
            print(f"Stats for {player2_name}:\n  Wins: {game2.player_wins},\n  Losses: {game2.player_losses},\n  draws: {game2.player_draws},\n  Win percentage: {(game2.player_wins/(game2.player_wins + game2.player_losses + game2.player_draws)) * 100:.2f}%.")
            break

# Start the game
play_game()
import sqlite3

# Connect to the SQLite databases
conn_all_scores = sqlite3.connect('./all_scores.db')
conn_trivia_scores = sqlite3.connect('./trivia/trivia_scores.db')
conn_tictactoe_scores = sqlite3.connect('./games.db')

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

