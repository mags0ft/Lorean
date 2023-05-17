from sqlitedict import SqliteDict

STD_SETUP = {
    "excludes": []
}

def create_database():
    db = SqliteDict("user_data.sqlite", autocommit = True)

    for key in STD_SETUP.keys():
        if not key in db.keys():
            db[key] = STD_SETUP[key]

    return db