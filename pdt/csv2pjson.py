#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

import os, sys, string, json, csv, time, uuid
from collections import OrderedDict
from datetime import datetime






def new_pjson_stub():

    ps = OrderedDict()

    #ProviderJSON stub
    ps['enumeration_type']=""
    ps['number'] =""
    ps['last_updated_epoch'] =""
    ps['created_epoch'] =""
    ps["basic"] = OrderedDict()
    ps["basic"]["status"]= ""
    ps["basic"]["name_prefix"]= ""
    ps["basic"]["first_name"]= ""
    ps["basic"]["last_name"]= ""
    ps["basic"]["middle_name"]= ""
    ps["basic"]["name_suffix"]= ""
    ps["basic"]["credential"]= ""
    ps["basic"]["doing_business_as"]= ""
    ps["basic"]["sole_proprietor"]= ""
    ps["basic"]["other_first_name_1"]= ""
    ps["basic"]["other_first_name_2"]= ""
    ps["basic"]["other_last_name_1"]= ""
    ps["basic"]["other_last_name_2"]= ""
    ps["basic"]["other_middle_name_1"]= ""
    ps["basic"]["other_middle_name_2"]= ""
    ps["basic"]["other_name_code_1"]= ""
    ps["basic"]["other_name_code_2"]= ""
    ps["basic"]["other_name_credential_1"]= ""
    ps["basic"]["other_name_credential_2"]= ""
    ps["basic"]["other_name_prefix_1"]= ""
    ps["basic"]["other_name_prefix_2"]= ""
    ps["basic"]["other_name_suffix_1"]= ""
    ps["basic"]["other_name_suffix_2"]= ""
    ps["basic"]["organization_name"]= ""
    ps["basic"]["organization_other_name"]= ""
    ps["basic"]["organization_other_name_code"]= ""
    ps["basic"]["organizational_subpart"]= ""
    ps["basic"]["ssn"]= ""
    ps["basic"]["ein"]= ""
    ps["basic"]["itin"]= ""
    ps["basic"]["gender"]= ""
    ps["basic"]["date_of_birth"]= ""
    ps["basic"]["state_of_birth"]= ""
    ps["basic"]["country_of_birth"]= ""
    ps["basic"]["number"]= ""
    ps["basic"]["initial_enumeration_date"]= ""
    ps["basic"]["enumeration_date"]= ""
    ps["basic"]["last_updated"]= ""
    ps["basic"]["date_of_death"]= ""
    ps["basic"]["reactivation_date"]= ""
    ps["basic"]["contact_method"]= "E"
    ps["basic"]["deactivated_details"]= ""
    ps["basic"]["deactivation_date"]= "None"
    ps["basic"]["deactivation_reason_code"]= ""
    ps["basic"]["decativation_note"]= ""
    ps["basic"]["deceased_notes"]= ""
    ps["basic"]["parent_organization"]= ""
    ps["basic"]["parent_organization_ein"]= ""
    ps["basic"]["parent_organization_legal_business_name"]= ""
    ps["basic"]["recativation_note"]= ""
    ps["basic"]["comments"]= ""
    ps["basic"]["authorized_official_credential"]= ""
    ps["basic"]["authorized_official_email"]= ""
    ps["basic"]["authorized_official_first_name"]= ""
    ps["basic"]["authorized_official_last_name"]= ""
    ps["basic"]["authorized_official_middle_name"]= ""
    ps["basic"]["authorized_official_prefix"]= ""
    ps["basic"]["authorized_official_suffix"]= ""
    ps["basic"]["authorized_official_telephone_number"]= ""
    ps["basic"]["authorized_official_telephone_extension"]= ""
    ps["basic"]["authorized_official_title"]= ""
    ps["basic"]["authorized_official_title_or_position"]= ""
    ps["basic"]["contact_person_credential"]= ""
    ps["basic"]["contact_person_email"]= ""
    ps["basic"]["contact_person_first_name"]= ""
    ps["basic"]["contact_person_last_name"]= ""
    ps["basic"]["contact_person_middle_name"]= ""
    ps["basic"]["contact_person_prefix"]= ""
    ps["basic"]["contact_person_suffix"]= ""
    ps["basic"]["contact_person_telephone_extension"]= ""
    ps["basic"]["contact_person_telephone_number"]= ""
    ps["basic"]["contact_person_title"]= ""
    ps["basic"]["contact_person_title_or_position"]= ""
    ps["addresses"] = []
    ps["taxonomies"] = []
    ps["licenses"] = []
    ps["identifiers"] = []
    return ps




def gao_csv2pjson(csvfile, output_dir):
    
    """Return a response_dict with summary of gao_csv2pjson transaction."""


    process_start_time = time.time()

    pdir = 1


    #make the output dir
    try:
        os.mkdir(output_dir)
    except:
        pass


    response_dict = OrderedDict()
    fh = open(csvfile, 'rb')
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

            #If the records is not redacted
            if row[1]:
                zip_record = zip(cleaned_headers, row)
                record = dict(zip(cleaned_headers, row))

                #get rid of blanks
                no_blank_zip = []
                for i in zip_record:
                    if i[1]:
                        no_blank_zip.append(i)

                #start our object off with a stub.
                p = new_pjson_stub()


                if row[1] == "1":
                    p["enumeration_type"] = "NPI-1"
                if row[1] == "2":
                    p["enumeration_type"] = "NPI-2"

                #determine the status
                if row[0]:
                    p["number"]             = int(row[0])

                #Load basic ----------------------------------------

                #if deactivated date and no reactivation date
                if row[43] and not row[44]:
                    p["basic"]["status"]= "D"
                    month  = row[43][0:2]
                    day    = row[43][3:5]
                    year   = row[43][6:10]
                    #deactivation date
                    p["basic"]["deactivation_date"] = "%s-%s-%s" % (year, month, day)
                else:
                    p["basic"]["status"]= "A"
                
                #reactivation date
                if row[44]:
                    month  = row[44][0:2]
                    day    = row[44][3:5]
                    year   = row[44][6:10]
                    p["basic"]["reactivation_date"] = "%s-%s-%s" % (year, month, day)
                

                #PII
                p["basic"]["ssn"] =  row[3]
                p["basic"]["itin"] = row[4]
                p["basic"]["ein"] =  row[5]
                p["basic"]["state_of_birth"] = row[47]
                p["basic"]["country_of_birth"] = row[48]

                if row[46]:
                    month  = row[46][0:2]
                    day    = row[46][3:5]
                    year   = row[46][6:10]
                    p["basic"]["date_of_birth"] = "%s-%s-%s" % (year, month, day)

                p['basic']["organization_parent_ein"]  =  row[331]


                #Provider name
                p["basic"]["name_prefix"]       = row[10].capitalize()
                p["basic"]['first_name']        = row[8].capitalize()
                p["basic"]["middle_name"]       = row[9].capitalize()
                p["basic"]['last_name']         = row[7].capitalize()
                p["basic"]["name_suffix"]       = row[11].capitalize()
                p["basic"]["credential"]        = row[12]
                p["basic"]["gender"]            = row[45]

                if row[307] in (True, "Y", "y", "YES"):
                    p["basic"]["sole_proprietor"]       = "YES"
                else:
                    p["basic"]["sole_proprietor"]       = "NO"

                p["basic"]["parent_organization_ein"]   = row[310]

                #provider_organization
                p["basic"]["organization_name"]         = row[13]
                p["basic"]["parent_organization_lbn"]   = row[309]

                #other name
                p["basic"]["other_organization_name"]   = row[13]
                p["basic"]["other_organization_code"]   = row[14]


                p["basic"]["other_last_name_1"]     = row[15].capitalize()
                p["basic"]["other_first_name_1"]    = row[16].capitalize()
                p["basic"]["other_middle_name_1"]   = row[17].capitalize()
                p["basic"]["other_name_prefix_1"]   = row[18].capitalize()
                p["basic"]["other_name_suffix_1"]   = row[19].capitalize()
                p["basic"]["other_name_credential_1"] = row[20]
                p["basic"]["other_name_code_1"]       = row[21]

                p["basic"]["enumeration_date"]          = row[40]
                
                if p["basic"]["enumeration_date"]:
                    p['created_epoch'] = int(datetime(int(p["basic"]["enumeration_date"][6:10]),
                                                           int(p["basic"]["enumeration_date"][0:2]),
                                                           int(p["basic"]["enumeration_date"][3:5]),
                                                           0, 0).strftime('%s'))
                
                
                p["basic"]["last_updated"]              = row[41]
                if p["basic"]["last_updated"]:
                    p['last_updated_epoch'] = int(datetime(int(p["basic"]["last_updated"][6:10]),
                                                           int(p["basic"]["last_updated"][0:2]),
                                                           int(p["basic"]["last_updated"][3:5]),
                                                           0, 0).strftime('%s'))
                
                
                p["basic"]["deactivation_date"]         = row[43]
                p["basic"]["reactivation_date"]         = row[44]
                p["basic"]["deactivation_reason_code"]  = row[42]


                if row[40]:
                    month = row[40][0:2]
                    day =  row[40][3:5]
                    year = row[40][6:10]
                    p["basic"]["enumeration_date"] = "%s-%s-%s" % (year, month, day)

                if row[41]:
                    month = row[41][0:2]
                    day =  row[41][3:5]
                    year = row[41][6:10]
                    p["basic"]["last_updated"] = "%s-%s-%s" % (year, month, day)

                if row[43]:
                    month = row[43][0:2]
                    day =  row[43][3:5]
                    year = row[43][6:10]
                    p["basic"]["deactivation_date"] = "%s-%s-%s" % (year, month, day)


                if row[44]:
                    month = row[44][0:2]
                    day =  row[44][3:5]
                    year = row[44][6:10]
                    p["basic"]["reactivation_date"] = "%s-%s-%s" % (year, month, day)


                #Contact person
                p["basic"]["contact_person_last_name"]          = row[58]
                p["basic"]["contact_person_first_name"]         = row[59]
                p["basic"]["contact_personl_middle_name"]       = row[60]
                p["basic"]["contact_person_prefix"]             = row[61]
                p["basic"]["contact_person_suffix"]             = row[62]
                p["basic"]["contact_person_credential"]         = row[63]
                p["basic"]["contact_person_title_or_position"]  = row[64]
                p["basic"]["contact_person_telephone_number"]   =  "%s-%s-%s" % (row[65][0:3], row[65][3:6], row[65][6:12])
                p["basic"]["contact_person_telephone_extension"] =  row[66]
                p["basic"]["contact_person_email"]               =  row[67]

                #not included in public file

                #Authorized official
                p["basic"]["authorized_official_last_name"] = row[49]
                p["basic"]["authorized_official_first_name"] = row[50]
                p["basic"]["authorized_official_middle_name"] = row[51]
                p["basic"]["authorized_official_prefix"] = row[52]
                p["basic"]["authorized_official_suffix"] = row[53]
                p["basic"]["authorized_official_credential"] = row[54]
                p["basic"]["authorized_official_title_or_position"] = row[55]

                if row[56]:
                    p["basic"]["authorized_official_telephone_number"] =  "%s-%s-%s" % (row[56][0:3], row[56][3:6], row[56][6:12])
                p["basic"]["authorized_official_telephone_extension"] =  row[57]
                p["basic"]["mode"] = "W"


                clean_basic = OrderedDict()
                for k,v in p["basic"].items():
                    if v:
                        if v.isdigit():
                            clean_basic[k] = int(v)
                        else:
                            clean_basic[k] = v
                    
                p["basic"] = clean_basic

                #Addresses
                #location ----------------------------------------------------
                a = OrderedDict()
                a["country_code"]                    = row[36]
                a["address_purpose"]                 = "LOCATION"

                if a["country_code"] == "US":
                    a["address_type"]                    = "DOM"
                    a["address_1"]                       =  row[31]
                    a["address_2"]                       =  row[32]
                    a["city"]                            =  row[33]
                    a["state"]                           =  row[34]
                    a["zip"]                             =  row[35]
                    
                    if a["zip"].isdigit():
                        a["zip"] = int(a["zip"])
                    
                    a["telephone_number_extension"]      =  row[38]

                    if row[34]:

                        a["us_telephone_number"]         =  "%s-%s-%s" % (row[37][0:3], row[37][3:6], row[37][6:12])

                    if  row[35]:
                        a["us_fax_number"]               =  "%s-%s-%s" % (row[39][0:3], row[39][3:6], row[39][6:12])

                else:
                    a["address_type"]                    = "FGN"
                    a["address_1"]                       =  row[31]
                    a["address_2"]                       =  row[32]
                    a["city"]                            =  row[33]
                    a["foreign_state"]                   =  row[34]
                    a["foreign_postal"]                  =  row[35]
                    
                    if a["foreign_postal"].isdigit():
                        a["foreign_postal"] = int(a["foreign_postal"])
                        
                    a["foreign_telephone_number"]        =  row[34]
                    a["foreign_fax_number"]              =  row[35]
                    a["telephone_number_extension"]      =  row[38]


                p['addresses'].append(a)

                #Mailing address ---
                a = OrderedDict()
                a["country_code"]                    = row[27]
                a["address_purpose"]                 = "MAILING"

                if a["country_code"] == "US":
                    a["address_type"]                    = "DOM"
                    a["address_1"]                       =  row[22]
                    a["address_2"]                       =  row[23]
                    a["city"]                            =  row[24]
                    a["state"]                           =  row[25]
                    a["zip"]                             =  row[26]
                    
                    if a["zip"].isdigit():
                        a["zip"] = int(a["zip"])
                    
                    
                    a["telephone_number_extension"]      =  row[29]
                    if row[26]:
                        a["us_telephone_number"] =  "%s-%s-%s" % (row[28][0:3], row[28][3:6], row[28][6:12])

                    if row[27]:

                        a["us_fax_number"]       =  "%s-%s-%s" % (row[30][0:3], row[30][3:6], row[30][6:12])

                else:
                    a["address_type"]                    = "FGN"
                    a["address_1"]                       =  row[22]
                    a["address_2"]                       =  row[23]
                    a["city"]                            =  row[24]
                    a["foreign_state"]                   =  row[25]
                    a["foreign_postal"]                  =  row[26]
                    
                    if a["foreign_postal"].isdigit():
                        a["foreign_postal"] = int(a["foreign_postal"])
                    
                    a["foreign_telephone_number"]        =  row[28]
                    a["foreign_fax_number"]              =  row[30]


                p['addresses'].append(a)

                #licenses and taxonomies----------------------------------------
                #starting at row 47, 2nd set starts at 51

                #Taxonomy
                taxonomy_code_position = 68
                primary_taxonomy_position = 71
                license_state_position = 70
                license_number_position = 69


                for i in range(1, 15):

                    if row[taxonomy_code_position]:
                        taxonomy = OrderedDict()
                        taxonomy['code'] = row[taxonomy_code_position]
                        if row[primary_taxonomy_position] in ("Y", "True", True, "YES"):
                            taxonomy['primary'] = True
                        else:
                            taxonomy['primary'] = False

                        p['taxonomies'].append(taxonomy)

                     #License
                    if row[license_number_position]:

                        license             = OrderedDict()
                        mlvs                = "%s-UNK-%s" % (row[license_state_position], row[license_number_position])
                        license['code']     = mlvs
                        license['state']    = row[license_state_position]
                        license['type']     = "UNK"
                        license['status']   = "UNK"

                        p['licenses'].append(license)


                    taxonomy_code_position += 4
                    primary_taxonomy_position += 4
                    license_state_position += 4
                    license_number_position += 4

                #identifiers----------------
                #starting at row 107

                identifier_position = 128
                identifier_code_position = 129
                identifier_state_position = 130
                identifier_issuer_position = 131

                for i in range(1, 50):

                    if row[identifier_position]:
                        identifier = OrderedDict()
                        identifier['identifier'] = row[identifier_position]
                        
                        if identifier["identifier"].isdigit():
                            identifier["identifier"] = int(identifier["identifier"])
                        
                        
                        identifier['code'] = row[identifier_code_position]
                        identifier['state'] = row[identifier_state_position]
                        identifier['issuer'] = row[identifier_issuer_position]
                        p['identifiers'].append(identifier)


                    identifier_position += 4
                    identifier_code_position  += 4
                    identifier_state_position  += 4
                    identifier_issuer_position  += 4


                if p["number"]:
                    fn = "%s.json" % (p["number"])
                    subdir = os.path.join(output_dir, str(p["number"])[0:4])
                else:
                    guid = str(uuid.uuid4())
                    if p["enumeration_type"]=="NPI-1" and  p["basic"]["first_name"] and p["basic"]["last_name"]:
                        fn = "%s-%s-%s.json" % (p["basic"]["first_name"], p["basic"]["last_name"], guid[0:8])
                    elif  p["enumeration_type"]=="NPI-2" and p["basic"]["organization_name"]:
                        fn = "%s-%s.json" % (p["basic"]["organization_name"], guid[0:8])
                    else:
                        fn = "%s.json" % (guid)
                    
                    subdir = os.path.join(output_dir, "no-id")

                try:
                    os.mkdir(subdir)
                except:
                    pass


                fp = os.path.join(subdir, fn)
                ofile =  open(fp, 'w')
                ofile.writelines(json.dumps(p, indent =4))
                ofile.close()
                po_count += 1
                if po_count % 100 == 0:
                   out  = "%s files created. Total time: %s seconds." % (po_count ,(time.time() - process_start_time) )
                   print out

                if po_count % 1000 == 0:
                   pdir += 1

                   out  = "%s files created. Total time: %s seconds." % (po_count ,(time.time() - process_start_time) )
                   print out


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

    return response_dict

if __name__ == "__main__":


    if len(sys.argv)!=3:
        print "Usage:"
        print "csv2pjson-public [CSVFILE] [OUTPUT_DIRECTORY]"
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]



    result = gao_csv2pjson(csv_file, output_dir)

    #output the JSON transaction summary
    print json.dumps(result, indent =4)
