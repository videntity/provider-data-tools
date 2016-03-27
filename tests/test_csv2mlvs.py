import unittest, os, imp


class Testcsv2mlvs(unittest.TestCase):

    def testRunCSV2MLVS(self):

        """Run CSV2mlvs should return results """
        csv2mlvs = imp.load_source('csv2mlvs', '../pdt/csv2mlvs')
        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        output_dir = "test_output"
        number_processed = 50000

        result = csv2mlvs.csv2mlvs(csvfile, output_dir)
        self.assertEqual(response_dict['num_files_created'], number_processed)

if __name__ == '__main__':
    unittest.main()
