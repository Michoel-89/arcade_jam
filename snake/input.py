# input.py
def get_user_details():
    print("Hello, welcome to our game!")
    name = input("Please, enter your name: ")
    city = input("Please, enter your city: ")
    return name, city

def run_game_script():
    import os
    os.system('python snake_cli.py')

def main():
    name, city = get_user_details()
    print(f"Thanks {name} from {city}, let's start the game now.")
    run_game_script()

    from db_utils import add_score, get_scores

# Add a score
add_score()

# Get all scores
scores = get_scores()
for score in scores:
    print(score)


if __name__ == "__main__":
    main()
