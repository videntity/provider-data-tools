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
 
def new_fhir_organization_stub(id, name, phone_number=None, website=None, version_id="1", source="default"):
    org = OrderedDict()
    # Organization JSON stub
    org["resourceType"] = "Organization"
    org["meta"] = {"versionId": version_id, "source": source}
    org["id"] = id
    org["name"] = name
    org["text"] = {"status": "generated", "div": """<div xmlns=http://www.w3.org/1999/xhtml><p>%s (%s)</p></div>""" % (name, id)}
        
    org["network"] = {"reference": "Organization/%s-network" % (id),
                      "display": "%s Network (%s)" % (name, id) }

    if phone_number:
        org['telecom'] = [ {"system": "phone", "value": phone_number, "use": "work"} ]
    
    if website:
        org['telecom'] = [ {"system": "url", "value": website} ]
    
    return org
 

def new_fhir_insuranceplan_stub(id, name, insurance_product_type=None, versionId="1", source="default"):

    insurance_plan = OrderedDict()
    insurance_plan["resourceType"] = "InsurancePlan"
    insurance_plan["meta"] = {
        "versionId": versionId, 
        "source": source, 
        "profile": [ "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-InsurancePlan" ]}
    insurance_plan["id"] = id
    insurance_plan["active"] = True
    insurance_plan["text"] = {"status": "generated",
                  "div": """<div xmlns=http://www.w3.org/1999/xhtml><p>%s(%s)</p></div>""" % (name,id)}

    if insurance_product_type:
        insurance_plan["type"] = [ {
            "coding": [ {
            "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/CodeSystem/InsuranceProductTypeCS",
            "code": insurance_product_type,
            } ]
        } ]
        insurance_plan["ownedBy"] = {"reference": "Organization/%s" % (id)}
    # TO DO - Add network block or orgs.    
    return insurance_plan
 

def build_fhir_insurance_network_from_csv(csvfile, output_dir="output"):
    """Return a response_dict with summary of the ND-JSON output."""
 
    process_start_time = time.time()
    pdir = 1
    # make the output dir
    try:
        os.mkdir(output_dir)
    except:
        pass
   
    # Start of opening of csv file to convert and test
    response_dict = OrderedDict()
    fh = open(csvfile, 'r', errors='ignore')
    csvhandle = csv.reader(fh, delimiter=',')
    rowindex = 0
    error_list = []
 
    # Create the NDJSON writers.
    out_fh1 = open("%s/OrganizationNetwork.ndjson" %(output_dir), 'w')
    organization_writer = ndjson.writer(out_fh1)
   
    out_fh2 = open("%s/InsurancePlan.ndjson" %(output_dir), 'w')
    insurance_plan_writer = ndjson.writer(out_fh2)
 
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
                c = c.lower()
                cleaned_headers.append(c)
            r = OrderedDict()
        else: 
            zip_record = list(zip(cleaned_headers, row))
            record = dict(list(zip(cleaned_headers, row)))
            # start our object off with a stub.
            print(record)
            org = new_fhir_organization_stub(record['insuranceplan_id'], record['name'],
                                             record['phone_number'], record['website'], 
                                             record['version_id'], record['source'])
            organization_writer.writerow(org)
            insurance_plan = new_fhir_insuranceplan_stub(record['insuranceplan_id'], 
                                                        record['name'], 
                                                        record['insurance_product_type'],
                                                        record['version_id'], record['source'])
            insurance_plan_writer.writerow(insurance_plan)
            rowindex += 1
    response_dict["rows_processed"] = rowindex
    out_fh1.close()
    out_fh2.close()
    fh.close()
    return response_dict
 
if __name__ == "__main__":
 
    # Parse args
    parser = argparse.ArgumentParser(
        description="""Output FHIR 4 Organization(Network) and InsurancePlan FHIR Reources based on CSV
                input.  Example of expected CSV input format is here: Example here https://example.com/nc-mediciad-plans.cvs
                """)
 
    parser.add_argument('input_csv', default="nc-medicaid-insurance-plans.csv", help='Input the CSV file containing a list of insurance plans and associated data. Example here https://example.com/nc-mediciad-plans.cvs')
    parser.add_argument('output_ndjson', default="",   help="Output Directory whe InsurancePlan.ndjson and Orgnaization.ndjson files are created.")
   
    args = parser.parse_args()
    result = build_fhir_insurance_network_from_csv(
                      args.input_csv,
                      args.output_ndjson)
    # output the JSON transaction summary
    print((json.dumps(result, indent=4)))