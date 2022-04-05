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
 

def clean_headers(headers, upper=True):
    cleaned_headers = []
    for c in headers:
        if upper:
            c = c.upper()
        c = c.replace(".", "")
        c = c.replace("(", "")
        c = c.replace(")", "")
        c = c.replace("$", "-")
        c = c.replace(" ", "_")
        c = c.replace("/", "-")
        c = c.replace("$", "-")
        c = c.replace("*", "-")
        cleaned_headers.append(c)
    return cleaned_headers


def build_csv_with_cleaned_headers(input_npi_file, output_file):
    
    csvfile = open(input_npi_file, 'r', errors='ignore')
    reader = csv.reader(csvfile)
 
    # "Opening file for writing."
    fh_write = open(output_file, 'w')
    # define a row index
    rowindex = 0
    for row in reader:

        if rowindex == 0:
            cleaned_headers =  clean_headers(row)
            writer = csv.writer(fh_write)
            writer.writerow(cleaned_headers)
        else:
            writer.writerow(row)
        
        rowindex += 1
    fh_write.close()


    return cleaned_headers

if __name__ == "__main__":
 
    # Parse args
    parser = argparse.ArgumentParser(
        description="""Input a CSV containing NPIs in the first (or specificed) column.
        Input also the taxononomies flat csv. This is the _taxonomy.csv output from the chop_nppes_public.py.
        command line utility.""")
    parser.add_argument('input_npi_csv',
        help='Input a CSV containing NPIs. Program expects the NPI in the first column (column 0) by default')

    parser.add_argument('output_csv', default="csv_with_taxonomy.csv",  help="Output the input file with the taxonomioes appended.")
    
    args = parser.parse_args()
    result = build_csv_with_cleaned_headers(args.input_npi_csv, args.output_csv)
    # output the JSON transaction summary
    print("Headers updated. Output file",  args.output_csv, "contains ", result)

