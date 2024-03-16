#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import os
import sys

from volkanic.utils import printerr

from cascadis.environ import GlobalInterface

gi = GlobalInterface()


def main(_prog: str, args: list[str]):
    cid, filename = args
    if os.path.exists(filename):
        printerr(f'refuse to overwrite existing: {filename}')
        sys.exit(1)
    with open(filename, 'wb') as fout:
        for chunk in gi.cas.load(cid):
            fout.write(chunk)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
