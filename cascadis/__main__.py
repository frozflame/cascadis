#!/usr/bin/env python3
# coding: utf-8
import volkanic

cmddef = """
api     cascadis.api:main
atx     cascadis.atx:main
conf    cascadis.environ:main
shell   cascadis.cli.shell:main
reg     cascadis.cli.reg:main
misc    cascadis.misc:main
"""

_prog = 'python3 -m cascadis'
registry = volkanic.CommandRegistry.from_cmddef(cmddef, _prog)

if __name__ == '__main__':
    registry()
