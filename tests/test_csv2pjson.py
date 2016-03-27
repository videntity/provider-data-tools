import unittest, os
from pdt.csv2pjson_public import publiccsv2pjson
from pdt.csv2pjson import gao_csv2pjson



class Testcsv2pjson(unittest.TestCase):

    def testRunCSV2PJSON_PUBLIC(self):

        """Run CSV2pjson_public should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        output_dir = "test_output"
        number_processed = 50000

        result = publiccsv2pjson(csvfile, output_dir)
        self.assertEqual(result['num_files_created'], number_processed)

    def testRunCSV2PJSON(self):

        """Run CSV2pjson should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        output_dir = "test_output"
        number_processed = 50000

        result = gao_csv2pjson(csvfile, output_dir)
        self.assertEqual(result['num_files_created'], number_processed)




if __name__ == '__main__':
    unittest.main()
