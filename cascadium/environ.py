#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import logging
import os
from functools import cached_property
from pathlib import Path

import volkanic
from joker.filesys.cas import ContentAddressedStorage
from pymongo import MongoClient
from pymongo.database import Database
from redis import Redis
from volkanic.utils import ignore_arguments, indented_json_print

_logger = logging.getLogger(__name__)


class GlobalInterface(volkanic.GlobalInterface):
    package_name = 'cascadium'
    default_config = {
        "cache_ttl": 0,
        "proxy_ttl": 5,
        "upstream": "",
        "mongo": {},
        "accessibility": 1,
        "auth_tokens": [],
        "data_dir": "/data",
        "use_nginx": False,
        "test_account": {
            "username": "",
            "password": ""
        }
    }

    @cached_property
    def files(self) -> Path:
        path = Path(self.conf['data_dir']) / f'{self.project_name}.files'
        path.mkdir(parents=True, exist_ok=True)
        return path

    @cached_property
    def cas(self) -> ContentAddressedStorage:
        kwargs = {
            'base_dir': self.files,
            'hash_algo': 'sha256',
            'dir_depth': 2,
        }
        return ContentAddressedStorage(**kwargs)

    @cached_property
    def _mongodb_and_pid(self) -> tuple[Database, int]:
        cfg = self.conf['mongo']
        cfg = cfg.copy()
        cfg.setdefault('directConnection', True)
        _logger.info('using mongo cfg %s', cfg)
        client = MongoClient(**cfg)
        return client.get_database(self.identifier), os.getpid()

    @property
    def mongodb(self):
        database, pid = self._mongodb_and_pid
        # for a new process, create a new MongoClient instance
        if pid != os.getpid():
            self.__dict__.pop('_mongodb_and_pid')
            database = self._mongodb_and_pid[0]
        return database

    @cached_property
    def redis(self) -> Redis:
        return Redis(**self.conf.get('redis', {}))


@ignore_arguments
def main():
    gi = GlobalInterface()
    indented_json_print(gi.conf)
    print('files:', gi.files)
