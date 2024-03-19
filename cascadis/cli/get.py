#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import argparse
import os
import sys

from joker.cast.iterative import chunkwize
from volkanic.utils import printerr

from cascadis.environ import GlobalInterface

gi = GlobalInterface()


def get_file_from_cas(cid: str, path: str, overwrite=False):
    dir_ = os.path.split(path)[0]
    os.makedirs(dir_, exist_ok=True)
    exists = os.path.exists(path)
    if not overwrite and exists:
        print(cid, 'SKIPPED', path)
        return
    with open(path, 'wb') as fout:
        for chunk in gi.cas.load(cid):
            fout.write(chunk)
    action = 'OVERWRITTEN' if exists else 'CREATED'
    print(cid, action, path)


def main(_prog: str, args: list[str]):
    desc = 'Get files from Cascadis.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '-O', '--overwrite', action='store_true',
        help='overwrite existing files',
    )
    parser.add_argument('cid', help='content identifier')
    parser.add_argument('path', help='file to be created')
    parser.add_argument(
        'more', nargs='*', default=[],
        help='more cid and path pairs',
    )
    ns = parser.parse_args(args)
    if len(ns.more) % 2:
        printerr('wrong number of arguments')
        sys.exit(1)
    get_file_from_cas(ns.cid, ns.path, overwrite=ns.overwrite)
    for cid, path in chunkwize(2, ns.more):
        get_file_from_cas(cid, path, overwrite=ns.overwrite)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
