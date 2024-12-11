def display_state(s, *, clear=False):
    """
    Display the state s

    If 'clear' is set to True, erase previous displayed states
   """
    def colored(r, g, b, text):
        rb, gb, bb = (r+2)/3, (g+2)/3, (b+2)/3
        rd, gd, bd = (r)/1.5, (g)/1.5, (b)/1.5
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

    def inverse(text):
        rb, gb, bb = .2, .2, .2
        rd, gd, bd = .8, .8, .8
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

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
    numrows = max(len(stack) for stack in s['stacks'])
    for row in range(numrows-1, -1, -1):
        for i in range(n_columns):
            num_in_col = len(s['stacks'][i])
            if num_in_col > row:
                val = s['stacks'][i][row]
                if num_in_col == row+1 and s['blocked'][i]:
                    print(inverse(' '+str(val)+' '), end=' ')
                else:
                    if s['complete'][i]:
                        print(colored(*colours[val-1], '   '), end=' ')
                    else:
                        print(colored(*colours[val-1], ' '+str(val)+' '), end=' ')
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
        'stacks': stacks
    }

    return state

# Q2
def parse_move(input_str):
    indexing = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}

    if input_str in ['R', 'r']:
        return 0
    if input_str in ['U', 'u']:
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

# Q3
def validate_move(state, move):
    if isinstance(move, int):
        return True  # Handle special cases like restart or undo

    initial_index, final_index, num_cards = move

    # Check if the move is valid based on stack rules
    if num_cards > len(state['stacks'][initial_index]):
        return False

    if len(state['stacks'][final_index]) > 0:
        if state['stacks'][initial_index][-1] + 1 != state['stacks'][final_index][-1]:
            return False

    return True

# Q4
def apply_move(state, move):
    initial_index, final_index, num_cards = move

    # Move cards
    moving_cards = state['stacks'][initial_index][-num_cards:]
    state['stacks'][initial_index] = state['stacks'][initial_index][:-num_cards]
    state['stacks'][final_index].extend(moving_cards)

    # Update blocked status
    for i in range(6):
        if len(state['stacks'][i]) == 0:
            state['blocked'][i] = False
        else:
            if len(state['stacks'][i]) > 1:
                state['blocked'][i] = (state['stacks'][i][-1] != state['stacks'][i][-2] + 1)

    # Update complete status
    for i in range(6):
        state['complete'][i] = (state['stacks'][i] == [9, 8, 7, 6, 5, 4, 3, 2, 1])

# Q5
def game_won(state):
    return state['complete'].count(True) == 4

# Main Game Function
def play_game():
    board = initial_state()
    history = [board.copy()]  # Keep track of history for undo
    print("New game started!")

    try:
        while True:
            display_state(board, clear=False)
            move = ()

            while True:
                try:
                    move_str = input()
                    move = parse_move(move_str)

                    if move == 0:  # Restart game
                        print("Restarting the game...")
                        board = initial_state()
                        history = [board.copy()]
                        break

                    if move == -1:  # Undo move
                        if len(history) > 1:
                            history.pop()
                            board = history[-1].copy()
                            print("Undo successful.")
                        else:
                            print("Cannot undo: No previous move available.")
                        continue

                    if validate_move(board, move):
                        break
                    else:
                        print("Invalid move: Move does not meet the game rules. Try again.")

                except ValueError as e:
                    print(f"Error: {e}. Please try again.")

            if move == 0:
                continue  # Skip applying a move and restart

            history.append(board.copy())
            apply_move(board, move)

            if game_won(board):
                display_state(board, clear=True)
                print("Congratulations! You won the game!")
                break

    except KeyboardInterrupt:
        print("\nGame interrupted. Exiting...")
        return

play_game()
