from utils.mongo import MongoUtils
from constants import Constants


def test_connection_and_insert_one():
    c: Constants = Constants()
    mu: MongoUtils = MongoUtils(
        username=c.secrets['mongo']['username'],
        password=c.secrets['mongo']['password'],
        cluster=c.secrets['mongo']['cluster'],
        database=c.secrets['mongo']['database'],
    )
    mu.db['test'].insert_one({'test': 'test'})
