import sqlite3

def migrate_db():
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute('CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, board TEXT)')
  c.execute('CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, movements INTEGER DEFAULT 0)')
  c.execute('CREATE TABLE IF NOT EXISTS winners (id INTEGER PRIMARY KEY, game_id INTEGER, player_id INTEGER, team BOOLEAN, FOREIGN KEY (game_id) REFERENCES games (id), FOREIGN KEY (player_id) REFERENCES players (id))')
  conn.commit()

def insert_game(board: list[list[str]], winner: int, team: bool) -> None:
  str_board = ""
  for row in board:
    str_board += ' '.join(row) + '\n'
  
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute(f"INSERT INTO games (board) VALUES ('{str_board}')")
  
  player_id = c.execute(f"SELECT id FROM players WHERE id = {winner}").fetchone()

  if not player_id:
    raise Exception('Player not found in database')
  
  c.execute(f"INSERT INTO winners (game_id, player_id, team) VALUES ('{c.lastrowid}', '{player_id[0]}', {team})")
  
  conn.commit()

def insert_player(id: int, name: str) -> None:
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute(f"INSERT INTO players (id, name) VALUES ({id}, '{name}')")
  conn.commit()

def get_player(id: int) -> tuple:
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  try:
    player = c.execute(f"SELECT * FROM players WHERE id = {id}").fetchone()
  except:
    player = None

  return player


def get_player_stats() -> list:
  conn = sqlite3.connect('database.db')
  c = conn.cursor()

  # Get name, movements and count of wins for each player
  stats = c.execute("SELECT players.name, players.movements, COUNT(winners.id) FROM players LEFT JOIN winners ON players.id = winners.player_id GROUP BY players.id").fetchall()

  return stats

def get_teams_stats() -> list:
  conn = sqlite3.connect('database.db')
  c = conn.cursor()

  stats = c.execute("SELECT team, COUNT(winners.id) FROM winners GROUP BY team").fetchall()

  return stats



def sum_movement(id: int) -> None:
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute(f"UPDATE players SET movements = movements + 1 WHERE id = {id}")
  conn.commit()


def health_check() -> bool:
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT name FROM sqlite_master WHERE type='table'")
  if not c.fetchall():
    return False
  else:
    return True