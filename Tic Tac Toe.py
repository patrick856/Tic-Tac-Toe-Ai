import random
import copy

def newBoard():
    return [[1,2,3], [4,5,6], [7,8,9]]

def render(board):
    print(' '.join(map(str, board[0])))
    print(' '.join(map(str, board[1])))
    print(' '.join(map(str, board[2])))
    print("")

def getMove(n):
    move = int(input('Player ' + str(n) + " turn:"))
    return move

def makeMove(board, turn, move, change):
    b = copy.deepcopy(board)
    j = (move-1)%3
    i = (move-1)//3
    if turn: # DO NOT PUT TURN == CHANGE
        b[i][j] = 'x'
    else: 
        b[i][j] = 'o'
    return b

def isValid(board, move):
    j = (move-1)%3
    i = (move-1)//3
    if board[i][j] == 'x' or board[i][j] == 'o':
        return False
    return True

def checkState(board):
    possibleWins = [
        [[0,0],[0,1],[0,2]],
        [[1,0],[1,1],[1,2]],
        [[2,0],[2,1],[2,2]],
        [[0,0],[1,0],[2,0]],
        [[0,1],[1,1],[2,1]],
        [[0,2],[1,2],[2,2]],
        [[0,0],[1,1],[2,2]],
        [[2,0],[1,1],[0,2]]
    ]
    for i in range(8):
        if board[possibleWins[i][0][0]][possibleWins[i][0][1]] == board[possibleWins[i][1][0]][possibleWins[i][1][1]] and board[possibleWins[i][0][0]][possibleWins[i][0][1]] == board[possibleWins[i][2][0]][possibleWins[i][2][1]]:
            return board[possibleWins[i][0][0]][possibleWins[i][0][1]] 

def randomAi(board, *args):
    while True:
        move = random.randint(1,9)
        if isValid(board, move):
            return move
        
def smartAi(board, turn, change):
    possibleWins = [
        [[0,0],[0,1],[0,2]],
        [[1,0],[1,1],[1,2]],
        [[2,0],[2,1],[2,2]],
        [[0,0],[1,0],[2,0]],
        [[0,1],[1,1],[2,1]],
        [[0,2],[1,2],[2,2]],
        [[0,0],[1,1],[2,2]],
        [[2,0],[1,1],[0,2]]
    ]

    if turn:
        player = 'x'
    else:
        player = 'o'
    
    for i in range(8):
        count = 0
        empty = 0
        for j in range(3):
            move = possibleWins[i][j][0]*3 + possibleWins[i][j][0] + 1
            if board[possibleWins[i][j][0]][possibleWins[i][j][1]] == player:
                count += 1
            elif isValid(board, move):
                empty = move
        if count == 2 and empty:
            return empty
    return randomAi(board)    

def expertAi(board, turn , change):
    possibleWins = [
        [[0,0],[0,1],[0,2]],
        [[1,0],[1,1],[1,2]],
        [[2,0],[2,1],[2,2]],
        [[0,0],[1,0],[2,0]],
        [[0,1],[1,1],[2,1]],
        [[0,2],[1,2],[2,2]],
        [[0,0],[1,1],[2,2]],
        [[2,0],[1,1],[0,2]]
    ]

    if turn:
        player = 'x'
        inverse = 'o'
    else:
        player = 'o'
        inverse = 'x'
    
    for i in range(8):
        count = 0
        empty = 0
        for j in range(3):
            move = possibleWins[i][j][0]*3 + possibleWins[i][j][0] + 1
            if board[possibleWins[i][j][0]][possibleWins[i][j][1]] == player:
                count += 1
            elif isValid(board, move):
                empty = move
        if count == 2 and empty:
            return empty
    for i in range(8):
        count = 0
        empty = 0
        for j in range(3):
            move = possibleWins[i][j][0]*3 + possibleWins[i][j][0] + 1
            if board[possibleWins[i][j][0]][possibleWins[i][j][1]] == inverse:
                count += 1
            elif isValid(board, move):
                empty = move
        if count == 2 and empty:
            return empty
    return randomAi(board)

def perfectAi(boardAi, turn, change):
    if boardAi == newBoard():
        return 5
    if turn:
        player = 'x'
        inverse = 'o'
    else:
        player = 'o'
        inverse = 'x'

    bestMove = 0
    bestScore = -1

    for i in range(1,10):
        if isValid(boardAi, i):
            b2 = makeMove(boardAi, turn, i, change)
            result = bestPlay(b2, abs(turn-1), change, player, inverse)
            if result >= bestScore:
                boardTuple = tuple(tuple(row) for row in copy.deepcopy(boardAi)) # dp --
                if turn:
                    memoX[boardTuple] = copy.deepcopy(result)
                else:
                    memoO[boardTuple] = copy.deepcopy(result)
                bestScore = result
                bestMove = i
    return bestMove

def bestPlay(board, turnAi, change, p, inv):
    boardTuple = tuple(tuple(row) for row in copy.deepcopy(board)) # dp --
    if boardTuple in memoX and turn: #
        return memoX[boardTuple] # --
    if boardTuple in memoO and not turn:
        return memoO[boardTuple]
    boardrec = copy.deepcopy(board)
    state = checkState(boardrec)
    if state == p:
        return 1
    if state == inv:
        return -1
    validMoves = []
    bp = []
    for i in range(1,10):
        if isValid(boardrec, i): validMoves.append(i)
    if len(validMoves) == 0: return 0
    for i in validMoves:
        bp.append(bestPlay(makeMove(boardrec, turnAi, i, change),abs(turnAi-1), change, p, inv))
    if turn == turnAi:
        if turn: 
            memoX[boardTuple] = copy.deepcopy(max(bp)) # dp --
        else:
            memoO[boardTuple] = copy.deepcopy(max(bp))
        return max(bp)
    else:
        if turn:
            memoX[boardTuple] = copy.deepcopy(min(bp)) # dp --
        else:
            memoO[boardTuple] = copy.deepcopy(min(bp)) # dp --
        return min(bp)
        

player1won = 0
player2won = 0
draw = 0
change = 0
memoX = {}
memoO = {}

while player1won+player2won+draw<100: # game loop
    board = newBoard()
    change = abs(change-1)
    turn = 1 # p1: 1 -> x ,p2: o -> o
    numberOfMoves = 0
    winner = 0
    while True: # round loop
        render(board)
        if turn == change:
            move = perfectAi(board, turn, change) #p1
        else:
            move = expertAi(board, turn, change) #p2
        # move = getMove(turn+1) - human play
        if not isValid(board, move):
            print("This isn't a valid move...")
            continue
        board = makeMove(board, turn, move, change)
        numberOfMoves += 1
        turn = abs(turn-1)
        state = checkState(board)
        if state == 'x':
            if change:
                winner = 1
            else:
                winner = 2
            break
        if state == 'o':
            if change:
                winner = 2
            else:
                winner = 1
            break
        if numberOfMoves == 9:
            break

    render(board)

    if winner == 1:
        print("Player 1 has won!")
        player1won += 1
    elif winner == 2:
        print("player 2 has won!")
        player2won += 1
    else:
        print("It's a draw!")
        draw += 1
    print(" - Stats -")
    print("Player 1: " + str(player1won))
    print("Player 2: " + str(player2won))
    print("Draw: " + str(draw))
    #newgame = input("New game? y/n")
    #if newgame == 'n':
    #    break
wait = input()