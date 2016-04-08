import unittest, os, csv
from pdt import chop_nppes_public




class TestChopNppesPublic(unittest.TestCase):

    def test_chop_taxonomy(self):

        """Run ensure_provider_indexes should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        number_processed = 50001
        chop_nppes_public.chop_taxonomy(csvfile)

        csvfile_taxonomy = os.path.join( os.path.dirname( __file__),  "fiftythousand_taxonomy.csv")

        with open(csvfile_taxonomy,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_flatten_taxonomy(self):

        csvfile_taxonomy = os.path.join( os.path.dirname( __file__),  "fiftythousand_taxonomy.csv")
        number_processed = 65001
        chop_nppes_public.flatten_taxonomy(csvfile_taxonomy)

        csvfile_taxonomy_flat = os.path.join( os.path.dirname( __file__),  "fiftythousand_taxonomy_flat.csv")

        with open(csvfile_taxonomy_flat,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_chop_identifiers(self):

        """Run ensure_provider_indexes should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        number_processed = 50001
        chop_nppes_public.chop_identifiers(csvfile)

        csvfile_identifiers = os.path.join( os.path.dirname( __file__),  "fiftythousand_identifiers.csv")

        with open(csvfile_identifiers,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_flatten_identifiers(self):

        csvfile_identifiers = os.path.join( os.path.dirname( __file__),  "fiftythousand_identifiers.csv")
        number_processed = 50001
        chop_nppes_public.flatten_identifiers(csvfile_identifiers)

        csvfile_identifiers_flat = os.path.join( os.path.dirname( __file__),  "fiftythousand_identifiers_flat.csv")

        with open(csvfile_identifiers_flat,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_chop_licenses(self):

        """Run ensure_provider_indexes should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        number_processed = 50001
        chop_nppes_public.chop_licenses(csvfile)

        csvfile_licenses = os.path.join( os.path.dirname( __file__),  "fiftythousand_licenses.csv")

        with open(csvfile_licenses,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_flatten_licenses(self):

        csvfile_licenses = os.path.join( os.path.dirname( __file__),  "fiftythousand_licenses.csv")
        number_processed = 50001
        chop_nppes_public.flatten_licenses(csvfile_licenses)

        csvfile_licenses_flat = os.path.join( os.path.dirname( __file__),  "fiftythousand_licenses_flat.csv")

        with open(csvfile_licenses_flat,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)


    def test_chop_addresses(self):

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        number_processed = 50001
        chop_nppes_public.chop_addresses(csvfile)

        csvfile_addresses = os.path.join( os.path.dirname( __file__),  "fiftythousand_addresses.csv")

        with open(csvfile_addresses,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_flatten_addresses(self):

        """Run ensure_provider_indexes should return results """

        csvfile_addresses = os.path.join( os.path.dirname( __file__),  "fiftythousand_addresses.csv")
        number_processed = 50001
        chop_nppes_public.flatten_addresses(csvfile_addresses)

        csvfile_addresses_flat = os.path.join( os.path.dirname( __file__),  "fiftythousand_addresses_flat.csv")

        with open(csvfile_addresses_flat,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_chop_basic(self):

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        number_processed = 50001
        chop_nppes_public.chop_basic(csvfile)

        csvfile_basic = os.path.join( os.path.dirname( __file__),  "fiftythousand_basic.csv")

        with open(csvfile_basic,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)

    def test_chop_other_names(self):

        """Run ensure_provider_indexes should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        number_processed = 50001
        chop_nppes_public.chop_other_names(csvfile)

        csvfile_other_names = os.path.join( os.path.dirname( __file__),  "fiftythousand_other_names.csv")

        with open(csvfile_other_names,"r") as f:
            reader = csv.reader(f,delimiter = ",")
            data = list(reader)
            row_count = len(data)
            self.assertEqual(row_count, number_processed)





if __name__ == '__main__':
    unittest.main()
