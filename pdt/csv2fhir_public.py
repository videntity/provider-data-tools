#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import os, sys, string, json, csv, time
from collections import OrderedDict
from datetime import datetime



def newfhir_deactive_stub():
    ps = OrderedDict()

    #ProviderJSON stub
    ps["resourceType"] = "Practitioner"
    ps['identifier'] = [
                    {
                      "use": "official",
                      "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": "",
                      "_value": {
                        "fhir_comments": [
                          "   NPI  "
                        ]
                      }
                    }
                  ]
    ps['active'] = bool(False)
    return ps

def new_fhir_practitioner_stub(npi, prefix, first_name, last_name, suffix):


    text = "%s %s %s %s %s" % (npi, prefix, first_name, last_name, suffix)
    ps = OrderedDict()
    ps["resourceType"] = "Practitioner"
    ps["text"] = { "status": "generated",
                   "div": "<div><p>%s</p></div>" % (text)
                 }
    ps['identifier'] = [
                    {
                      "use": "official",
                      "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": npi,
                      "_value": {
                        "fhir_comments": [
                          "   NPI  "
                        ]
                      }
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
    ps["address"]= []
    ps['telecom'] = []

    return ps



def new_fhir_organization_stub(npi, organization_name):

    text = "NPI %s for %s" % (npi, organization_name)
    os = OrderedDict()
    os["resourceType"] = "Organization"
    os["npi"] = npi
    os["text"] = { "status": "generated",
                   "div": "<div><p>%s</p></div>" % (text)
                 }
    os['identifier'] = [
                    {
                      "use": "official",
                      "system": "http://hl7.org/fhir/sid/us-npi",
                      "value": npi,
                      "_value": {
                        "fhir_comments": [
                          "   NPI  "
                        ]
                      }
                    }
                  ]
    os['active'] = bool(True)
    os['name'] = organization_name
    os["address"]= []
    os['telecom'] = []
    return os





def publiccsv2fhir(csvfile, output_dir):

    """Return a response_dict with summary of  publiccsv2fhir transaction."""


    process_start_time = time.time()

    pdir = 1


    #make the output dir
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

    response_dict = OrderedDict()
    fh = open(csvfile, 'r')
    csvhandle = csv.reader(fh, delimiter=',')
    rowindex = 0
    po_count = 0
    error_list = []

    for row in csvhandle :
        if rowindex==0:

            rowindex += 1
            column_headers = row

            cleaned_headers = []
            for c in column_headers:
                c= c.replace(".", "")
                c= c.replace("(", "")
                c= c.replace(")", "")
                c =c.replace("$", "-")
                c =c.replace(" ", "_")
                cleaned_headers.append(c)
        else:

            #If the records is not redacted (because its inactive)

            zip_record = list(zip(cleaned_headers, row))
            record = dict(list(zip(cleaned_headers, row)))

            #get rid of blanks
            no_blank_zip = []
            for i in zip_record:
                if i[1]:
                    no_blank_zip.append(i)

            #start our object off with a stub.

            if row[1] == "1":
                r =  new_fhir_practitioner_stub(row[0], row[8],  row[6], row[5], row[9])

            elif row[1] == "2":
                r =  new_fhir_organization_stub(row[0], row[4])

            else:
                r = newfhir_deactive_stub()



            #Work Address

            a = OrderedDict()
            r['address']=[]
            a["use"]  = "work"
            a["line"] = []
            a["line"].append(row[28].upper())
            if row[29]:
                a["line"].append(row[29].upper())
            a["city"]        = row[30].upper()
            a["state"]       = row[31].upper()
            a["postalCode"]  = row[32].upper()
            a["country"]     = row[33].upper()

            r['address'].append(a)

            #Gender
            if row[1] == "1":
                if row[41] == "M":
                    r["gender"] = "male"
                elif row[41] == "F":
                    r["gender"] = "female"
                elif row[41] != "M" or "F":
                    r["gender"] = "other"
                else:
                    r["gender"] = "unknown"

            #Organization Contact
            #Is this logic ok, or problematic?
            if row[43]:
                contact = [
                            {
                'purpose': {
                    'text': "Admin",
                },
                'name': {
                          "family": [
                            row[42]
                          ],
                          "given": [
                            row[43]
                          ],
                          "suffix": [
                            row[312]
                          ],
                          "prefix": [
                            row[311]
                          ]
                      },

                'telecom': [
                                {
                                "system": "phone",
                                "value": "%s-%s-%s" % (row[46][0:3], row[46][3:6], row[46][6:12]),
                                "use" : "work"
                                }
                        ]
                    }
                ]
                r['contact'] = contact

            #Provider Business Practice Location Address Telephone Number
            if row[34]:
                t = [
                        {
                            "system": "phone",
                            "value": "%s-%s-%s" % (row[34][0:3], row[34][3:6], row[34][6:12]),
                            "use" : "work"
                        }
                    ]
                r['telecom'] = t
            #Provider Business Practice Location Address Fax Number
            if row[35]:
                t = [
                        {
                            "system": "fax",
                            "value": "%s-%s-%s" % (row[35][0:3], row[35][3:6], row[35][6:12]),
                            "use" : "work"
                        }
                    ]
                r['telecom'] = t



            #Mailing address --------------------
            a = OrderedDict()
            a['use'] = 'home'
            a['line'] = []
            a['line'].append(row[20].upper())
            if row[21]:
                a['line'].append(row[21].upper())
            a["city"]                            =  row[22].upper()
            a["state"]                           =  row[23].upper()
            a["postalCode"]                       =  row[24].upper()
            a["country"] = row[25].upper()
            r['address'].append(a)


            #Phone and Fax numbers
            if row[26]:
                t = [
                        {
                            "system": "phone",
                            "value": "%s-%s-%s" % (row[26][0:3], row[26][3:6], row[26][6:12]),
                            "use" : "home"
                        }
                    ]
                r['telecom'] = t


            if row[27]:
                t = [
                        {
                            "system": "fax",
                            "value": "%s-%s-%s" % (row[27][0:3], row[27][3:6], row[27][6:12]),
                            "use" : "home"
                        }
                    ]
                r['telecom'] = t

            #Extension, specifically taxonomy codes

            # Getting taxonomy codes

            for i in range(50,107,4):
                if row[i] == "Y":

                    taxonomy = OrderedDict()
                    #Fill in url
                    taxonomy['url'] = ''
                    coding = OrderedDict()
                    coding['system'] = "http://www.nucc.org/"
                    coding['code'] = row[i-3],
                    #To be filled in
                    coding['display'] = ""
                    taxonomy['valueCodeableConcept'] = coding
                    r['extension'] = [taxonomy]


            fn = "%s.json" % (row[0])

            if not r['resourceType']:
                subdir = os.path.join(output_dir, "Deactive",  str(row[0])[0:4])
            elif r['resourceType']=="Practitioner":
                subdir = os.path.join(output_dir, "Practitioner",  str(row[0])[0:4])
            elif r['resourceType']=="Organization":
                subdir = os.path.join(output_dir, "Organization",  str(row[0])[0:4])



            try:
                os.mkdir(subdir)
            except:
                pass


            fp = os.path.join(subdir, fn)
            ofile =  open(fp, 'w')
            ofile.writelines(json.dumps(r, indent =4))
            ofile.close()
            po_count += 1

            if po_count % 1000 == 0:
               pdir += 1
               out  = "%s files created. Total time is %s seconds." % (po_count ,(time.time() - process_start_time) )
               print((out))


            rowindex += 1


        if error_list:
                response_dict['num_files_created']=rowindex-1
                response_dict['num_file_errors']=len(error_list)
                response_dict['errors']=error_list
                response_dict['code']=400
                response_dict['message']="Completed with errors."
        else:

                response_dict['num_files_created']=rowindex -1
                response_dict['num_csv_rows']=rowindex -1
                response_dict['code']=200
                response_dict['message']="Completed without errors."
    fh.close()
    return response_dict

if __name__ == "__main__":


    if len(sys.argv)!=3:
        print("Usage:")
        print("csv2fhir-public.py [CSVFILE] [OUTPUT_DIRECTORY]")
        sys.exit(1)

    csv_file   = sys.argv[1]
    output_dir = sys.argv[2]

    result = publiccsv2fhir(csv_file, output_dir)

    #output the JSON transaction summary
    print((json.dumps(result, indent =4)))
