#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 15:15:35 2024

@author: catherinelin
"""

"""
MATH20621 - Coursework 3
Student name: Yule Lin
Student id:   11374311
Student mail: yule.lin@student.manchester.ac.uk
"""


def display_state(s, *, clear=False):
    """
    Display the state s

    If 'clear' is set to True, erase previous displayed states
   """

    def colored(r, g, b, text):
        rb, gb, bb = (r + 2) / 3, (g + 2) / 3, (b + 2) / 3
        rd, gd, bd = (r) / 1.5, (g) / 1.5, (b) / 1.5
        return f"\033[38;2;{int(rb * 255)};{int(gb * 255)};{int(bb * 255)}m\033[48;2;{int(rd * 255)};{int(gd * 255)};{int(bd * 255)}m{text}\033[0m"

    def inverse(text):
        rb, gb, bb = .2, .2, .2
        rd, gd, bd = .8, .8, .8
        return f"\033[38;2;{int(rb * 255)};{int(gb * 255)};{int(bb * 255)}m\033[48;2;{int(rd * 255)};{int(gd * 255)};{int(bd * 255)}m{text}\033[0m"

    colours = [(1.0, 0.349, 0.369),
               (1.0, 0.573, 0.298),
               (1.0, 0.792, 0.227),
               (0.773, 0.792, 0.188),
               (0.541, 0.788, 0.149),
               (0.322, 0.651, 0.459),
               (0.098, 0.509, 0.769),
               (0.259, 0.404, 0.675),
               (0.416, 0.298, 0.576)]

    n_columns = len(s['stacks'])
    if clear:
        print(chr(27) + "[2J")

    print('\n')
    row = 0
    numrows = max(len(stack) for stack in s['stacks'])
    for row in range(numrows - 1, -1, -1):
        for i in range(n_columns):
            num_in_col = len(s['stacks'][i])
            if num_in_col > row:
                val = s['stacks'][i][row]
                if num_in_col == row + 1 and s['blocked'][i]:
                    print(inverse(' ' + str(val) + ' '), end=' ')
                else:
                    if s['complete'][i]:
                        print(colored(*colours[val - 1], '   '), end=' ')
                    else:
                        print(colored(*colours[val - 1], ' ' + str(val) + ' '), end=' ')
            else:
                print('    ', end='')
        print()
    print(' A   B   C   D   E   F')


# Q1
def initial_state():
    import random

    cards = [i for i in range(1, 10)]
    repeat_list = cards * 4

    random.shuffle(repeat_list)

    stacks = [repeat_list[i::6] for i in range(6)]

    state = {
        'blocked': [False] * 6,
        'complete': [False] * 6,
        'stacks': stacks}

    return state


# Q2
def parse_move(input_str):
    indexing = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}

    if input_str == 'R' or input_str == 'r':
        return 0
    if input_str == 'U' or input_str == 'u':
        return -1

    if len(input_str) < 2:
        raise ValueError("Invalid input: Input must have at least two characters")

    if input_str[0] not in indexing or input_str[1] not in indexing:
        raise ValueError("Invalid input: Characters not included in index")

    if len(input_str) > 3:
        raise ValueError("Invalid input: Input can't have more than 3 characters")

    initial_index = indexing[input_str[0]]
    final_index = indexing[input_str[1]]

    if len(input_str) == 3:
        try:
            num_cards = int(input_str[2:])
            if num_cards <= 0:
                raise ValueError("Invalid input: Number of cards must be a positive integer.")
        except ValueError:
            raise ValueError("Invalid input: Number of cards must be a valid integer.")
    else:
        num_cards = 1

    return initial_index, final_index, num_cards

    if len(input_str) == 3:
        num_cards = int(input_str[2])
        return (initial_index, final_index, num_cards)
    else:
        num_cards = 1
        return (initial_index, final_index, num_cards)


# Q3
def validate_move(state, move):
    initial_index, final_index, num_cards = move

    #completed
    if state['complete'][initial_index] == True or state['complete'][final_index] == True:
        return False

    #general validation

    if num_cards > 9 or num_cards <= 0 or num_cards > len(state['stacks'][initial_index]):
        return False

    #moving one card
    if num_cards == 1 or num_cards is None:
        if state['blocked'][initial_index] == True:
            if len(state['stacks'][final_index]) == 0:
                return True

            if state['blocked'][final_index] == False:
                if state['stacks'][final_index][-1] == state['stacks'][initial_index][-1] + 1:
                    return True
                else:
                    return False

            else:
                return False
        if state['blocked'][initial_index] == False:
            if state['blocked'][final_index] == False:
                return True
            if state['blocked'][final_index] == True:
                return False
            if len(state['stacks'][final_index]) == 0:
                return True




    #moving multiple cards
    else:
        sequence = state['stacks'][initial_index][-num_cards:]
        for i in range(len(sequence)):
            if sequence[i] != sequence[i + 1] + 1:
                return False
            if sequence[i] == sequence[i + 1] + 1:
                if state['blocked'][final_index] == True:
                    return False
                if len(state['stacks'][final_index]) == 0:
                    return True

                if state['stacks'][final_index][-1] != sequence[0] + 1:
                    return False
                else:
                    return True
            if state['stacks'][final_index][-1] == sequence[0] + 1:
                return True

    #blocked
    if state['blocked'][final_index] == True:
        return False


# Q4
def apply_move(state, move):
    initial_index, final_index, num_cards = move

    moving_cards = state['stacks'][initial_index][-num_cards:]
    state['stacks'][initial_index] = state['stacks'][initial_index][:-num_cards]
    state['stacks'][final_index] = state['stacks'][final_index] + moving_cards

    if num_cards == 1:

        if len(state['stacks'][final_index]) == 1:  # If the final stack now contains only one card
            if state['blocked'][initial_index] == True:  # If the initial stack was blocked, unblock it
                state['blocked'][initial_index] = False
                state['stacks'][final_index] = moving_cards
                state['stacks'][initial_index] = state['stacks'][initial_index]


        else:

            if state['stacks'][final_index][-num_cards - 1] == 1 + moving_cards[
                -num_cards]:  # If the top card in the final stack matches the game sequence rule
                if state['blocked'][initial_index] == True:
                    state['blocked'][initial_index] = False  # Unblock the initial stack if it was blocked
                elif state['blocked'][initial_index] == False:
                    state['blocked'][initial_index] = False
                elif state['blocked'][final_index] == False:
                    state['blocked'][final_index] = False

        if len(state['stacks'][
                   final_index]) >= num_cards + 1:  # If the final stack does not follow the game sequence rule
            if state['stacks'][final_index][-num_cards - 1] != 1 + moving_cards[-num_cards]:
                # Make the final stack as blocked if both stacks were initially unblocked
                if state['blocked'][final_index] == False and state['blocked'][initial_index] == False:
                    state['blocked'][final_index] = True

    # Handle scenarios for moving multiple cards
    if num_cards > 1 and num_cards <= len(state['stacks'][initial_index]):
        # Ensure the move follows the game sequence rule for stacked cards
        if state['stacks'][initial_index][-num_cards] == state['stacks'][final_index][-1] - 1:
            state['stacks'][initial_index] = state['stacks'][initial_index]
            state['stacks'][final_index] = state['stacks'][final_index]

    if state['stacks'][final_index] == [9, 8, 7, 6, 5, 4, 3, 2, 1]:
        state['complete'][final_index] = True


# Q5
def game_won(state):
    if state['complete'].count(True) == 4:
        return True
    else:
        return False


# For questions 1-5, DO NOT edit the play_game function.
# For the tasks in questions 1-5 initial_state, parse_move,
# validate_move, apply_move, and game_won must work with the
# the unmodified play_game function.

# For questions 6, 7 and 8, you should modify the play_game
# function

def play_game():
    # When we start the game,
    board = initial_state()
    state_history = []  # History stack to save game states

    try:
        while True:

            # Display the current game state
            display_state(board, clear=False)

            while True:
                try:
                    # Read input from the user.
                    # (Do not alter this line, even in questions 6, 7, 8.)
                    move_str = input()

                    # Handle Undo by popping out values from state_history
                    if move_str.lower() == 'u':
                        if state_history:
                            board = state_history.pop()
                            display_state(board, clear=False)
                        else:
                            print("no moves to undo")
                        continue

                    # Parse the text typed by the user and convert it to a move
                    move = parse_move(move_str)

                    # Handle Restart
                    if move == 0:
                        play_game()

                    # Validate the move
                    if validate_move(board, move):
                        # If the move is valid then save the current state before applying the move
                        state_history.append({
                            'blocked': board['blocked'][:],
                            'complete': board['complete'][:],
                            'stacks': [stack[:] for stack in board['stacks']]
                        })
                        break
                    else:
                        print("Invalid move: Move does not meet the game rules. Try again.")

                except ValueError as e:
                    print(f"Error: {e}. Please try again.")

            # Apply the valid move
            apply_move(board, move)

            # If we've won, end the game
            if game_won(board):
                display_state(board, clear=True)
                print("Congratulations! You won the game!")
                break

    except KeyboardInterrupt:  # If the user presses Ctrl-C, quit
        print("\nGame interrupted. Exiting...")
        return


play_game()
