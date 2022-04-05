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


def split_practitioners_and_organizations(csvfile, include_state_list=[]):
    """Splt the two entrity type into two files.."""

    if sys.version_info[0] < 3:
        fh = open(csvfile, 'rb')
    else:
        fh = open(csvfile, 'r', newline='', encoding='iso-8859-1')
    f = csv.reader(fh, delimiter=',')
    pract_output_file = csvfile[:-4]
    pract_output_file = "%s_practitioners.csv" % (pract_output_file)
    org_output_file = csvfile[:-4]
    org_output_file = "%s_organizations.csv" % (org_output_file)


    if sys.version_info >= (3, 0, 0):
        p_outputcsvfileb = open(pract_output_file, 'w', newline='')
    else:
        p_outputcsvfileb = open(pract_output_file, 'wb')

    if sys.version_info >= (3, 0, 0):
        o_outputcsvfileb = open(org_output_file, 'w', newline='')
    else:
        o_outputcsvfileb = open(org_output_file, 'wb')




    p_csvwriterb = csv.writer(p_outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    o_csvwriterb = csv.writer(o_outputcsvfileb, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)


    rowindex = 0
    """#skip the first row """
    """#next(csvfile)"""
    print("start file iteration")
    for row in f:
        if include_state_list:
            if row[23] in include_state_list or row[31] in include_state_list: 
        
                if row[1] == "1":
                    p_csvwriterb.writerow(row)
                elif row[1] == "2":
                    o_csvwriterb.writerow(row)
        else:
            if row[1] == "1":
                p_csvwriterb.writerow(row)
            elif row[1] == "2":
                o_csvwriterb.writerow(row)
        rowindex+=1
        

    print("Done. Iterated over", rowindex, "rows.")
    fh.close()
    p_outputcsvfileb.close()
    o_outputcsvfileb.close()
    


if __name__ == "__main__":

    if len(sys.argv) < 2:
        main_file = 'test.csv'
    else:
        main_file = sys.argv[1]
    
    
    if len(sys.argv) > 2:
        include_state_list = sys.argv[2:]
    else:
        include_state_list = []    
    split_practitioners_and_organizations(main_file, include_state_list)
