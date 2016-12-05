import unittest
import os
import random
import pdt.json_schema_check
from pdt import csv2fhir_public


class TestCSV2FHIR_PUBLIC(unittest.TestCase):

    def test_run_CSV2FHIR_PUBLIC(self):
        """Run CSV2FHIR should return results """
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        csvfile = os.path.join(CURRENT_DIR, "fiftythousand.csv")
        output_dir = "fhir_test_output"
        with open(csvfile):

            result = csv2fhir_public.publiccsv2fhir(csvfile, output_dir)
            self.assertTrue(os.path.exists("fhir_test_output"))

    def test_FHIR_results(self):
        """Put newly created files through json_schema to check"""
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

        for x in range(1000, 2000):
            if os.path.exists(os.path.join("fhir_test_output", "Practitioner",
                                           str(x))):
                for files in os.listdir(os.path.join("fhir_test_output",
                                                     "Practitioner", str(x))):
                    result = pdt.json_schema_check.json_schema_check(
                        os.path.join(CURRENT_DIR, "..", "pdt",
                                     "fhir_json_schema", "Practitioner.json"),
                        os.path.join("fhir_test_output", "Practitioner",
                                     str(x), files))
                    self.assertEqual(result['errors'], [])
                # To test to make sure works when running from different
                # directories, using nosetest.
                # If not using a test runner, make sure to run tests from the
                # project root.
                # if x > 1200:
                #     self.fail()
                    # print(x)
            if os.path.exists(os.path.join("fhir_test_output", "Organization",
                                           str(x))):
                for files in os.listdir(os.path.join("fhir_test_output",
                                                     "Organization", str(x))):
                    result = pdt.json_schema_check.json_schema_check(
                        os.path.join(CURRENT_DIR, "..", "pdt",
                                     "fhir_json_schema", "Organization.json"),
                        os.path.join("fhir_test_output", "Organization",
                                     str(x), files))
                    self.assertEqual(result['errors'], [])
                # if x > 1200:
                #     self.fail()

if __name__ == '__main__':
    unittest.main()
