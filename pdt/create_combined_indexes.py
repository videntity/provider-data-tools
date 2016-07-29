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


def ensure_provider_indexes(database_name, collection1, collection2, host=MONGO_HOST,
                            port=MONGO_PORT, background=True):
    """Apply suiteable indexes to combined nppes/pecos fhir collection."""

    response_dict = OrderedDict()
    mc = MongoClient(host=host, port=port)
    db = mc[database_name]
    try:


        collection = db[collection1]

        collection.create_index([("identifier.value", ASCENDING)],
                                background=background)

        collection.create_index([("telecom.value", ASCENDING)],
                                background=background)

        collection.create_index([("address.postalCode", ASCENDING)],
                                background=background)
        collection.create_index([("address.state", ASCENDING)],
                                background=background)
        collection.create_index([("address.city", ASCENDING)],
                                background=background)
        collection.create_index([("address.line", ASCENDING)],
                                background=background)
        collection.create_index([("name.suffix", ASCENDING)],
                                background=background)
        collection.create_index([("name.given", ASCENDING)],
                                background=background)
        collection.create_index([("name.family", ASCENDING)],
                                background=background)

        collection.create_index([("name.suffix", ASCENDING)],
                                background=background)

        collection.create_index([("extension.valueCodeableConcept.coding.code",
                                  ASCENDING)],
                                background=background)

        response_dict['collection1'] = collection1
        response_dict['created_indexes'] = True
        response_dict['background'] = background
    except:
        response_dict['collection1'] = collection1
        response_dict['code'] = 500
        response_dict['errors'] = [str(sys.exc_info()), ]
        response_dict['message'] = str(sys.exc_info())

    # Combined Organizations

    try:

        collection = db[collection2]

        collection.create_index([("identifier.value", ASCENDING)],
                                background=background)

        collection.create_index([("telecom.value", ASCENDING)],
                                background=background)
        collection.create_index([("contact.telecom.value", ASCENDING)],
                                background=background)

        collection.create_index([("address.postalCode", ASCENDING)],
                                background=background)
        collection.create_index([("address.state", ASCENDING)],
                                background=background)
        collection.create_index([("address.city", ASCENDING)],
                                background=background)
        collection.create_index([("address.line", ASCENDING)],
                                background=background)
        collection.create_index([("name", ASCENDING)],
                                background=background)
        collection.create_index([("contact.name.prefix", ASCENDING)],
                                background=background)
        collection.create_index([("contact.name.given", ASCENDING)],
                                background=background)
        collection.create_index([("contact.name.family", ASCENDING)],
                                background=background)

        collection.create_index([("contact.name.suffix", ASCENDING)],
                                background=background)

        collection.create_index([("extension.valueCodeableConcept.coding.code",
                                  ASCENDING)],
                                background=background)

        response_dict['collection2'] = collection2
        response_dict['created_indexes2'] = True
        response_dict['background2'] = background
    except:
        response_dict['collection2'] = collection2
        response_dict['code2'] = 500
        response_dict['errors2'] = [str(sys.exc_info()), ]
        response_dict['message2'] = str(sys.exc_info())

    return response_dict

if __name__ == "__main__":

    if len(sys.argv) != 7:
        print("Usage:")
        print(
            "create_combined_indexes.py [DATABASE] [COMBINED PRACTITIONER COLLECTION NAME] [COMBINED ORGANIZATION COLLECTION NAME] [HOST] [PORT] [BACKGROUND Y/N]")
        sys.exit(1)

    database = sys.argv[1]
    collection1 = sys.argv[2]
    collection2 = sys.argv[3]
    host = sys.argv[4]
    port = int(sys.argv[5])

    if sys.argv[6].lower() in ("y", "yes", "t", "true"):
        background = True
    else:
        background = False

    result = ensure_provider_indexes(
        database, collection1, collection2, host, port, background)
    print(json.dumps(result, indent=4))
