#!/usr/bin/env python
import argparse
import os
import re
import shutil
import sys

from ConfigParser import SafeConfigParser


PARSER = argparse.ArgumentParser(description="Import some aliases")
PARSER.add_argument('profile', help="Profile to output config for")
PARSER.add_argument('-c', '--config',
                    default='~/.akrc',
                    help="Directory where profiles are stored")
PARSER.add_argument('--init-alias',
                    default='ak',
                    help="When using the 'init' profile, the alias "
                         "name to insert")


ALIAS_RE = re.compile('^[A-Za-z0-9 _-]+$')


def profile_filename(config_dir, profile_name):
  return os.path.expanduser('%s/%s.ini' % (config_dir, profile_name))


def main():
  args = PARSER.parse_args()

  if args.profile == 'init':
    write_init_profile(args.config, args.init_alias)

  profile_fn = profile_filename(args.config, args.profile)
  profile_commands_dir = os.path.expanduser('%s/.%s' % (args.config, args.profile))

  sys.stderr.write("Using profile in '%s'\n" % profile_fn)

  config = SafeConfigParser()
  config.read(profile_fn)

  try:
    shutil.rmtree(profile_commands_dir, ignore_errors=True)
  except OSError:
    pass

  os.mkdir(profile_commands_dir)

  for alias, command in config.items('aliases'):
    if not ALIAS_RE.match(alias):
      sys.stderr.write("Alias '%s' not allowed; skipped\n" % alias)
      continue

    if '$@' not in command:
      command = '%s "$@"' % command

    command_fn = '%s/%s' % (profile_commands_dir, alias)
    with open(command_fn, 'w') as handle:
      handle.write(command)

    print "function '%s' { eval \"$(cat '%s')\" }" % (alias, command_fn)


def write_init_profile(config_dir, init_alias):
  try:
    os.mkdir(os.path.expanduser(config_dir))
  except OSError:
    pass

  my_abs_path = os.path.abspath(os.path.expanduser(__file__))
  with open(profile_filename(config_dir, 'init'), 'w') as handle:
    handle.write('[aliases]\n')
    handle.write('{init_alias} = eval "$("{my_path}" "$@")"'.format(
      init_alias=init_alias,
      my_path=my_abs_path,
    ))


if __name__ == '__main__':
  main()
