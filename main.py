import os




############################################  
#
#     /*      BOARD FUNCTIONS     */
#
############################################

def reset_everything() -> None:
  create_board()
  reset_autor()

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


def check_winner(board: list[list[str]], row: int, col: int) -> bool:
  token = board[row][col]

  for r in range(row - 1, row + 2):
    for c in range(col - 1, col + 2):
      if r == row and c == col:
        continue
      if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]):
        continue
      if board[r][c] == token:
        for i in range(2, 4):
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

def is_autor_same_as_last_movement(autor: str) -> bool:
  with open('last_autor.txt', 'r') as f:
    last_autor = f.read()
  
  return autor == last_autor


def is_red_turn(board: list[list[str]]) -> bool:
  count_red = 0
  count_blue = 0
  for row in board:
    count_red += row.count('1')
    count_blue += row.count('2')
  
  if count_red == count_blue:
    return True




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



def register_autor(autor: str) -> None:
  with open('last_autor.txt', 'w') as f:
    f.write(autor)

def reset_autor() -> None:
  with open('last_autor.txt', 'w') as f:
    f.write('')

def write_readme(board: list[list[str]], autor: str, movement: str, winner: str) -> None:

  flag = False

  with open('README.md', 'w') as f:
    f.write('# Connect 4\n\n')
    for row in board:
      row[:] = ['🟥' if x == '1' else '🟦' if x == '2' else '‍ ' for x in row]
      f.write('| ' + ' | '.join(row) + ' |' + '\n')
      if not flag:
        f.write('| - | - | - | - | - | - | - |\n')
        flag = True

    if autor:
      f.write('\n### Last movement: ' + autor + '\n')
    if movement:
      f.write('### Played in column: ' + movement + '\n')
    f.write('### Next turn: ' + ('🟥' if is_red_turn(board) else '🟦') + '\n')
    if winner:
      f.write('### 🎉 The winner of last game was: ' + winner + '\n')
    f.write('\n\n🕹️ For playing, just create an **issue** with the column you want to play.\n')


############################################  
#
#     /*      LOGIC     */
#
############################################


if __name__ == '__main__':

    autor = os.environ['AUTOR']
    movement = os.environ['MOVEMENT']

    print('Autor:', autor)
    print('Movement:', movement)

    #if is_autor_same_as_last_movement(autor):
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
      autor, movement = '', ''

    write_board(board)
    register_autor(autor)
    write_readme(board, autor, movement, winner)
    print('Game played successfully')

    
