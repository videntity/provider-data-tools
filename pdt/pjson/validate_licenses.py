#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Written by Alan Viars
import json
import sys
import datetime
import re
from choices import LICENSE_TYPE_CODES


def validate_license_list(l, enumeration_type, action):
    errors = []

    # define a max_values dict
    max_values = {
        'code': 50,
        'status': 10,
    }

    # Test for max_length errors

    for d in l:
        # form an address string.

        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(
                    d.get(
                        k,
                        "").encode(
                        'ascii',
                        'ignore').decode('ascii')):
                    error = "%s : %s max allowable length %s." % (
                        d.get['code'], max_values[k])
                    errors.append(error)

        if len(d.get('code')) < 7:
            # The code is to shourt to be valid
            error = "%s : License code is too short to be valid." % (
                d.get('code'))
            errors.append(error)
        else:
            license_code = d.get('code')[0:6]
            if action != "public":
                if license_code not in LICENSE_TYPE_CODES:
                    error = "%s : License code must be a valid license type code.  See https://github.com/HHSIDEAlab/mlvs/blob/master/docs/USProviderLicenseTypesFeb2014.csv" % (
                        d.get('code'))
                    errors.append(error)

    return errors
