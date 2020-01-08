#!/usr/bin/env python3
#
"""Play a series of tic-tac-toe games between an human and an AI player"""
from argparse import ArgumentParser

import sys
import random

import numpy as np

from jokettt.board import Board
from jokettt.consoleplayer import ConsolePlayer
from jokettt.minimaxplayer import MinimaxPlayer
from jokettt.learnerplayer import LearnerPlayer

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def play_human_vs_ai_game(human_player, ai_player, first_ai, board):
    """Play a tic-tac-toe game between an human and an AI player"""
    result = 0
    print("----------------------------------------------------")
    if first_ai:
        print("  --- NEW GAME --- My turn to begin ---")
    else:
        print("  --- NEW GAME --- Your turn to begin ---")

    console_player_turn = not first_ai

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

    # --------------------------------------------------
    # 1. PARSE COMMAND LINE ARGUMENTS
    parser = ArgumentParser()
    parser.add_argument("player_mode", help="the mode of the player",
                        choices=["minimax", "learner"], nargs='?', default="minimax")
    parser.add_argument("-v", "--verbosity", action="count",
                        help="increase output verbosity")
    args = parser.parse_args()
    if args.verbosity:
        verbosity = args.verbosity
    else:
        verbosity = 0

    # --------------------------------------------------
    # 2. PRINTS SOME INFORMATION
    print("TYPE OF AI PLAYER = {}".format(args.player_mode))

    # --------------------------------------------------
    # 3. DECLARES BOARD AND PLAYERS
    board = Board(AI_PIECE, HUMAN_PIECE)
    if args.player_mode == "minimax":
        auto_player = MinimaxPlayer(AI_PIECE, False, verbosity)
    else:
        auto_player = LearnerPlayer(AI_PIECE, board, {}, ALPHA_VALUE, verbosity)

    console_player = ConsolePlayer(HUMAN_PIECE, verbosity)

    # --------------------------------------------------
    # 4. PLAYS!
    first_ai = False   # first move of first game is for human
    while True:
        board.reset()

        res = play_human_vs_ai_game(console_player, auto_player, first_ai, board)

        if res < 0:
            print("You lose! :-D")
        elif res > 0:
            print("You win!! :-(")
        else:
            print("Draw! ;-)")

        # change turn
        first_ai = not first_ai

if __name__ == "__main__":
    main()
