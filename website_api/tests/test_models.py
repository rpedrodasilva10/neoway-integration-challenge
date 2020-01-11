import os
import unittest

from flask import request, current_app
from . import Company, db
from . import app


class TestCompanyModel(unittest.TestCase):
    """Class to test the endpoint /company"""

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        # Loads database and set app context to test
        ctx = self.app.app_context()
        ctx.push()
        db.create_all(app=self.app)

        self.client.post('/company/data', json=dict(csvpath='test_data.csv'))

    def tearDown(self):
        db.drop_all(app=self.app)

    def test_add_company(self):
        company_name = 'company'
        zipcode = 'zipcode'
        result = Company.add_company(company_name, zipcode)
        self.assertEqual(company_name, result.company_name)

    def test_get_all_companies(self):
        count = 0
        Company.add_company('company_one', '12345')
        Company.add_company('company_two', '12345')
        for company in Company.get_all_companies():
            count += 1

        self.assertEqual(count > 1, True)

    def test_get_a_company(self):
        part_name = 'mock this data'
        zipcode = '12345'
        result = Company.add_company(part_name, zipcode)

        self.assertEqual(Company.get_company(
            part_name[:5], zipcode).id, result.id)

    def test_update_company_website(self):
        website = "https://www.neoway.com.br"
        part_name = 'test website update'
        zipcode = '56785'
        result = Company.add_company(part_name, zipcode)

        Company.update_company_website(result.id, website)

        obj = Company.get_company('website', zipcode)
        self.assertEqual(obj.website, website)
    
    def test_four_digit_zipcode(self):
        part_name = 'testing'
        zipcode= '1234'
        result = Company.add_company(part_name, zipcode)

        obj = Company.get_company(part_name, zipcode)
        self.assertEqual(None, result)
