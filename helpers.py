import os
import subprocess
import fileinput
import click
import fileinput
import json
import re

def is_canonical(version):
  return re.match(r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$', version) is not None


def get_git_tag():
  app_version = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('UTF-8').rstrip()
  if (('fatal' in app_version) or
     not is_canonical(app_version)):
    app_version = '0.0.1'
  else:
    app_version = app_version if app_version[0].lower() != 'v' else app_version[1:]

  return app_version


def pre_image_build(app_name):
  """Create the application configuration file.

  The version of the application is read from git tags.

  Args:
    app_name (str): The name of the application to
  """

  app_version = get_git_tag()

  # Update the version in the package __init__ file
  for line in fileinput.input(os.path.join("src", '__init__.py'), inplace=True):
    if line.startswith('__version__'):
      versions = app_version.split('-')
      app_version = versions[0]
      if len(app_version.split('.')) < 3 and len(versions) > 1:
        app_version += f".{versions[1]}"
      print(f"__version__ = '{app_version}'", end='\n')
    else:
      print(f"{line}", end='')


@click.command()
@click.argument('args', nargs=-1)
def main(args):
  switcher = {
    "pre_image_build": pre_image_build,
  }
  func = switcher.get(str(args[0]), lambda: None)

  if len(args) > 1:
    func(*args[1:])
  else:
    func()


if __name__ == '__main__':
  main()
