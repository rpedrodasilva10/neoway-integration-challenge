
from sqlalchemy import create_engine

import csv
import os
from sqlalchemy import create_engine


db_name = "integration.db"
# No need to use pandas?
if not os.path.isfile(db_name):
    db = create_engine('sqlite:///' + db_name)
    conn = db.connect()

    conn.execute(
        """ 
        CREATE TABLE companies (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            company_name TEXT NOT NULL , 
            zipcode INTEGER(5) NOT NULL,
            website TEXT
            );
         """
    )

    with open("./q1_catalog.csv") as f:
        csvFile = csv.reader(f, delimiter=";")

        # Insert each row into database
        for row in csvFile:
            name, zipadress = row[0].upper(), row[1]

            conn.execute(
                """
                INSERT INTO companies (company_name, zipcode) VALUES (?,?)        
                """,
                (name, zipadress),
            )
else:
    db = create_engine('sqlite:///' + db_name)
    conn = db.connect()

#    for row in conn.execute("SELECT * FROM companies"):
#        print(row)
