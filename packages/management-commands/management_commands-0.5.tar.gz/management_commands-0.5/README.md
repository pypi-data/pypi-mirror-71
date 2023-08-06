# Commands
Extra small zero-dependency management commands library for python apps

# Installation
`pip3 install management_commands`

# Example
```python
import os

from management_commands import Command, main


class Ls(Command):
    def add_arguments(self, parser):
        parser.add_argument('-1', action='store_true', dest='onecol')
        parser.add_argument('path')

    def handle(self, onecol, path, **kwargs) -> None:
        sep = ', '

        if onecol:
            sep = '\n'

        print(sep.join(os.listdir(path)))


if __name__ == '__main__':
    main(commands=[Ls()])
```

```bash
$ python3 example.py 
usage: example.py [-h] {ls} ...

$ python3 example.py --help
usage: example.py [-h] {ls} ...

optional arguments:
  -h, --help  show this help message and exit

commands:
  {ls}

$ python3 example.py ls .
LICENSE, dist, Makefile, MANIFEST.in, README.md, commands.egg-info, setup.py, example.py, .gitignore, management_commands, management_commands.egg-info, venv, .git, .idea

$ python3 example.py ls -1 .
LICENSE
dist
Makefile
MANIFEST.in
README.md
commands.egg-info
setup.py
example.py
.gitignore
management_commands
management_commands.egg-info
venv
.git
.idea
```
