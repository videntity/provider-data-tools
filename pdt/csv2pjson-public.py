#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

import os, sys, string, json, csv, time
from collections import OrderedDict
from datetime import datetime



def new_pjson_deactive_stub():
    ps = OrderedDict()
    
    #ProviderJSON stub
    ps['enumeration_type']=""
    ps['number'] =""
    ps['title'] ="Deactive"
    ps["basic"] = OrderedDict()
    ps["basic"]["status"]= "D" 
    ps["basic"]["deactivation_date"]= ""
    return ps
    
def new_pjson_stub():
    
    ps = OrderedDict()
    
    #ProviderJSON stub
    ps['enumeration_type']=""
    ps['number'] =""
    ps['title'] = ""
    ps['last_updated_epoch'] =""
    ps['created_epoch'] =""
    ps["basic"] = OrderedDict()
    ps["basic"]["name_prefix"]= "" 
    ps["basic"]["first_name"]= "" 
    ps["basic"]["last_name"]= "" 
    ps["basic"]["middle_name"]= "" 
    ps["basic"]["name_suffix"]= "" 
    ps["basic"]["credential"]= "" 
    ps["basic"]["sole_proprietor"]= "" 
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
    ps["basic"]["status"]= "A" 
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
    ps["other_names"]       = []
    ps["addresses"]         = []
    ps["taxonomies"]        = []
    ps["licenses"]          = []
    ps["taxonomy_licenses"] = []
    ps["identifiers"]       = []
    ps["taxonomy_groups"]   = []
    return ps
    

def publiccsv2pjson(csvfile, output_dir):

    """Return a response_dict with summary of  publiccsv2pjson transaction."""


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

            #If the records is not redacted (because its inactive)
            
            zip_record = zip(cleaned_headers, row)
            record = dict(zip(cleaned_headers, row))
            
            #get rid of blanks 
            no_blank_zip = []
            for i in zip_record:
                if i[1]:
                    no_blank_zip.append(i)
                        
            #start our object off with a stub.
            
            if row[1]:
                p = new_pjson_stub()
                
                
                if row[1] == "1":
                    p["enumeration_type"] = "NPI-1"
                    p["title"] = "%s %s" % (row[6], row[5])
                    if row[10]:
                         p["title"] = "%s, %s" % (p["title"], row[10])
                    
                elif row[1] == "2":
                    p["enumeration_type"] = "NPI-2"
                    p["title"] = row[4]
                    
                else:
                    #The record is deactivated
                    p['basic']['status'] ="D"
                    p["title"] = "Deactivated"
                
                p["number"]             = row[0] 
                #Load basic                
                for i in range(0, len(row)):
                    if row[i]:
                        row[i] = row[i].decode('ascii', 'ignore')
                    else:
                         row[i] = ""
                

                #Provider name
                p["basic"]["name_prefix"]       = row[8].capitalize()
                p["basic"]['first_name']        = row[6].upper()
                p["basic"]["middle_name"]       = row[7].upper()
                p["basic"]['last_name']         = row[5].upper()
                p["basic"]["name_suffix"]       = row[9]
                p["basic"]["credential"]        = row[10]
                p["basic"]["gender"]            = row[41].upper()
                
                if row[307] in (True, "Y", "y", "YES"):
                    p["basic"]["sole_proprietor"]   = "YES"
                else:
                    p["basic"]["sole_proprietor"]   = "NO"
                    
                
                #provider_organization
                p["basic"]["organization_name"] = row[4]
                
                
                p["basic"]["ein"]              = row[3]     
                if p["basic"]["ein"] == "<UNAVAIL>":
                    p["basic"]["ein"] = ""
                
                p["basic"]["parent_organization_ein"] = row[310]
                p["basic"]["parent_organization_legal_business_name"] = row[309]
                
                
                p["basic"]["enumeration_date"]      = row[36]
                if p["basic"]["enumeration_date"]:
                    p['created_epoch'] = int(datetime(int(p["basic"]["enumeration_date"][6:10]),
                                                           int(p["basic"]["enumeration_date"][0:2]),
                                                           int(p["basic"]["enumeration_date"][3:5]),
                                                           0, 0).strftime('%s'))
                
                
                p["basic"]["last_updated"]              = row[37]
                if p["basic"]["last_updated"]:
                    p['last_updated_epoch'] = int(datetime(int(p["basic"]["last_updated"][6:10]),
                                                           int(p["basic"]["last_updated"][0:2]),
                                                           int(p["basic"]["last_updated"][3:5]),
                                                           0, 0).strftime('%s'))
                
                
                p["basic"]["deactivation_date"]         = row[39]
                p["basic"]["reactivation_date"]         = row[40]
                p["basic"]["deactivation_reason_code"]  = row[38]
                
                if row[37]:
                    month = row[37][0:2]
                    day =  row[37][3:5]
                    year = row[37][6:10]
                    p["basic"]["last_updated"] = "%s-%s-%s" % (year, month, day)
                
                if row[36]:
                    month = row[36][0:2]
                    day =  row[36][3:5]
                    year = row[36][6:10]
                    p["basic"]["enumeration_date"] = "%s-%s-%s" % (year, month, day)
                
                if row[39]:
                    month = row[39][0:2]
                    day =  row[39][3:5]
                    year = row[39][6:10]
                    p["basic"]["deactivation_date"] = "%s-%s-%s" % (year, month, day)
                
                
                if row[40]:
                    month = row[40][0:2]
                    day =  row[40][3:5]
                    year = row[40][6:10]
                    p["basic"]["reactivation_date"] = "%s-%s-%s" % (year, month, day)
                
            
                #Contact person not included in public file
               
                #Authorized official
                p["basic"]["authorized_official_last_name"]  = row[42].upper()
                p["basic"]["authorized_official_first_name"] = row[43].upper()
                p["basic"]["authorized_official_middle_name"] = row[44].upper()
                
                ao_phone_number = row[46].upper()
                
                ao_phone_number = "%s-%s-%s" % (ao_phone_number[0:3], ao_phone_number[3:6], ao_phone_number[6:12])
                
                if ao_phone_number != "--":
                    p["basic"]["authorized_official_telephone_number"] = ao_phone_number
                
                p["basic"]["authorized_official_title_or_position"] = row[45].upper()
                
                
                clean_basic = OrderedDict()
                for k,v in p["basic"].items():
                    if v:
                        clean_basic[k] = v
                         
                p["basic"] = clean_basic
                
                if row[11] or row[13] or row[14]:
                    other_name  = OrderedDict()
                    if row[11]:
                        other_name["organization_name"] = row[11].upper()
                    
                    if row[12]:
                        other_name["code"]= row[12].upper()
                    if row[19]:
                        other_name["code"]= row[19].upper()
                    
                    if row[13]:
                        other_name["last_name"]=row[13].upper()
                    if row[14]:
                        other_name["first_name"]=row[14].upper()
                    if row[15]:
                        other_name["middle_name"]=row[15].upper()
                    if row[16]:
                        other_name["prefix"]=row[16].capitalize()
                    if row[17]:
                        other_name["suffix"]=row[17].capitalize()
                    if row[18]:
                        other_name["credential"]=row[18]
                    p["other_names"].append(other_name)    
                
                
                #Addresses
                #location ---
                a = OrderedDict()
                a["country_code"]                    = row[33].upper()
                a["address_purpose"]                 = "LOCATION"
                
                if a["country_code"] == "US":
                    a["address_type"]                    = "DOM"
                    a["address_1"]                       =  row[28].upper()
                    a["address_2"]                       =  row[29].upper()
                    a["city"]                            =  row[30].upper()
                    a["state"]                           =  row[31].upper()
                    a["zip"]                             =  row[32].upper()
                                        
                    if row[34]:
                        
                        a["us_telephone_number"]         =  "%s-%s-%s" % (row[34][0:3], row[34][3:6], row[34][6:12])
                    
                    if  row[35]:    
                        a["us_fax_number"]               =  "%s-%s-%s" % (row[35][0:3], row[35][3:6], row[35][6:12])
    
                    
                else:
                    a["address_type"]                    = "FGN"
                    a["address_1"]                       =  row[28].upper()
                    a["address_2"]                       =  row[29].upper()
                    a["city"]                            =  row[30].upper()
                    a["foreign_state"]                   =  row[31].upper()
                    a["foreign_postal"]                  =  row[32].upper()                   
                    a["foreign_telephone_number"]        =  row[34].upper()
                    a["foreign_fax_number"]              =  row[35].upper()
    
    
                p['addresses'].append(a)
                
                #Maiing address ---
                a = OrderedDict()
                a["country_code"]                    = row[25].upper()
                a["address_purpose"]                 = "MAILING"
                
                if a["country_code"] == "US":
                    a["address_type"]                    = "DOM"
                    a["address_1"]                       =  row[20].upper()
                    a["address_2"]                       =  row[21].upper()
                    a["city"]                            =  row[22].upper()
                    a["state"]                           =  row[23].upper()
                    a["zip"]                             =  row[24].upper()
                    
                    if row[26]:
                        a["us_telephone_number"] =  "%s-%s-%s" % (row[26][0:3], row[26][3:6], row[26][6:12])
                    
                    if row[27]:
                        
                        a["us_fax_number"]       =  "%s-%s-%s" % (row[27][0:3], row[27][3:6], row[27][6:12])
                    
                    
                    
                else:
                    a["address_type"]                    = "FGN"
                    a["address_1"]                       =  row[20].upper()
                    a["address_2"]                       =  row[21].upper()
                    a["city"]                            =  row[22].upper()
                    a["foreign_state"]                   =  row[23].upper()
                    a["foreign_postal"]                  =  row[24].upper()
                    a["foreign_telephone_number"]        =  row[26].upper()
                    a["foreign_fax_number"]              =  row[27].upper()
    
    
                p['addresses'].append(a)
                
                #licenses and taxonomies----------------------------------------
                #starting at row 47, 2nd set starts at 51
                
                #Taxonomy
                taxonomy_code_position = 47
                primary_taxonomy_position = 50
                license_state_position = 49
                license_number_position = 48
                
                
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
                        license['state']    = row[license_state_position].upper()
                        license['type']     = "UNK"
                        license['status']   = "UNK"
                        
                        p['licenses'].append(license)
                    
                    #Taxonomy and License
                    if row[license_number_position] and row[taxonomy_code_position]:
                        taxonomy_license  = OrderedDict()
                        taxonomy_license['taxonomy_code'] = row[taxonomy_code_position]
                        mlvs = "%s-UNK-%s" % (row[license_state_position], row[license_number_position])
                        taxonomy_license['license_code'] = mlvs
                        p['taxonomy_licenses'].append(taxonomy_license)
                    
                    
                    taxonomy_code_position += 4
                    primary_taxonomy_position += 4
                    license_state_position += 4
                    license_number_position += 4
                
                #identifiers----------------
                #starting at row 107
                
                identifier_position = 107
                identifier_code_position = 108
                identifier_state_position = 109
                identifier_issuer_position = 110
                
                for i in range(1, 50):
                    
                    if row[identifier_position]:
                        identifier = OrderedDict()
                        identifier['identifier'] = row[identifier_position]                        
                        identifier['code'] = row[identifier_code_position]
                        identifier['state'] = row[identifier_state_position].upper()
                        identifier['issuer'] = row[identifier_issuer_position]
                        p['identifiers'].append(identifier)
                            
                
                    identifier_position        += 4
                    identifier_code_position   += 4
                    identifier_state_position  += 4
                    identifier_issuer_position += 4
                    
                #Get Taxonomy Groups for Type 2
                for i in range(314, 328):
                    if row[i]:
                        code, description = row[i].split(" ", 1)
                        tg = {"code": code, "description": description}
                        p['taxonomy_groups'].append(tg)
        
                #Remove any empty arrays
                if not p["other_names"]:
                    del p["other_names"]
                
                if not p["addresses"]:
                    del p["addresses"]
                
                if not p["taxonomies"]:
                    del p["taxonomies"]
                
                if not p["taxonomy_licenses"]:
                    del p["taxonomy_licenses"]                  
                
                if not p["licenses"]:
                    del p["licenses"]                
                     
                if not p["identifiers"]:
                    del p["identifiers"]
                    
                if not p["taxonomy_groups"]:
                    del p["taxonomy_groups"]                         
                
                
                
            else:
                
                p = new_pjson_deactive_stub()
                p["number"] = row[0]
                if row[39]:
                    month = row[39][0:2]
                    day =  row[39][3:5]
                    year = row[39][6:10]
                    p["basic"]["deactivation_date"] = "%s-%s-%s" % (year, month, day)
            
            fn = "%s.json" % (p["number"])
            
            subdir = os.path.join(output_dir, str(p["number"])[0:4])
            
            try:
                os.mkdir(subdir)
            except:
                pass
                   
                
            fp = os.path.join(subdir, fn)
            ofile =  open(fp, 'w')
            ofile.writelines(json.dumps(p, indent =4))
            ofile.close()
            po_count += 1
            
            if po_count % 1000 == 0:
               pdir += 1
               out  = "%s files created. Total time is %s seconds." % (po_count ,(time.time() - process_start_time) )
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
        print "csv2pjson-public.py [CSVFILE] [OUTPUT_DIRECTORY]"
        sys.exit(1)

    csv_file   = sys.argv[1]
    output_dir = sys.argv[2]

    result = publiccsv2pjson(csv_file, output_dir)
    
    #output the JSON transaction summary
    print json.dumps(result, indent =4)
