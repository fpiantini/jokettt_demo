#!/usr/bin/env python3
#
"""Play a tic-tac-toe games between two AI players"""

from argparse import ArgumentParser, ArgumentTypeError

from jokettt.board import Board
from jokettt.learnerplayer import LearnerPlayer
from jokettt.minimaxplayer import MinimaxPlayer

DEFAULT_ALPHA_VALUE = 0.1

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
def play_ai_vs_ai_game(player_a, player_b, board, player_a_first, verbosity_level):
    """Play a tic-tac-toe game between an human and an AI player"""
    result = 0
    if verbosity_level > 0:
        print("----------------------------------------------------")
        print("  --- NEW GAME ---")
    player_a_turn = player_a_first

    while result == 0 and board.is_not_full():

        if player_a_turn:
            _x, _y = player_a.move(board)
            _, result = board.place_pawn(_x, _y, player_a.piece)
        else:
            _x, _y = player_b.move(board)
            _, result = board.place_pawn(_x, _y, player_b.piece)
            result = -result

        if verbosity_level > 1:
            print('%s' % board)
        player_a_turn = not player_a_turn

    if verbosity_level > 1:
        print('%s' % board)

    if result > 0:
        # player_a wins
        if isinstance(player_b, LearnerPlayer):
            player_b.learn_from_defeat(board)
        return 1
    if result < 0:
        # player_b player wins
        if isinstance(player_a, LearnerPlayer):
            player_a.learn_from_defeat(board)
        return -1
    # draw
    return 0

# --------------------------------------------------------------------
def update_results_and_print_statistics(res, total_games, results):
    """Update results and print games statistics"""
    if res > 0:
        results['player_a_win'] += 1
        result_string = "Player A wins!  "
    elif res < 0:
        results['player_b_win'] += 1
        result_string = "Player B wins!  "
    else:
        results['draw'] += 1
        result_string = "Draw!           "
    print("%s --- {draw = %d, A_win = %d, B_win = %d} - {%.3f, %.3f, %.3f}" %
          (result_string, results['draw'], results['player_a_win'], results['player_b_win'],
           results['draw'] / total_games,
           results['player_a_win'] / total_games,
           results['player_b_win'] / total_games,))

# --------------------------------------------------------------------
# --------------------------------------------------------------------
#   ***  MAIN ***
# --------------------------------------------------------------------
# --------------------------------------------------------------------
def main():
    """Main program: parses options, declare board and players, and
        plays a series of games"""

    parser = ArgumentParser()
    parser.add_argument("-a", "--player_a", choices=["minimax", "learner", "random"],
                        help="the mode of the player A", default="minimax")
    parser.add_argument("-b", "--player_b", choices=["minimax", "learner", "random"],
                        help="the mode of the player B", default="learner")
    parser.add_argument("--alpha1", type=alpha_value, default=0.1,
                        help="alpha parameter for the player A (only if learner)")
    parser.add_argument("--alpha2", type=alpha_value, default=0.1,
                        help="alpha parameter for the player B (only if learner)")
    parser.add_argument("-m", "--multiple-games",
                        help="play multiple games", action="store_true")
    parser.add_argument("-s", "--switch_turn", action="store_true",
                        help="swith first move between players (only if multiple games)")
    parser.add_argument("-v", "--verbosity", action="count",
                        help="increase output verbosity")
    args = parser.parse_args()
    if args.verbosity:
        verbosity = args.verbosity
    else:
        verbosity = 0
    if args.alpha1:
        alpha1 = args.alpha1
    else:
        alpha1 = DEFAULT_ALPHA_VALUE
    if args.alpha2:
        alpha2 = args.alpha2
    else:
        alpha2 = DEFAULT_ALPHA_VALUE

    board = Board('x', 'o')
    if args.player_a == "minimax":
        player_a = MinimaxPlayer('x')
        print("PLAYER A = ", args.player_a)
    elif args.player_a == "learner":
        player_a = LearnerPlayer('x', board, {}, alpha1, verbosity)
        print("PLAYER A = ", args.player_a, ", alpha = ", alpha1)
    else:
        player_a = MinimaxPlayer('x', True)
        print("PLAYER A = random (dumb) player")
    if args.player_b == "minimax":
        player_b = MinimaxPlayer('o')
        print(" PLAYER B = ", args.player_b)
    elif args.player_b == "learner":
        player_b = LearnerPlayer('o', board, {}, alpha2, verbosity)
        print(" PLAYER B = ", args.player_b, ", alpha = ", alpha2)
    else:
        player_b = MinimaxPlayer('x', True)
        print(" PLAYER B = random (dumb) player")

    results = {}
    results['player_a_win'] = 0
    results['player_b_win'] = 0
    results['draw'] = 0
    total_games = 0
    player_a_turn = True

    res = play_ai_vs_ai_game(player_a, player_b, board, player_a_turn, verbosity)
    total_games += 1
    update_results_and_print_statistics(res, total_games, results)

    while args.multiple_games:
        board.reset()
        if args.switch_turn:
            player_a_turn = not player_a_turn
        res = play_ai_vs_ai_game(player_a, player_b, board, player_a_turn, verbosity)
        total_games += 1
        update_results_and_print_statistics(res, total_games, results)



# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
