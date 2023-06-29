import subprocess
import time
from pick import pick

def get_user_details():
    print("Hello, welcome to the snake game!")
    name = input("Please, enter your name: ")
    city = input("Please, enter your city: ")
    return name, city

def run_game_script():
    subprocess.call(['python', 'snake/snake_cli.py'])

def main():
    name, city = get_user_details()
    print(f'\033[1;34mThanks {name} from {city}, let\'s start the game now.\033[0m')
    time.sleep(5)
    run_game_script()

    title = 'Please choose a game: '
    options = ['Tic tac toe', 'Trivia', 'Snake']
    option, index = pick(options, title)
    if index == 0:
        subprocess.call(['python', 'tic_tac_toe/tic_tac_toe.py'])
    elif index == 1:
        subprocess.call(['python', 'trivia/trivia_cli.py'])
    elif index == 2:
        subprocess.call(['python', 'snake/input.py'])

if __name__ == "__main__":
    main()




