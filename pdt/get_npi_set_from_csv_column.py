#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
 
import os
import sys
import string
import json
import csv
import time
import argparse
from collections import OrderedDict
from datetime import datetime
 

def clean_headers(headers):
    cleaned_headers = []
    for c in headers:
        c = c.replace(".", "")
        c = c.replace("(", "")
        c = c.replace(")", "")
        c = c.replace("$", "-")
        c = c.replace(" ", "_")
        c = c.replace("/", "-")
        c = c.replace("\\", "-")
        cleaned_headers.append(c)
    return cleaned_headers


def get_npi_set_from_csv_column(input_file, output_file, npi_column=0, header_row=True):
    fh_read = open(input_file, 'r', errors='ignore')
    csvhandle_read = csv.reader(fh_read, delimiter=',')
    fh_write = open(output_file, 'w')
    csvhandle_write = csv.writer(fh_write, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    npis = []
    rowindex = 0
    not_npis = []
    for row in csvhandle_read:       
        if rowindex == 0:
            if header_row:
                column_headers = row
            else:
                column_headers = ['npi',]            
            csvhandle_write.writerow(clean_headers(column_headers))
        else: # rowindex >= 1  
            if len(row[npi_column])==10:
                npis.append(row[npi_column])
            else:
                not_npis.append(row[npi_column])
        rowindex += 1
    fh_read.close()

    # Now create a set from the list.
    npi_set = list(set(npis))
    
    #write the output file
    for npi in npi_set:
        csvhandle_write.writerow([npi,])
    fh_write.close()

    print("Total NPIs:", rowindex, "Set of NPIs", len(npi_set), "skipped/not NPIs:",len(not_npis))
    
    return {"output_file": output_file, 
            "total_input_rows": rowindex,
            "total_output_rows": len(npi_set),
            "not_npis": len(not_npis)         }
        

    


if __name__ == "__main__":
 
    # Parse args
    parser = argparse.ArgumentParser(
        description="""Input a CSV containing NPIs in the first (or specificed) column.
        Output a CSV of only the set of NPIs.""")
    parser.add_argument('input_csv',
        help='Input a CSV containing NPIs. Program expects the NPI in the first column (column 0) by default')
    parser.add_argument('output_csv', default="npi_set.csv",  help="Output NPI set CSV filename.")
    parser.add_argument('--column', default=0, help="Grab another column besides 0 out of the CSV.")
    parser.add_argument('--no_header_row', default="", help="Set to true to grab row 0 too.")
    args = parser.parse_args()
    result = get_npi_set_from_csv_column(args.input_csv, 
                                         args.output_csv, 
                                         args.column,
                                         args.no_header_row)
    # output the JSON transaction summary
    print((json.dumps(result, indent=4)))