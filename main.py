import os




############################################  
#
#     /*      BOARD FUNCTIONS     */
#
############################################

def reset_everything() -> None:
  create_board()
  reset_author()

def create_board() -> None:
  board = [['0' for _ in range(7)] for _ in range(6)]
  
  with open('board.txt', 'w') as f:
    for row in board:
      f.write(' '.join(row) + '\n')


def read_board() -> list[str]:
  with open('board.txt', 'r') as f:
    board = f.readlines()
  
  if not board:
    create_board()
    with open('board.txt', 'r') as f:
      board = f.readlines()
  
  return board


def write_board(board: list[list[str]]) -> None:
  with open('board.txt', 'w') as f:
    for row in board:
      f.write(' '.join(row) + '\n')


def convert_board_to_list(board: list[str]) -> list[list[str]]:
  new_board = []
  for row in board:
    row = row.strip('\n')
    new_board.append(row.split(' '))
  return new_board


def check_full_board(board: list[list[str]]) -> bool:
  for row in board:
    if '0' in row:
      return False
  return True


def check_winner(board: list[list[str]], row: int, col: int) -> bool:
  board = board[::-1]
  token = board[row][col]

  for r in range(row - 1, row + 2):
    for c in range(col - 1, col + 2):
      if r == row and c == col:
        continue

      if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]):
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

def is_author_same_as_last_movement(author: str) -> bool:
  with open('last_author.txt', 'r') as f:
    last_author = f.read()
  
  return author == last_author


def is_red_turn(board: list[list[str]]) -> bool:
  count_red = 0
  count_blue = 0
  for row in board:
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

def play_game(board: list[list[str]], movement: str) -> list[list[str]]:
  token = '1' if is_red_turn(board) else '2'

  flag = False

  new_board = board[::-1]

  for rowIndex, row in enumerate(new_board):
    if row[int(movement)] == '0':
      row[int(movement)] = token
      flag = True

      if check_winner(board, rowIndex, int(movement)):
        raise Exception('Red Wins') if token == '1' else Exception('Blue Wins')

      break

  if not flag:
    if check_full_board(board):
      raise Exception('Board is full')
    else:
      raise Exception('Invalid movement')

  
  return board



def register_author(author: str) -> None:
  with open('last_author.txt', 'w') as f:
    f.write(author)

def reset_author() -> None:
  with open('last_author.txt', 'w') as f:
    f.write('')

def write_readme(board: list[list[str]], author: str, movement: str, winner: str) -> None:

  flag = False

  with open('README.md', 'w') as f:
    f.write('# Connect 4\n\n')
    for row in board:
      row[:] = ['🟥' if x == '1' else '🟦' if x == '2' else '‍ ' for x in row]
      f.write('| ' + ' | '.join(row) + ' |' + '\n')
      if not flag:
        f.write('| - | - | - | - | - | - | - |\n')
        flag = True

    if winner:
      f.write('\n### 🎉 ' + author + ' won the game with the ' + winner + ' team!\n')
      f.write('### Red will start the new game!\n')
    else:
      f.write('\n### Last movement: ' + author + '\n')
      f.write('### Played in column: ' + movement + '\n')
      f.write('### Next turn: ' + ('🟥' if is_red_turn(board) else '🟦') + '\n')

    f.write('\n🕹️ For playing, just create an **issue** with the number of the column.\n')

    f.write('\n---------------------------\n')
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

    author = os.getenv('AUTHOR', 'n/a')
    movement = os.getenv('MOVEMENT', '0')

    print('Author:', author)
    print('Movement:', movement)

    #if is_author_same_as_last_movement(author):
      #print('Playing twice in a row.')
      #raise Exception('Playing twice in a row.')

    board = read_board()
    board = convert_board_to_list(board)

    winner = ""

    try:
      board = play_game(board, movement)
    except Exception as e:
      if str(e) == 'Red Wins':
        winner = 'Red'
      elif str(e) == 'Blue Wins':
        winner = 'Blue'
      else:
        raise Exception(str(e))

    if winner:
      reset_everything()
    else:
      write_board(board)
      register_author(author)

    write_readme(board, author, movement, winner)
    print('Game played successfully')

    
