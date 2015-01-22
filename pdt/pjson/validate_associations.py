#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars

import json, sys, datetime, re
from choices import ASSOCIATION_DATA_TYPE, ASSOCIATION_PURPOSE, ENDPOINT_DATA_TYPE, STATES
from validate_email import validate_email


def validate_association_list(l, enumeration_type):
    errors = []
    warnings = []
    primary_count  = 0
    max_values = {
        'purpose': 25,
        'association_data_type': 10,
        'endpoint_data_type': 50,
        'association_identifier': 1024,
        'endpoint': 1024,
        'description': 1024,
        'state': 2,
        
        }
    i=0
    
    for d in l:
    
        association_string = "Assoication %s: " % (i)

        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(str(d.get(k))):
                    error = "%s : %s exceeds max allowable length of %s." % (association_string,
                                                                  k,
                                                                  max_values[k])
                    errors.append(error)
    
        
        #check for required information
        if d.get('purpose') not in ASSOCIATION_PURPOSE:
            error = "%s assoication_purpose %s is not a valid value.  Valid values are %s." % (
                association_string, d.get('purpose'), ASSOCIATION_PURPOSE)
            errors.append(error)
            
        
        if d.get('association_data_type') not in ASSOCIATION_DATA_TYPE:
            error = "%s assoication_data_type %s is not a valid value.  Valid values are %s." % (
                                            association_string,
                                            d.get('association_data_type'),
                                            ASSOCIATION_DATA_TYPE)
            errors.append(error)
        
        if not str(d.get('association_data_type')) and \
                d.get('purpose') not in ASSOCIATION_PURPOSE:
            error = "%s assoication_data_type %s is required when purpose is one of theese %s" % (
                                                    association_string,
                                                    d.get('association_data_type'),
                                                    ASSOCIATION_PURPOSE)
            errors.append(error)

        if d.get('endpoint_data_type') and d.get('endpoint_data_type') not in ENDPOINT_DATA_TYPE:
            error = "%s endpoint_data_type %s is not a valid value. Valid values are %s." % \
                  (association_string, d.get('endpoint_data_type', ''), ENDPOINT_DATA_TYPE)
            errors.append(error)
        
        if d.get('purpose', '') == "HIE-EXCHANGE" and not d.get('endpoint_data_type', ''):
            error = "%s endpoint_data_type is required when the purpose is HIE-EXCHANGE." % \
                  (association_string)
            errors.append(error)
            
        if not d.get('association_identifier', '') and \
            d.get('association_data_type', '') in ASSOCIATION_DATA_TYPE:
            error = "%s association_identifier is required when association_data_type is in %s." % \
                  (association_string, ASSOCIATION_DATA_TYPE)
            errors.append(error)
        
        if not d.get('endpoint') and d.get('purpose') in ("HIE-EXCHANGE", "DOMAIN"):
            error = "%s endpoint is required when purpose is in %s." % \
                  (association_string, ("HIE-EXCHANGE", "DOMAIN"))
            errors.append(error)
            
        if d.get('accepting_new_patients', None) not in (True, False, None):
            error = "%s accepting_new_patients must be boolean. i.e. true or false." % \
                  (association_string)
            errors.append(error)
            
        if d.get('purpose') == "MEDICAID-NETWORK" and not  d.get('state'):
            error = "%s state is required when purpose = MEDICIAD-NETWORK." % \
                  (association_string)
            errors.append(error)
        
        if d.get('state') and d.get('state') not in STATES:
            error = "%s state %s is not a valid value. Valid values are %s." % \
                  (association_string, d.get('state'), STATES)
            errors.append(error)
            
        if d.get('endpoint_data_type') in ('DIRECT-EMAIL-ADDRESS', 'REGULAR-EMAIL-ADDRESS'):
            is_valid = validate_email(d.get('endpoint'))
            if not is_valid:
                error = "%s %s has and endpoint_data_type of %s and is not a valid email." % \
                      (association_string, d.get('endpoint'), d.get('endpoint_data_type') )
                errors.append(error)
    
        i += 1
    retval = [errors, warnings]
    return retval