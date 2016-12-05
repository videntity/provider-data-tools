#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars

import json
import sys
import os
import datetime
import csv


def validate_taxonomy_list(taxonomies, enumeration_type, licenses,
                           taxonomy_licenses, sole_proprietor, action):

    csvfile = os.path.join(os.path.dirname(__file__),
                           "taxonomy-license-crosswalk.csv")

    errors = []
    primary_count = 0

    taxonomy_license_crosswalk = {}
    # Load the CSV
    fh = open(csvfile, 'rb')
    csvr = csv.reader(fh, delimiter=',')
    for row in csvr:
        key = row[0]
        entity_type = row[1]
        if row[2] == "False":
            license_required = False
        else:
            license_required = True

        taxonomy_license_crosswalk[key] = (entity_type, license_required)

    for t in taxonomies:
        if action != "public":

            # check for required information
            if t.get('code') not in taxonomy_license_crosswalk.keys():
                error = "%s : code (taxonomy) is not a valid taxonomy code. See http://www.wpc-edi.com/taxonomy" % t.get('code')
                errors.append(error)

        if not isinstance(t.get('primary'), type(True)):
            error = "%s : primay must be true or false." % (d.get('code'))
            errors.append(error)

        if t.get('primary'):
            primary_count += 1
    # check that only one taxonomy is marked as primary
    if primary_count != 1:
        error = "Exactly 1 taxonomy code must be marked as primary. The primary count is %s." % (
            primary_count)
        errors.append(error)

    # Get the taxonomy license codes
    tl_codes = []
    for tl in taxonomy_licenses:
        tl_codes.append(tl.get('taxonomy_code'))

    for t in taxonomies:
        # print t
        # check for required information

        # Check to see if the taxonomy is right for the enumeration_type
        if t.get('code') in taxonomy_license_crosswalk.keys():
            cw = taxonomy_license_crosswalk[t.get('code')]
            code = cw[0]
            requires_license = cw[1]

            # print code , requires_license
            if action != "public":
                if cw[
                        0] == "I" and enumeration_type != "NPI-1" and sole_proprietor == "NO":
                    error = "Taxonomy %s is only for for individuals / NPI-1." % (
                        t.get('code'))
                    errors.append(error)
                if cw[0] == "O" and enumeration_type != "NPI-2":
                    error = "Taxonomy %s is only for for organizations / NPI-2." % (
                        t.get('code'))
                    errors.append(error)
                # Check to see if the taxonomy requires a license
                if requires_license and t.get('code') not in tl_codes:
                    error = "Taxonomy %s requires a license." % (t.get('code'))
                    errors.append(error)

    return errors
