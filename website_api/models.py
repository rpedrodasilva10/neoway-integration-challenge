
import json

from website_api.extensions import db
# Shortcuts for readable code
Column = db.Column
String = db.String
Integer = db.Integer
UniqueConstraint = db.UniqueConstraint


class Company(db.Model):
    """Company model abstracts the type from  csvfiles"""

    __tablename__ = "companies"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(80), nullable=False)
    zipcode = Column(String(5), nullable=False)
    website = Column(String(80), nullable=True)

    # __table_args__ = (
    #    UniqueConstraint('company_name', 'zipcode',
    #                     name='unique_name_zipcode'),
    # )

    def add_company(_name, _zipcode, _website=None):
        """Adds a company into database"""
        company_obj = Company(
            company_name=_name, zipcode=_zipcode, website=_website)
        db.session.add(company_obj)
        db.session.commit()

        return company_obj

    def get_all_companies():
        """Retrieves all companys from database"""
        return Company.query.all()

    def get_company(name, zipcode=None):
        """Gets a specific company, searching part of the name and zipcode"""
        if name and zipcode:
            return Company.query.filter(Company.company_name.like('%' + name + '%'), Company.zipcode == zipcode).first()

    def update_company_website(_id, website):
        """Updates name, zipcode and website from a specific company"""
        if _id:
            company = Company.query.filter_by(id=_id).first()
            company.website = website
            db.session.commit()

    def load_db(csvfile):
        with open(csvfile) as f:
            csvFile = csv.reader(f, delimiter=";")

            # Insert each row into database
            for row in csvFile:
                name, zipadress = row[0].upper(), row[1]
                if name != "NAME":
                    self.add_company(name, zipadress, '')

    def __repr__(self):
        company_object = {
            'id': self.id,
            'company_name': self.company_name,
            'zipcode': self.zipcode,
            'website': self.website
        }
        return company_object
