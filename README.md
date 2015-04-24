Provider Data Tools
===================

Version: 0.5.2

This reposiory contains a number of command-line utilities and related code libraries for
parsing, creating, and validating provider data data.  They are:

* chop-nppes-public   - Parse the npi public data dissemination into flattened files
* csv2mongo           - Converting a CSV into documents directly into a MongoDB datbase/collection
* json2mongo          - Convert a JSON file object into a record in a MongoDB datbase/collection.
* jsondir2mongo       - Convert a directory of files containing JSON objects into documents in a MongoDB database/collection.
* csv2pjson           - Parse NPI CSV files, containing PII, into provider JSON. Used for bulk upload.
* csv2pjson-public.py - Parse the npi public data dissemination into ProviderJSON files
* validate-pjson      - Parse a Provider JSON document and output errors and warnings as JSON.
* loadnppes.py        - Download public, parse to JSON, and load to MongoDB in one step.

Installation
------------

This simple utility creates several "flattened" CSV files from the origional NPPES public data dissemination file.  The only requirements to use the tool are

1. Obtain the public "NPPES Data Dissemination" CSV file
2. Have Python installed on your computer.  If you ae usung Mac or Linux, Python is already installed).

You can install the tool using `pip` or download it from GitHub (https://github.com/hhsidealab/provider-data-tools)


To install with pip just type:

    ~$ sudo pip install pdt

The utility `chop-nppes-public` will be installed at the system level, if you use `sudo`.


chop-nppes-public
-----------------


To make use of this script you need first fecth the "NPPES Data Dissemination" file.

To obtain the "NPPES Data Dissemination", go to  http://nppes.viva-it.com/NPI_Files.html.
Get the "Full Replacement Monthly" zip file.  Unzip the file with the unzip tool of your choice.



To run the utility simply call it on a command line and proivde one command line argument, the csv file to parse:

    ~$ chop-nppes-public npidata_20050523-20140413.csv

The file name `npidata_20050523-20140413.csv` will vary depending on the date.

The script make take a few minutes to complete. When it completes you will have more files
in your current directory. Everything is still indexed by NPI. These files are described below.


* _basic.csv             - Contains basic demographic info
* _addresses_flat.csv    - one address per line identifier as practice or mailing
* _identifiers_flat.csv  - one identifer per line
* _licenses_flat.csv 	 - one license per line
* _taxonomy_flat.csv     - one taxonomy code per line and identified as primary or not.


csv2mongo
---------

`csv2mongo` convert a CSV into a MongoDB collection.  The script expects the first row of
data to contain header information. Any whitespace and other funky characters in the
header row are auto-fixed by converting to ` `, `_`, or `-`.

Usage:

    csv2mongo [CSVFILE] [DATABASE] [COLLECTION] [DELETE_COLLECTION_BEFORE_IMPORT (T/F)]


Example:

    csv2mongo npidata_20050523-20140413.csv npi nppes T




json2mongo
----------

`json2mongo` imports a JSON object file into a MongoDB document. The file is checked
for validity (i.e. {}) before attempting to import it into MongoDB.


Usage:

    json2mongo [JSONFILE] [DATABASE] [COLLECTION] [DELETE_COLLECTION_BEFORE_IMPORT (T/F)]


Example:


    json2mongo test.json npi nppes T



jsondir2mongo
-------------


`jsondir2mongo` imports a directory containing files of JSON objects to MongoDB documents.
 The files are checked for validity (i.e. {}) before attempting to import it each into
 MongoDB. Files that are not JSON objects are automatically skipped.  A summary is retuned with the process ends

Usage:

    json2mongo [JSONFILE] [DATABASE] [COLLECTION] [DELETE_COLLECTION_BEFORE_IMPORT (T/F)]


Example:


    json2mongo data npi nppes T

Example output:


    Clearing the collection prior to import.

Start the import of the directory data into the collection test within the database csv2json .


    {
            "info": [
                "The collection was cleared prior to import."
            ],
            "num_files_attempted": 4,
            "num_files_imported": 2,
            "num_file_errors": 2,
            "errors": [
                "File data/3.json did not contain a json object, i.e. {}.",
                "File data/4.json did not contain valid JSON."
            ],
            "code": 400,
            "message": "Completed with errors."
        }


In the above example, the files `1.json` and `2.json` were processed while `3.json` and
`4.json` were not imported.

csv2pjson.py
------------

Convert the GAO CSV file format to a directory of files in ProviderJSON format.

Usage:

    csv2pjson.py [CSV_FILE] [OUTPUT_DIR]


Example:


    csv2pjson.py gao-csvfile.csv output

Output:


One file is created per line in the CSV file file inside the directory `output`.
Files are fanned out into a directory structure so as not to create millions of files
in one directory.




csv2pjson-public.py
------------------

Convert the NPPES Public Data Dissemination  CSV file format to a directory og files in ProviderJSON format.

Usage:

    csv2pjson.py [CSV_FILE] [OUTPUT_DIR]


Example:


    csv2pjson.py public-csvfile.csv output

Output:

  One file is created per line in the CSV file file inside  the directory`output`. Files are fanned out
  into a directory structure so as not to create millions of files in one directory.




validate-pjson
--------------

Validate the PJSON for complaince with a create/update request. It returns errors and warnings in JSON to stdout.

Usage:


    validate-pjson [ProivderJSON] [update|create]


Example:

    validate-pjson  1003819723.json update

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


loadnppes.py
------------

By streamlining several of the pdt utilities, the script loadnppes.py combines functionalty
for automatic setup. The script will download public data, parse to JProvider SON, and load
to MongoDB in one step. Note this script requires `unzip` and `wget` to be installed.

Usage:

    loadnppes.py [PROCESS_FULL Y/N] [DOWNLOAD_FROM_PUBLIC_FILE Y/N]"

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
