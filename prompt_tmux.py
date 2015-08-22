#! /usr/bin/python

import os
import sys
import urwid


class TuiPrompt:

  def AvailableChoice(self, hide_attached):
    cmd = 'tmux ls'
    if hide_attached:
      cmd += ' | grep -v "(attached)"'

    res = list(os.popen(cmd))
    return map(lambda x: (x.split(':')[0], x[:-1]), res)

  def item_chosen(self, button, c):
    self._final_choice = c
    raise urwid.ExitMainLoop()

  def WrapButtons(self, button_content_list):
    button_list = []
    for action, button_text in button_content_list:
      button = urwid.Button(button_text)
      urwid.connect_signal(button, 'click', self.item_chosen, action)
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
    available = self.AvailableChoice(hide_attached)
    if skip_choice:
      if len(available) == 0:
        self._final_choice = ''
        return
      elif len(available) == 1:
        self._final_choice = available[0][0]
        return
    urwid.MainLoop(
        self.WrapButtons(available + [('', 'Create new tmux session')]),
        palette=[('reversed', 'standout', '')]).run()

  def get(self):
    return self._final_choice


def OldSchoolShowAndType():
  os.popen('clear')
  res = list(os.popen('tmux list-sessions | grep -v "(attached)"'))
  l = len(res)
  if l == 0:
    return ''
  if l == 1:
    return res[0].split(':')[0]
  else:
    print '\n'.join(res)
    valid_sess = map(lambda x: x.split(':')[0], res)
    while True:
      resp = raw_input()
      if resp == '':
        return valid_sess[0]
      else:
        if resp in map(lambda x: x.split(':')[0], res):
          return resp
        else:
          #print 'enter a valid session name'
          return ''


if __name__ == '__main__':
  fast_start = True
  while True:
    sess_name = TuiPrompt(hide_attached=fast_start,
                          skip_choice=fast_start).get()
    if sess_name == '':
      os.popen('tmux')
    else:
      if len(sys.argv) == 1 or len(sys.argv[1]) == 0:
        t = """tmux new-window -t %s:0 \; send-keys -t %s:0 "prodaccess && echo 'closing in 5s' && sleep 5 && exit" Enter""" % (
            sess_name, sess_name)
        os.popen(t)
      os.popen('tmx %s' % (sess_name,))
    fast_start = False
