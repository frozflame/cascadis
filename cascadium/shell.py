#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

from cascadium.environ import GlobalInterface

gi = GlobalInterface()


def main(_prog, _args):
    try:
        from IPython import start_ipython
        start_ipython([], user_ns=globals())
    except ImportError:
        pass
