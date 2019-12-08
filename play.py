#!/usr/bin/env python3
#
"""Play a series of tic-tac-toe games between an human and an AI player"""
from argparse import ArgumentParser

import jokettt

from jokettt.board.board import Board
from jokettt.players.consoleplayer import ConsolePlayer
from jokettt.players.minimaxplayer import MinimaxPlayer
from jokettt.players.learnerplayer import LearnerPlayer

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def play_human_vs_ai_game(human_player, ai_player, auto_player_first, board):
    """Play a tic-tac-toe game between an human and an AI player"""
    result = 0
    print("----------------------------------------------------")
    print("  --- NEW GAME ---")
    console_player_turn = not auto_player_first

    if console_player_turn:
        print('%s' % board)

    while result == 0 and board.is_not_full():

        if console_player_turn:
            _x, _y = human_player.move(board)
            _, result = board.place_pawn(_x, _y, human_player.piece)
        else:
            _x, _y = ai_player.move(board)
            _, result = board.place_pawn(_x, _y, ai_player.piece)
            result = -result

        print('%s' % board)
        console_player_turn = not console_player_turn

    print('%s' % board)

    if result < 0:
        # AI player wins
        return -1
    if result > 0:
        # Human wins
        if isinstance(ai_player, LearnerPlayer):
            ai_player.learn_from_defeat(board)
        return 1
    # draw
    return 0

# --------------------------------------------------------------------
# --------------------------------------------------------------------
#   ***  MAIN ***
# --------------------------------------------------------------------
# --------------------------------------------------------------------
AI_PIECE = 'x'
HUMAN_PIECE = 'o'
ALPHA_VALUE = 0.1
def main():
    """Main program: parses options, declare board and players, and
        plays a series of games"""
    parser = ArgumentParser()
    parser.add_argument("player_mode", help="the mode of the player",
                        choices=["minimax", "learner"], nargs='?', default="minimax")
    parser.add_argument("-s", "--second",
                        help="give the first move to the machine", action="store_true")
    parser.add_argument("-v", "--verbosity", action="count",
                        help="increase output verbosity")
    args = parser.parse_args()
    if args.verbosity:
        verbosity = args.verbosity
    else:
        verbosity = 0

    if args.second:
        print("FIRST MOVE TO THE MACHINE!")
    else:
        print("FIRST MOVE TO YOU!")

    print("TYPE OF AI PLAYER = {}".format(args.player_mode))

    board = Board(AI_PIECE, HUMAN_PIECE)
    if args.player_mode == "minimax":
        auto_player = MinimaxPlayer(AI_PIECE, False, verbosity)
    else:
        auto_player = LearnerPlayer(AI_PIECE, board, ALPHA_VALUE, verbosity)

    console_player = ConsolePlayer(HUMAN_PIECE, verbosity)

    while True:
        board.reset()
        res = play_human_vs_ai_game(console_player, auto_player, args.second, board)

        if res < 0:
            print("You lose! :-D")
        elif res > 0:
            print("You win!! :-(")
        else:
            print("Draw! ;-)")

if __name__ == "__main__":
    main()
