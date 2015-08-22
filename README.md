# Tmux prompt

A simple wrapper written in Python. Prompt to choose a session when you need.

## Usage

Default usage
> ./prompt_tmux.py

Flags
> ./prompt_tmux.py -h
> usage: prompt_tmux.py [-h] [--no_fast_start] [--no_prompt_again]

Prompt to choose a tmux session, cannot be run within a tmux window.

optional arguments:
  -h, --help         show this help message and exit
  --no_fast_start    Switch this flag to let the program shows all
                     sessions(including attached), and not skip choosing
                     anyway
  --no_prompt_again  Swith this flag to let the program exit after detach
                     sessions.
