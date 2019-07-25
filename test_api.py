import os
import unittest

from flask import request, current_app as app


TEST_DB = 'test.db'
# db = get_db('tmpdb')


class TestCompany(unittest.TestCase):
    """Class to test the endpoint /company"""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_get_company_OK(self):
        """Test get company passing zipcode and company_name"""
        company_name = "PIZZA"
        zipcode = "44667"
        response = self.app.get(
            '/company?company_name=' + company_name + "&zipcode=" + zipcode)
        self.assertEqual(response.status_code, 200)

    def test_get_company_zipcode(self):
        """Test get company passing zipcode as None"""
        company_name = "PIZZA"
        zipcode = None
        response = self.app.get(
            '/company?company_name=' + company_name)
        self.assertEqual(response.status_code, 422)

    def test_get_company_company_name(self):
        """Test get company passing company_name as None"""
        company_name = None
        zipcode = "44667"
        response = self.app.get('/company?zipcode=' + zipcode)
        self.assertEqual(response.status_code, 422)

    def test_get_company_not_found(self):
        """Test get company passing company_name as None"""
        company_name = "Not in the dabase"
        zipcode = "99999"
        response = self.app.get(
            '/company?company_name=' + company_name + "&zipcode=" + zipcode)
        self.assertEqual(response.status_code, 404)

    def test_post_company_OK(self):
        """Test POST company passing a valid csv file"""
        csvPath = 'q2_clientData.csv'
        response = self.app.post('/company', json=dict(csvpath=csvPath))

        self.assertEqual(response.status_code, 200)

    def test_post_company_bad_csvfile(self):
        """Test POST company passing a valid csv file"""
        csvPath = 'q2_clientData'
        response = self.app.post('/company', json=dict(csvpath=csvPath))

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
