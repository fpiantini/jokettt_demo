# jokettt_demo
Demo programs for the [jokettt](https://github.com/fpiantini/jokettt) tic-tac-toe demo engine.

## Setup

Conda is used to setup the development environment. To setup the environment, the first time enter the following command:

```bash
conda env create
```

And enter the following command to activate the ```jokettt_demo``` conda env:

```bash
conda activate jokettt_demo
```

## Demos

To play a game against an invincible Minimax engine:

```bash
./play.sh minimax
```

To play a series of games against a "learning" engine:

```bash
./play.sh learner
```

To watch the minimax engine and the learner engine figthing one against the other in multiple games, enter the command:

```bash
./play_ai.py -m -f minimax -s learner
```