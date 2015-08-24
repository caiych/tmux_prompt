#! /usr/bin/python

import os
import sys
import urwid
import argparse


class TuiPrompt:
  """A text user interface, prompt to choose a tmux session.
  """

  def AvailableChoice(self, hide_attached):
    """Get all available sessions from command 'tmux ls'

    Args:
      hide_attached: set to True to skip sessions already attached by some
        client

    Returns:
      a list of (session name, displayed text)

    """
    cmd = 'tmux ls'
    if hide_attached:
      cmd += ' | grep -v "(attached)"'

    res = list(os.popen(cmd))
    return map(lambda x: (x.split(':')[0], x[:-1]), res)

  def ItemChosen(self, button, c):
    """Callback function for an action item.

    Will be called by urwid, when the button is hit.
    Set the self._final_choice and end the loop.

    Args:
      button: the urwid button item, automatically passed by urwid, never used
        in this method.
      c: session name
    Returns:
      An exit exception. Will be captured by urwid main loop.

    """
    self._final_choice = c
    raise urwid.ExitMainLoop()

  def WrapButtons(self, button_content_list):
    """Generate the urwid widget to display

    Args:
      button_content_list: genreated by self.AvailableChoice, a list of (session
        name, display text)

    Returns:
      a urwid widget, ready to render.
    """
    button_list = []
    for action, button_text in button_content_list:
      button = urwid.Button(button_text)
      urwid.connect_signal(button, 'click', self.ItemChosen, action)
      button_list.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.Overlay(
        urwid.ListBox(urwid.SimpleFocusListWalker(button_list)),
        urwid.SolidFill(),
        align='center',
        width=('relative', 60),
        valign='middle',
        height=('relative', 60),
        min_width=20,
        min_height=9)

  def __init__(self, hide_attached=True, skip_choice=True):
    """Construct the prompt object to start the TUI.

    Args:
      hide_attached: set to True to skip sessions attached by some clients.
      skip_choice: set to True when there's only one choice to make.
    Returns:
      None
    """
    available = self.AvailableChoice(hide_attached)
    if skip_choice:
      if len(available) == 0:
        # When there's no session, the only choice is to create a new one.
        self._final_choice = ''
        return
      elif len(available) == 1:
        # When there's only one session, the only choice is to attach to this
        # one.
        self._final_choice = available[0][0]
        return
    self._loop = urwid.MainLoop(
        self.WrapButtons(available + [('', 'Create new tmux session')]),
        palette=[('reversed', 'standout', '')],
        unhandled_input=self.UnHandledInput)
    self._loop.run()

  def get(self):
    return self._final_choice

  def UnHandledInput(self, k):
    if k == 'j':
      self._loop.process_input(['down'])
    elif k == 'k':
      self._loop.process_input(['up'])


if __name__ == '__main__':
  flags_parser = argparse.ArgumentParser(
      description=
      'Prompt to choose a tmux session, cannot be run within a tmux window.')
  flags_parser.add_argument(
      '--no_fast_start',
      action='store_true',
      help='Switch this flag to let the program shows all sessions(including '
      'attached), and not skip choosing anyway')
  flags_parser.add_argument(
      '--no_prompt_again',
      action='store_true',
      help='Swith this flag to let the program exit after detach sessions.')
  flags = flags_parser.parse_args()

  fast_start = not flags.no_fast_start
  while True:
    sess_name = TuiPrompt(hide_attached=fast_start,
                          skip_choice=fast_start).get()
    if sess_name == '':
      os.popen('tmux')
    else:
      os.popen('tmux attach -t %s' % (sess_name,))
    fast_start = False
    if flags.no_prompt_again:
      break
