from engines import Engine
from copy import deepcopy

import time

class StudentEngine(Engine):
    """ Game engine that you should you as skeleton code for your 
    implementation. """

    alpha_beta = False
    max_depth = 2
    # statistics
    generated_nodes = 0
    duplicate_nodes = 0 
    runtime = 0
    # auxiliary data structure
    rounds = 0
    leaf_nodes = 0 # average branching factor = geenrated_nodes / (generated_nodes - leaf_nodes)
    seen_boards = set()
    
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Wrapper function that chooses either vanilla minimax or 
        alpha-beta. """
        self.rounds += 1
        begin = time.time()

        f = self._get_ab_minimax_move if self.alpha_beta else self._get_minimax_move
        move = f(board, color, move_num, time_remaining, time_opponent)
        
        self.runtime += (time.time() - begin)
        # self._print_statistics()
        return move

    def _get_minimax_move(self, board, color, move_num=None,
                         time_remaining=None, time_opponent=None):
        # Get a list of all legal moves.
        moves = board.get_legal_moves(color)        
        # Return the best move according to the utility function _minimax_score
        return max(moves, key=lambda move: self._minimax_score(board, move, color, color, 1))

    def _minimax_score(self, board, move, init_color, cur_color, depth):
        self.generated_nodes += 1
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, cur_color)
        # Check for duplicate board with the same initial color
        self._check_duplicate(board, cur_color)

        # base case (reach max_depth or no move)
        op_moves = newboard.get_legal_moves(-cur_color)
        if depth == self.max_depth or len(op_moves) == 0:
            self.leaf_nodes += 1
            return self._minimax_utility(newboard, init_color)
        # recursive rule (max node prefers high score, min node prefers low score)
        best_score = float('-inf') if (init_color == cur_color) else float('inf')
        for op_move in op_moves:
            temp_score = self._minimax_score(newboard, op_move, init_color, -cur_color, depth + 1)
            if (init_color == cur_color and temp_score > best_score) or (init_color != cur_color and temp_score < best_score):
                best_score = temp_score

        return best_score

    def _minimax_utility(self, board, color):
        '''source of heuristic function: 
           http://www.cs.cornell.edu/~yuli/othello/othello.html'''
        num_pieces_op = len(board.get_squares(-color))
        num_pieces_me = len(board.get_squares(color))

        num_moves_op = len(board.get_legal_moves(-color))
        num_moves_me = len(board.get_legal_moves(color))

        corners = [[0, 0], [0, 7], [7, 0], [7, 7]]
        num_corners_op = 0
        num_corners_me = 0
        for corner in corners:
            if board[corner[0]][corner[1]] == -color:
                num_corners_op += 1
            elif board[corner[0]][corner[1]] == color:
                num_corners_me += 1

        return (0.01 * (num_pieces_me - num_pieces_op)  + 
                1 * (num_moves_me - num_moves_op) + 
                10 * (num_corners_me - num_corners_op))


    def _get_ab_minimax_move(self, board, color, move_num=None,
                            time_remaining=None, time_opponent=None):
        # Get a list of all legal moves.
        moves = board.get_legal_moves(color)
        # Return the best move according to the utility function _ab_minimax_score
        return max(moves, key=lambda move: self._ab_minimax_score(board, move, color, color, 1, float('-inf'), float('inf')))

    def _ab_minimax_score(self, board, move, init_color, cur_color, depth, alpha, beta):
        self.generated_nodes += 1
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, cur_color)
        # Check for duplicate board with the same initial color
        self._check_duplicate(board, cur_color)

        # base case (reach max_depth or no move)
        op_moves = newboard.get_legal_moves(-cur_color)
        if depth == self.max_depth or len(op_moves) == 0:
            self.leaf_nodes += 1
            return self._minimax_utility(newboard, init_color)
        # recursive rule (max node prefers high score, min node prefers low score)
        best_score = float('-inf') if (init_color == cur_color) else float('inf')
        for op_move in op_moves:
            temp_score = self._ab_minimax_score(newboard, op_move, init_color, -cur_color, depth + 1, alpha, beta)
            # alpha-beta pruning
            if init_color == cur_color:
                best_score = max(best_score, temp_score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, temp_score)
                beta = min(beta, best_score)
            if alpha >= beta:
                break

        return best_score

    def _check_duplicate(self, board, cur_color):
        encoding = ''
        for i in range(8):
            for j in range(8):
                encoding += str(board[i][j])
        encoding += str(cur_color)

        self.duplicate_nodes = self.duplicate_nodes + 1 if encoding not in self.seen_boards else self.duplicate_nodes
        self.seen_boards.add(encoding)

    def _print_statistics(self):
        print(f'Total number of nodes generated per round = { self.generated_nodes / self.rounds }')
        print(f'Total number of duplicate nodes per round = { self.duplicate_nodes / self.rounds }')
        print(f'Average branching factor = { self.generated_nodes / (self.generated_nodes - self.leaf_nodes) }')
        print(f'Runtime per round = { self.runtime / self.rounds }')

engine = StudentEngine


