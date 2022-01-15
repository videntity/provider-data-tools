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
        c = c.replace("\\", "-")
        cleaned_headers.append(c)
    return cleaned_headers


def build_csv_with_taxonomy(input_npi_file, input_taxonomy_file, output_file, 
                            npi_column=0):
    
    #load the entire tazonomy in 
    
    
    fh_read_tax = open(input_taxonomy_file, 'r', errors='ignore')
    taxonomy_reader = csv.reader(fh_read_tax, delimiter=',')
    rowindex = 0
    all_taxonomies = OrderedDict()

    print("Reading taxonomies into memory. This might take a few minutes...")
    for row in taxonomy_reader:       
        if rowindex == 0:
            taxonomy_column_headers = row
        # otherwise
        all_taxonomies[row[npi_column]]=row
        rowindex += 1
    fh_read_tax.close()
    print("Reading taxonomies into memory complete.")
    fh_read_npi = open(input_npi_file, 'r', errors='ignore')
    reader_npi = csv.reader(fh_read_npi, delimiter=',')


    fh_write = open(output_file, 'w')
    csv_writer = csv.writer(fh_write, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    npis = []
    rowindex = 0
    not_npis = []
    no_taxonomy_defined_list = []
    for row in reader_npi:       
        if rowindex == 0:
            column_headers =  row +  taxonomy_column_headers [1:]      
            csv_writer.writerow(clean_headers(column_headers))
        else: # rowindex >= 1  
            if len(row[npi_column])==10:
                try:
                    new_row = row + all_taxonomies[row[npi_column]][1:]
                except KeyError:
                    new_row = row
                    no_taxonomy_defined_list.append(row[npi_column])
                    print(row[npi_column], "has no taxonomy!")
                csv_writer.writerow(new_row)
            else:
                csv_writer.writerow(row)
                not_npis.append(row[npi_column])


        rowindex += 1
    fh_read_npi.close()
    fh_read_npi.close()

    print("Total NPIs:", rowindex,  "Skipped/not NPIs:",len(not_npis))
    
    return {
            "total_output_rows": rowindex,
            "total_not_npis": len(not_npis),
            "not_npis": not_npis,
            "total_missing_taxonomy": len(no_taxonomy_defined_list),
            "total_output_rows": rowindex
            }
        

    


if __name__ == "__main__":
 
    # Parse args
    parser = argparse.ArgumentParser(
        description="""Input a CSV containing NPIs in the first (or specificed) column.
        Input also the taxononimies flat csv. This is part of the output from chop_nppes_public.py.
        Output """)
    parser.add_argument('input_npi_csv',
        help='Input a CSV containing NPIs. Program expects the NPI in the first column (column 0) by default')
    parser.add_argument('input_taxonomy_csv',
        help='Input a CSV containing all NPIs and their taxonomies. Output from chop_nppes_public.py.')

    parser.add_argument('output_csv', default="csv_with_taxonomy.csv",  help="Output the input file with the taxonomioes appended.")
    parser.add_argument('--column', default=0, help="Grab another column besides 0, as the NPI, out of the CSV.")
    args = parser.parse_args()
    result = build_csv_with_taxonomy(args.input_npi_csv, 
                                     args.input_taxonomy_csv,
                                     args.output_csv,
                                     args.column)
    # output the JSON transaction summary
    print((json.dumps(result, indent=4)))