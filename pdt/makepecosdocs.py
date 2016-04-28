#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import urllib2,sys
from datetime import datetime

from pymongo import MongoClient
import os, sys, string, json, csv
from collections import OrderedDict


MONGO_HOST="127.0.0.1"
MONGO_PORT=27017


def makepecosdb(database_name="pecos"):
    
    i=0
    try:

        mc =   MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db          =   mc[database_name]
        base_collection  =  db['base']
        addresses_collection  =  db['addresses']
        reassignments_collection  =  db['reassignments']
        compiled_individuals_collection  =  db['compiled_individuals']
        compiled_organizations_collection  =  db['compiled_organizations']
        
        for bdoc in base_collection.find():
            i+=1
            d = OrderedDict()
            if bdoc['ENRLMT_ID'].startswith('O'):
                 d['resourceType'] = "Organization"
            elif bdoc['ENRLMT_ID'].startswith('I'):
                d['resourceType'] = "Practitioner"
            
            if bdoc['FIRST_NAME']:
                
                d['NAME'] = "%s %s" % (bdoc['FIRST_NAME'], bdoc['LAST_NAME'])
            else:
                d['NAME'] = bdoc['ORG_NAME']
            
            
            d['DESCRIPTION'] = bdoc['PROVIDER_TYPE_DESC']
            d["NPI"] =  bdoc['NPI']
            d["works_for"] =  []
            d["has_providers"] =  []
            for rdoc in reassignments_collection.find({"REASGN_BNFT_ENRLMT_ID":bdoc['ENRLMT_ID']}):
                
                ac = base_collection.find({'ENRLMT_ID':rdoc["RCV_BNFT_ENRLMT_ID"]})
                for a in ac:
                   affiliate = OrderedDict()
                   
                   if a['FIRST_NAME']:
                       affiliate['NAME'] = "%s %s" % (a['FIRST_NAME'], a['LAST_NAME'])
                   else:
                       affiliate['NAME'] = a['ORG_NAME']
                   
                   affiliate['NPI']=a['NPI']
                   affiliate['ENRLMT_ID']=a['ENRLMT_ID']
                   affiliate['DESCRIPTION'] = a['PROVIDER_TYPE_DESC']
                   d["works_for"].append(affiliate)
            
            for rdoc in reassignments_collection.find({"RCV_BNFT_ENRLMT_ID":bdoc['ENRLMT_ID']}):
                
                ac = base_collection.find({'ENRLMT_ID':rdoc["REASGN_BNFT_ENRLMT_ID"]})
                for a in ac:
                   affiliate = OrderedDict()
                   if a['FIRST_NAME']:
                       affiliate['NAME'] = "%s %s" % (a['FIRST_NAME'], a['LAST_NAME'])
                   else:
                       affiliate['NAME'] = a['ORG_NAME']
                   
                   affiliate['NPI']=a['NPI']
                   affiliate['ENRLMT_ID']=a['ENRLMT_ID']
                   affiliate['DESCRIPTION'] = a['PROVIDER_TYPE_DESC']
                   d["has_providers"].append(affiliate)
            
            if not d["has_providers"]:
                del d["has_providers"]
            if not d["works_for"]:
                del d["works_for"]
            
            if d['resourceType']=="Organization":
                compiled_organizations_collection.insert(d)
            elif d['resourceType']=="Practitioner":
                compiled_individuals_collection.insert(d)
                    
            #print json.dumps(d, indent =4)
            
        # Walk through base
        
        
    except:
        print sys.exc_info()
        
    print i, "Processed"
    

   


if __name__ == "__main__":
    
    
    if len(sys.argv)!=1:
        print "Usage:"
        print "makepecosdocs.py"
        sys.exit(1)

    #Run it
    makepecosdb()