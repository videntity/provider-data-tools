#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

from pymongo import MongoClient, ASCENDING, DESCENDING
import os
import sys
import string
import json
from collections import OrderedDict

import functools
import pymongo
import time
import hashlib

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017


def ensure_provider_indexes(database_name, collection1, host=MONGO_HOST,
                            port=MONGO_PORT, background=True):
    """Apply suiteable indexes to pecos compiled collection."""
    mc = MongoClient(host=host, port=port)
    db = mc[database_name]

    response_dict = OrderedDict()
    try:

        collection = db[collection1]

        collection.create_index([("NAME", ASCENDING)],
                                background=background)

        collection.create_index([("DESCRIPTION", ASCENDING)],
                                background=background)

        collection.create_index([("NPI", ASCENDING)],
                                background=background)
        collection.create_index([("works_for.NAME", ASCENDING)],
                                background=background)
        collection.create_index([("works_for.NPI", ASCENDING)],
                                background=background)
        collection.create_index([("works_for.ENRLMT_ID", ASCENDING)],
                                background=background)
        collection.create_index([("works_for.DESCRIPTION", ASCENDING)],
                                background=background)
        collection.create_index([("has_providers.NAME", ASCENDING)],
                                background=background)
        collection.create_index([("has_providers.NPI", ASCENDING)],
                                background=background)
        collection.create_index([("has_providers.ENRLMT_ID", ASCENDING)],
                                background=background)
        collection.create_index([("has_providers.DESCRIPTION", ASCENDING)],
                                background=background)
        response_dict['collection'] = collection1
        response_dict['created_indexes'] = True
        response_dict['background'] = background
    except:
        response_dict['collection'] = collection1
        response_dict['code'] = 500
        response_dict['errors'] = [str(sys.exc_info()), ]
        response_dict['message'] = str(sys.exc_info())

    

    return dict(response_dict)

if __name__ == "__main__":

    if len(sys.argv) != 6:
        print("Usage:")
        print("create_pecos_compiled_indexes.py [DATABASE] [PECOS COMPILED INDIVIDUALS COLLECTIONS NAME]  [HOST] [PORT] [BACKGROUND Y/N]")
        sys.exit(1)

    database = sys.argv[1]
    collection1 = sys.argv[2]
    host = sys.argv[3]
    port = int(sys.argv[4])

    if sys.argv[5].lower() in ("y", "yes", "t", "true"):
        background = True
    else:
        background = False

    result = ensure_provider_indexes(
        database, collection1, host, port, background)
    print(json.dumps(result, indent=4))
