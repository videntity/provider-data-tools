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


def make_pecos_nppes_fhir_docs(database_name="pecos"):

    i = 0
    try:

        mc = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db = mc[database_name]
        fhir_organization = db['fhir_organization']
        addresses = db['addresses']
        base_pecos = db['base']
        compiled_organizations_collection = db['compiled_organizations']

        for bdoc in fhir_organization.find():
            #Counter for display

            i += 1
    # ----------------------------------------------------
    # INCORPORATE ADDRESSES and other ID's
    # ----------------------------------------------------
            try:
                match_bases = base_pecos.find({'NPI': bdoc['identifier'][0]['value']})
            except KeyError:
                continue
            m_addresses = []
            identifiers = []
            for matches in match_bases:
                try:
                    match_addresses = addresses.find({'ENRLMT_ID': matches['ENRLMT_ID']})
                except KeyError:
                    continue
                for ma in match_addresses:
                    # Create fhir address from pecos addresses
                    address = OrderedDict()
                    address['use'] = 'work'
                    address['postalCode'] = ma['ZIP_CD']
                    address['city'] = ma['CITY_NAME']
                    address['country'] = 'USA'
                    address['state'] = ma['STATE_CD']
                    # I don't think that text is exactly meant for this purpose, but
                    # we're using it here for now.
                    address['text'] = 'PECOS data practice location'
                    # Append address and remove duplicates
                    if address not in m_addresses:
                        m_addresses.append(address)

                # Other Identifiers: ENRLMT_ID, PECOS_ASCT_CNTL_ID
                enrlmt_id = OrderedDict()
                enrlmt_id['use'] = 'official'
                enrlmt_id_cc = OrderedDict()
                enrlmt_id_cc['text'] = 'Enrollment ID in PECOS basic data set'
                enrlmt_id['type'] = enrlmt_id_cc
                enrlmt_id['system'] = 'https://data.cms.gov/public-provider-enrollment'
                enrlmt_id['value'] = matches['ENRLMT_ID']
                if enrlmt_id not in identifiers:
                    identifiers.append(enrlmt_id)

                # PECOS_ASCT_CNTL_ID
                pecosAsctCntlId = OrderedDict()
                pecosAsctCntlId['use'] = 'official'
                pecosAsctCntlId_cc = OrderedDict()
                pecosAsctCntlId_cc['text'] = 'PECOS_ASCT_CNTL_ID in PECOS basic data set'
                pecosAsctCntlId['type'] = pecosAsctCntlId_cc
                pecosAsctCntlId['system'] = 'https://data.cms.gov/public-provider-enrollment'
                pecosAsctCntlId['value'] = matches['PECOS_ASCT_CNTL_ID']
                if pecosAsctCntlId not in identifiers:
                    identifiers.append(pecosAsctCntlId)
    # --------------------------------------------------------------
    # INCORPORATE AFFILIATIONS
    # --------------------------------------------------------------
            # Match up npi numbers between pecos and nppes
            try:
                match_compiled_organizations = compiled_organizations_collection.find(
                    {'NPI': bdoc['identifier'][0]['value']})
            except KeyError:
                continue
            extensions = []
            for mco in match_compiled_organizations:
                try:
                    # Create Codings
                    npi_coding = OrderedDict()
                    npi_coding['system'] = 'https://nppes.cms.hhs.gov/NPPES/Welcome.do'
                    npi_coding['code'] = mco['has_providers'][0]['NPI']
                    npi_coding['display'] = 'NPI number of affiliation'
                    # Leaving off the 'userSelected' category for now.

                    enrollmentid_coding = OrderedDict()
                    enrollmentid_coding['system'] = 'https://data.cms.gov/public-provider-enrollment'
                    enrollmentid_coding['code'] = mco['has_providers'][0]['ENRLMT_ID']
                    enrollmentid_coding['display'] = 'PECOS Enrollment ID of affiliation'

                    # Create Codeable concept
                    value_codeable_concept = OrderedDict()
                    value_codeable_concept['coding'] = [npi_coding, enrollmentid_coding]
                    value_codeable_concept['text'] = mco['has_providers'][0]['NAME'] + ', ' + mco['has_providers'][0]['DESCRIPTION']

                    # Create fhir affiliation from compiled_individuals
                    affiliation = OrderedDict()
                    affiliation['url'] = 'https://data.cms.gov/public-provider-enrollment'
                    # print(value_codeable_concept['text'])
                    affiliation['valueCodeableConcept'] = value_codeable_concept
                    # wrap in list, and remove duplicates
                    if affiliation not in extensions:
                        extensions.append(affiliation)
                except KeyError:
                    continue



            fhir_organization.update_one({"_id":bdoc['_id']}, {"$pushAll": {"extension": extensions, "address": m_addresses, "identifier": identifiers}}, upsert=True)
            # if d['resourceType'] == "Organization":
            #     compiled_organizations_collection.insert(d)
            # elif d['resourceType'] == "Practitioner":
            #     compiled_individuals_collection.insert(d)

            # print json.dumps(d, indent =4)

        # Walk through base

    except:
        print(sys.exc_info())

    print(i, "Processed")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("make_pecos_nppes_org_fhir.py [DATABASE NAME]")
        sys.exit(1)

    database_name = sys.argv[1]
    # Run it
    make_pecos_nppes_fhir_docs(database_name=database_name)
