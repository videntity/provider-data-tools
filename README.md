Disecting Provider Data
=======================


I am currently working as an HHS External Entrpreneur focusing on modernizing the National Plan and Provider Eumeration System (NPPES).   NPPES is a database of all health providers in the United States where each provider is enumerated and issued a National Provider Identifier (NPI).  This public data source is consumed by many systems and organizations such as insurance comapnies. Making this data more acceisible is a goal of the NPPEs Modernization Project.


Through the process of conducting stakeholder interviews, several people pointed out that the current provider download file is difficult to use.  One of the chief complaints I heard was the fact that taxonomy and license information was difficult to extract. People have asked for things like taxonomy codes, license information, and other identifiers to be put into their own CSV files ao that there is one item per line instead of all provider information on one line.


The hope is that through the NPPES Modernizatiopn Project,a public API will exist to make iteasy to query for this information. In the meantime however, I have developed a simple script that will create several "flattened" CSV files from the origional "wide file".  I have shared this with several folks already and I thought it was time to make this utility more widely abaiable.  The only requirement to run the script is for you to have the public "NPPES Data Dissemination" and Python installed on your computer.  If you ae usung Mac or Linux Python is already installed).

To use the tool, you first need to obtain the "NPPES Data Dissemination". You can get that fgoing to http://npi.io and clicking on "Public NPI Download".

After downloading and decompressing the archive, navigate to that folder. In our example, we will assume the large CSV is `/home/alan/nppes-data/foo.csv`.

Copy the script (below) and place it in the same folder as `foo.csv`.
Now simply run the script by passing in `foo.csv` as the one and only argument.

    python chop-public.py foo.csv

The script make take a few moments to complete, but when it does you will now have more files in the current directory.

    _addresses.csv
    _basic.csv
    _addresses_flat.csv
    _identifiers_flat.csv
    _licenses_flat.csv
    _taxonomy_flat.csv

So now each of these result