from pymongo import MongoClient

def connect_db(verbose=False):
    '''Connect to Database. 
    Args: 
        connection_string: str
    Return:
        db: Pymongo session to the db
    '''
    try:
        #uri ='mongodb://db:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
        uri = 'mongodb://admin:admin@db:27017/admin?authSource=admin&authMechanism=SCRAM-SHA-1'
        clt = MongoClient(uri)
        db = clt["db"]
        return db
    except Exception as err:
        print(err)