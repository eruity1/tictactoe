import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_board():
  return [[EMPTY, EMPTY, EMPTY],
          [EMPTY, EMPTY, EMPTY],
          [EMPTY, EMPTY, EMPTY]]


def player(board):
  x_count = sum(row.count(X) for row in board)
  o_count = sum(row.count(O) for row in board)
  return X if x_count == o_count else O

def actions(board):
  return {(i, j) 
          for i in range(3)
          for j in range(3)
          if board[i][j] == EMPTY}

def result(board, action):
  i, j = action
  if board[i][j] is not EMPTY:
    raise Exception("Invalid Move")
  new_board = copy.deepcopy(board)
  new_board[i][j] = player(board)
  return new_board

def winner(board):
  for i in range(3):
    if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
      return board[i][0]
    if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
      return board[0][i]

  if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
    return board[0][0]
  if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
    return board[0][2]
  return EMPTY

def game_over(board):
  return winner(board) is not EMPTY or all(
    cell is not EMPTY for row in board for cell in row
  )

def utility(board):
  w = winner(board)
  if w == X:
    return 1
  elif w == O:
    return -1
  return 0

def minimax(board):
  if game_over(board):
    return None

  current = player(board)

  def max_value(state):
    if game_over(state):
      return utility(state), None
    v = -math.inf
    best_action = None
    for action in actions(state):
      min_result, _ = min_value(result(state, action))
      if min_result > v:
        v = min_result
        best_action = action
        if v == 1:
          break
    return v, best_action
  
  def min_value(state):
    if game_over(state):
      return utility(state), None
    v = math.inf
    best_action = None
    for action in actions(state):
      max_result, _ = max_value(result(state, action))
      if max_result < v:
        v = max_result
        best_action = action
        if v == -1:
          break
    return v, best_action
    
  if current == X:
    _, action = max_value(board)
  else:
    _, action = min_value(board)
  return action
