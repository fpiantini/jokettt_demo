#!/usr/bin/env python3
#
"""Play tic-tac-toe games between a learner players and another
   AI player (minimax, random or another learner).
   At the end of the training save the 'learned' data"""

from argparse import ArgumentParser, ArgumentTypeError

import os
import sys
import random

import numpy as np

from jokettt.board import Board
from jokettt.learnerplayer import LearnerPlayer
from jokettt.minimaxplayer import MinimaxPlayer

LEARNER_PIECE = 'x'
OPPONENT_PIECE = 'o'
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
def number_of_games(_n):
    """Definition of argument type for number of games to play,
       a positive integer. If zero, play forever"""
    try:
        num_games = int(_n)
    except ValueError:
        raise ArgumentTypeError("%r not an integer" % (_n,))

    if num_games < 0:
        raise ArgumentTypeError("illegal value %r. Shall be a positive integer" % (num_games,))
    return num_games

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def file_to_save(_x):
    """Definition of argument type for learner save data file,
       a string with a pathname of a file."""
    return _x

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def file_to_load(_x):
    """Definition of argument type for learner init data,
       a string with a pathname of a file. The file shall exist"""

    if not os.path.exists(_x):
        raise ArgumentTypeError("%s does not exist" % (_x,))
    if not os.path.isfile(_x):
        raise ArgumentTypeError("%s is not a file" % (_x,))
    return _x

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def build_random_ztable_initdata():
    ztable_init = np.empty([3, 3, 2], dtype=int)
    random.seed()
    for _x in range(0, 3):
        for _y in range(0, 3):
            for _e in range(0, 2):
                ztable_init[_x][_y][_e] = random.randint(0, sys.maxsize)
    return ztable_init


# --------------------------------------------------------------------
# --------------------------------------------------------------------
def play_ai_vs_ai_game(player_a, player_b, board, player_a_first, verbosity_level):
    """Play a tic-tac-toe game between two AI players"""
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

    # --------------------------------------------------
    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument("-t", "--opponenttype", choices=["minimax", "learner", "random"],
                        help="the mode of the opponent player", default="minimax")
    parser.add_argument("--alpha1", type=alpha_value, default=0.1,
                        help="alpha parameter for the learner player")
    parser.add_argument("--alpha2", type=alpha_value, default=0.1,
                        help="alpha parameter for the opponent player (only if learner)")
    parser.add_argument("-n", "--num_games", type=number_of_games, default=100,
                        help="Number of games to play")
    parser.add_argument("--switch_turn", action="store_true",
                        help="swith first move between players")
    parser.add_argument("-l", "--loaddata", type=file_to_load,
                        help="load learned data from file")
    parser.add_argument("-s", "--savedata", type=file_to_save,
                        help="save learned data to file")
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

    # --------------------------------------------------
    # If requested, load learned data
    if args.loaddata:
        try:
            print("...loading data from %s" % args.loaddata)
            init_data = np.load(args.loaddata, allow_pickle=True)
        except:
            print("error reading learned data from file %s" % args.loaddata)
            init_ztable = build_random_ztable_initdata()
            init_values = {}

        try:
            init_ztable = init_data['zobrist_hash']
        except:
            print("error reading 'zobrist_hash' from loaded file")
            init_ztable = build_random_ztable_initdata()

        try:
            init_values = init_data['value_tuple'].item()
        except:
            print("error reading 'value_tuple' from loaded file")
            init_values = {}

    else:
        init_ztable = build_random_ztable_initdata()
        init_values = {}

    if args.savedata:
        print("...the learned data will be saved to %s.npz" % args.savedata)
    else:
        print("...the learned data will not be saved")

    # --------------------------------------------------
    # Declares board and players
    board = Board(LEARNER_PIECE, OPPONENT_PIECE, init_ztable)
    player_a = LearnerPlayer(LEARNER_PIECE, board, init_values, alpha1, verbosity)
    print(" LEARNER PLAYER --- alpha = ", alpha1)

    if args.opponenttype == "minimax":
        player_b = MinimaxPlayer(OPPONENT_PIECE)
        print(" OPPONENT IS A SMART MINIMAX PLAYER")
    elif args.opponenttype == "learner":
        player_b = LearnerPlayer(OPPONENT_PIECE, board, alpha2)
        print(" OPPONENT IS A LEARNER PLAYER --- alpha = ", alpha2)
    else:
        player_b = MinimaxPlayer(OPPONENT_PIECE, True)
        print(" OPPONENT IS A RANDOM (DUMB) PLAYER")

    # --------------------------------------------------
    # Play games
    print(" playing ", args.num_games, " games")
    results = {}
    results['player_a_win'] = 0
    results['player_b_win'] = 0
    results['draw'] = 0
    total_games = 0
    player_a_turn = True

    for _ in range(0, args.num_games):
        res = play_ai_vs_ai_game(player_a, player_b, board, player_a_turn, verbosity)
        total_games += 1
        update_results_and_print_statistics(res, total_games, results)
        if args.switch_turn:
            player_a_turn = not player_a_turn
        board.reset()

    # --------------------------------------------------
    # If requested, save learned data
    if args.savedata:
        np.savez(args.savedata, zobrist_hash = board.zhash_table,
                 value_tuple = player_a.values)
        ###print(board.zhash_table)
        ###print(player_a.values)

    # --------------------------------------------------
    # Exits
    sys.exit(0)


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
