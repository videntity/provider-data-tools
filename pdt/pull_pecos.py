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
import sys
from subprocess import call


def pull_pecos(download_all=True, Base=False,
               Reassignment=False, Address=False):
    try:

        html_page = urlopen("https://data.cms.gov/public-provider-enrollment")
        file_names = ['Base-Provider-Enrollment-File', 'Reassignment-Sub-File',
                      'Address-Sub-File']

        # Identify file links and parse into a list of strings
        soup = BeautifulSoup(html_page, "html.parser")
        file_links = []
        for file_name in file_names:
            for link in soup.findAll('a'):
                if file_name in link.get('href', ""):
                    file_links.append(list(link.get('href', "").split('/')))

        csv_prefix = 'https://data.cms.gov/api/views/'
        # Possible feature to add is allowing people to name the output file.
        # Currently it supplants the downloaded file supplants a file that is
        # already named the default value.

        # Download files according to user input
        if download_all:
            print("Downloading Base, Address and Reassignment CSV files")
            for csv_link in file_links:
                call(["wget", "--output-document=" + csv_link[-2] + ".csv",
                      csv_prefix + csv_link[-1] + '/rows.csv?accessType=DOWNLOAD'])

        if Base:
            print("Downloading Base CSV file")
            call(["wget", "--output-document=pecos_base.csv", csv_prefix +
                  file_links[0][-1] + '/rows.csv?accessType=DOWNLOAD'])

        if Reassignment:
            print("Downloading Reassignment CSV file")
            call(["wget", "--output-document=pecos_reassignment.csv",
                  csv_prefix + file_links[1][-1] + "/rows.csv?accessType=DOWNLOAD"])

        if Address:
            print("Downloading Address CSV file")
            call(["wget", "--output-document=pecos_address.csv", csv_prefix +
                  file_links[2][-1] + "/rows.csv?accessType=DOWNLOAD"])

    except:
        print(sys.exc_info)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage:")
        print("pull_pecos.py [DOWNLOAD ALL Y/N] "
              "[DOWNLOAD BASE Y/N] [DOWNLOAD REASSIGNMENT Y/N] "
              " [DOWNLOAD ADDRESS Y/N]")
        print("Example:")
        print("pull_pecos.py Y N N N")
        sys.exit(1)

    if sys.argv[1] in ("Y", "y", "T", True):
        download_all = True
    else:
        download_all = False

    if sys.argv[2] in ("Y", "y", "T", True):
        Base = True
    else:
        Base = False

    if sys.argv[3] in ("Y", "y", "T", True):
        Reassignment = True
    else:
        Reassignment = False

    if sys.argv[4] in ("Y", "y", "T", True):
        Address = True
    else:
        Address = False

    # Get the file from the command line
    pull_pecos(download_all, Base, Reassignment, Address)
