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