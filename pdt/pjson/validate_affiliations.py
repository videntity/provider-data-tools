#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars

import json, sys, datetime, re
from choices import AFFILIATION_DATA_TYPE, AFFILIATION_PURPOSE, ENDPOINT_DATA_TYPE, STATES
from validate_email import validate_email
from baluhn import verify
LUHN_PREFIX ="80840"

def validate_affiliation_list(l, enumeration_type):
    errors = []
    warnings = []
    primary_count  = 0
    max_values = {
        'purpose': 25,
        'affiliation_data_type': 10,
        'endpoint_data_type': 50,
        'affiliation_identifier': 1024,
        'endpoint': 1024,
        'description': 1024,
        'state': 2,
        }

    i=0

    for d in l:

        affiliation_string = "Affiliation %s: " % (i)

        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(d.get(k,"").encode('ascii', 'ignore').decode('ascii')):
                    error = "%s : %s exceeds max allowable length of %s." % (affiliation_string,
                                                                  k,
                                                                  max_values[k])
                    errors.append(error)


        #check for required information
        if d.get('purpose') not in AFFILIATION_PURPOSE:
            error = "%s purpose %s is not a valid value.  Valid values are %s." % (
                affiliation_string, d.get('purpose'), AFFILIATION_PURPOSE)
            errors.append(error)


        if d.get('affiliation_data_type') not in AFFILIATION_DATA_TYPE:
            error = "%s affiliation_data_type %s is not a valid value.  Valid values are %s." % (
                                            affiliation_string,
                                            d.get('affiliation_data_type'),
                                            AFFILIATION_DATA_TYPE)
            errors.append(error)

        if not str(d.get('affiliation_data_type')) and \
                d.get('purpose') not in AFFILIATION_PURPOSE:
            error = "%s affiliation_data_type %s is required when purpose is one of these %s" % (
                                                    affiliation_string,
                                                    d.get('affiliation_data_type'),
                                                    AFFILIATION_PURPOSE)
            errors.append(error)

        if d.get('endpoint_data_type') and d.get('endpoint_data_type') not in ENDPOINT_DATA_TYPE:
            error = "%s endpoint_data_type %s is not a valid value. Valid values are %s." % \
                  (affiliation_string, d.get('endpoint_data_type', ''), ENDPOINT_DATA_TYPE)
            errors.append(error)

        if d.get('purpose', '') == "HIE-EXCHANGE" and not d.get('endpoint_data_type', ''):
            error = "%s endpoint_data_type is required when the purpose is HIE-EXCHANGE." % \
                  (affiliation_string)
            errors.append(error)

        if not d.get('affiliation_identifier', '') and \
            d.get('affiliation_data_type', '') in AFFILIATION_DATA_TYPE:
            error = "%s affiliation_identifier is required when affiliation_data_type is in %s." % \
                  (affiliation_string, AFFILIATION_DATA_TYPE)
            errors.append(error)

        if not d.get('endpoint') and d.get('purpose') in ("HIE-EXCHANGE", "DOMAIN"):
            error = "%s endpoint is required when purpose is in %s." % \
                  (affiliation_string, ("HIE-EXCHANGE", "DOMAIN"))
            errors.append(error)

        if d.get('accepting_new_patients', None) not in (True, False, None):
            error = "%s accepting_new_patients must be boolean. i.e. true or false." % \
                  (affiliation_string)
            errors.append(error)

        if d.get('for_additional_documentation_request', None) not in (True, False, None):
            error = "%s for_additional_documentation_request must be boolean. i.e. true or false." % \
                  (affiliation_string)
            errors.append(error)

        if d.get('purpose') == "MEDICAID-NETWORK" and not  d.get('state'):
            error = "%s state is required when purpose = MEDICIAD-NETWORK." % \
                  (affiliation_string)
            errors.append(error)

        if d.get('state') and d.get('state') not in STATES:
            error = "%s state %s is not a valid value. Valid values are %s." % \
                  (affiliation_string, d.get('state'), STATES)
            errors.append(error)
        if d.get('affiliation_data_type') in ('NPI-1', 'NPI-2'): 
            prefixed_number = "%s%s" % (LUHN_PREFIX, d['affiliation_identifier'])
            luhn_verified = verify(prefixed_number)
            if not luhn_verified:
                error ="The NPI affiliation_identifier %s did not pass Luhn algorithm check digit sanitiy check." % (d['affiliation_identifier'])
                errors.append(error)

        if d.get('endpoint_data_type') in ('DIRECT-EMAIL-ADDRESS', 'REGULAR-EMAIL-ADDRESS'):
            is_valid = validate_email(d.get('endpoint'))
            if not is_valid:
                error = "%s %s has and endpoint_data_type of %s and is not a valid email." % \
                      (affiliation_string, d.get('endpoint'), d.get('endpoint_data_type') )
                errors.append(error)

        i += 1
    retval = [errors, warnings]
    return retval