#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Written by Alan Viars
import json, sys, datetime, re
from choices import ASSOCIATION_DATA_TYPE, ASSOCIATION_PURPOSE, ENDPOINT_DATA_TYPE



def validate_association_list(l, enumeration_type):
    errors = []
    warnings = []
    primary_count  = 0
    max_values = {
        'purpose': 50,
        'association_data_type': 20,
        'endpoint_data_type': 50,
        'association': 1024,
        'endpoint': 1024,
        'description': 1024
        
        }
    i=0
    
    for d in l:
    
        association_string = "Assoication %s." % (i)

        
        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(str(d.get(k))):
                    error = "%s : %s exceeds max allowable length of %s." % (association_string,
                                                                  k,
                                                                  max_values[k])
                    errors.append(error)
    
        
        #check for required information
        if str(d.get('purpose', '')) not in ASSOCIATION_PURPOSE:
            error = "%s : assoication purpose not in %s" % (d.get('purpose'), ASSOCIATION_PURPOSE)
            errors.append(error)
            
    
        i += 1
    retval = [errors, warnings]
    return retval