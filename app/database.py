"""
This module handles the creation and management of the database.
"""

from sqlitedict import SqliteDict


STD_SETUP = {
    "excludes": [],
    "locations": []
}


def create_database():
    """
    Creates the boilerplate database schema.
    """
    
    db = SqliteDict("user_data.sqlite", autocommit = True)

    for key in STD_SETUP.keys():
        if key in db.keys():
            continue

        db[key] = STD_SETUP[key]

    return db
