# Tmux prompt

A simple wrapper written in Python. Prompt to choose a session when you need.

## Usage

Default usage
```
./prompt_tmux.py
```

Flags
```
./prompt_tmux.py -h
usage: prompt_tmux.py [-h] [--no_fast_start] [--no_prompt_again]

Prompt to choose a tmux session, cannot be run within a tmux window.

optional arguments:
  -h, --help         show this help message and exit
  --no_fast_start    Switch this flag to let the program shows all
                     sessions(including attached), and not skip choosing
                     anyway
  --no_prompt_again  Swith this flag to let the program exit after detach
                     sessions.
```

It rational to put something like this in your .bashrc or .zshrc:

```shell
if [[ ! $TERM =~ screen ]]; then
  exec /path/to/the/prompt_tmux.py # flags you prefer
fi
```

It's likely you've already have similar if but a simple tmux inside. Just
replace tmux with the exec command above, and you are ready to go.
