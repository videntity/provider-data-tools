#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os
import json
import csv
import time
import argparse
from collections import OrderedDict
import ndjson
import uuid
from datetime import date
today = date.today()


def sort_taxonomies(record):
    taxonomies = []

    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_1']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_1'])

    # if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_2']:
    #    taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_2'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_3']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_3'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_4']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_4'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_5']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_5'])

    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_6']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_6'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_7']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_7'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_8']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_8'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_9']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_9'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_10']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_10'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_11']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_11'])

    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_12']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_12'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_13']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_13'])
    if record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_15']:
        taxonomies.append(record['HEALTHCARE_PROVIDER_TAXONOMY_CODE_15'])

    return taxonomies


def generate_fhir_qualifications(taxonomies, nucc_taxonomies):
    qualifications = []
    for t in taxonomies:
        qual_string = """
          {"code": {
            "coding": [{
            "system": "http://taxonomy.nucc.org/",
            "code": "%s",
            "display": "%s"}]},
            "value": "%s"
            }""" % ((t, nucc_taxonomies[t], t))
        qual = json.loads(qual_string)
        qualifications.append(qual)
    return qualifications


def generate_locations(record):
    locations = []

    location = OrderedDict({"resourceType": "Location",  "meta": {
        "lastUpdated": today.strftime("%Y-%m-%d"),
        "profile": ["http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Location"]}})
    location['active'] = True
    lines = []
    lines.append(record['SERVICE_LOCATION_ADDR1'], )
    if record['SERVICE_LOCATION_ADDR2']:
        lines.append(record['SERVICE_LOCATION_ADDR2'],)
    location["address"] = {"line": lines,
                           "city": record['SERVICE_LOCATION_CITY'],
                           "state": record['SERVICE_LOCATION_STATE'],
                           "postalCode": record['SERVICE_LOCATION_ZIP_CODE']}

    # Nox accvepting new as default
    accepting_new_patients_code = "nopt"
    if record['ACCEPTING_NEW_PATIENTS'] == "Y":
        accepting_new_patients_code = "newpt"

    # Add the extension to cover accepting new patients
    location["extension"] = [
        {
            "extension": [
                {
                    "url": "acceptingPatients",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/CodeSystem/AcceptingPatientsCS",
                                "code": accepting_new_patients_code
                            }
                        ]
                    }
                }]
        }]

    # Add the hours of operation
    location["hoursOfOperation"] = []
    hho = {}
    days_of_week = []
    if not record['MONDAY'].startswith("NOT A"):
        days_of_week.append("mon")
    if not record['TUESDAY'].startswith("NOT A"):
        days_of_week.append("tue")
    if not record['WEDNESDAY'].startswith("NOT A"):
        days_of_week.append("wed")
    if not record['SUNDAY'].startswith("NOT A"):
        days_of_week.append("sun")
    hho['daysOfWeek'] = days_of_week
    allDay = False
    if record['MONDAY'].startswith("OPEN 24"):
        allDay = True
        hho['allDay'] = allDay
    location["hoursOfOperation"].append(hho)

   # If there are sprcific hours, create additional entries
    if not allDay:
        DAYS_OF_WEEK = {'MONDAY': 'mon', 'TUESDAY': 'tue', 'WEDNESDAY': 'wed',
                        'THURSDAY': 'thu', 'FRIDAY': 'fri', 'SATURDAY': 'sat', 'SUNDAY': 'sun'}
        for d in DAYS_OF_WEEK.keys():
            if record[d]:
                hho = {}
                hho['daysOfWeek'] = [DAYS_OF_WEEK[d], ]
                if record[d][0].isnumeric():
                    hho["openingTime"] = record[d][0:5]
                if record[d][9:11].isnumeric():
                    miltime = record[d][9:14]
                    if "PM" in record[d][9:] and int(record[d][9:11]) < 13:
                        miltime = int(record[d][9:11]) + 12
                        miltime = "%s:%s" % (miltime, record[d][12:14])
                    hho["closingTime"] = miltime
                location["hoursOfOperation"].append(hho)

    locations.append(location)
    return locations


def sort_networks(record):
    networks = []
    if record['MEDICAID']:
        networks.append('medicaid-direct-nc-network')
    if record['TRIBAL_OPTION']:
        networks.append('ebci-nc-network')
    if record['AMERIHEALTH']:
        networks.append('amerihealthcaritas-nc-network')
    if record['HEALTHYBLUE']:
        networks.append('healthyblue-nc-network')
    if record['CAROLINA_COMPLETE_CARE']:
        networks.append('carolina-complete-health-nc-network')
    if record['UNITED_HEALTHCARE']:
        networks.append('united-healthcare-community-plan-nc-network')
    if record['WELLCARE']:
        networks.append('wellcare-nc-network')
    return networks


def new_fhir_practitioner_role(npi, first_name, last_name, network=[],
                               qualifications=[], locations=[]):

    text = "%s %s" % (first_name, last_name,)
    ps = OrderedDict()
    ps["resourceType"] = "PractitionerRole"
    ps["meta"] = {"lastUpdated": today.strftime("%Y-%m-%d")}
    ps["id"] = str(uuid.uuid4())
    ps["text"] = {"status": "generated",
                  "div": """<div xmlns=http://www.w3.org/1999/xhtml><p>%s</p></div>""" %
                  (text)}
    ps['identifier'] = [
        {"use": "official",
         "system": "http://hl7.org/fhir/sid/us-npi",
         "value": str(npi)
         }
    ]

    if network:
        ps["network"] = []
        for n in network:
            ps["network"].append({"reference": "Organization/%s" % (n)})

    if qualifications:
        ps["qualifications"] = qualifications
        ps["specialty"] = qualifications

    if locations:
        ps["location"] = locations
    return ps


def new_fhir_organization(npi, organization_name, network=[], qualifications=[], locations=[]):

    text = "%s: NPI= %s (Type 2-Organization/Facility/Pharmacy)" % (organization_name, npi,)
    os = OrderedDict()
    os["resourceType"] = "Organization"
    os["meta"] = {"lastUpdated": today.strftime("%Y-%m-%d")}
    os["id"] = str(uuid.uuid4())
    os["text"] = {"status": "generated",
                  "div": """<div xmlns=http://www.w3.org/1999/xhtml><p>%s</p></div>""" % (text)}
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

    if network:
        os["network"] = []
        for n in network:
            os["network"].append({"reference": "Organization/%s" % (n)})
    if qualifications:
        os["qualifications"] = qualifications
        os["specialty"] = qualifications
    if locations:
        os["location"] = locations
    return os


def csv2davinci_pd_fhir(csvfile, csvplansfile,  output_dir="output", npi_list_file=""):
    """Return a response_dict with summary of public csv2davinci_pd_fhir creation."""

    # Make variable/paths for nucc_taxonomy open file
    nucc_tax = os.path.join(os.path.dirname(__file__), "nucc_taxonomy_220.csv")
    nucc_taxonomies = {}
    with open(nucc_tax, newline='') as nucccsvfile:
        reader = csv.DictReader(nucccsvfile)
        for row in reader:
            code = row['Code']
            description = "%s,%s,%s" % (
                row['Grouping'], row['Classification'], row['Specialization'])
            nucc_taxonomies[code] = description
    npis = []
    if npi_list_file:
        print("Reading in files of NPIs to process.")
        npi_fh = open(npi_list_file, 'r')
        npi_csvhandle_read = csv.reader(npi_fh, delimiter=',')
        for row in npi_csvhandle_read:
            if len(row[0]) == 10:
                npis.append(row[0])
        npi_fh.close()
        print("Done reading in %s NPIs", len(npis))
    else:
        print("Creating all NPIS. No NPI file given.")
    npis = set(npis)

    # Open the Plans file.
    fh = open(csvplansfile, 'r', errors='ignore')
    csvhandle = csv.reader(fh, delimiter=',')
    plans = []
    rowindex = 0
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
            record = list(zip(cleaned_headers, row))
            plans.append(record)
    fh.close()
    print("PLANS loaded")

    # Start of opening of csv file to convert and test
    response_dict = OrderedDict()
    fh = open(csvfile, 'r', errors='ignore')
    csvhandle = csv.reader(fh, delimiter=',')
    rowindex = 0
    practitioner_count = 0
    organization_count = 0

    # make the output dir
    try:
        os.mkdir(output_dir)
    except Exception:
        # It alread exists!
        print("Output directory already exists")

    # Create the NDJSON writers.
    out_fh1 = open("%s/Organization2.ndjson" % (output_dir), 'w')
    organization_writer = ndjson.writer(out_fh1)

    out_fh2 = open("%s/PractitionerRole.ndjson" % (output_dir), 'w')
    practitioner_writer = ndjson.writer(out_fh2)

    fh = open(csvfile, 'r', errors='ignore')
    main_csvhandle = csv.DictReader(fh, delimiter=',')
    rowindex = 0

    for record in main_csvhandle:
        # print(record)
        # Add accepting new patients and days of week as part of location
        locations = generate_locations(record)
        networks = sort_networks(record)
        taxonomies = sort_taxonomies(record)
        fhir_qualifications = generate_fhir_qualifications(
            taxonomies, nucc_taxonomies)
        r = {'resourceType': "OperationalOutcome"}
        if 'ENTITY_TYPE_CODE' in record.keys():
            if record["ENTITY_TYPE_CODE"] == "1":
                r = new_fhir_practitioner_role(record['NPI-ATYP'],
                                               record['PROVIDER_LAST_NAME-_ORGANIZATION_NAME'],
                                               record['PROVIDER_FIRST_NAME'],
                                               networks, fhir_qualifications, locations)

            elif record["ENTITY_TYPE_CODE"] == "2":
                r = new_fhir_organization(record['NPI-ATYP'],
                                          record['PROVIDER_LAST_NAME-_ORGANIZATION_NAME'],
                                          networks, fhir_qualifications, locations)

        # TODO Add addresses

        print(rowindex)

        if r['resourceType'] == "PractitionerRole":
            # Write to Practitioner Role NDJSON File
            if not npis:
                # Process all in this case.
                practitioner_writer.writerow(r)
                practitioner_count += 1
            elif row["NPI-ATYP"] in npis:
                practitioner_writer.writerow(r)
                practitioner_count += 1

        # Write to Organization Affiliation NDJSON File
        elif r['resourceType'] == "Organization":
            # Default: do all states and territories
            if not npis:
                # Process all in this case.
                organization_writer.writerow(r)
                organization_count += 1
            elif row["NPI-ATYP"] in npis:
                organization_writer.writerow(r)
                organization_count += 1

        rowindex += 1

    response_dict['total_rows_processed'] = rowindex - 1
    response_dict['practitioner_role_count'] = practitioner_count
    response_dict['organization_count'] = organization_count
    response_dict['num_csv_rows'] = rowindex - 1
    # response_dict['num_unique_npis'] =len(npis)

    out_fh1.close()
    out_fh2.close()
    fh.close()
    return response_dict


if __name__ == "__main__":

    # Parse args
    parser = argparse.ArgumentParser(
        description="""Output FHIR 4 Organization and PractitionerRole resource files using the 
                       NCDHHS formatted file as input.
                       Output is two NDJSON files.
                    """)

    parser.add_argument(
        'input_csv', help='Input the NCDHHS list of provider CSV.')
    parser.add_argument(
        'plan_input_csv', help='Input a CSV containing all the plans.')

    parser.add_argument('--output_directory', default="output",
                        help="Output NDJSON filename.")
    parser.add_argument('--npis', default="",  nargs='?',
                        help="Include a filepath containing a CSV with NPIs in first column (0),")
    args = parser.parse_args()
    result = csv2davinci_pd_fhir(args.input_csv,
                                 args.plan_input_csv,
                                 args.output_directory,
                                 args.npis)
    # output the JSON transaction summary
    print((json.dumps(result, indent=4)))
