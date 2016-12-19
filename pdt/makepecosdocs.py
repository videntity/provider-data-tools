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
import random
from random import randint

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017


STATUS_CHOICES = ("Y", "Y", "Y", "Y", "N")
TIN_TYPE_CHOICES = ("S", "S", "S", "S", "S", "S", "E", "E" "I")

TIN_CHOICES = ("560611570"
               "560611571",
               "560611572",
               "560611573",
               "560611574",
               "560611575")

APM_PROGRAM_NAME_CHOICES = ('SSP', 'Nextgen')


PART_B_CHOICES = ("Y", "N")


def makepecosdb(database_name="pecos", collection_name="compiled"):

    i = 0
    try:

        mc = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db = mc[database_name]
        # Drop old collections
        try:
            db.drop_collection('compiled_individuals')
            db.drop_collection('compiled_organizations')
            db.drop_collection('compiled')
        except:
            print(sys.exc_info)
        base_collection = db['base']
        addresses_collection = db['addresses']
        reassignments_collection = db['reassignments']
        specialties_collection = db['specialties']
        compiled_individuals_collection = db['compiled_individuals']
        compiled_organizations_collection = db['compiled_organizations']
        compiled_collection = db['compiled']

        for bdoc in base_collection.find():
            i += 1
            d = OrderedDict()

            d['pecos_id'] = bdoc['PECOS_ASCT_CNTL_ID']
            d['enrollment_id'] = bdoc['ENRLMT_ID']
            d['npi'] = bdoc['NPI']

            # d['tin'] = str(randint(560611570, 560700000))

            if bdoc['ENRLMT_ID'].startswith('O'):
                d['enrollment_type'] = "O"
                d['entity_type'] = "2"
                # d['tin_type'] = random.choice(TIN_TYPE_CHOICES)
            elif bdoc['ENRLMT_ID'].startswith('I'):
                d['enrollment_type'] = "I"
                d['entity_type'] = "1"
            d['first_name'] = bdoc['FIRST_NAME']
            d['last_name'] = bdoc['LAST_NAME']
            d['organization_name'] = bdoc['ORG_NAME']

            d['apm_program_name'] = random.choice(STATUS_CHOICES)
            d['apm_entity_name'] = "Some APN Entity Name"
            d['status'] = random.choice(STATUS_CHOICES)
            # d['number_patiens_seen'] = randint(1, 999)
            # d['part_b_allowed_charges'] = randint(0, 15000)

            if bdoc['FIRST_NAME']:
                d['name'] = "%s %s" % (bdoc['FIRST_NAME'], bdoc['LAST_NAME'])
            else:
                d['name'] = bdoc['ORG_NAME']

            # d['first_approved_date'] = "2000-01-01"
            # d['last_approved_date'] = "2016-11-11"

            d['reassignments'] = []
            d['addresses'] = []
            base_specialty = OrderedDict()
            base_specialty['code'] = bdoc['PROVIDER_TYPE_CD'][3:]
            base_specialty['decription'] = bdoc["PROVIDER_TYPE_DESC"]
            d['specialties'] = [base_specialty,]
            
            
            d['addresses'] = []
            d["ad"] = "This API is powered by Djmongo. http://videntity.com"

            if d['entity_type'] == "1":

                for rdoc in reassignments_collection.find(
                        {"REASGN_BNFT_ENRLMT_ID": bdoc['ENRLMT_ID']}):

                    ac = base_collection.find(
                        {'ENRLMT_ID': rdoc["RCV_BNFT_ENRLMT_ID"]})

                    for a in ac:
                        reassigned_to = OrderedDict()

                        if a['FIRST_NAME']:
                            reassigned_to['name'] = "%s %s" % (
                                a['FIRST_NAME'], a['LAST_NAME'])
                        else:
                            reassigned_to['name'] = a['ORG_NAME']
                        reassigned_to['pecos_id'] = a['PECOS_ASCT_CNTL_ID']
                        reassigned_to['npi'] = a['NPI']
                        reassigned_to['enrollment_id'] = a['ENRLMT_ID']
                        reassigned_to['tin'] = "SCRUBBED"
                        reassigned_to['tin_type'] = ""

                        if str(a['ENRLMT_ID']).startswith("O"):

                            reassigned_to['entity_type'] = "2"
                        else:
                            reassigned_to['entity_type'] = "1"

                        d["reassignments"].append(
                            {"reassigned_to": reassigned_to, "effective_date": "1980-01-01"})

            elif d['entity_type'] == "2":
                for rdoc in reassignments_collection.find(
                        {"RCV_BNFT_ENRLMT_ID": bdoc['ENRLMT_ID']}):

                    ac = base_collection.find(
                        {'ENRLMT_ID': rdoc["REASGN_BNFT_ENRLMT_ID"]})
                    for a in ac:
                        assignee = OrderedDict()
                        if a['FIRST_NAME']:
                            assignee['name'] = "%s %s" % (
                                a['FIRST_NAME'], a['LAST_NAME'])
                        else:
                            assignee['name'] = a['ORG_NAME']

                        assignee['pecos_id'] = a['PECOS_ASCT_CNTL_ID']
                        assignee['npi'] = a['NPI']
                        assignee['enrollment_id'] = a['ENRLMT_ID']
                        assignee['tin'] = "SCRUBBED"
                        assignee['tin_type'] = ""
                        if str(a['ENRLMT_ID']).startswith("O"):

                            assignee['entity_type'] = "2"
                        else:
                            assignee['entity_type'] = "1"

                        d["reassignments"].append(
                            {"assignee": assignee, "effective_date": "1980-01-01"})

            # Get addresses
            for a in addresses_collection.find(
                    {"ENRLMT_ID": bdoc['ENRLMT_ID']}):
                address = OrderedDict()
                address['address_type'] = "P"
                address['line_1'] = "123 Fake Street"
                address['line_2'] = ""
                address['city'] = a["CITY_NAME"]
                address['state'] = a["ZIP_CD"]
                address['zip_code'] = a["STATE_CD"]
                d["addresses"].append(address)

            # Get specialties
            for s in specialties_collection.find(
                    {"ENRLMT_ID": bdoc['ENRLMT_ID']}):
                specialty = OrderedDict()
                specialty['code'] = s['PROVIDER_TYPE_CD'][3:]
                specialty['decription'] = s["PROVIDER_TYPE_DESC"]
                # specialty['mips_eligible_clinician'] = random.choice(
                #   ('Y', 'N'))
                d["specialties"].append(specialty)

            if i % 1000 == 0:
                print(i)
            # print json.dumps(d, indent =4)
            compiled_collection.insert(d)

        # Walk through base

    except:
        print(sys.exc_info())
        print json.dumps(d, indent=4)

    print(i, "Processed")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("makepecosdocs.py [DB NAME]")
        sys.exit(1)

    database_name = sys.argv[1]
    # Run it
    makepecosdb(database_name)
