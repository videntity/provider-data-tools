#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import sys
from datetime import datetime

from pymongo import MongoClient
import os
import sys
import string
import json
import csv
from collections import OrderedDict


MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017


def makepecos_fhir_db(database_name="pecos"):

    i = 0
    # try:

    mc = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = mc[database_name]
    base_collection = db['base']
    addresses_collection = db['addresses']
    reassignments_collection = db['reassignments']
    compiled_fhir_individuals_collection = db['compiled_individuals_fhir']
    compiled_fhir_organizations_collection = db['compiled_organizations_fhir']

    for bdoc in base_collection.find():
        i += 1
        d = OrderedDict()
        if bdoc['ENRLMT_ID'].startswith('O'):
            d['resourceType'] = "Organization"
        elif bdoc['ENRLMT_ID'].startswith('I'):
            d['resourceType'] = "Practitioner"

        # Get name
        name = OrderedDict()
        if bdoc['FIRST_NAME']:

            name['family'] = [bdoc['LAST_NAME']]
            name['given'] = [bdoc['FIRST_NAME']]

            d['name'] = [name]
        else:
            d['name'] = bdoc['ORG_NAME']

        # Description Extension
        # **extension for entire stript **
        extension = []
        description = OrderedDict()
        description['url'] = 'https://data.cms.gov/public-provider-enrollment'
        description['valueString'] = bdoc['PROVIDER_TYPE_DESC']
        extension.append(description)

        # NPI
        identifier = OrderedDict()
        identifier['value'] = bdoc['NPI']
        identifier['use'] = 'official'
        identifier['system'] = 'http://hl7.org/fhir/sid/us-npi'
        d['identifier'] = [identifier]

        extension_works_for = []
        extension_has_providers = []
        for rdoc in reassignments_collection.find(
                {"REASGN_BNFT_ENRLMT_ID": bdoc['ENRLMT_ID']}):

            ac = base_collection.find(
                {'ENRLMT_ID': rdoc["RCV_BNFT_ENRLMT_ID"]})
            for a in ac:
                # Create Codings
                npi_coding = OrderedDict()
                npi_coding[
                    'system'] = 'https://nppes.cms.hhs.gov/NPPES/Welcome.do'
                npi_coding['code'] = a['NPI']
                npi_coding['display'] = 'NPI number of affiliation'
                # Leaving off the 'userSelected' category for now.

                enrollmentid_coding = OrderedDict()
                enrollmentid_coding[
                    'system'] = 'https://data.cms.gov/public-provider-enrollment'
                enrollmentid_coding['code'] = a['ENRLMT_ID']
                enrollmentid_coding[
                    'display'] = 'PECOS Enrollment ID of affiliation'

                # Create Codeable concept
                value_codeable_concept = OrderedDict()
                value_codeable_concept['coding'] = [
                    npi_coding, enrollmentid_coding]
                if d['resourceType'] == "Organization":
                    value_codeable_concept['text'] = a[
                        'ORG_NAME'] + ',' + a['PROVIDER_TYPE_DESC']
                elif d['resourceType'] == "Practitioner":
                    value_codeable_concept['text'] = a[
                        'FIRST_NAME'] + ',' + a['LAST_NAME'] + ',' + a['PROVIDER_TYPE_DESC']

                # Create fhir affiliation from compiled_individuals
                affiliation = OrderedDict()
                affiliation[
                    'url'] = 'https://data.cms.gov/public-provider-enrollment'
                # print(value_codeable_concept['text'])
                affiliation['valueCodeableConcept'] = value_codeable_concept
                # wrap in list
                # affiliation = [affiliation]
                extension_works_for.append(affiliation)

        for rdoc in reassignments_collection.find(
                {"RCV_BNFT_ENRLMT_ID": bdoc['ENRLMT_ID']}):

            ac = base_collection.find(
                {'ENRLMT_ID': rdoc["REASGN_BNFT_ENRLMT_ID"]})
            for a in ac:
                # Create Codings
                npi_coding = OrderedDict()
                npi_coding[
                    'system'] = 'https://nppes.cms.hhs.gov/NPPES/Welcome.do'
                npi_coding['code'] = a['NPI']
                npi_coding['display'] = 'NPI number of affiliation'
                # Leaving off the 'userSelected' category for now.

                enrollmentid_coding = OrderedDict()
                enrollmentid_coding[
                    'system'] = 'https://data.cms.gov/public-provider-enrollment'
                enrollmentid_coding['code'] = a['ENRLMT_ID']
                enrollmentid_coding[
                    'display'] = 'PECOS Enrollment ID of affiliation'

                # Create Codeable concept
                value_codeable_concept = OrderedDict()
                value_codeable_concept['coding'] = [
                    npi_coding, enrollmentid_coding]
                if d['resourceType'] == "Organization":
                    value_codeable_concept['text'] = a[
                        'ORG_NAME'] + ',' + a['PROVIDER_TYPE_DESC']
                elif d['resourceType'] == "Practitioner":
                    value_codeable_concept['text'] = a[
                        'FIRST_NAME'] + ',' + a['LAST_NAME'] + ',' + a['PROVIDER_TYPE_DESC']

                # Create fhir affiliation from compiled_individuals
                affiliation = OrderedDict()
                affiliation[
                    'url'] = 'https://data.cms.gov/public-provider-enrollment'
                # print(value_codeable_concept['text'])
                affiliation['valueCodeableConcept'] = value_codeable_concept
                # wrap in list
                affiliation = affiliation
                extension_has_providers.append(affiliation)

        if extension_has_providers == []:
            # del d["extension_has_providers"]
            extension.append(extension_works_for)

        if extension_works_for == []:
            # del d["extension_works_for"]
            extension.append(extension_has_providers)
        d['extension'] = extension

        if d['resourceType'] == "Organization":
            compiled_fhir_organizations_collection.insert(d)
        elif d['resourceType'] == "Practitioner":
            compiled_fhir_individuals_collection.insert(d)

        # print json.dumps(d, indent =4)

    # Walk through base

    # except:
    #     print(sys.exc_info)

    print(i, "Processed")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("makepecosdocs.py [DATABASE NAME]")
        sys.exit(1)

    database_name = sys.argv[1]
    # Run it
    makepecos_fhir_db(database_name=database_name)
