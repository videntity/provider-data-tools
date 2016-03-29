import unittest, os
from pdt import csv2mlvs


class TestCSV2MLVS(unittest.TestCase):

    def test_run_CSV2MLVS(self):

        """Run CSV2mlvs should return results """
        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        mlvs_csv = os.path.join( os.path.dirname( __file__),  "mlvs.csv")
        output_dir = "mlvs_test_output"
        number_processed = 3

        result = csv2mlvs(mlvs_csv, output_dir)
        self.assertEqual(result['num_files_created'], number_processed)

if __name__ == '__main__':
    unittest.main()
