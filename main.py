import os




############################################  
#
#     /*      BOARD FUNCTIONS     */
#
############################################

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


def register_autor(autor: str) -> None:
  with open('last_autor.txt', 'w') as f:
    f.write(autor)

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

  for row in board[::-1]:
    if row[int(movement)] == '0':
      row[int(movement)] = token
      flag = True
      break

  if not flag:
    raise Exception('Invalid movement')
  
  return board




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

    if is_autor_same_as_last_movement(autor):
      print('Playing twice in a row.')
      raise Exception('Playing twice in a row.')

    board = read_board()
    board = convert_board_to_list(board)

    board = play_game(board, movement)

    register_autor(autor)
    write_board(board)
    print('Game played successfully')

    
