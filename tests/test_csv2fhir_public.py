import unittest, os, random
import pdt.json_schema_check
from pdt import csv2fhir_public

class TestCSV2FHIR_PUBLIC(unittest.TestCase):


    def test_run_CSV2FHIR_PUBLIC(self):

        """Run CSV2FHIR should return results """
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        csvfile = os.path.join( CURRENT_DIR,  "fiftythousand.csv")
        output_dir = "fhir_test_output"
        with open(csvfile):

            result = csv2fhir_public.publiccsv2fhir(csvfile, output_dir)
            self.assertTrue(os.path.exists("fhir_test_output"))

    def test_FHIR_results(self):

        """Put newly created files through json_schema to check"""
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join( CURRENT_DIR,  "fhir_test_output")
        json_schema = os.path.join( CURRENT_DIR,  "fhir_practitioner_schema.json")



        for x in range(1000,2000):
            if os.path.exists(os.path.join("fhir_test_output", "Practitioner", str(x))):
                for files in os.listdir(os.path.join("fhir_test_output","Practitioner",str(x))):
                    result = pdt.json_schema_check.json_schema_check(os.path.join( CURRENT_DIR, "fhir_practitioner_schema.json"), os.path.join("fhir_test_output", "Practitioner", str(x), files))
                    self.assertEqual(result['errors'], [])
                # To test to make sure works when running from different directories, using nosetest.
                # If not using a test runner, make sure to run tests from the project root.
                # if x > 1500:
                #     self.assertFail()
            # else:
            #     print(x)
            if os.path.exists(os.path.join("fhir_test_output", "Organization", str(x))):
                for files in os.listdir(os.path.join("fhir_test_output","Organization",str(x))):
                    result = pdt.json_schema_check.json_schema_check(os.path.join( CURRENT_DIR, "fhir_organization_schema.json"), os.path.join("fhir_test_output", "Organization", str(x), files))
                    self.assertEqual(result['errors'], [])


if __name__ == '__main__':
    unittest.main()
