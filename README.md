Provider Data Tools - Dissecting Public Provider Data
=====================================================

By Alan Viars

This simple utility creates several "flattened" CSV files from the origional NPPES public data dissemination file.  The only requirements to use the tool are

1. obtain the public "NPPES Data Dissemination" CSV file
2. Have Python installed on your computer.  If you ae usung Mac or Linux, Python is already installed).

You can install the tool using `pip` or download it from GitHub (https://github.com/hhsidealab/provider-data-tools)


To install with pip just type:

    ~$ sudo pip install pdt

The utility `chop-nppes-public` will be installed at the system level, if you use `sudo`.

To obtain the "NPPES Data Dissemination", go to  http://nppes.viva-it.com/NPI_Files.html. You can get that by going to http://npi.io and clicking on "Public NPI Download". As of this writing, the most recent version is dated April 13, 2014 and the CSV filename is `npidata_20050523-20140413.csv`.

To run the utility simply call it on a command line and proivde one command line argument, the master file:

    ~$ chop-nppes-public npidata_20050523-20140413.csv

The script make take a few minutes to complete. When it completes you will have more files in your current directory. Everything is still indexed by NPI. These files are described below.

	_basic.csv     - Contains basic demographic info
    _addresses_flat.csv    - one address per line identifier as practice or mailing
    _identifiers_flat.csv    -one identifer per line
    _licenses_flat.csv 		- one license per line
    _taxonomy_flat.csv      - one taxonomy code per line and identified as primary or not.

I hope this utility saves you time in processing NPPES Public Data Dissemination. -Alan