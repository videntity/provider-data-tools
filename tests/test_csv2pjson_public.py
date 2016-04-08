import unittest, os
from pdt import csv2pjson_public




class TestCSV2PJSONPublic(unittest.TestCase):

    # Be more specific about the dictionary that is created

    def test_pjson_deactivation(self):
        csv2pjson_public.new_pjson_deactive_stub

    def test_pjson_creation(self):
        csv2pjson_public.new_pjson_stub

    def test_publiccsv2pjson(self):

        """Run CSV2pjson_public should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        output_dir = "test_output"
        number_processed = 50000

        result = csv2pjson_public.publiccsv2pjson(csvfile, output_dir)
        self.assertEqual(result['num_files_created'], number_processed)


if __name__ == '__main__':
    unittest.main()
