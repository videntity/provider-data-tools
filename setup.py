import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name="pdt",
      version="0.7.7",
      description="Provider Data Tools",
      long_description="""A collection of scripts and APIs for working with"""
                       """health care provider data and beyond. Many tools"""
                       """are generic utilities.""",
      author="Alan Viars",
      author_email="sales@videntity.com",
      url="https://github.com/hhsidealab/provider-data-tools",
      download_url="https://github.com/hhsidealab/provider-data-tools/"
                   "tarball/master",
      install_requires=['validate_email', 'beautifulsoup4', 'luhn', 'jdt',
                        'jsonschema'],
      packages=['pdt', 'pdt.pjson', 'tests', 'pdt.fhir_json_schema'],
      package_data={'': ['taxonomy-license-crosswalk.csv', 'fiftythousand.csv',
                         'first10.csv', 'Practitioner.json',
                         'Organization.json', 'nucc_taxonomy_160.csv']},
      scripts=['pdt/chop_nppes_public.py',
               'pdt/csv2mlvs.py',
               'pdt/build-cdn.sh',
               'pdt/create_provider_indexes.py',
               'pdt/csv2pjson_public.py',
               'pdt/csv2fhir_public.py',
               'pdt/loadnppes.py',
               'pdt/vnpi.py',
               'pdt/pjson/validate_pjson',
               'pdt/pjson/validate_pjson_affiliations',
               'pdt/pjson/validate_pjson_dir',
               'pdt/json_schema_check.py',
               'pdt/json_schema_check_fhir.py',
               'pdt/pull_pecos.py',
               'pdt/combine_nppes_pecos_fhir.py',
               'pdt/create_pecos_addresses_indexes.py',
               'pdt/create_pecos_base_indexes.py',
               'pdt/create_pecos_compiled_individuals_indexes.py',
               'pdt/create_pecos_compiled_organizations_indexes.py',
               'pdt/create_pecos_reassignments_indexes.py',
               'pdt/create_pract_nppes_fhir_indexes.py',
               'pdt/create_pract_nppes_pecos_fhir_indexes.py',
               'pdt/makepecosdocs.py',
               'pdt/pull_new_files_ready.py'
               ]
      )
