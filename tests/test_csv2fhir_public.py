import unittest, os
from pdt import csv2fhir_public as fhir


class TestCSV2FHIR_PUBLIC(unittest.TestCase):

    def test_run_CSV2FHIR_PUBLIC(self):

        """Run CSV2FHIR should return results """
        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        output_dir = "fhir_test_output"
        number_processed = 50000

        result = fhir.publiccsv2fhir(csvfile, output_dir)
        self.assertEqual(result['num_files_created'], number_processed)

if __name__ == '__main__':
    unittest.main()
