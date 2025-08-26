#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

from pymongo import MongoClient, ASCENDING, DESCENDING
import os
import sys
import string
import json
import functools
import pymongo
import time
import hashlib
import os
from bson.json_util import dumps

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017


def dump_pecos_compiled_to_disk(directory,
        database, collection_name, host, port):
    """Apply suiteable indexes to combined nppes/pecos fhir collection."""

    response_dict = {}
    mc = MongoClient(host=host, port=port)
    db = mc[database]
    i=0
    try:
        os.makedirs(f"{directory}/", exist_ok=True)
        collection = db[collection_name]

        objects = collection.find({})
        for o in objects:
            jsontext = dumps(o, indent=2, ensure_ascii=False)
            del o['_id']
            directory_fan = o['npi'][0:4]
            fdirectory = os.path.join(directory, directory_fan)
            os.makedirs(f"{fdirectory}/", exist_ok=True)
            filename = os.path.join(fdirectory, o['npi'] + ".json")
            with open(filename, 'w') as f:
                f.write(jsontext)
            i += 1
            if i % 1000 == 0:
                print(i)


    except:
        response_dict['collection'] = collection_name
        response_dict['code'] = 500
        response_dict['errors'] = [str(sys.exc_info()), ]
        response_dict['message'] = str(sys.exc_info())
    
    return response_dict

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage:")
        print(
            "dump_pecos_compiled_to_disk.py [DIRECTORY] [DATABASE] [COMPILED_COLLECTION]")
        sys.exit(1)
    directory = sys.argv[1]
    database = sys.argv[2]
    collection = sys.argv[3]
    host = "127.0.0.1"
    port = 27017

   

    result = dump_pecos_compiled_to_disk(directory, database, 
                                        collection, host, port)
    print(json.dumps(result, indent=4))
