#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os
import sys
import string
import json
import csv
from collections import OrderedDict
import functools
import time
import hashlib


def chop_taxonomy(csvfile):
    """"Chop taxonomy up into its own file. Not flattened."""
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_taxonomy.csv" % (output_file)
    outputcsvfileb = open(output_file, 'wb')

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    rowindex = 0

    print("Parsing", csvfile, "to create", output_file)

    for row in f:
        t = row[0:2] + row[4:7] + row[47:48] + row[54:56] + row[58:60] + row[62:64] \
            + row[66:68] + row[70:72] + row[74:76] + row[78:80] + row[82:84] \
            + row[86:88] + row[90:92] + row[94:96] + row[98:10] \
            + row[102:104] + row[106:107]  # + row[110:111]

        csvwriterb.writerow(t)
        rowindex += 1

    print("Done. Iterated over", rowindex, "rows. ")
    fh.close()
    outputcsvfileb.close()
    return output_file


def flatten_taxonomy(csvfile):
    """"Flatten the taxonomy output file."""
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_flat.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    rowindex = 0

    print("Parsing", csvfile, "to create", output_file)
    for row in f:
        # If header row.
        if rowindex == 0:
            column_headers = row[0:5] + \
                ["Healthcare_Provider_Taxonomy_Code", "Primary"]
            cleaned_headers = []
            for c in column_headers:
                c = c.replace(".", "")
                c = c.replace("(", "")
                c = c.replace(")", "")
                c = c.replace("$", "-")
                c = c.replace(" ", "_")
                cleaned_headers.append(c)
            csvwriterb.writerow(cleaned_headers)
            rowindex += 1
        else:
            # print "here"
            start = 5
            finish = 7
            for i in range(1, 14):

                # print "HERE", start, finish, len(row)
                flat_row = row[0:5] + row[start:finish]
                # only write the taxonomy code if the cell is not blank
                if row[start]:
                    csvwriterb.writerow(flat_row)
                start += 2
                finish += 2
                rowindex += 1
    print("Done. Iterated over", rowindex, "rows. ")
    fh.close()
    outputcsvfileb.close()
    return output_file


def chop_identifiers(csvfile):
    """"Chop identifiers up into its own file. Not flattened."""

    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_identifiers.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    rowindex = 0

    print("Parsing", csvfile, "to create", output_file)

    for row in f:
        t = row[0:2] + row[4:7] + row[107:307]

        csvwriterb.writerow(t)
        rowindex += 1

    print("Iterated over", rowindex, "rows.")
    fh.close()
    outputcsvfileb.close()
    return output_file


def flatten_identifiers(csvfile):
    """"Flatten the identifiers output file."""
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_flat.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    rowindex = 0
    print("Parsing", csvfile, "to create", output_file)
    for row in f:
        # If header row.
        if rowindex == 0:
            column_headers = row[0:5] + \
                ["Identifier", "Type Code", "State", "Issuer"]
            cleaned_headers = []
            for c in column_headers:
                c = c.replace(".", "")
                c = c.replace("(", "")
                c = c.replace(")", "")
                c = c.replace("$", "-")
                c = c.replace(" ", "_")
                cleaned_headers.append(c)
            csvwriterb.writerow(cleaned_headers)
            rowindex += 1
        else:
            # print "here"
            start = 5
            finish = 9
            for i in range(1, 50):
                flat_row = row[0:5] + row[start:finish]
                # only write the taxonomy code if the cell is not blank
                if row[start]:
                    csvwriterb.writerow(flat_row)
                start += 4
                finish += 4
                rowindex += 1
    print("Done. Iterated over", rowindex, "rows. ")
    fh.close()
    outputcsvfileb.close()
    return output_file


def chop_licenses(csvfile):
    """Chop license up into its own file. Not flattened."""
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_licenses.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    rowindex = 0
    print("Parsing", csvfile, "to create", output_file)

    for row in f:
        l = row[0:2] + row[4:7]  + row[48:50] + row[52:54] + row[56:58] + row[60:62] + \
            row[64:66] + row[68:70] + row[72:74] + row[76:78] + row[80:82] + \
            row[84:86] + row[88:90] + row[92:94] + row[96:98] + row[100:102] + \
            row[104:106]

        csvwriterb.writerow(l)
        rowindex += 1

    print("Done. Iterated over", rowindex, "rows. ")

    fh.close()
    outputcsvfileb.close()
    return output_file


def flatten_licenses(csvfile):
    """"Flatten the licenses output file."""
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_flat.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)

    rowindex = 0

    print("Parsing", csvfile, "to create", output_file)
    for row in f:
        # If header row.
        if rowindex == 0:
            column_headers = row[0:5] + ["Number", "State"]
            cleaned_headers = []
            for c in column_headers:
                c = c.replace(".", "")
                c = c.replace("(", "")
                c = c.replace(")", "")
                c = c.replace("$", "-")
                c = c.replace(" ", "_")
                cleaned_headers.append(c)
            csvwriterb.writerow(cleaned_headers)
            rowindex += 1
        else:
            # print "here"
            start = 5
            finish = 7
            for i in range(1, 15):
                flat_row = row[0:5] + row[start:finish]
                # only write the taxonomy code if the cell is not blank
                if row[start]:
                    csvwriterb.writerow(flat_row)
                start += 2
                finish += 2
                rowindex += 1
    print("Done. Iterated over", rowindex, "rows. ")
    fh.close()
    outputcsvfileb.close()
    return output_file


def chop_other_names(csvfile):
    """Chop other names up into its own file.
    No need toflatten because only one item is in the public file
    """
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_other_names.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    rowindex = 0
    print("Parsing", csvfile, "to create", output_file)

    for row in f:
        # only write this data if something is there.
        if row[11] or row[12] or row[13]:
            l = row[0:2] + row[4:7] + row[11:19]
            csvwriterb.writerow(l)
        rowindex += 1

    print("Done. Iterated over", rowindex, "rows.")
    fh.close()
    outputcsvfileb.close()
    return output_file


def chop_addresses(csvfile):
    """Chop addresses up into its own file. Not flattened."""
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_addresses.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    rowindex = 0
    print("Parsing", csvfile, "to create", output_file)

    for row in f:
        l = row[0:2] + row[4:7] + row[20:36]
        csvwriterb.writerow(l)
        rowindex += 1

    print ("Done. Iterated over", rowindex, "rows.")
    fh.close()
    outputcsvfileb.close()
    return output_file


def flatten_addresses(csvfile):
    """"Flatten the addresses output file."""
    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_flat.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)

    rowindex = 0

    print ("Parsing", csvfile, "to create", output_file)
    for row in f:
        # If header row.
        if rowindex == 0:
            column_headers = row[0:5] + ["Address Type", "Street1", "Street2", "City", "State",
                                         "ZipCode", "CountryCode",
                                         "Telephone Number",  "Fax Number", ]

            cleaned_headers = []
            for c in column_headers:
                c = c.replace(".", "")
                c = c.replace("(", "")
                c = c.replace(")", "")
                c = c.replace("$", "-")
                c = c.replace(" ", "_")
                cleaned_headers.append(c)
            csvwriterb.writerow(cleaned_headers)
            rowindex += 1
        else:
            start = 5
            finish = 13
            flat_row = row[0:5] + ["Business_Mailing", ] + row[start:finish]
            csvwriterb.writerow(flat_row)
            rowindex += 1

            start += 8
            finish += 8
            flat_row = row[0:5] + ["Practice_Location", ] + row[start:finish]
            csvwriterb.writerow(flat_row)
            rowindex += 1

    print("Done. Iterated over", rowindex, "rows. ")
    fh.close()
    outputcsvfileb.close()
    return output_file


def chop_basic(csvfile):
    """Chop basic info into its own file."""

    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    output_file = csvfile[:-4]
    output_file = "%s_basic.csv" % (output_file)

    if sys.version_info >= (3, 0, 0):
        outputcsvfileb = open(output_file, 'w', newline='')
    else:
        outputcsvfileb = open(output_file, 'wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)

    rowindex = 0
    """#skip the first row """
    """#next(csvfile)"""
    print("start file iteration")
    for row in f:
        csvwriterb.writerow(row[0:20] + row[36:47] + row[307:314])
        rowindex += 1

    print("Done. Iterated over", rowindex, "rows.")
    fh.close()
    outputcsvfileb.close()
    return output_file


if __name__ == "__main__":

    if len(sys.argv) < 2:
        main_file = 'test.csv'
    else:
        main_file = sys.argv[1]

    # taxonomy and flat taxonomy
    taxonomy_filename = chop_taxonomy(main_file)
    flatten_taxonomy(taxonomy_filename)

    # licenses and flat licenses
    licenses_filename = chop_licenses(main_file)
    flatten_licenses(licenses_filename)

    # identifiers and flat identifiers
    identifiers_filename = chop_identifiers(main_file)
    flatten_identifiers(identifiers_filename)

    # addresses and flat addresses
    addresses_filename = chop_addresses(main_file)
    flatten_addresses(addresses_filename)

    # chop other_names
    chop_other_names(main_file)

    # chop basic
    chop_basic(main_file)
