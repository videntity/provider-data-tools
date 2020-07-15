#!/home/ubuntu/.virtualenvs/pdt/bin/python3.5
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import os
import sys
import string
import json
import csv
import time
import json_schema_check
from collections import OrderedDict
from datetime import datetime
import ndjson

def newfhir_deactive_stub():
    ps = OrderedDict()

    # ProviderJSON stub
    ps["resourceType"] = "Practitioner"
    ps['identifier'] = [
        {
            "use": "official",
            "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": "",
        }
    ]
    ps['active'] = bool(False)
    return ps


def new_fhir_practitioner_stub(npi, prefix, first_name, last_name, suffix):

    text = "%s %s %s %s %s" % (npi, prefix, first_name, last_name, suffix)
    ps = OrderedDict()
    ps["resourceType"] = "Practitioner"
    ps["id"] = npi
    ps["text"] = {"status": "generated",
                  "div": "<div><p>%s</p></div>" % (text)
                  }
    ps['extension'] = []
    ps['identifier'] = [
        {
            "use": "official",
            "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": str(npi)
        }
    ]
    ps['active'] = bool(True)
    ps['name'] = [
        {
            "family": [
                last_name
            ],
            "given": [
                first_name
            ],
            "suffix": [
                suffix
            ],
            "prefix": [
                prefix
            ]


        }
    ]
    ps["address"] = []
    ps['telecom'] = []
    ps['qualification'] = []

    return ps


def new_fhir_organization_stub(npi, organization_name):

    text = "%s: NPI= %s (Type 2-Organization/Facility/Pharmacy)" % (organization_name, npi,)
    os = OrderedDict()
    os["resourceType"] = "Organization"
    os["id"] = npi
    os["text"] = {"status": "generated",
                  "div": "<div><p>%s</p></div>" % (text)
                  }
    os['extension'] = []
    os['identifier'] = [
        {
            "use": "official",
             "coding": [
                { "system": "http://hl7.org/fhir/v2/0203i",
                  "value": str(npi),
                  "display": "National provider identifier"
                },
                ],
             "text": "US National Provider Identifier"
        }
    ]
    os['name'] = organization_name
    os["address"] = []
    os['telecom'] = []
    os['qualification'] = []
    return os


def publiccsv2fhir(csvfile, output_dir, schema_check=False,
                   include_state_list=[], include_npi_list=[]):
    """Return a response_dict with summary of  publiccsv2fhir transaction."""

    process_start_time = time.time()
    pdir = 1

    # make the output dir
    try:
        os.mkdir(output_dir)
    except:
        pass
    try:
        os.mkdir(os.path.join(output_dir, "Practitioner"))
    except:
        pass
    try:
        os.mkdir(os.path.join(output_dir, "Organization"))
    except:
        pass

    try:
        os.mkdir(os.path.join(output_dir, "Deactive"))
    except:
        pass

    # Make variable/paths for nucc_taxonomy and schema checker, open file
    nucc_tax = os.path.join(os.path.dirname(__file__),
                            "nucc_taxonomy_201.csv")
    # Check which version of Python, and open csv accordingly
    # TODO remove Python2 support
    if sys.version_info[0] < 3:
        csvfile_tax = open(nucc_tax, 'rb')
    else:
        csvfile_tax = open(nucc_tax, 'r', newline='', encoding='iso-8859-1')
    
    tax_reader = csv.reader(csvfile_tax, delimiter=',')
    
    # Load taxonomy
    # read csv file as a list of lists
    list_of_rows = []
    with open(os.path.join(os.path.dirname(__file__),"nucc_taxonomy_201.csv"), 'r', newline='', encoding='iso-8859-1') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
    tax_display = OrderedDict()
    for row in list_of_rows:
        tax_display[row[0]] = "%s, %s, %s" % (row[1], row[2], row[3],)
        tax_display[row[0]] = tax_display[row[0]].strip().strip(',')


    practitioner_path = os.path.join(os.path.dirname(__file__),
                                     "fhir_json_schema", "Practitioner.json")
    organization_path = os.path.join(os.path.dirname(__file__),
                                     "fhir_json_schema", "Organization.json")

    # Start of opening of csv file to convert and test
    response_dict = OrderedDict()
    fh = open(csvfile, 'r')
    csvhandle = csv.reader(fh, delimiter=',')
    rowindex = 0
    po_count = 0
    practitioner_count = 0
    organization_count = 0
    deactive_count = 0
    error_list = []

    # Create the NDJSON writers.
    out_fh1 = open("Organization.ndjson", 'w')
    organization_writer = ndjson.writer(out_fh1)
    
    out_fh2 = open("Practitioner.ndjson", 'w')
    practitioner_writer = ndjson.writer(out_fh2)

    for row in csvhandle:
        if rowindex == 0:

            rowindex += 1
            column_headers = row

            cleaned_headers = []
            for c in column_headers:
                c = c.replace(".", "")
                c = c.replace("(", "")
                c = c.replace(")", "")
                c = c.replace("$", "-")
                c = c.replace(" ", "_")
                cleaned_headers.append(c)
        else:

            # If the records is not redacted (because its inactive)

            zip_record = list(zip(cleaned_headers, row))
            record = dict(list(zip(cleaned_headers, row)))

            # get rid of blanks
            no_blank_zip = []
            for i in zip_record:
                if i[1]:
                    no_blank_zip.append(i)

            # start our object off with a stub.

            if row[1] == "1":
                r = new_fhir_practitioner_stub(row[0], row[8],  row[6], row[5],
                                               row[9])

            elif row[1] == "2":
                r = new_fhir_organization_stub(row[0], row[4])

            else:
                r = newfhir_deactive_stub()

            # Practice Address

            a = OrderedDict()
            r['address'] = []
            a["use"] = "work"
            a["line"] = []
            a["line"].append(row[28].upper())
            if row[29]:
                a["line"].append(row[29].upper())
            a["city"] = row[30].upper()
            a["state"] = row[31].upper()
            a["postalCode"] = row[32].upper()
            a["country"] = row[33].upper()

            r['address'].append(a)
            # Mailing address --------------------
            a = OrderedDict()
            if row[1] == "1":
                a['use'] = 'home'
                a['line'] = []
                a['line'].append(row[20].upper())
                if row[21]:
                    a['line'].append(row[21].upper())
                a["city"] = row[22].upper()
                a["state"] = row[23].upper()
                a["postalCode"] = row[24].upper()
                a["country"] = row[25].upper()
                r['address'].append(a)

            # Gender
            if row[1] == "1":
                if row[41] == "M":
                    r["gender"] = "male"
                elif row[41] == "F":
                    r["gender"] = "female"
                elif row[41] != "M" or "F":
                    r["gender"] = "other"
                else:
                    r["gender"] = "unknown"

            # Organization Contact
            if row[43]:
                contact_list = list()
                contact = OrderedDict()
                purpose = OrderedDict()
                purpose['text'] = "Admin"
                contact['purpose'] = purpose
                name = OrderedDict()
                name["family"] = [row[42]]
                name["given"] = [row[43]]
                name["suffix"] = [row[312]]
                name["prefix"] = [row[311]]
                contact['name'] = name

                contact['telecom'] = [
                    {
                        "system": "phone",
                        "value": "%s-%s-%s" % (row[46][0:3],
                                               row[46][3:6],
                                               row[46][6:12]),
                        "use": "work"
                    }
                ]
                contact_list.append(contact)
                r['contact'] = contact_list
                
            # Provider Business Practice Location Address Telephone Number
            t = OrderedDict()
            if row[34]:
                t['system'] = "phone"
                t['value'] = "%s-%s-%s" % (row[34][0:3], row[34][3:6],
                                           row[34][6:12])
                t['use'] = "work"
                r['telecom'] = [t]
            
            # Provider Business Practice Location Address Fax Number
            if row[35]:
                t = OrderedDict()
                t['system'] = "fax"
                t['value'] = "%s-%s-%s" % (row[35][0:3], row[35][3:6],
                                           row[35][6:12])
                t['use'] = "work"
                r['telecom'].append(t)

            # Mailing Phone and Fax numbers for Practitioners
            if row[1] == "1":
                if row[26]:
                    t = OrderedDict()
                    t['system'] = "phone"
                    t['value'] = "%s-%s-%s" % (row[26][0:3], row[26][3:6],
                                               row[26][6:12])
                    t['use'] = 'home'
                    r['telecom'].append(t)

                if row[27]:
                    t = OrderedDict()
                    t['system'] = "fax"
                    t['value'] = "%s-%s-%s" % (row[27][0:3], row[27][3:6],
                                               row[27][6:12])
                    t['use'] = 'home'
                    r['telecom'].append(t)


            # Getting taxonomy codes to store in qualifications
            for i in range(50, 107, 4):
                if row[i] == "Y":

                    taxonomy = OrderedDict()
                    taxonomy["code"] = OrderedDict()
                    taxonomy["value"] = str(row[i - 3])
                    coding = OrderedDict()
                    #extension = OrderedDict()

                    coding['system'] = "http://taxonomy.nucc.org/"
                    coding['code'] = str(row[i - 3])
                    coding['display'] = tax_display[coding['code']]

                    for row_tax in tax_reader:
                        # print(row_tax)
                        if coding['code'] == row_tax[0]:
                            coding['display'] = row_tax[2]

                    taxonomy['code']['coding'] = [coding, ]

                    #extension['url'] = "http://www.nucc.org/"
                    #extension['valueCodeableConcept'] = taxonomy

                    r['qualification'].append(taxonomy)

            # identifiers----------------
            # starting at row 107

            identifier_position = 107
            identifier_code_position = 108
            identifier_state_position = 109
            identifier_issuer_position = 110

            for i in range(1, 50):

                if row[identifier_position]:
                    identifier = OrderedDict()
                    identifier['use']="official"
                    
                    if "MEDICAID" in row[identifier_issuer_position]:
                        code = "MCD"
                        display = "Practitioner Medicaid number"
                    
                    elif "DEA" in row[identifier_issuer_position]:
                        code = "DEA"
                        display = "Drug Enforcement Administration registration number"
    
                    else:
                        code = "AN"
                        display = "Account number"
                        
                    identifier['type']=[{"system":"http://hl7.org/fhir/v2/0203",
                                        "code": code,
                                        "display": display
                                        },]
                    identifier['value'] = row[identifier_position]
                    identifier['text'] = row[identifier_code_position]
                    identifier['state'] = row[
                        identifier_state_position].upper()
                    identifier['issuer'] = row[identifier_issuer_position]
                    r['identifier'].append(identifier)

                identifier_position += 4
                identifier_code_position += 4
                identifier_state_position += 4
                identifier_issuer_position += 4
               
                # licenses 
                # starting at row 49
                license_state_position = 49
                license_number_position = 48

                for i in range(1, 15):
                     # License
                    if row[license_number_position]:
                        license = OrderedDict()
                        license["use"] = "official"
                        license["coding"] = [
                            {"system": "http://hl7.org/fhir/v2/0203",
                             "code": "MD",
                             "display": "Medcial license"},                       ]
                        license['value'] = row[license_number_position]
                        license['state'] = row[license_state_position].upper()
                        license['issuer'] = row[identifier_issuer_position].upper()
                        if not license['issuer'] and license['state']:
                            license['issuer'] = license['state']
                        if not license['issuer']:
                            license['issuer'] = "UNSPECIFIED" 

                        license['text'] = "%s issued by %s"  % (license['value'], license['issuer'])

                        r['qualification'].append(license)
                        
                        #skip to the next
                        license_state_position += 4
                        license_number_position += 4    


            fn = "%s.json" % (row[0])

            if not row[1]:
                deactive_count += 1 
            if r['resourceType'] == "Practitioner":
                # Write to Practitioner NDJSON File
                for a in r['address']:
                    if a['state'] in include_state_list and a['use']=="work":
                        practitioner_writer.writerow(r)
                        practitioner_count +=1 
                # Write to Organization NDJSON File
            elif r['resourceType'] == "Organization":
                for a in r['address']:
                    if a['state'] in include_state_list and a['use']=="work":
                        organization_writer.writerow(r)
                        organization_count += 1

            #fp = os.path.join(subdir, fn)
            #ofile = open(fp, 'w')
            #ofile.writelines(json.dumps(r, indent=4))
            #ofile.close()
            
            if schema_check:
                if row[1] == "1":
                    results = json_schema_check.json_schema_check(
                        practitioner_path, fp)
                    if results['errors'] != []:
                        response_dict['errors'] = results['errors']
                if row[2] == "2":
                    results = json_schema_check.json_schema_check(
                        organization_path, fp)
                    if results['errors'] != []:
                        response_dict['errors'] = results['errors']
            po_count += 1

            if po_count % 1000 == 0:
                pdir += 1
                out = "%s lines processed. Total time is %s seconds." % (
                    po_count, (time.time() - process_start_time))
                print((out))

            rowindex += 1


    response_dict['total_rows_processed'] = rowindex - 1
    response_dict['practitioner_count'] = practitioner_count
    response_dict['organization_count'] = organization_count
    response_dict['deactive_count'] = deactive_count
    response_dict['num_csv_rows'] = rowindex - 1

    out_fh1.close()
    out_fh2.close()
    fh.close()
    csvfile_tax.close()
    return response_dict

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage:")
        print("csv2fhir_public.py [CSVFILE] [OUTPUT_DIRECTORY]")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]

    result = publiccsv2fhir(csv_file, output_dir, include_state_list=[
                                        'WV', 'VA', 'SC', 'NC', 'TE', 'GA'])
    

    # output the JSON transaction summary
    print((json.dumps(result, indent=4)))