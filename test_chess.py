import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
import random
import sys


def test_utility(board, alphabeta, minimax):
    print("AlphaBetaAI vs. Minimax AI testing: \n")
    for i in range(10):
        possible_moves = list(board.legal_moves)
        move = random.choice(possible_moves)
        board.push(move)
        print("Responding to state...")
        print(board)
        ab_utility = alphabeta.evaluation_function(board, 'black')
        mm_utility = minimax.evaluation_function(board, 'black')
        print('AlphaBetaAI utility: {}, MinimaxAI utility: {}\n'.format(ab_utility, mm_utility))
    return 0


if __name__ == '__main__':
    print("Do you want to compare AlphaBeta utility with Minimax?\nYes: 1\nNo: 2\n")
    compare = input()

    if int(compare) == 1:
        test_utility(chess.Board(), AlphaBetaAI(), MinimaxAI())

    print("Enter the corresponding number for the AI you would like to play:\n")
    print("Minimax AI: 1\nAlphaBetaAI: 2\nRandomAI: 3\n")
    ai = input()
    print("Enter which side you would like to play as:\n")
    print("White: 1\nBlack: 2\n")
    side = input()
    print(ai, side)
    if int(ai) == 1:
        print("\nPlaying MinimaxAI ")
        if int(side) == 1:
            print("Playing as White")
            player1 = HumanPlayer()
            player2 = MinimaxAI()
        else:
            print("Playing as Black")
            player1 = MinimaxAI(team='white')
            player2 = HumanPlayer()
    elif int(ai) == 2:
        print("\nPlaying AlphaBetaAI ")
        if int(side) == 1:
            print("Playing as White")
            player1 = HumanPlayer()
            player2 = AlphaBetaAI(team='white')
        else:
            print("Playing as Black")
            player1 = AlphaBetaAI(team='white')
            player2 = HumanPlayer()
    else:
        print("\nPlaying RandomAI ")
        if int(side) == 1:
            print("Playing as White")
            player1 = HumanPlayer()
            player2 = RandomAI()
        else:
            print("Playing as Black")
            player1 = AlphaBetaAI(team='white')
            player2 = RandomAI()
    print('\n')
    print('Would you like the AI to use iterative deepening?')
    print("WARNING: This can make the program very slow (especially with Minimax)\n")
    print("Yes: 1\nNo: 2\n")
    iter = input()
    if int(iter) == 1:
        if int(side) == 1:
            player2.set_iter()
        else:
            player1.set_iter()

    game = ChessGame(player1, player2)

    print(game)
    while not game.is_game_over():
        game.make_move()
        print(game)

    moves = game.board.fullmove_number
    print("game over in {} moves".format(moves))

    winner = game.board.outcome()
    print(winner.result())

    print(hash(str(game.board)))
