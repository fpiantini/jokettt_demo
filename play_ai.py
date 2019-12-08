#!/usr/bin/env python3
#
"""Play a tic-tac-toe games between two AI players"""

from argparse import ArgumentParser, ArgumentTypeError

from jokettt.board.board import Board
from jokettt.players.learnerplayer import LearnerPlayer
from jokettt.players.minimaxplayer import MinimaxPlayer

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def alpha_value(_x):
    """Definition of argument type for learner alpha value,
       a float number in the range (0.0, 1.0]"""
    try:
        alpha = float(_x)
    except ValueError:
        raise ArgumentTypeError("%r not a floating point literal" % (_x,))

    if alpha <= 0.0 or alpha > 1.0:
        raise ArgumentTypeError("%r not in range (0.0, 1.0]" % (alpha,))
    return alpha

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def play_ai_vs_ai_game(first_player, second_player, board, verbosity_level):
    """Play a tic-tac-toe game between an human and an AI player"""
    result = 0
    if verbosity_level > 0:
        print("----------------------------------------------------")
        print("  --- NEW GAME ---")
    first_player_turn = True

    while result == 0 and board.is_not_full():

        if first_player_turn:
            _x, _y = first_player.move(board)
            _, result = board.place_pawn(_x, _y, first_player.piece)
        else:
            _x, _y = second_player.move(board)
            _, result = board.place_pawn(_x, _y, second_player.piece)
            result = -result

        if verbosity_level > 1:
            print('%s' % board)
        first_player_turn = not first_player_turn

    if verbosity_level > 1:
        print('%s' % board)

    if result > 0:
        # first player wins
        if isinstance(second_player, LearnerPlayer):
            second_player.learn_from_defeat(board)
        return 1
    if result < 0:
        # Second player wins
        if isinstance(first_player, LearnerPlayer):
            first_player.learn_from_defeat(board)
        return -1
    # draw
    return 0

# --------------------------------------------------------------------
def update_results_and_print_statistics(res, total_games, results):
    """Update results and print games statistics"""
    if res > 0:
        results['first_win'] += 1
        result_string = "First player wins!  "
    elif res < 0:
        results['second_win'] += 1
        result_string = "Second player wins! "
    else:
        results['draw'] += 1
        result_string = "Draw!               "
    print("%s --- {draw = %d, 1st_win = %d, 2nd_win = %d} - {%.3f, %.3f, %.3f}" %
          (result_string, results['draw'], results['first_win'], results['second_win'],
           results['draw'] / total_games,
           results['first_win'] / total_games,
           results['second_win'] / total_games,))

# --------------------------------------------------------------------
# --------------------------------------------------------------------
#   ***  MAIN ***
# --------------------------------------------------------------------
# --------------------------------------------------------------------
def main():
    """Main program: parses options, declare board and players, and
        plays a series of games"""

    parser = ArgumentParser()
    parser.add_argument("-f", "--first", choices=["minimax", "learner", "random"],
                        help="the mode of the first player", default="minimax")
    parser.add_argument("-s", "--second", choices=["minimax", "learner", "random"],
                        help="the mode of the second player", default="learner")
    parser.add_argument("--alpha1", type=alpha_value, default=0.1,
                        help="alpha parameter for the first player (only if learner)")
    parser.add_argument("--alpha2", type=alpha_value, default=0.1,
                        help="alpha parameter for the second player (only if learner)")
    parser.add_argument("-m", "--multiple-games",
                        help="play multiple games", action="store_true")
    parser.add_argument("-v", "--verbosity", action="count",
                        help="increase output verbosity")
    args = parser.parse_args()

    board = Board('x', 'o')
    if args.first == "minimax":
        first_player = MinimaxPlayer('x')
        print("FIRST PLAYER  = ", args.first)
    elif args.first == "learner":
        first_player = LearnerPlayer('x', board, args.alpha1)
        print("FIRST PLAYER  = ", args.first, ", alpha = ", args.alpha1)
    else:
        first_player = MinimaxPlayer('x', True)
        print("FIRST PLAYER  = random (dumb) player")
    if args.second == "minimax":
        second_player = MinimaxPlayer('o')
        print("SECOND PLAYER = ", args.second)
    elif args.second == "learner":
        second_player = LearnerPlayer('o', board, args.alpha2)
        print("SECOND PLAYER = ", args.second, ", alpha = ", args.alpha2)
    else:
        second_player = MinimaxPlayer('x', True)
        print("SECOND PLAYER = random (dumb) player")
    if args.verbosity:
        verbosity = args.verbosity
    else:
        verbosity = 0

    results = {}
    results['first_win'] = 0
    results['second_win'] = 0
    results['draw'] = 0
    total_games = 0

    res = play_ai_vs_ai_game(first_player, second_player, board, verbosity)
    total_games += 1
    update_results_and_print_statistics(res, total_games, results)

    while args.multiple_games:
        board.reset()
        res = play_ai_vs_ai_game(first_player, second_player, board, verbosity)
        total_games += 1
        update_results_and_print_statistics(res, total_games, results)



# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
