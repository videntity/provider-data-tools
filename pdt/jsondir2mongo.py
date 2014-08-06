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

def jsondir2mongo( json_dir, database_name="database1",
               collection_name="collection1",
               delete_collection_before_import=False):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    print "Start the import of the directory", json_dir, "into the collection", collection_name, "within the database", database_name, "."


    try:

        mconnection = Connection("127.0.0.1")
        db          = mconnection[database_name]
        collection  = db[collection_name]
        
        fileindex = 0
        mongoindex = 0
        errors=0
        error_list =[]
        success =0
        
        
        
        if delete_collection_before_import:
            print "Clearing the collection prior to import."
            myobjectid=collection.remove({})
        
        #get the files in the specified directory
        onlyfiles = [ f for f in os.listdir(json_dir) if os.path.isfile(os.path.join(json_dir,f)) ]
        
        
        
        for f in onlyfiles:
            j = None
            error_message = ""
            fp = os.path.join(json_dir, f)
            
            
            fh = open(fp, 'rU')
            
            
            fileindex += 1
            j = fh.read()
            fh.close()
            
            try:
                j = json.loads(j)
                if type(j) != type({}):
                    error_message = "File " + fp +  " did not contain a json object, i.e. {}."
                    error_list.append(error_message)
            
            except :
            
                error_message = "File " + fp +  " did not contain valid JSON."
                error_list.append(error_message)
                    
            if not error_message:
                try:
                    myobjectid=collection.insert(j)
                    mongoindex += 1
                except:
                    error_message = "Error writing " + fp +  " to Mongo. " + str(sys.exc_info())
                    error_list.append(error_message)

        if error_list:
                response_dict ={}
                response_dict['num_files_imported']=mongoindex
                response_dict['num_file_errors']=len(error_list)
                response_dict['errors']=error_list
                response_dict['code']=400
                response_dict['message']="Completed with errors."
        else:

                response_dict ={}
                response_dict['num_files_imported']=mongoindex
                response_dict['num_file_errors']=len(error_list)
                response_dict['code']=200
                response_dict['message']="Completed."

    
    except:
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
        print "python json2mongo.py [JSON_DIR] [DATABASE] [COLLECTION] [DELETE_COLLECTION_BEFORE_IMPORT (T/F)]"
        sys.exit(1)

    json_dir = sys.argv[1]
    database = sys.argv[2]
    collection = sys.argv[3]
    delete_collection_before_import = sys.argv[4]

    if sys.argv[4].lower() in ('t', 'true', '1'):
        delete_collection_before_import = True
    else:
        delete_collection_before_import = False
    result = jsondir2mongo(json_dir, database, collection, delete_collection_before_import)
    print json.dumps(result, indent =4)
