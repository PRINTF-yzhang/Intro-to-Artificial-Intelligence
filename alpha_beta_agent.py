import math
import agent
import board

###########################
# Alpha-Beta Search Agent #
###########################


class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.p_inf = math.inf
        self.n_inf = - math.inf
    # self.action = -1

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        # return the calculated best move for the agent
        return self.alphabeta_move(brd)
    


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state,
        column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb, col))
        return succ
            
        # Use alpha-beta pruning to find the best move.
        # Cuts off search and an evaluation function are used to test cuts off at depth.
        # Source code of cutoff and evaluation function comes from
        # https://github.com/TristanMoers/IA_Assignment3/blob/master/franaubry-tak-public-12a84f0ec28c/minimax.py
        # "The cutoff function returns true if the alpha-beta/minimax search has to stop; false otherwise
    def cutoff(self, brd, depth):
        if depth > self.max_depth:
            return True
        # get outcome form board.py
        # player win
        if brd.get_outcome() is not 0:
            return True

        return False

        # The evaluate function must return an integer value representing the utility function of the board.
    def evaluate(self, brd, move):
        if brd.player == 1:
            player = 2;
        else:
            player = 1;

        score = calculate_score(brd, player, move)

        return score

    def alphabeta_move(self, brd):
        best_value = self.n_inf
        for (s, m) in self.get_successors(brd):
            getMax = self.max_value(s, m, self.n_inf, self.p_inf, 0)
            v_value = getMax[0]
            best_move = getMax[1]
            if v_value > best_value:
                best_value = v_value
                self.action = best_move
    
        return self.action
        
        
            
            # return max value based on the pseudocode from hw2 with the implementation
            # of cuts off search and evaluation function
            # PARAM [board] brd: the current board state
            # PARAM [int] alpha: the alpha value
            # PARAM [int] beta: the beta value
            # PARAM [int] depth: the depth to search to
            # PARAM [int] move: the next action
            # RETURN [tuple] (best_value,best_move): current best value and best action.
            #
            
    def max_value(self, brd, move, alpha, beta, depth):
        if self.cutoff(brd,depth):
            return self.evaluate(brd, move), move
        best_value = self.n_inf
        b_move = None
        for (s, m) in self.get_successors(brd):
            # was depth-1 in the pseudocode
            getMin = self.min_value(s, m, alpha, beta, depth+1)
            v_value = getMin[0]
            b_move = getMin[1]
            if v_value > best_value:
                best_move = b_move
                best_value = v_value
            if best_value >= beta:
                return best_value,best_move
            alpha = max(alpha, best_move)
        return best_value, best_move

# return min value based on the pseudocode from hw2 with the implementation
# of cuts off search and evaluation function
    def min_value(self, brd, move, alpha, beta, depth):
        if self.cutoff(brd,depth):
            return self.evaluate(brd, move), move
        min_value = self.p_inf
        best_move = None
        for (s, m) in self.get_successors(brd):
            # was depth-1 in the pseudocod
            getMax = self.max_value(s, m, alpha, beta, depth+1)
            v_value = getMax[0]
            b_move = getMax[1]
            if v_value < min_value:
                min_value= v_value
                best_move = b_move
            if min_value <= alpha:
                return min_value, best_move
            beta = min(beta, min_value)
    
        return min_value, best_move

#calculate the current score to determing the move
def calculate_score(brd, player, move):
    total_score = 0
    y = 0
    while y < brd.h and brd.board[y][move] != 0:
        y = y + 1
    y = y - 1
    total_score += check_seven_score(brd, player, move, y)
    total_score += check_win_score(brd, player)

    return total_score

# In hw2 I said:
    # To optimized the algorithm.We probably need a function that can limited the range of next move.
    # For example, the next move can only happen from the close positions, which can greatly shorten
    # the searching nodes.
    # here is the implementation


def check_seven(brd, player, x, y):
    score = 0
    if (y - 1 > 0) and (x - 1 > 0) and (x + 1 < brd.w) and (y + 1 < brd.h):
        cell1 = brd.board[y - 1][x]
        cell2 = brd.board[y][x - 1]
        cell3 = brd.board[y][x + 1]
        cell4 = brd.board[y + 1][x - 1]
        cell5 = brd.board[y + 1][x + 1]
        cell6 = brd.board[y - 1][x - 1]
        cell7 = brd.board[y - 1][x + 1]
        if cell1 == 0:
            score += 5
        elif cell1 == player:
            score += 8
        elif cell2 == 0:
            score += 5
        elif cell2 == player:
            score += 8
        elif cell3 == 0:
            score += 5
        elif cell3 == player:
            score += 8
        elif cell4 == 0:
            score += 5
        elif cell4 == player:
            score += 8
        elif cell5 == 0:
            score += 5
        elif cell5 == player:
            score += 8
        elif cell6 == 0:
            score += 5
        elif cell6 == player:
            score += 8
        elif cell7 == 0:
            score += 5
        elif cell7 == player:
            score += 8

    return score

# get current score from check_seven
def check_seven_score(brd, player, move, y):
    current_score = 0
    current_score += check_seven(brd, player, move, y)

    return current_score

# Anticipate direct losing moves
#The idea is to anticipate and avoid exploring very bad moves allowing the opponent to win directly at the next turn.
# That way we are able to prune the search tree faster and reduce the number of explored nodes.
# idea comes from http://blog.gamesolver.org/solving-connect-four/09-anticipate-losing-moves/

def direct_losing_move(brd, move,player):
    nb = brd.copy()
    
    if brd.player == 1:
        player = 2
    else:
        player = 1
    nb.add_token(move)

# Checks if the opponent or AI can won
def check_win_score(brd,player):

    if brd.get_outcome == player:
        return 100000
    elif brd.get_outcome == brd.player:
        return -100000
    else:
        return 0
# #from hw1
# def isLineAt(self, brd, x, y, dx, dy):
#     """Return True if a line of identical tokens exists starting at (x,y)
#         in direction (dx,dy)"""
#     s_position = brd.board[y][x]
#     for i in range(1,brd.n):
#         f_position = self.board[y + i * dy][x + i * dx]
#         if f_position != s_position:
#             return False
#     return True;
#
#
# def isAnyLineAt(self,brd, x, y):
#     """Return True if a line of identical symbols exists starting at (x,y)
#         in any direction"""
#     return (self.isLineAt(brd,x, y, 1, 0) or # Horizontal
#             self.isLineAt(brd,x, y, 0, 1) or # Vertical
#             self.isLineAt(brd,x, y, 1, 1) or # Diagonal up_x
#             self.isLineAt(brd,x, y, 1, -1)) # Diagonal down


# for 7*6 use depth=4 ; for 14*12uaw depth=6;
THE_AGENT = AlphaBetaAgent("ZhangYing", 2)
