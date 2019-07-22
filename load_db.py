
from sqlalchemy import create_engine

import csv
import os
from sqlalchemy import create_engine


def get_db():
    db_name = "integration.db"
    if not os.path.isfile(db_name):
        db = create_engine('sqlite:///' + db_name)
        conn = db.connect()

        conn.execute(
            """ 
            CREATE TABLE companies (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                company_name TEXT NOT NULL , 
                zipcode VARCHAR(5)  NOT NULL,
                website VARCHAR(100) DEFAULT ''
                );
            """
        )

        with open("./q1_catalog.csv") as f:
            csvFile = csv.reader(f, delimiter=";")

            # Insert each row into database
            for row in csvFile:
                name, zipadress = row[0].upper(), row[1]
                if name != "NAME":
                    conn.execute(
                        """
                        INSERT INTO companies (company_name, zipcode) VALUES (?,?)        
                        """,
                        (name, zipadress),
                    )
    else:
        db = create_engine('sqlite:///' + db_name)
        conn = db.connect()

    return conn
