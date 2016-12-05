#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Written by Alan Viars
import json
import sys
import datetime
import re
from choices import (
    SUFFIX_CHOICES,
    PREFIX_CHOICES,
    INDIVIDUAL_OTHER_NAME_CHOICES,
    SOLE_PROPRIETOR_OTHER_NAME_CHOICES,
    ORGANIZATION_OTHER_NAME_CHOICES,
    OTHER_NAME_CHOICES)


def validate_other_name_list(l, enumeration_type, basic):
    errors = []
    primary_count = 0

    if enumeration_type == "NPI-1":
        sole_proprietor = basic['sole_proprietor']
    else:
        sole_proprietor = "NO"

    max_values = {
        'type': 100,
        'code': 1,
        'prefix': 5,
        'organization_name': 150,
        'first_name': 150,
        'middle_name': 150,
        'last_name': 150,
        'suffix': 4,
        'credential': 50,
        'othertype': ''
    }
    i = 0
    for d in l:

        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(
                    d.get(
                        k,
                        "").encode(
                        'ascii',
                        'ignore').decode('ascii')):
                    error = "other_name %s: %s exceeds max allowable length of %s." % (
                        i, k, max_values[k])
                    errors.append(error)

        # Type II
        if enumeration_type == "NPI-2" and str(d.get('code',
                                                     '')) not in ORGANIZATION_OTHER_NAME_CHOICES:
            error = "other_name %s: %s other_name for organizations is not in %s." % (
                i, d.get('code'), ORGANIZATION_OTHER_NAME_CHOICES)
            errors.append(error)

        if enumeration_type == "NPI-2" and not d.get('organization_name', ''):
            error = "other_name %s: organization_name required for NPI-2," % (
                i)
            errors.append(error)

        # Type 1
        if enumeration_type == "NPI-1" and sole_proprietor == "NO" and str(
                d.get('code', '')) not in INDIVIDUAL_OTHER_NAME_CHOICES:
            error = "other_name %s: %s other_name for individuals is not in %s" % (
                i, d.get('code'), INDIVIDUAL_OTHER_NAME_CHOICES)
            errors.append(error)

        if enumeration_type == "NPI-1" and sole_proprietor == "NO" and not str(
                d.get('first_name', '')):
            error = "other_name %s: first_name required for NPI-1." % (i)
            errors.append(error)

        if enumeration_type == "NPI-1" and sole_proprietor == "NO" and not str(
                d.get('last_name', '')):
            error = "other_name %s: last_name required for NPI-2" % (i)
            errors.append(error)

        # Type 1 Sole proprietor
        if enumeration_type == "NPI-1" and sole_proprietor == "YES" and str(
                d.get('code', '')) not in SOLE_PROPRIETOR_OTHER_NAME_CHOICES:
            error = "other_name %s: %s other_name for sole_proprietor is not in %s." % (
                i, d.get('code'), SOLE_PROPRIETOR_OTHER_NAME_CHOICES)
            errors.append(error)

        if enumeration_type == "NPI-1" and sole_proprietor ==  "YES" \
                and not ( str(d.get('last_name', '')) and str(d.get('first_name', ''))) \
                and not str(d.get('organization_name', '')):
            error = "other_name %s: Either organization_name or first_name and last_name are required for a sole proprietor." % (
                i)
            errors.append(error)

        # General
        # supply othertypwe when type is not given.
        if not str(d.get('code', '')) and not str(d.get('othertype', '')):
            error = "other_name %s: othertype must be supplied if other_name type code is blank." % (
                i)
            errors.append(error)

        # suffix
        suffix = d.get('suffix', '')
        if suffix and suffix not in SUFFIX_CHOICES:
            error = "other_name %s: suffix must be in %s" % (i, SUFFIX_CHOICES)
            errors.append(error)

        # prefix
        prefix = d.get('prefix', '')
        if prefix and prefix not in PREFIX_CHOICES:
            error = "other_name %s: prefix must be in %s" % (i, PREFIX_CHOICES)
            errors.append(error)

        i += 1
    return errors
