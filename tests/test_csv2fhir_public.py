import unittest, os, random
from pdt import csv2fhir_public as fhir
from pdt import json_schema_check


class TestCSV2FHIR_PUBLIC(unittest.TestCase):

    def test_run_CSV2FHIR_PUBLIC(self):

        """Run CSV2FHIR should return results """
        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        output_dir = "fhir_test_output"
        number_processed = 50000

        result = fhir.publiccsv2fhir(csvfile, output_dir)
        self.assertEqual(result['num_files_created'], number_processed)
        self.assertEqual(result['message'], "Completed without errors.")

    def test_FHIR_results(self):

        """Put newly created files through json_schema to check"""
        output_dir = os.path.join( os.path.dirname( __file__),  "fhir_test_output")
        json_schema = os.path.join( os.path.dirname( __file__),  "fhir_practitioner_schema.json")

        for x in range(1000,2000):
            if os.path.exists("output_dir/Practioner/x"):
                random_file = random.choice(os.listdir("output_dir/x"))
                result = json_schema_check.json_schema_check(json_schema, random_file)
                print(result)
                self.assertEqual(result['errors'], [])

if __name__ == '__main__':
    unittest.main()
