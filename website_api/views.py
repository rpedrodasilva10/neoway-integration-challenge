import markdown
import csv
import json
import os

from .models import db, Company
from flask import request, current_app as app, jsonify
from flask_restplus import Api, Resource, namespace

api = Api(app)
ns = api.namespace('',
                   description='Website Integration')


@ns.route('/company')
class CompanyAPI(Resource):
    """Entity to retrieve and update data about companies"""

    @app.route("/readme", methods=['GET'])
    def index():
        """Index will show the documentation"""
        with open("./README.md", 'r') as markdown_file:
            # Read the content of the documentation file
            content = markdown_file.read()

        # Converting to HTML
        return markdown.markdown(content)

    @api.doc(
        responses={
            404: 'Resource not found',
            200: 'Success',
        },
        params={
            'company_name': 'Part of the company name text',
            'zipcode': 'Company five digit text zipcode'
        }
    )
    def get(self):
        """Retrieves a specific company, given a name and zipcode, or all resources"""
        companies = []
        part_name = request.args.get('company_name', None)
        zipcode = request.args.get('zipcode', None)

        if part_name is None or zipcode is None:
            for company in Company.get_all_companies():
                companies.append(company.__repr__())
            return {'message': 'All companies from the database', 'data': companies}
            # return {'message': 'company_name and zipcode are required arguments', 'data': []}, 422
        else:
            # Search by name and zipcode
            company_obj = Company.get_company(part_name, zipcode)

            if company_obj:
                companies.append(company_obj.__repr__())

        if len(companies) > 0:
            return {'message': 'Success', 'data': companies}, 200
        else:
            return {'message': 'Resource not found', 'data': []}, 404

    @api.doc(
        responses={
            400: 'Cannot process the given file',
            200: 'Success',
            404: 'There is no data to update in the database'
        },
        params={
            'csvpath': 'Csv filename to be processed',

        }
    )
    def put(self):
        """Sets the website column, based on a CSV file"""
        csvpath = ""

        if request.is_json:
            csv_json = request.get_json()
            csvpath = csv_json['csvpath']
        else:
            csvpath = request.args.get('csvpath', '')

        if os.path.isfile(csvpath):
            if Company.query.first():
                rv = self.set_website(csvpath)
                if len(rv) > 0:
                    return {'message': 'Success', 'updated': rv}, 200
                return {'message': 'Cannot process the given file', 'updated': rv}, 400
            else:
                return {'message': 'There is no data to update in the database', 'updated': []}, 404
        else:
            return {'message': 'No such file with the given name', 'data': csvpath}, 404

    def set_website(self, csv_path):
        """Updates website field from companies within the given csv"""
        updated = []

        if '.csv' not in csv_path:
            return updated

        with open(csv_path) as f:
            csvFile = csv.reader(f, delimiter=";")
            for row in csvFile:
                name, zipcode, website = row[0].upper(), row[1], row[2]
                if name != "NAME":
                    company_obj = Company.get_company(name, zipcode)
                    if company_obj:
                        # If found, updates the website
                        Company.update_company_website(company_obj.id, website)
                        updated.append(company_obj.__repr__())

        return updated


@ns.route('/company/data')
class MockData(Resource):
    """Treats mockdata from database"""

    def delete(self):
        """Clear database"""
        company_list = Company.get_all_companies()
        for obj in company_list:
            db.session.delete(obj)
            db.session.commit()

        if Company.query.first() is None:
            return {'message': 'Success, database cleared', 'data': []}, 200

    @api.doc(
        responses={
            201: 'Success, companies added',
        },
        params={
            'csvpath': 'Csv filename to be processed',
        }
    )
    def post(self):
        """Loads the mock data into database"""

        # Controls inserted data
        companies = []
        print(request.is_json)
        if request.is_json:
            company_json = request.get_json()
            csvpath = company_json['csvpath']
        else:
            csvpath = request.args.get('csvpath', '')

        if '.csv' not in csvpath.lower():
            return {'message': 'Cannot process the given file', 'file': csvpath}, 400

        with open(csvpath) as f:
            csv_rows = csv.reader(f, delimiter=';')
            for row in csv_rows:
                    # Upper name and five digit text zipcode
                name, zipaddress = row[0].upper(), row[1][: 5]
                if name != 'NAME':
                    company_obj = Company.add_company(name, zipaddress)
                    companies.append(
                        company_obj.__repr__()
                    )

            return {'message': 'Success, companies added', 'data': companies}, 201
