import os




############################################  
#
#     /*      BOARD FUNCTIONS     */
#
############################################

# Reset the board and the author
def reset_everything() -> None:
  create_board()
  register_author('')


# Create a new board with 6 rows and 7 columns
def create_board() -> None:
  board = [['0' for _ in range(7)] for _ in range(6)]
  
  with open('board.txt', 'w') as f:
    for row in board:
      f.write(' '.join(row) + '\n')


# Read the board from the corresponding file
def read_board() -> list[str]:
  with open('board.txt', 'r') as f:
    board = f.readlines()
  
  if not board:
    create_board()
    with open('board.txt', 'r') as f:
      board = f.readlines()
  
  return board


# Write the board to the corresponding file
def write_board(board: list[list[str]]) -> None:
  with open('board.txt', 'w') as f:
    for row in board:
      f.write(' '.join(row) + '\n')


# Convert the board to a list of lists
def convert_board_to_list(board: list[str]) -> list[list[str]]:
  new_board = []
  for row in board:
    row = row.strip('\n')
    new_board.append(row.split(' '))
  return new_board


# If the board is full return True
def check_full_board(board: list[list[str]]) -> bool:
  for row in board:
    if '0' in row:
      return False
  return True


def check_winner(board: list[list[str]], row: int, col: int) -> bool:
  # Reverse the board to play from the bottom and get the token
  board = board[::-1]
  token = board[row][col]

  # In any direction (horizontal, vertical, diagonal) check if there are 4 tokens of the same color
  for r in range(row - 1, row + 2):
    for c in range(col - 1, col + 2):
      if r == row and c == col: # Skip the current position
        continue

      if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]): # Skip if out of bounds
        continue

      if board[r][c] == token:
        for i in range(1, 4):
          new_row = row + i * (r - row)
          new_col = col + i * (c - col)
          try:
            if board[new_row][new_col] != token:
              break
            if i == 3:
              return True
          except:
            break
  
  return False

############################################  
#
#     /*      BOOLEAN FUNCTIONS     */
#
############################################

# Check if the author is the same as the last movement. NOT IN USE
def is_author_same_as_last_movement(author: str) -> bool:
  with open('last_author.txt', 'r') as f:
    last_author = f.read()
  
  return author == last_author


# Check if it is the red turn
def is_red_turn(board: list[list[str]]) -> bool:
  count_red = 0
  count_blue = 0
  for row in board:
    print(row)
    count_red += row.count('1')
    count_blue += row.count('2')

  
  if count_red == count_blue:
    return True

  return False



############################################  
#
#     /*      GAME FUNCTION     */
#
############################################

# Game logic
def play_game(board: list[list[str]], movement: str, red_turn: bool) -> list[list[str]]:
  token = '1' if red_turn else '2'  # Determines the token to play

  flag = False  # Check if the movement is valid

  new_board = board[::-1]   # Reverse the board to play from the bottom

  for rowIndex, row in enumerate(new_board):
    if row[int(movement)] == '0':
      row[int(movement)] = token
      flag = True

      # Check if there is a winner
      if check_winner(board, rowIndex, int(movement)):
        raise Exception('Red Wins') if token == '1' else Exception('Blue Wins')

      break

  # If the movement is invalid, raise an exception
  if not flag:
    if check_full_board(board):
      raise Exception('Board is full')
    else:
      raise Exception('Invalid movement')

  
  return board


# Register the author in the corresponding file
def register_author(author: str) -> None:
  with open('last_author.txt', 'w') as f:
    f.write(author)


def write_readme(board: list[list[str]], author: str, movement: str, winner: str, red_turn: bool) -> None:
  first_iteration = True

  # Writing the README
  with open('README.md', 'w') as f:

    f.write('# Connect 4\n\n')

    # Writing the BOARD
    for row in board:
      if first_iteration:
        f.write('| 0 | 1 | 2 | 3 | 4 | 5 | 6 |\n')
        f.write('| - | - | - | - | - | - | - |\n')
        first_iteration = False
      row[:] = ['🟥' if x == '1' else '🟦' if x == '2' else '‍ ' for x in row]
      f.write('| ' + ' | '.join(row) + ' |' + '\n')
        
    # Writing the last author and movement
    if winner:
      f.write('\n### 🎉 ' + author + ' won the game with the ' + winner + ' team!\n')
      f.write('### Red will start the new game!\n')
    else:
      f.write('\n### Last movement: ' + author + '\n')
      f.write('### Played in column: ' + movement + '\n')
      f.write('### Next turn: ' + ('🟥' if red_turn else '🟦') + '\n')

    # Writing the instructions
    f.write('\n🕹️ For playing, just create an **issue** with the number of the column.\n')

    f.write('\n---------------------------\n')

    # Writing the TO DO
    f.write('TO DO:\n')
    f.write('- [ ] Both team could start the game, not only red\n')
    f.write('- [ ] Logging victories for both teams\n')
    f.write('- [ ] Logging authors, plays and wins, score system\n')
    f.write('- [ ] See old boards\n')


############################################  
#
#     /*      LOGIC     */
#
############################################


if __name__ == '__main__':

    # Get the author and movement from the environment
    author = os.getenv('AUTHOR', 'n/a')
    movement = os.getenv('MOVEMENT', '0')
    print('Author:', author)
    print('Movement:', movement)

    # Check if the last author is the same as the current author. NOT IN USE
    #if is_author_same_as_last_movement(author):
      #print('Playing twice in a row.')
      #raise Exception('Playing twice in a row.')

    # Read the board and convert it to a list
    board = read_board()
    board = convert_board_to_list(board)

    # Check if is the red turn
    red_turn = is_red_turn(board)

    # Play the game with the movement and check if any winners
    winner = ""
    try:
      board = play_game(board, movement, red_turn)
    except Exception as e:
      if str(e) == 'Red Wins':
        winner = 'Red'
      elif str(e) == 'Blue Wins':
        winner = 'Blue'
      else:
        raise Exception(str(e))
    
    # Change the turn
    red_turn = not red_turn

    # If there is a winner, reset the board and author
    # Else, write the board and register the author
    if winner:
      reset_everything()
    else:
      write_board(board)
      register_author(author)

    # Write the README
    write_readme(board, author, movement, winner, red_turn)
    print('Game played successfully')

    
