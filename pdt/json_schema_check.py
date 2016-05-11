#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import os, sys, json, jsonschema
from jsonschema import exceptions
from collections import OrderedDict



def json_schema_check(json_schema_path, file_to_check_path):

    with open(file_to_check_path) as json_file:
        deserialized_json_file = json.load(json_file)
        # print deserialized_json_file

    with open(json_schema_path) as json_schema:
        deserialized_json_schema = json.load(json_schema)
        # print deserialized_json_schema


    # print(exceptions.best_match(jsonschema.Draft4Validator(deserialized_json_schema).iter_errors(11)).message)
    v = jsonschema.Draft4Validator(deserialized_json_schema)
    errors = sorted(v.iter_errors(deserialized_json_file), key=lambda e: e.path)
    for error in errors:
        print(error.message)
    # for error in errors:
    #     for suberror in sorted(error.context, key=lambda e: e.schema_path):
    #         print(list(suberror.schema_path), suberror.message)


    # jsonschema.validate(deserialized_json_file, deserialized_json_schema)

    """JSON SCHEMA CHECK"""
    results = OrderedDict()
    # results['hello']="World"
    if errors:
        results['errors'] = errors

    else:
        results['results'] = "Congrats! The JSON file fits the schema. There were no errors."


    return results

if __name__ == "__main__":


    if len(sys.argv)!=3:
        print("Usage:")
        print("json_schema_check.py [JSON SCHEMA] [JSON FILE TO CHECK]")
        sys.exit(1)

    json_schema_path   = sys.argv[1]
    file_to_check_path = sys.argv[2]

    result = json_schema_check(json_schema_path, file_to_check_path)
    #output the JSON transaction summary
    print(json.dumps(result, indent =4))
