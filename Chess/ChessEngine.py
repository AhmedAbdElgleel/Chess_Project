"""
this class is responsible for storing all info about the current game state of the chess game & also responsible for
determine the valid moves at the current state and keep a move log
"""


class GameState():
    def __init__(self):
        # this is nested list 8x8 ,each element of the list has 2 characters
        # the first char either black (b) nor white (w)
        # the second char indicate the piece type for example King (k),Queen(Q),Rock(R)...etc
        # "--" represent empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMove, 'R': self.getRookMove, 'N': self.getKnightMove,
                              'B': self.getBishopMove, 'Q': self.getQueenMove, 'K': self.getKingMove}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)  # we will continue tracking the king movement to control the checkmate
        self.blackKingLocation = (0, 4)
        self.checkMate = False   # check mate = true when the king has no valid movement(no valid square to move)
        self.staleMate = False   # stalemate = true when the king has no valid or there is no valid moves and king is not in check

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # at this point al move are valid we will recorrect it latter
        self.whiteToMove = not self.whiteToMove  # swap players
        # after each move we will update the current king location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):  # to undo the move
        if len(self.moveLog) != 0:  # to make sure their is a movment done already
            move = self.moveLog.pop()  # pop return index the last element so we could easy remove it
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch back turns
            '''
            update the king move if we do undoMovment
            '''
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
    def cancelUndo(self,move):
        self.makeMove(move)

    def getValidMovie(self):
        #1.)generate all possible moves
        moves = self.getAllPossibleMoves()
        #2.)for each move,make the move
        for i in range(len(moves)-1, -1, -1):             # when removing from a list go backwards through that list  leh 3mlna kda ywo ywo ywo hy rkz m3aya
            self.makeMove(moves[i])                      # el fkra lets say [1,2,3,3,4,5] is and we want to remove num==3 to the iterator stop at third eleemnt to remove it and shift other elements to left we we could have bugs bec.the dirction of shifting is the opposite to dirction of search so we could missed an elemnet so to overcome on this we could make the direction of shift is the same as dirction of search so the shifted elements we already checked it  so we will start from last index = len(moves)-1 with -1 step(when removing from a list go backsward through the list)
            # 3.) generate all opposite'moves
            # 4.)for each of your opposite's move,see if your king is under attack
            self.whiteToMove = not self.whiteToMove      # we need to make sure that we switch the turns before we call in check because makeMove() switch the turns so we need to switch the turn backs
            if self.inCheck():
                moves.remove(moves[i])                   #if they do attack your king ,not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()                              # we call this to cancel makeMove()effect
        if len(moves) == 0:                              # if length of valid move =0 whick mean that is either check mate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False          # we just make sure they still false because the user may be do check then undo it so we want to make sure that is work correclty
            self.staleMate = False
        return moves
    '''
    determine if the current player is in check
    '''

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])   # y32y if white's turn to move lets first check and see if the square is under attack so that person is in check w tb3t ll fucntion square attack the current king location(x,y)
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    '''
    determine if the enemy can attack the square r,c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove   #switch to opposite's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove    # switch back the turn so this function will not modify the turn order
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # this mean that square is really under attack
                return True  # as its really under attack
        return False         # which mean that the square is not under attack
    '''
    all move without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # num of row
            for c in range(len(self.board[r])):  # num of col for each row
                turn = self.board[r][c][0]  #thats mean the first char of images of picess 'w'
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]  #thats mean the Sec char of images of picess 'p' OR 'R' OR ETC...
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMove(self, r, c, moves):  # this is A Function responsibale for pawn move
        # important note the board form up to down kol morab3 feh mtratb form 0 to 7
        # 3shan kda the white pawn when move he move (row-1) to move to up
        # but the first step can move (row - 2) so that is a spacial case
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # this is the spacial case when the wp in the row 6
                    moves.append(Move((r, c), (r-2, c), self.board))
            # there is also a spacial case that when there is an soldier form black next to the front end the white pawn
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # this is a black moves
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMove(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enmemyColor = "b" if self.whiteToMove else "w"  # that is a spcial way  in python to  write the old shape of this :-
        # if self.whiteToMove:
        # enmemyColor = "b"
        # else:
        # enmemyColor = "w"
        for d in directions:
            for i in range(1, 8):  # maxmmim move he can move
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enmemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMove(self, r, c, moves):
        KnightMove = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in KnightMove:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMove(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enmemyColor = "b" if self.whiteToMove else "w"  # that is a spcial way  in python to  write the old shape of this :-
        # if self.whiteToMove:
        # enmemyColor = "b"
        # else:
        # enmemyColor = "w"
        for d in directions:
            for i in range(1, 8):  # maxmmim move he can move
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enmemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMove(self, r, c, moves):
        self.getRookMove(r, c, moves)
        self.getBishopMove(r, c, moves)
        # that beacous the Queeen Can Move like that the Rook & Bisshop

    def getKingMove(self, r, c, moves):
        kingMove = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMove[i][0]
            endCol = c + kingMove[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move:
    # maps keys to values
    # For converting (row, col) to Chess Notations => (0,0) -> a8
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # can't be '--'
        self.pieceCaptured = board[self.endRow][self.endCol]  # can be '--' -> no piece was captured

        # CastleMove
        self.isCastleMove = isCastleMove

        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def getChessNotation(self):
        return self.getFileRank(self.startRow, self.startCol) + self.getFileRank(self.endRow, self.endCol)

    def getFileRank(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    '''
	overriding equal to method
	'''
    def __eq__(self, other):
        return isinstance(other, Move) and self.moveId == other.moveId