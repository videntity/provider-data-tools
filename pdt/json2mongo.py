#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

from pymongo import Connection
import os, sys, string, json
from collections import OrderedDict

import functools
import pymongo
import time
import hashlib

MONGO_HOST="127.0.0.1"
MONGO_PORT=27017

def csv2mongo( jsonfile, database_name="database1",
               collection_name="collection1",
               delete_collection_before_import=False):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    print "Start the import of", jsonfile, "into the collection", collection_name, "within the database", database_name, "."


    try:

        mconnection = Connection("127.0.0.1")
        db          = mconnection[database_name]
        collection  = db[collection_name]

        if delete_collection_before_import:
            print "Clearing the collection prior to import."
            myobjectid=collection.remove({})

        fh = open(jsonfile, 'rU')

        j = fh.read()
        
        
        try:
            j = json.loads(j)
        
        except :
        
        
            response_dict['num_results']=0
            response_dict['code']=400
            response_dict['type']="Error"
            response_dict['results']=[]
            response_dict['message']="Invalid JSON"
            return response_dict
        
        
        if type(j) != type({}):
            response_dict['num_results']=0
            response_dict['code']=400
            response_dict['type']="Error"
            response_dict['results']=[]
            response_dict['message']="Error: File must contain a json object, i.e. {}."
            return response_dict
            
            

        rowindex = 0
        mongoindex = 0
        errors=0
        error_list =[]
        success =0
        

        try:
            myobjectid=collection.insert(j)
            mongoindex+=1



        except:
            error_message = "Error on row " + str(rowindex) +  ". " + str(sys.exc_info())
            error_list.append(error_message)
            print error_message
            sys.exit()

        rowindex+=1


        if error_list:
                response_dict ={}
                response_dict['num_rows_imported']=rowindex
                response_dict['num_rows_errors']=len(error_list)
                response_dict['errors']=error_list
                response_dict['code']=400
                response_dict['message']="Completed with errors."
                print response_dict
                sys.exit()
        else:

                response_dict ={}
                response_dict['num_rows_imported']=mongoindex
                response_dict['num_csv_rows']=rowindex
                response_dict['code']=200
                response_dict['message']="Completed."

    
    except:
        print "Error writing to  Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
        return response_dict


    return response_dict

if __name__ == "__main__":

    
    if len(sys.argv)!=5:
        print "Usage:"
        print "python json2mongo.py [JSONFILE] [DATABASE] [COLLECTION] [DELETE_COLLECTION_BEFORE_IMPORT (T/F)]"
        sys.exit(1)

    json_file = sys.argv[1]
    database = sys.argv[2]
    collection = sys.argv[3]
    delete_collection_before_import = sys.argv[4]

    if sys.argv[4].lower() in ('t', 'true', '1'):
        delete_collection_before_import = True
    else:
        delete_collection_before_import = False
    result = csv2mongo(json_file, database, collection, delete_collection_before_import)
    print json.dumps(result, indent =4)
