#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Written by Alan Viars
import json, sys, datetime, re
from choices import COUNTRIES, STATES, ADDRESS_PURPOSE, ADDRESS_TYPE


def validate_address_list(l, enumeration_type):
    errors = []

    #define a max_values dict
    max_values = {
        'address_type'              : 12,
        'address_purpose'           : 20,
        'address_1'                 : 200,
        'address_2'                 : 200,
        'city'                      : 200,
        'state'                     : 2,
        'zip'                       : 10,
        'country_code'              : 2,
        'us_telephone_number'       : 12,
        'telephone_number_extension': 10,
        'us_fax_number'             : 12,
        'foreign_telephone_number'  : 20,
        'foreign_fax_number'        : 20,
        'mpo'                       : 3,
        'website'                   : 1024,
        'lat'                       : 20,
        'long'                      : 20,
        }

    #Test for max_length errors

    for d in l:


        for k in max_values.keys():
            if d.get(k):

                    if max_values[k] < len(str(d.get(k))):
                        error = "%s : %s max allowable length %s." % (address_string, k, max_values[k])
                        errors.append(error)

        #check for required information


        if d.get('address_type') not in ADDRESS_TYPE:
            error = "%s : address_type must be in %s" % (address_string, ADDRESS_TYPE)
            errors.append(error)

        if d.get('address_purpose') not in ADDRESS_PURPOSE:
            error = "%s : address_purpose must be in %s" % (address_string, ADDRESS_PURPOSE)
            errors.append(error)

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
            error = "%s : state must be 2 letter ISO code or ZZ for foreign."  % (address_string)
            errors.append(error)

        if d.get('country_code') not in COUNTRIES:
                error = "%s : country_code must be 2 letter ISO code."   % (address_string)
                errors.append(error)


        return errors

