import os, unittest, csv
from pdt.pjson import validate_pjson


class TestValidateJSON(unittest.TestCase):

    def test_run_validate_json(self):

        """Run validate_json should return errors, if any """
        sample_json = os.path.join( os.path.dirname( __file__),  "sample.json")



        errors = validate_addresses
        self.assertEqual(errors, 0)

if __name__ == '__main__':
    unittest.main()
