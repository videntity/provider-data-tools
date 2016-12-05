#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

from bs4 import BeautifulSoup
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import re
import glob
import sys
from subprocess import call
from datetime import datetime


def do_update(process_full=True, download=True):
    try:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug",
                  "Sept", "Oct", "Nov", "Dec"]
        # Get just the html page
        html_page = urlopen("http://download.cms.gov/nppes/NPI_Files.html")
        link_prefix = "http://download.cms.gov/nppes/"

        soup = BeautifulSoup(html_page, "html.parser")
        month = ""
        year = datetime.now().year
        # get all links
        zipfilelinks = []
        for link in soup.findAll('a'):
            print(link)
            # get just zips
            if link.get('href', "").endswith(".zip"):
                zipfilelinks.append(link.get('href', ""))

        print(zipfilelinks)
        # determine full v/s weekly
        weeklylinks = []
        full_link = ""
        for link in zipfilelinks:

            for m in months:
                if link.__contains__(m):
                    full_link = link_prefix + link
                    month = m
            if link.__contains__("Report"):
                deactivation_link = link
            else:
                weeklylinks.append(link)

        # Download full file
        if process_full:

            if download:
                print("Downloading", full_link)
                call(["wget", full_link])

            # Get filename and unzip
            filename = full_link.split("/")
            zipfilename = filename[-1]
            print("Unzip", zipfilename)

            call(["unzip", zipfilename])

            # inspect the local directory for the CSV
            csv_files = glob.glob("*.csv")

            for f in csv_files:
                if f.__contains__("Header"):
                    header_file = f
                else:
                    main_file_to_import = f

            # Now import the file
            print("Import", main_file_to_import)
            # first convert to json, and fhir-json respectively
            json_output_dir = "json-output/"
            fhir_output_dir = "fhir-nppes-output/"
            call(["csv2pjson-public.py", main_file_to_import, json_output_dir])
            call(["csv2fhir_public.py", main_file_to_import, fhir_output_dir])
            # Pull PECOS Data/files
            call(["pull_pecos.py", "y", "n", "n", "n"])
    except:
        print(sys.exc_info)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage:")
        print("pull_new_files_ready.py [PROCESS_FULL Y/N] "
              "[DOWNLOAD_FROM_PUBLIC_FILE Y/N]")
        print("Example:")
        print("loadnppes.py Y Y")
        sys.exit(1)

    if sys.argv[1] in ("Y", "y", "T", True):
        process_full = True
    else:
        process_full = False

    if sys.argv[2] in ("Y", "y", "T", True):
        download = True
    else:
        download = False

    # Get the file from the command line
    do_update(process_full, download)
