import os
import random
from string import punctuation

DEBUG = True

BACK_BLUE = u"\u001b[44m"
BACK_RED = u"\u001b[41m"
BACK_YELLOW = u"\u001b[43m"
BACK_GREEN = u"\u001b[42m"
BACK_GREY = u"\u001b[47m"

FRONT_WHITE = u"\u001b[37;1m"
RESET = u"\u001b[0m"

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


# My dictionary is missing loads of words. Use this to add ones you're missing
def add_to_dictionary(word):
    with open("turdle_words.txt", "r") as words_txt:
        clean_words = [line.strip() for line in words_txt.readlines()]
        clean_words.append(word.strip().lower())
    clean_words.sort()

    with open("turdle_words.txt", "w") as new_words_txt:
        new_words_txt.write("\n".join(clean_words))


# Make the word into fun little tiles to print
def tile_word(word, colour):
    global RESET
    tiled_word = ""
    for _letter in word:
        tiled_word += "{} {} {} ".format(colour, _letter, RESET)

    return tiled_word.strip()


# Read the 5-letter English words file
def read_dictionary():
    with open("turdle_words.txt", "r") as words_txt:
        return [line.strip() for line in words_txt.readlines()]


clean_words = read_dictionary()
winning_word = random.choice(clean_words)

guess = False
guess_count = 1
character_limit = 5  # Don't edit this unless you want to update the words list
turns = 6
state = {x: ["", "", 0] for x in range(character_limit)}
history = []
clean_history = []

clear_console()

title = tile_word("TURDLE", BACK_BLUE)
print(u"Welcome to {} !\n".format(title))
print(u"An original game by Nick Rodgers\n")
print(u"You've got 6 attempts at guessing the 5-letter word")
print(u"Type a word to start / Type 'quit' to quit")

def print_history(history):
    for entry in history:
        print("{}\n".format(entry))

    for space in range(turns - len(history)):
        print("{}\n".format(tile_word("-" * character_limit, BACK_GREY)))


while guess is False:
    """
    if guess_count == 1:
        print()
    """

    # Python 3 doesn't have raw_input so patch it to work with 2 and 3
    try:
        input = raw_input
    except NameError:
        pass

    # Get the guess from the user
    guess = input(u" >> ".format(guess_count, turns)).lower()

    # Bail out if the user types 'quit'
    if guess == "quit":
        break

    # Gotta be 5 character long
    if len(guess) != 5:
        clear_console()
        print_history(history)
        print("Word needs to be 5 characters long")
        guess = False
        continue

    # No special characters
    if any([x in guess for x in punctuation]):
        clear_console()
        print_history(history)
        print("You cannot use any special characters")
        guess = False
        continue

    # User has already guessed this
    if guess in clean_history:
        clear_console()
        print_history(history)
        print("This has been guessed before")
        guess = False
        continue

    # Guess has to be in our dictionary
    if guess not in clean_words:
        # If you're in debug mode you can add a word to the dictionary at this point
        if DEBUG:
            add = input("Add to dictionary? (y/n)")
            if add == "y":
                add_to_dictionary(guess)
                clear_console()
                print("Added {}".format(guess))
                clean_words = read_dictionary()
                print_history(history)

        clear_console()
        print_history(history)
        print("Word not in our dictionary")
        guess = False
        continue

    guess_count += 1


    if guess == winning_word:  # You guessed the word!
        clear_console()
        history.append("{}".format(tile_word(guess.upper(), BACK_GREEN)))
        print_history(history)

        print(u"\n\n{}    {}\n".format(tile_word("YOU", BACK_RED), tile_word("WON!", BACK_RED)))

        break
    else:
        # If not, start working out what the user got right and wrong
        for i, letter in enumerate(guess):
            winning_letter = winning_word[i]

            # Right letter, right place
            if winning_letter == letter:
                state[i] = [u"{} {} {}".format(BACK_GREEN, letter.upper(), RESET), letter, 2]
                continue

            # Right letter, wrong place
            if letter in winning_word:
                state[i] = [u"{} {} {}".format(BACK_YELLOW, letter.upper(), RESET), letter, 1]
                continue

            # Wrong letter, wrong place
            state[i] = [u"{} {} {}".format(BACK_RED, letter.upper(), RESET), letter, 0]

        history.append(" ".join([x[0] for x in state.values()]))
        clean_history.append(guess)

    # Too many guesses - you lose
    if guess_count > turns:
        clear_console()
        print_history(history)

        print(u"\n\n{}    {}\n".format(tile_word("YOU", BACK_RED), tile_word("LOSE", BACK_RED)))
        print(u"It was {}".format(tile_word(winning_word.upper(), BACK_BLUE)))
        break

    clear_console()

    print_history(history)

    guess = False

input("\n\nPress Enter to exit...")
