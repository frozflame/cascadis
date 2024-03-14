#!/usr/bin/env python3
# coding: utf-8
import volkanic

cmddef = """
api     cascadium.api:main
atx     cascadium.atx:main
conf    cascadium.environ:main
shell   cascadium.shell:main
"""

_prog = 'python3 -m cascadium'
registry = volkanic.CommandRegistry.from_cmddef(cmddef, _prog)

if __name__ == '__main__':
    registry()
