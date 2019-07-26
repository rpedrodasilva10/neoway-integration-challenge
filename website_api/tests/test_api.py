import os
import unittest

from flask import request, current_app
from . import Company, db
from . import app


class TestCompanyAPI(unittest.TestCase):
    """Class to test the endpoint /company"""

    def setUp(self):
        #self.app = app.test_client()
        self.app = app
        self.client = self.app.test_client()

        # Loads database and set app context to test
        ctx = self.app.app_context()
        ctx.push()
        db.create_all(app=self.app)

        self.client.post('/company/data', json=dict(csvpath='test_data.csv'))

    def tearDown(self):
        db.drop_all(app=self.app)

    def test_post_company_data(self):
        csv_path = 'q1_catalog.csv'

        response = self.client.post(
            '/company/data', json=dict(csvpath=csv_path))

        self.assertEqual(response.status_code, 201)

    def test_get_company_OK(self):
        """Test get company passing zipcode and company_name"""

        company_name = "Not in the database"
        zipcode = "12345"
        Company.add_company(company_name, zipcode)

        response = self.client.get(
            '/company?company_name=' + company_name + "&zipcode=" + zipcode)
        self.assertEqual(response.status_code, 200)

    def test_get_company_zipcode(self):
        """Test get company passing zipcode as None"""
        company_name = "tola"
        zipcode = None
        response = self.client.get(
            '/company?company_name=' + company_name)
        self.assertEqual(response.status_code, 200)

    def test_get_company_company_name(self):
        """Test get company passing company_name as None"""
        company_name = None
        zipcode = "78229"
        response = self.client.get('/company?zipcode=' + zipcode)
        self.assertEqual(response.status_code, 200)

    def test_get_company_not_found(self):
        """Test get company passing company_name as None"""
        company_name = "Not in the dabase"
        zipcode = "99999"
        response = self.client.get(
            '/company?company_name=' + company_name + "&zipcode=" + zipcode)
        self.assertEqual(response.status_code, 404)

    def test_put_company_OK(self):
        """Test PUT company passing a valid csv file"""
        csvPath = 'q2_clientData.csv'
        response = self.client.put('/company', json=dict(csvpath=csvPath))

        self.assertEqual(response.status_code, 200)

    def test_put_company_bad_csvfile(self):
        """Test POST company passing invalid csv file"""
        #self.client.post('/company/data', json=dict(csvpath="q1_catalog.csv"))
        csvPath = 'xd'

        response = self.client.put('/company', json=dict(csvpath=csvPath))

        self.assertEqual(response.status_code, 400)
