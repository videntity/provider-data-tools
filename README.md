pdt - Provider Data Tools
=========================

Version: 0.8.4



This repository contains a number of command-line utilities and related code libraries for
parsing, creating, and validating US-based health provider data.  These tools are:  

  __Parsing Scripts__  

* chop_nppes_public.py   - Parse the npi public data dissemination into flattened files.
* csv2pjson_public.py - Parse the npi public data dissemination into ProviderJSON files.
* csv2fhir.py  - Parse the npi public data dissemination to FHIR Practitioner and Organization Resources.
* validate_pjson      - Parse a Provider JSON document and output errors and warnings as JSON.
* validate_pjson_dir  - Bulk validation of the output of csv2pjson-public.py.  
* makepecosdocs.py    - Creates affiliations from initial PECOS data sets within MongoDB.
* combine_nppes_pecos_org_fhir.py - Combines NPPES and PECOS organization data within MongoDB, based on NPI's.
* combine_nppes_pecos_pract_fhir.py - Combines NPPES and PECOS practitioner data within MongoDB, based on NPI's.

__Indexing Scripts__  

Note: These scripts are only meant to be run after the data/files to be indexed have already been loaded into MongoDB.

* create_provider_indexes.py - Create default MongoDB indexes on Provider JSON data to support public       search on common fields.   

* create_pecos_indexes.py - Create default MongoDB indexes on PECOS data (Base, Reassignments, Addresses)

* create_pecos_compiled_indexes.py - Create default MongoDB indexes on PECOS compiled data (after running makepecosdocs.py)

* create_combined_indexes.py - Create default MongoDB indexes on combined PECOS and NPPES data (after running the combine* scripts)


__Pulling/Loading Scripts__  

* pull_pecos.py       - Download all or pieces of the PECOS Database in CSV format.
* loadnppes.py        - Download public NPPES file, parse to JSON, and load to MongoDB in one step.
* load_pecos.py       - Download public PECOS csv file(s) and NPPES data, parse, load and combine in MongoDB in one step.
* load_nppes_and_pecos.py - loadnppes.py and load_pecos.py in one step.

__Utility Scripts__

* json_schema_check_fhir.py - A FHIR resource specific JSON schema validator.
* json_schema_check.py - Generic JSON schema validation against a JSON file.

Please note the utilities `csv2json`, `json2mongo`, and `jsondir2mongo` have been
moved from `pdt` and placed in their own package called `jdt`. These tools are generic
and have utility outside health provider data.


Requirements
------------
These scripts require Python >= 3.3

In order to utilize all of the scripts that Provider Data Tools provides, you will need to have MongoDB Installed and running. See [MongoDB](https://docs.mongodb.com/manual/installation/) Docs for reference on installation.


Installation
------------

You can install the tool using `pip`.

To install with pip just type:

    ~$ sudo pip install pdt

Note: If you use `sudo`, the scripts  will be installed at the system level and used by all users.
Add  `--upgrade` to the above install instructions to ensure you fetch the newest version.

chop_nppes_public.py
-----------------


To make use of this script you need first fecth the "NPPES Data Dissemination" file.

To obtain the "NPPES Data Dissemination", go to  http://download.cms.gov/nppes/NPI_Files.html.
Get the "Full Replacement Monthly" zip file.  Unzip the file with the unzip tool of your choice.



To run the utility simply call it on a command line and provide one command line argument, the csv file to parse:

    ~$ chop_nppes_public.py npidata_20050523-20220404.csv

The file name `npidata_20050523-20220404.csv` will vary depending on the date.

The script make take a few minutes to complete. When it completes you will have more files
in your current directory. Everything is still indexed by NPI. These files are described below.


* _basic.csv             - Contains basic demographic info.
* _addresses_flat.csv    - one address per line identifier as practice or mailing.
* _identifiers_flat.csv  - one identifier per line.
* _licenses_flat.csv 	 - one license per line.
* _taxonomy_flat.csv     - one taxonomy code per line and identified as primary or not.


csv2pjson_public.py
------------------

Convert the NPPES Public Data Dissemination CSV file format to a directory of files in
ProviderJSON format.

Usage:

    csv2pjson_public.py [CSV_FILE] [OUTPUT_DIR]


Example:


    csv2pjson_public.py public_csvfile.csv output

Output:

  One file is created per line in the CSV file file inside  the directory`output`. Files are fanned out
  into a directory structure so as not to create millions of files in one directory.


csv2fhir.py
------------------

Convert the NPPES Public Data Dissemination  CSV file format to a directory of files in
ProviderJSON format.

Usage:

    csv2fhir.py [CSV_FILE] [OUTPUT_DIR]


Example:


    csv2fhir_public.py public_csvfile.csv output

Output:

  One file is created per line in the CSV file file inside  the directory`output`. Files are fanned out
  into a directory structure so as not to create millions of files in one directory.





validate_pjson
--------------

Validate the PJSON for compliance with a create/update request. It returns errors and warnings in
JSON to stdout.

Usage:


    validate_pjson [ProivderJSON] [update|create]


Example:

    validate_pjson  1003819723.json update

Example Output:

    {
    "errors": [
        "authorized_official_telephone_number must be in XXX-XXX-XXXX format.",
        "EIN is required for a type-2 organization provider."
    ],
    "warnings": [
        "Enumeration date is generated by CMS. The provided value will be ignored.",
        "Last updated date is generated by CMS. The provided value will be ignored.",
        "status is determined by CMS. The provided value will be ignored."
    ]
    }




pull_pecos.py
------------

The script will download all or individual Public Provider Enrollment Files
from https://data.cms.gov/public-provider-enrollment in CSV format. Note that
`wget` is a requirement for this script.

  Usage:

      pull_pecos.py [DOWNLOAD ALL Y/N] [DOWNLOAD BASE Y/N] [DOWNLOAD REASSIGNMENT Y/N]  [DOWNLOAD ADDRESS Y/N]

  Example:

      pull_pecos.py y n n n

  Example Output:


          Downloading Address CSV file
        --2016-07-12 10:39:00--  https://data.cms.gov/api/views/je57-c47h/rows.csv?accessType=DOWNLOAD
        Resolving data.cms.gov (data.cms.gov)... 216.227.229.148
        Connecting to data.cms.gov (data.cms.gov)|216.227.229.148|:443... connected.
        HTTP request sent, awaiting response... 200 OK
        Length: unspecified [text/csv]
        Saving to: ‘pecos_address.csv’

        pecos_address.csv
          [                  <=>              ]   3.14M   914KB/s   


  loadnppes.py
------------

By streamlining several of the pdt utilities, the script loadnppes.py combines functionalty
for automatic setup. The script will download public data, parse to JProvider SON, and load
to MongoDB in one step. Note this script requires `unzip` and `wget` to be installed.

Usage:

    loadnppes.py [PROCESS_FULL Y/N] [DOWNLOAD_FROM_PUBLIC_FILE Y/N] [DELETE FILES AFTER UPLOADED TO MONGO?]"

Example:

    loadnppes.py y y

Example Output:



    Downloading http://nppes.viva-it.com/NPPES_Data_Dissemination_March_2015.zip
    --2015-04-13 14:14:57--  http://nppes.viva-it.com/NPPES_Data_Dissemination_March_2015.zip
    Resolving nppes.viva-it.com (nppes.viva-it.com)... 68.142.118.4, 68.142.118.254
    Connecting to nppes.viva-it.com (nppes.viva-it.com)|68.142.118.4|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 514406694 (491M) [application/zip]
    Saving to: `NPPES_Data_Dissemination_March_2015.zip'

    0% [                                       ] 2,691,064   58.1K/s  eta 3h 38m
    .
    .
    .
