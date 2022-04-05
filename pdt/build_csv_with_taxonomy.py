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
                            npi_field="NPI/ATYP"):
    
    #load the entire taxonomy in 
    fh_read_tax = open(input_taxonomy_file, 'r', errors='ignore')
    taxonomy_reader = csv.reader(fh_read_tax, delimiter=',')
    rowindex = 0
    all_taxonomies = {}

    print("Reading taxonomies into memory. This might take a few minutes...")
    for row in taxonomy_reader:       
        if rowindex == 0:
            taxonomy_column_headers = row
        else:
            # otherwise create a dict. 
            taxonomy = OrderedDict()
            taxonomy = list(zip(taxonomy_column_headers, row))
            all_taxonomies[row[0]] = taxonomy
        rowindex += 1
    fh_read_tax.close()
    print("Reading %s CMS taxonomies into memory complete." % (rowindex))

    csvfile = open(input_npi_file, 'r', errors='ignore')
    reader = csv.DictReader(csvfile)
    no_taxonomy_defined_list = []
    not_npis = []
    all_taxonomies_keys =  all_taxonomies.keys()
    
    # print("ATK",all_taxonomies_keys)
    print("Opening file for writing.")
    fh_write = open(output_file, 'w')


    rowindex=0
    for row in reader:
        # Add the two records together and write the new CSV.
        # print("NPI", row[npi_field])
        # print("ATK",all_taxonomies_keys)
        # print(row[npi_field])
        if rowindex == 0:
            header =  list(reader.fieldnames) + list(taxonomy_column_headers)
            print(header)
            writer = csv.DictWriter(fh_write, fieldnames=header)
            writer.writeheader()
            print("Header written.")
        else:
            if row[npi_field] in all_taxonomies_keys:
                # print("Found: ", row[npi_field])
                if len(row[npi_field])==10:
                    combined_row = {**row, **OrderedDict(all_taxonomies[row[npi_field]]) }
                    writer.writerow(combined_row)
                else:
                    not_npis.append(row[npi_field])
            else:
                pass
        rowindex += 1
    fh_write.close()

    return {"total_output_rows": rowindex,
            "total_not_npis": len(not_npis),
            "not_npis": not_npis,
            "total_missing_taxonomy": len(no_taxonomy_defined_list),
            }

if __name__ == "__main__":
 
    # Parse args
    parser = argparse.ArgumentParser(
        description="""Input a CSV containing NPIs in the first (or specificed) column.
        Input also the taxononomies flat csv. This is the _taxonomy.csv output from the chop_nppes_public.py.
        command line utility.""")
    parser.add_argument('input_npi_csv',
        help='Input a CSV containing NPIs. Program expects the NPI in the first column (column 0) by default')
    parser.add_argument('input_taxonomy_csv',
        help='Input a CSV containing all NPIs and their taxonomies. Output from chop_nppes_public.py.')

    parser.add_argument('output_csv', default="csv_with_taxonomy.csv",  help="Output the input file with the taxonomioes appended.")
    parser.add_argument('--npifield', default="NPI-ATYP", help="Grab another field besides 'NPI-ATYP' out of the CSV.")
    args = parser.parse_args()
    result = build_csv_with_taxonomy(args.input_npi_csv, args.input_taxonomy_csv,
                                     args.output_csv, args.npifield)
    # output the JSON transaction summary
    print(result['total_output_rows'])
    #print((json.dumps(result, indent=4)))