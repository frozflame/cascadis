#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import os
import sys
from concurrent.futures import ThreadPoolExecutor

from joker.cast.iterative import chunkwize

from cascadis.environ import GlobalInterface
from cascadis.solutions import register_cli_upload
from cascadis.utils import find_regular_files

gi = GlobalInterface()


def put_file_into_cas(path):
    with open(path, 'rb') as fin:
        content = fin.read()
        cid = gi.cas.save([content])
        path = os.path.abspath(path)
        print(cid, path)
    register_cli_upload(cid, path)
    return cid


def put_files_in_dir_into_cas(dirpath):
    executor = ThreadPoolExecutor(max_workers=10)
    paths = find_regular_files(dirpath)
    for batch in chunkwize(1000, paths):
        executor.map(put_file_into_cas, batch)


def main(_prog: str, args: list[str]):
    for path in args:
        if os.path.isdir(path):
            put_files_in_dir_into_cas(path)
        else:
            put_file_into_cas(path)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
