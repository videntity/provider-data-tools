#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Written by Alan Viars
import json
import sys
import datetime
import re
from choices import STATES


def validate_identifier_list(l, enumeration_type):
    errors = []
    primary_count = 0
    max_values = {
        'state': 2,
        'code': 2,
        'issuer': 150,
        'identifier': 20,
    }
    for d in l:

        identifer_string = "%s %s %s issued by %s" % (d['identifier'],
                                                      d['code'], d['state'],
                                                      d['issuer'])

        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(
                    d.get(
                        k,
                        "").encode(
                        'ascii',
                        'ignore').decode('ascii')):
                    error = "%s : %s exceeds max allowable length of %s." % (
                        identifer_string, k, max_values[k])
                    errors.append(error)

        # check for required information
        if str(
            d.get(
                'code',
                '')) not in (
            "",
            "01",
            "02",
            "04",
            "05",
            "06",
            "07",
            "08",
            "1",
            "2",
            "4",
            "5",
            "6",
            "7",
                "8"):
            error = "%s : identifier code is not in ['', '01', '02', '04','05', '06', '07', '08']" % d.get(
                'code')
            errors.append(error)

        # if state is provided then it should be valid.
        if d.get('state') and d.get('state') not in STATES:
            error = "%s : identifier code is not a valid 2-letter state code." % (
                identifer_string, d.get('state'))
            errors.append(error)

    return errors
