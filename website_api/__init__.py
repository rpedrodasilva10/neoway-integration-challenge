import os
import markdown
import csv
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from load_db import get_db
app = Flask(__name__)
api = Api(app)


class Company(Resource):
    """Entity to retrieve and update data about companies"""
    @app.route("/")
    def index():
        """Index will show the documentation"""
        with open("./README.md", 'r') as markdown_file:
            # Read the content of the documentation file
            content = markdown_file.read()

        # Converting to HTML
        return markdown.markdown(content)

    def get(self):
        """Retrieves a specific resource"""
        conn = get_db()
        companies = []
        part_name = request.args.get('company_name', None)
        zipcode = request.args.get('zipcode', None)

        if part_name is None or zipcode is None:
            return {'message': 'company_name and zipcode are required args', 'data': []}, 422
        else:
            for row in conn.execute("SELECT * FROM companies WHERE company_name like ? AND zipcode like ?", ('%'+part_name+'%', zipcode)):
                companies.append(
                    {
                        'id': row[0],
                        'company_name': row[1],
                        'zipcode': row[2],
                        'website': row[3]
                    }
                )
        if len(companies) > 0:
            return {'message': 'Success', 'data': companies}, 200
        else:
            return {'message': 'Resource not found', 'data': []}, 404

    def post(self):
        """Sets the website column, based on a CSV file"""
        csvpath = request.args.get('csvpath', '')
        rv = self.set_website(csvpath)
        if len(rv) > 0:
            return {'message': 'Success', 'data': rv}, 200
        return {'message': 'Fail', 'data': rv}, 400

    def set_website(self, csv_path):
        """Updates website field from companies within the given csv"""
        conn = get_db()
        updated = []
        with open(csv_path) as f:
            csvFile = csv.reader(f, delimiter=";")
            for row in csvFile:
                name, website = row[0].upper(), row[2]
                if name != "NAME":
                    cursor = conn.execute(
                        "SELECT company_name FROM companies WHERE company_name = ?", (name))

                    if cursor.fetchone() is not None:
                        conn.execute(
                            "UPDATE companies SET website = ? WHERE company_name = ?", (website, name,))

                        # Controls updated keys
                        updated.append(
                            {'company_name': name, 'website': website}
                        )

        return updated


api.add_resource(Company, '/company')
