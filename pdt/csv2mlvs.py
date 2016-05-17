#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

import os, sys, string, json, csv
from collections import OrderedDict

def csv2mlvs(csvfile, output_dir="output"):

    """Return a response_dict with summary of csv2mlvs transaction."""

    response_dict = OrderedDict()
    print("Start the conversion of", csvfile, "into the MLVS into the directory ", output_dir, ".")

    #open the csv file.
    csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

    rowindex    = 0


    error_list  = []

    try:
        os.mkdir(output_dir)
        print("Output directory", output_dir, "created.")
    except:
        print("Output directory", output_dir, "already exists.")


    for row in csvhandle :

        if rowindex==0:
             column_headers = row
             cleaned_headers = []
             for c in column_headers:
                c= c.replace(".", "")
                c= c.replace("(", "")
                c= c.replace(")", "")
                c =c.replace("$", "-")
                c =c.replace(" ", "_")
                cleaned_headers.append(c)
        else:

            record = dict(list(zip(cleaned_headers, row)))

            #create the state dir if not already created
            state_dir = os.path.join(output_dir, record["state"])
            try:
                os.mkdir(state_dir)
                print("State directory", state_dir, "created.")
            except:
                pass

            #create the license_type dir if not already created
            lt_dir = os.path.join(state_dir, record["license_type"])
            try:
                os.mkdir(lt_dir)
                print("License type directory", lt_dir, "created.")
            except:
                pass


            fn = "%s.json" % (record["number"])
            fp = os.path.join(lt_dir, fn)

            ofile =  open(fp, 'w')
            ofile.writelines(json.dumps(record, indent =4))
            ofile.close()

        rowindex += 1


    if error_list:
            response_dict['num_files_created']=rowindex-1
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
    else:

            #response_dict['num_rows_imported']=mongoindex
            response_dict['num_files_created']=rowindex-1
            response_dict['code']=200
            response_dict['message']="Completed without errors."


    return response_dict

if __name__ == "__main__":


    if len(sys.argv)!=3:
        print("Usage:")
        print("csv2mlvs.py [CSVFILE] [OUTPUT_DIR]")
        print("See mlvs.csv in the samples directory for a sample CSV file layout.")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]

    result = csv2mlvs(csv_file, output_dir)

    #output the JSON transaction summary
    print(json.dumps(result, indent =4))
