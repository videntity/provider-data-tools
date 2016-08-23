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


def ensure_provider_indexes(database_name, collection1, collection2, collection3,
                            host=MONGO_HOST, port=MONGO_PORT, background=True):
    """Apply suiteable indexes to pecos Base collection."""

    response_dict = OrderedDict()
    mc = MongoClient(host=host, port=port)
    db = mc[database_name]
    # PECOS Base
    try:

        collection = db[collection1]

        collection.create_index([("PROVIDER_TYPE_DESC", ASCENDING)],
                                background=background)

        collection.create_index([("ORG_NAME", ASCENDING)],
                                background=background)

        collection.create_index([("FIRST_NAME", ASCENDING)],
                                background=background)
        collection.create_index([("LAST_NAME", ASCENDING)],
                                background=background)
        collection.create_index([("NPI", ASCENDING)],
                                background=background)
        collection.create_index([("GNDR_SW", ASCENDING)],
                                background=background)
        collection.create_index([("STATE_CD", ASCENDING)],
                                background=background)
        collection.create_index([("MDL_NAME", ASCENDING)],
                                background=background)
        collection.create_index([("PROVIDER_TYPE_CD", ASCENDING)],
                                background=background)

        collection.create_index([("ENRLMT_ID", ASCENDING)],
                                background=background)

        collection.create_index([("PECOS_ASCT_CNTL_ID",
                                  ASCENDING)],
                                background=background)

        response_dict['collection1'] = collection1
        response_dict['created_indexes1'] = True
        response_dict['background1'] = background
    except:
        response_dict['collection1'] = collection1
        response_dict['code1'] = 500
        response_dict['errors1'] = [str(sys.exc_info()), ]
        response_dict['message1'] = str(sys.exc_info())

    # Reassignments

    try:
        collection = db[collection2]

        collection.create_index([("REASGN_BNFT_ENRLMT_ID", ASCENDING)],
                                background=background)

        collection.create_index([("RCV_BNFT_ENRLMT_ID", ASCENDING)],
                                background=background)

        collection.create_index([("RCV_BNFT_ENRLMT_ID", ASCENDING),
                                 ("REASGN_BNFT_ENRLMT_ID", ASCENDING)],
                                background=background)

        collection.create_index([("REASGN_BNFT_ENRLMT_ID", ASCENDING),
                                 ("RCV_BNFT_ENRLMT_ID", ASCENDING)],
                                background=background)

        response_dict['collection2'] = collection2
        response_dict['created_indexes2'] = True
        response_dict['background2'] = background
    except:
        response_dict['collection2'] = collection2
        response_dict['code2'] = 500
        response_dict['errors2'] = [str(sys.exc_info()), ]
        response_dict['message2'] = str(sys.exc_info())

    # PECOS Addresses
    try:

        collection = db[collection3]

        collection.create_index([("CITY_NAME", ASCENDING)],
                                background=background)

        collection.create_index([("STATE_CD", ASCENDING)],
                                background=background)

        # collection.create_index([("address.postalCode",     ASCENDING),
        #                          ("enumeration_type", ASCENDING),
        #                          ("addresses.city",   ASCENDING),
        #                          ("addresses.state",  ASCENDING),
        #                          ("basic.first_name", ASCENDING),
        #                          ("basic.last_name",  ASCENDING),
        #                          ("basic.organization_name", ASCENDING),
        #                          ("basic.doing_business_as", ASCENDING)
        #                          ], name="biggie",
        #                         background=background)

        collection.create_index([("ZIP_CD", ASCENDING)],
                                background=background)
        collection.create_index([("ENRLMT_ID", ASCENDING)],
                                background=background)
        collection.create_index([("id", ASCENDING)],
                                background=background)

        response_dict['collection3'] = collection3
        response_dict['created_indexes3'] = True
        response_dict['background3'] = background
    except:
        response_dict['collection3'] = collection3
        response_dict['code3'] = 500
        response_dict['errors3'] = [str(sys.exc_info()), ]
        response_dict['message3'] = str(sys.exc_info())

    return response_dict

if __name__ == "__main__":

    if len(sys.argv) != 8:
        print("Usage:")
        print("create_pecos_indexes.py [DATABASE] [PECOS BASE COLLECTION NAME] [PECOS REASSIGNMENTS COLLECTION NAME] [PECOS ADDRESSES COLLECTION NAME] [HOST] [PORT] [BACKGROUND Y/N]")
        sys.exit(1)

    database = sys.argv[1]
    collection1 = sys.argv[2]
    collection2 = sys.argv[3]
    collection3 = sys.argv[4]
    host = sys.argv[5]
    port = int(sys.argv[6])

    if sys.argv[7].lower() in ("y", "yes", "t", "true"):
        background = True
    else:
        background = False

    result = ensure_provider_indexes(
        database, collection1, collection2, collection3, host, port, background)
    print(json.dumps(result, indent=4))
