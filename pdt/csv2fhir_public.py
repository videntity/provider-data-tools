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
import json_schema_check
from collections import OrderedDict
from datetime import datetime
import ndjson
 
def newfhir_deactive_stub():
    ps = OrderedDict()
 
    # ProviderJSON stub
    ps["resourceType"] = "Practitioner"
    ps['identifier'] = [{"use": "official", "system": "http://hl7.org/fhir/sid/us-npi", "value": ""},]
    ps['active'] = bool(False)
    return ps
 

def new_fhir_practitioner_stub(npi, prefix, first_name, last_name, suffix, npis_to_process=[]):
 
    text = "%s %s %s %s %s" % (npi, prefix, first_name, last_name, suffix)
    ps = OrderedDict()
    ps["resourceType"] = "Practitioner"
    ps["id"] = npi
    ps["text"] = {"status": "generated",
                  "div": """<div xmlns=http://www.w3.org/1999/xhtml><p>%s</p></div>""" % (text)
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
            "family": last_name,
            "given": [first_name],
        }]
 
    if suffix:
        ps['name'][0]["suffix"]=[suffix,]
    if prefix:
        ps['name'][0]["prefix"]=[prefix,]



    ps["address"] = []
    ps['telecom'] = []
    ps['qualification'] = []
 
    return ps
 

def new_fhir_organization_stub(npi, organization_name, npis_to_process=[]):
 
    text = "%s: NPI= %s (Type 2-Organization/Facility/Pharmacy)" % (organization_name, npi,)
    os = OrderedDict()
    os["resourceType"] = "Organization"
    os["id"] = npi
    os["text"] = {"status": "generated",
                  "div": """<div xmlns=http://www.w3.org/1999/xhtml><p>%s</p></div>""" % (text)
                  }
    os['extension'] = []
    os['identifier'] = [
        {
        "use": "official",
        "system": "http://hl7.org/fhir/sid/us-npi",
        "value": str(npi),
        }
   
    ]
    os['name'] = organization_name
    os["address"] = []
    os['telecom'] = []
    os['qualification'] = []
    return os
 

def csv2fhir(csvfile, output_dir="output",
                include_state_list=[],
                npi_list_file="",
                include_payer_network=""):
    """Return a response_dict with summary of public csv2fhir transaction."""
 
    process_start_time = time.time()
    pdir = 1
   
    # Make variable/paths for nucc_taxonomy open file
    nucc_tax = os.path.join(os.path.dirname(__file__), "nucc_taxonomy_220.csv")
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
    with open(os.path.join(os.path.dirname(__file__),"nucc_taxonomy_220.csv"), 'r', newline='', encoding='iso-8859-1') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
    tax_display = OrderedDict()
    for row in list_of_rows:
        tax_display[row[0]] = "%s, %s, %s" % (row[1], row[2], row[3],)
        tax_display[row[0]] = tax_display[row[0]].strip().strip(',')
 
   
    npis=[]
    if npi_list_file:
        print("Reading in files of NPIs to process")
        npi_fh = open(npi_list_file, 'r')
        npi_csvhandle_read = csv.reader(npi_fh, delimiter=',')
        
        for row in npi_csvhandle_read:
            if len(row[0]) == 10:
                npis.append(row[0])
        npi_fh.close()
        print("Done reading in %s NPIs", len(npis))
    npis = set(npis)

   # open the 
    payer_network = OrderedDict()
    # If the payer network file is present make sure we can open/parse it and load it into mempory.
    print("here", include_payer_network)
    if include_payer_network:
        print("Reading in files of Payer network file")
        with open(include_payer_network, 'r', encoding='iso-8859-1') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = csv.reader(read_obj)
            for row in csv_reader:
                if len(row[0]) == 10:
                    print(row)
                else:
                    print("Not an NPI!")
        read_obj.close()
        print("Done reading in Payer network file.")



    # Start of opening of csv file to convert and test
    response_dict = OrderedDict()
    fh = open(csvfile, 'r', errors='ignore')
    csvhandle = csv.reader(fh, delimiter=',')
    rowindex = 0
    po_count = 0
    practitioner_count = 0
    organization_count = 0
    deactive_count = 0
    error_list = []
 
    # make the output dir
    try:
        os.mkdir(output_dir)
    except:
        pass
    # Create the NDJSON writers.
    out_fh1 = open("%s/Organization.ndjson" %(output_dir), 'w')
    organization_writer = ndjson.writer(out_fh1)
   
    out_fh2 = open("%s/Practitioner.ndjson" %(output_dir), 'w')
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
            r = OrderedDict()
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
                r = new_fhir_practitioner_stub(row[0], row[8],  row[6], row[5], row[9])
 
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
                a['use'] = 'billing'
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
                contact['purpose'] = OrderedDict()
                contact['purpose']['coding'] = []
                coding = OrderedDict()
                coding['system'] = "http://terminology.hl7.org/CodeSystem/contactentity-type"
                coding['code'] = "ADMIN"
                contact['purpose']['coding'] = [coding, ]
                name = OrderedDict()
                name["family"] = row[42]
                name["given"] = [row[43]]
                if row[312]:
                    name["suffix"] = [row[312]]
                if row[311]:
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
                    t['use'] = 'work'
                    r['telecom'].append(t)
 
                if row[27]:
                    t = OrderedDict()
                    t['system'] = "fax"
                    t['value'] = "%s-%s-%s" % (row[27][0:3], row[27][3:6],
                                               row[27][6:12])
                    t['use'] = 'work'
                    r['telecom'].append(t)
 

            # Getting taxonomy codes to store in qualifications
            for i in range(50, 107, 4):
                if row[i] == "Y":
 
                    taxonomy = OrderedDict()
                    taxonomy["code"] = OrderedDict()
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
 
                    #extension['url'] = http://www.nucc.org/
                    #extension['valueCodeableConcept'] = taxonomy
 
                    r['qualification'].append(taxonomy)
                    r['identifier'].append(taxonomy)
            # identifiers----------------
            # starting at row 107
 
            identifier_position = 107
            identifier_code_position = 108
            identifier_state_position = 109
            identifier_issuer_position = 110
 
            for i in range(1, 50):
               
                if not row[identifier_position]:
                    # print("No identifier")
                    pass
                elif row[identifier_position]:
                    identifier = OrderedDict()
                    identifier['use']="official"
                   
                    if "MEDICAID" in row[identifier_issuer_position]:
                        code = "MCD"
                        display = "Practitioner Medicaid Number: %s" % (row[identifier_position])
                   
                    elif "DEA" in row[identifier_issuer_position]:
                        code = "DEA"
                        display = "Drug Enforcement Administration Registration Number %s" % (row[identifier_position])
   
                    else:
                        code = "PRN"
                        display = "Provider Number %s" % (row[identifier_position])
                       
                    identifier['system']="http://terminology.hl7.org/CodeSystem/v2-0203"
                    identifier['value'] = row[identifier_position]
                   
                    identifier['type'] = OrderedDict()
                    # mytype=[OrderedDict(()[]
                    identifier['type']['coding'] = []
                    coding = OrderedDict()
                    coding['code'] = code
                    coding['system'] = "http://terminology.hl7.org/CodeSystem/v2-0203"
                    identifier['type']['coding'].append(coding)
       
                    #identifier['type'] = mytype
                    #identifier['type'][0]['coding']['code'] = code
                    #identifier['state'] = row[
                    #    identifier_state_position].upper()
                    #if not identifier['state']:
                    #    del identifier['state']
                    #if not identifier['text']:
                    #    del identifier['text']
                    # identifier['issuer'] = row[identifier_issuer_position]
               
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
                license = OrderedDict()
                if not row[license_number_position]:
                        # print("NO LICENSE", license_number_position)
                        pass
                elif row[license_number_position]:
                   
                    license = OrderedDict()
                    license['code']= OrderedDict()
                    license['code']["coding"] = [
                                {"system": "urn:oid:2.16.840.1.113883.4.642.3.44",
                                "code": "MD",
                                "display": "Issuer %s assigned %s, the identifier (and/or license number)." % (row[license_state_position].upper(),
                                                                                                               row[license_number_position].upper())   
                                # "value": row[license_number_position],
                                # "state": row[license_state_position].upper(),
                                }]

                license_state_position += 4
                license_number_position += 4
 
                if license.keys():
                    r['qualification'].append(license)
                          
                       
            # cleanup identifiers
            if not r['identifier']:
                del r['identifier']
                # cleanup extensions
            if 'extension' in r.keys():
                if not r['extension']:
                    del r['extension']
             # skip to the next
 
            if not row[1]:
                deactive_count += 1
            if r['resourceType'] == "Practitioner":
                # Write to Practitioner NDJSON File

                if not include_state_list and not npis:
                    # Process all in this case.
                    practitioner_writer.writerow(r)
                    practitioner_count += 1
                elif row[0] in npis:
                    practitioner_writer.writerow(r)
                    practitioner_count += 1
                else:
                    include_this_provider = False
                    # print(r['address'])
                    for a in r['address']:
                        if a['state'] in include_state_list and a['use'] in ("work", "billing", "home"):
                            include_this_provider = True
                            # print("Non-work address", include_state_list, a['state'])
                            pass
                        else:
                            # print("Not in state!", include_state_list, a['state'])
                            pass
                    for i in r['identifier']:
                        if 'state' in i.keys():
                            if i['state'] in include_state_list:
                                include_this_provider = True
                    if include_this_provider == True or row[0] in npis:
                        practitioner_writer.writerow(r)
                        practitioner_count += 1
                    # if i['type']=='MCD':
                    #    print("Medicaid id for %s" % (i['state']))
            # Write to Organization NDJSON File
            elif r['resourceType'] == "Organization":
                # Default: do all states and territories
                if not include_state_list and not npis:
                    # Process all in this case.
                    organization_writer.writerow(r)
                    organization_count += 1
                elif row[0] in npis:
                    organization_writer.writerow(r)
                    organization_count += 1
                else:
                    include_this_organization = False
               
                    for a in r['address']:
                        if a['state'] in include_state_list: # and a['use']=="work":
                            include_this_organization = True
       
                    for i in r['identifier']:
                        if 'state' in i.keys():
                            if i['state'] in include_state_list:
                                include_this_organization = True
 
                    if include_this_organization == True:
                        organization_writer.writerow(r)
                        organization_count += 1
                # Total count
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
    # response_dict['num_unique_npis'] =len(npis)
 
    out_fh1.close()
    out_fh2.close()
    fh.close()
    csvfile_tax.close()
    return response_dict
 
if __name__ == "__main__":
 
    # Parse args
    parser = argparse.ArgumentParser(
        description="""Output FHIR 4 Organization and Practitioner Resource NDJSON files using the 
                       CMS NPPESS CSV as input.
                       """
 
    parser.add_argument('input_csv',
        help='Input the NPPES CSV file. Get the latest file here https://download.cms.gov/nppes/NPI_Files.html')
    parser.add_argument('output_ndjson', default="output.ndjson",  help="Output NDJSON filename.")
    parser.add_argument('--npis', default="",  nargs='?',
        help="Include a filepath containing a CSV with NPIs in first column (0),")
    parser.add_argument('--include_payer_network', default="",  nargs='?',
        help="Include a filepath containing a CSV with Payer input. See https://github.com/TransparentHealth/provider-data-tools for info.")
    parser.add_argument('--states', nargs='+', default=[],
        help="Include one or more states or teritories in the output. All are processed by default.")

   
   
    args = parser.parse_args()
    print()
    result = csv2fhir(args.input_csv,
                      args.output_ndjson,
                      args.states, args.npis,
                      args.include_payer_network)
    # output the JSON transaction summary
    print((json.dumps(result, indent=4)))
