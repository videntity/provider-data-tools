#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import os
import sys
import json
import jsonschema
from jsonschema import exceptions
from collections import OrderedDict


def json_schema_check_fhir(fhir_key_word_schema, json_string):

    input_json_string = json.loads(json_string)
    fhir_json_schema = os.path.join(os.path.dirname(
        __file__), 'fhir_json_schema', '%s.json' % (fhir_key_word_schema))

    with open(fhir_json_schema) as json_schema:
        deserialized_json_schema = json.load(json_schema)

    v = jsonschema.Draft4Validator(deserialized_json_schema)
    errors = sorted(v.iter_errors(input_json_string), key=lambda e: e.path)
    for error in errors:
        print(error.message)

    """JSON SCHEMA CHECK"""
    results = OrderedDict()
    if errors:
        results['errors'] = errors

    else:
        results['errors'] = []
        results[
            'results'] = "Congrats! The JSON file fits the schema. There were no errors."

    return results

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage:")
        print("json_schema_check_fhir.py [FHIR JSON SCHEMA] [JSON STRING]")
        sys.exit(1)

    fhir_key_word_schema = sys.argv[1]
    json_string = sys.argv[2]

    result = json_schema_check_fhir(fhir_key_word_schema, json_string)
    print(json.dumps(result, indent=4))
