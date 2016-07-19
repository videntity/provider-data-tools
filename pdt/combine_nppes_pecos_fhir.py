#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import sys
import os
import sys
import string
import json
import csv
import pprint
from datetime import datetime
from pymongo import MongoClient
from collections import OrderedDict


MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017


def makepecos_fhir_docs(database_name="fhir"):

    i = 0
    # try:

    mc = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = mc[database_name]
    nppes_practitioner = db['Practitioner']
    fhir_practitioner = db['fhir_practitioner']
    addresses = db['addresses']
    base_pecos = db['base']
    compiled_individuals_collection = db['compiled_individuals']

    for bdoc in nppes_practitioner.find():
        #Counter for display
        i += 1
        # Insert initial nppes document into new collection
        fhir_practitioner.insert(bdoc)
        # Match up npi numbers between pecos and nppes
        match = compiled_individuals_collection.find_one(
            {'NPI': bdoc['identifier'][0]['value']})
        match_base = base_pecos.find_one({'NPI': bdoc['identifier'][0]['value']})
        match_address = addresses.find_one({'ENRLMT_ID': match_base['ENRLMT_ID']})
        # Create fhir address from pecos addresses
        address = OrderedDict()
        address['use'] = 'work'
        address['postalCode'] = match_address['ZIP_CD']
        address['city'] = match_address['CITY_NAME']
        address['country'] = 'USA'
        address['state'] = match_address['STATE_CD']
        # I don't think that text is exactly meant for this purpose, but
        # we're using it here for now.
        address['text'] = 'PECOS data practice location'
        # Append address
        fhir_practitioner.update_one(bdoc,
                                      {"$push": {"address": address}})

        # Create Codings
        npi_coding = OrderedDict()
        npi_coding['system'] = 'https://nppes.cms.hhs.gov/NPPES/Welcome.do'
        npi_coding['code'] = match['works_for'][0]['NPI']
        npi_coding['display'] = 'NPI number of affiliation'
        # Leaving off the 'userSelected' category for now.

        enrollmentid_coding = OrderedDict()
        enrollmentid_coding['system'] = 'https://data.cms.gov/public-provider-enrollment'
        enrollmentid_coding['code'] = match['works_for'][0]['ENRLMT_ID']
        enrollmentid_coding['display'] = 'PECOS Enrollment ID of affiliation'

        # Create Codeable concept
        value_codeable_concept = OrderedDict()
        value_codeable_concept['coding'] = [npi_coding, enrollmentid_coding]
        value_codeable_concept['text'] = match['works_for'][0]['NAME'] + ',' + match['works_for'][0]['DESCRIPTION']

        # Create fhir affiliation from compiled_individuals
        affiliation = OrderedDict()
        affiliation['url'] = 'https://data.cms.gov/public-provider-enrollment'
        # print(value_codeable_concept['text'])
        affiliation['valueCodeableConcept'] = value_codeable_concept
        # wrap in list
        affiliation = [affiliation]
        fhir_practitioner.update_one(bdoc, {"$push": {"extension": affiliation}})
        # if d['resourceType'] == "Organization":
        #     compiled_organizations_collection.insert(d)
        # elif d['resourceType'] == "Practitioner":
        #     compiled_individuals_collection.insert(d)

        # print json.dumps(d, indent =4)

    # Walk through base

    # except:
    #     print(sys.exc_info())

    print(i, "Processed")


if __name__ == "__main__":

    if len(sys.argv) != 1:
        print("Usage:")
        print("makepecos_fhir_docs.py")
        sys.exit(1)

    # Run it
    makepecos_fhir_docs()
