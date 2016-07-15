#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars

import json
import sys
import datetime
import re
from choices import COUNTRIES, STATES, ADDRESS_PURPOSE, ADDRESS_TYPE


def validate_address_list(l, enumeration_type):
    errors = []
    LOCATION_ADDRESS_FOUND = False
    MAILING_ADDRESS_FOUND = False
    # define a max_values dict
    max_values = {
        'address_type': 12,
        'address_purpose': 20,
        'address_1': 200,
        'address_2': 200,
        'city': 200,
        'state': 2,
        'zip': 10,
        'country_code': 2,
        'us_telephone_number': 12,
        'telephone_number_extension': 10,
        'us_fax_number': 12,
        'foreign_telephone_number': 20,
        'foreign_fax_number': 20,
        'mpo': 3,
        'lat': 20,
        'long': 20,
    }

    # Test for max_length errors

    for d in l:
        address_string = "%s %s %s %s %s" % (d.get('address_1', "").encode('ascii', 'ignore').decode('ascii'),
                                             d.get('address_2', "").encode(
                                                 'ascii', 'ignore').decode('ascii'),
                                             d.get('city', "").encode(
                                                 'ascii', 'ignore').decode('ascii'),
                                             d.get('state', "").encode(
                                                 'ascii', 'ignore').decode('ascii'),
                                             d.get('zip', "").encode('ascii', 'ignore').decode('ascii'))

        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(d.get(k, "").encode('ascii', 'ignore').decode('ascii')):

                    error = "%s : %s max allowable length %s." % (
                        address_string, k, max_values[k])
                    errors.append(error)

        # check for required information

        if d.get('address_type') not in ADDRESS_TYPE:
            error = "%s : address_type must be in %s." % (
                address_string, ADDRESS_TYPE)
            errors.append(error)

        if d.get('override_address_standardization') and \
           d.get('override_address_standardization') not in (True, False):
            error = "%s : override_address_standardization must be true or false." % (
                address_string)
            errors.append(error)

        if d.get('accept_address_standardization') and \
           d.get('accept_address_standardization') not in (True, False):
            error = "%s : accept_address_standardization must be true or false." % (
                address_string)
            errors.append(error)

        if d.get('address_purpose') not in ADDRESS_PURPOSE:
            error = "%s : address_purpose must be in %s." % (
                address_string, ADDRESS_PURPOSE)
            errors.append(error)

        if d.get('address_purpose') == "MAILING":
            MAILING_ADDRESS_FOUND = True

        if d.get('address_purpose') == "LOCATION":
            LOCATION_ADDRESS_FOUND = True

        if not d.get('address_1'):
            error = "%s : address_1 is required." % (address_string)
            errors.append(error)

        if not d.get('city'):
            error = "%s : city is required." % (address_string)
            errors.append(error)

        if not d.get('state'):
            error = "%s : state is required." % (address_string)
            errors.append(error)

        if not d.get('zip'):
            error = "%s : zip is required." % (address_string)
            errors.append(error)

        if not d.get('country_code'):
            error = "%s : country_code is required." % (address_string)
            errors.append(error)

        if d.get('state') not in STATES:
            error = "%s : state must be 2 letter ISO code or set to ZZ for a foreign country." % (
                address_string)
            errors.append(error)

        if d.get('country_code') not in COUNTRIES:
            error = "%s : country_code must be 2 letter ISO code." % (
                address_string)
            errors.append(error)

    # Check to see if both a mail and practice location is on file for NPI-1
    # and NPI-2
    if enumeration_type in ("NPI-1", "NPI-2") and not LOCATION_ADDRESS_FOUND:
        errors.append("A practice location address was not found.")

    if enumeration_type in ("NPI-1", "NPI-2", "HPID", "OEID") and not MAILING_ADDRESS_FOUND:
        errors.append("A mailing address was not found.")

    return errors
