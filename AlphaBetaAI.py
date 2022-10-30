import random

import chess
from math import inf


class AlphaBetaAI():
    def __init__(self, depth=3, team='black', iter=False):
        if team == 'black':
            self.team = chess.BLACK
            self.otherteam = chess.WHITE
        else:
            self.team = chess.WHITE
            self.otherteam = chess.BLACK
        self.maxdepth = depth
        self.iter = iter
        pass

    def set_iter(self):
        self.iter = True

    def choose_move(self, board):
        if self.iter:
            counter = 0
            i = 1
            last_utility = 0
            last_move = 0
            while i < 5:
                self.maxdepth = i
                move = self.alphabeta_move(board)
                board.push(move)
                utility = self.evaluation_function(board, 'max')
                board.pop()
                if utility <= last_utility - 10:
                    break
                if move == last_move:
                    counter += 1
                else:
                    if counter != 0:
                        print("Best move changed from {} to {} "
                              "with change of depth limit from {} to {}".format(last_move, move, i - 1, i))
                    counter = 0
                if counter > 2:
                    break
                else:
                    last_utility = utility
                    last_move = move
                    i += 1
        else:
            move = self.alphabeta_move(board)
        print("AlphaBeta AI recommending move " + str(move))
        return move

    def alphabeta_move(self, board):
        possible_moves = list(board.legal_moves)
        best_utility = float('-inf')
        best_move = random.choice(possible_moves)
        for move in possible_moves:
            depth = 0
            board.push(move)
            alpha = float('-inf')
            beta = float('inf')
            utility = self.min_value(board, depth, alpha, beta)
            board.pop()
            if utility > best_utility:
                best_utility = utility
                best_move = move
        return best_move

    def min_value(self, board, depth, alpha, beta):
        depth += 1
        if self.cutoff_test(board, depth):
            return self.evaluation_function(board, 'min')
        possible_moves = list(board.legal_moves)
        worst_utility = float('inf')
        for move in possible_moves:
            board.push(move)
            utility = self.max_value(board, depth, alpha, beta)
            board.pop()
            if utility < worst_utility:
                worst_utility = utility
            if utility < alpha:
                return worst_utility
            beta = min(beta, worst_utility)
        return worst_utility

    def max_value(self, board, depth, alpha, beta):
        depth += 1
        if self.cutoff_test(board, depth):
            return self.evaluation_function(board, 'max')
        possible_moves = list(board.legal_moves)
        best_utility = float('-inf')
        for move in possible_moves:
            board.push(move)
            utility = self.min_value(board, depth, alpha, beta)
            board.pop()
            if utility > best_utility:
                best_utility = utility
            if utility > beta:
                return best_utility
            alpha = max(alpha, best_utility)
        return best_utility

    def cutoff_test(self, board, depth):
        if depth > self.maxdepth:
            return True
        elif board.is_checkmate():
            return True
        elif board.is_stalemate():
            return True
        else:
            return False

    def evaluation_function(self, board, side):
        utility = 0
        last_move = board.peek()
        if board.outcome():
            outcome = board.outcome()
            if outcome.termination == 1:
                if outcome.winner == self.team:
                    utility = float('inf')
                else:
                    utility = float('-inf')
                return utility
            else:
                return utility

        weights = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 0}

        for i in range(1, 6):
            utility += weights[i] * len(board.pieces(i, self.team))
            utility -= weights[i] * len(board.pieces(i, self.otherteam))

        if side == 'min':
            if board.is_check():
                utility += 100
            if str(last_move)[1] < str(last_move)[3]:
                piece = board.piece_at(last_move.to_square)
                utility += weights[piece.piece_type]
            utility -= len(list(board.legal_moves))
        else:
            if board.is_check():
                utility -= 100
            if str(last_move)[1] > str(last_move)[3]:
                piece = board.piece_at(last_move.to_square)
                utility -= weights[piece.piece_type]
            utility += len(list(board.legal_moves))
        return utility

