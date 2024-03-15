#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import importlib
import json
import re

import setuptools
from volkanic.introspect import find_all_plain_modules
from volkanic.utils import printerr

from cascadis.environ import GlobalInterface

gi = GlobalInterface()

dotpath_prefixes = [
    'cascadis.',
    'tests.',
]


def test_json_integrity():
    for path in gi.project_dir.rglob('*.json'):
        print('checking json file', path)
        json.load(path.open())


def _check_prefix(path):
    for prefix in dotpath_prefixes:
        if path.startswith(prefix):
            return True
    return False


def test_module_imports():
    pdir = gi.under_project_dir()
    for dotpath in find_all_plain_modules(pdir):
        if _check_prefix(dotpath):
            print('importing', dotpath)
            importlib.import_module(dotpath)


def read_all_py_files():
    pdir = gi.under_project_dir()
    for path in setuptools.findall(pdir):
        if not path.endswith('.py'):
            continue
        for idx, line in enumerate(open(path)):
            line = line.strip()
            if not line:
                continue
            yield path, idx, line


def test_error_key_uniqueness():
    regex = re.compile(r'TE-\w+')
    location_of_error_keys = {}
    for path, idx, line in read_all_py_files():
        loc = f'{path}:{idx}'
        if not (mat := regex.search(line)):
            continue
        ek = mat.group()
        if ek in location_of_error_keys:
            printerr(ek, *location_of_error_keys[ek])
            printerr(ek, loc, line)
            raise ValueError(f'duplicate error key "{ek}"')
        location_of_error_keys[ek] = loc, line


if __name__ == '__main__':
    test_module_imports()
    test_error_key_uniqueness()
    test_json_integrity()
