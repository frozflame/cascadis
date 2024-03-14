#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

from typing import TypedDict

from flask import request

from cascadium.environ import GlobalInterface

gi = GlobalInterface()


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
