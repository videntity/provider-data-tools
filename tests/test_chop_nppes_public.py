import unittest, os, csv
from pdt import chop_nppes_public


# This test suite is meant to be run from the **project root**

class TestChopNppesPublic(unittest.TestCase):

    def test_taxonomy_creation(self):

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        chop_nppes_public.chop_taxonomy(csvfile)

        self.assertTrue(os.stat('tests/fiftythousand_taxonomy.csv'))

        csvfile_taxonomy = os.path.join( os.path.dirname( __file__),  "fiftythousand_taxonomy.csv")
        chop_nppes_public.flatten_taxonomy(csvfile_taxonomy)

        self.assertTrue(os.stat('tests/fiftythousand_taxonomy_flat.csv'))

    def test_identifiers_creation(self):

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        chop_nppes_public.chop_identifiers(csvfile)

        self.assertTrue(os.stat('tests/fiftythousand_identifiers.csv'))

        csvfile_identifiers = os.path.join( os.path.dirname( __file__),  "fiftythousand_identifiers.csv")
        chop_nppes_public.flatten_identifiers(csvfile_identifiers)

        self.assertTrue(os.stat('tests/fiftythousand_identifiers_flat.csv'))

    def test_chop_licenses_creation(self):

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        chop_nppes_public.chop_licenses(csvfile)

        self.assertTrue(os.stat('tests/fiftythousand_licenses.csv'))


        csvfile_licenses = os.path.join( os.path.dirname( __file__),  "fiftythousand_licenses.csv")
        chop_nppes_public.flatten_licenses(csvfile_licenses)

        self.assertTrue(os.stat('tests/fiftythousand_licenses_flat.csv'))


    def test_chop_addresses_creation(self):

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        chop_nppes_public.chop_addresses(csvfile)

        self.assertTrue(os.stat('tests/fiftythousand_addresses.csv'))

        csvfile_addresses = os.path.join( os.path.dirname( __file__),  "fiftythousand_addresses.csv")
        chop_nppes_public.flatten_addresses(csvfile_addresses)

        self.assertTrue(os.stat('tests/fiftythousand_addresses_flat.csv'))

    def test_chop_basic_creation(self):

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        chop_nppes_public.chop_basic(csvfile)

        self.assertTrue(os.stat('tests/fiftythousand_basic.csv'))


    def test_chop_other_names_creation(self):

        """Run ensure_provider_indexes should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        chop_nppes_public.chop_other_names(csvfile)

        self.assertTrue(os.stat('tests/fiftythousand_other_names.csv'))



if __name__ == '__main__':
    unittest.main()
