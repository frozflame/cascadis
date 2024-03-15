#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import datetime
import mimetypes
from typing import Iterable, TypedDict

import pymongo.errors
from flask import request

from cascadis.environ import GlobalInterface

gi = GlobalInterface()


def query_by_file_id(file_id):
    coll = gi.mongodb.get_collection('file_registry')
    cursor = coll.find({'file_id': file_id})
    return list(cursor)


def legacy_register(file_id, path, ttl=86400):
    coll = gi.mongodb['file_registry']
    now = datetime.datetime.now()
    expired_at = now + datetime.timedelta(seconds=ttl)
    record = {
        'file_id': file_id, 'path': path,
        'created_at': now,
        'expired_at': expired_at,
    }
    try:
        ir = coll.insert_one(record)
    except pymongo.errors.DuplicateKeyError:
        return
    return ir.inserted_id


def register_and_query(file_id, path):
    reg_id = legacy_register(file_id, path)
    coll = gi.mongodb.get_collection('file_registry')
    for rec in coll.find({'_id': reg_id}):
        rec['_new'] = True
        yield rec
    yield from coll.find({'file_id': file_id, '_id': {'$ne': reg_id}})


def read_uploading_file(chunksize=16384) -> Iterable[bytes]:
    fup = request.files.get('file')
    while chunk := fup.stream.read(chunksize):
        yield chunk


class UploadRecord(TypedDict):
    cid: str
    method: str
    username: str
    mimetype: str | None
    filename: str | None


def register_http_upload(cid: str):
    coll = gi.mongodb['uploads']
    fup = request.files.get('file')
    record: UploadRecord = {
        'cid': cid,
        'method': 'http',
        'username': 'admin',
        'mimetype': fup.mimetype,
        'filename': fup.filename,
    }
    coll.insert_one(record)


def register_cli_upload(cid: str, filename: str):
    coll = gi.mongodb['uploads']
    record: UploadRecord = {
        'cid': cid,
        'method': 'cli',
        'username': 'admin',
        'mimetype': mimetypes.guess_type(filename)[0],
        'filename': filename,
    }
    coll.insert_one(record)
