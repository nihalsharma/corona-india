import datetime

from pymongo import MongoClient

from settings.settings import MONGODB_HOST


class _DBConnSingleton(object):
    class __DBConnection:
        connection = None

        def __init__(self):
            self.client = MongoClient(MONGODB_HOST, 27017, connect=False)
            self.db = self.client['corona_india']

        def get_client(self):
            return self.client, self.db

        def save_subscriber(self, email, country, frequency):
            print(locals())
            collection = self.db['subscribers']
            collection.find_one_and_update({'email': email}, {
                '$set': {'subscribed_on': str(datetime.datetime.now().date()), 'subscribed': True, 'country': country,
                         'frequency': frequency}}, upsert=True)

        def unsubscribe(self, email):
            collection = self.db['subscribers']
            collection.find_one_and_update({'email': email}, {'$set': {'subscribed': False}}, upsert=False)

        def fetch_news(self, name):
            collection = self.db['news']
            cursor = collection.find({'country': name}).sort([("_id", -1)]).limit(50)
            india_news = list(cursor)
            return india_news

        def fetch_news_with_subtag(self, name, tag):
            collection = self.db['news']
            cursor = collection.find({'country': name, 'sub_tags': tag}).sort([("_id", -1)]).limit(50)
            india_news = list(cursor)
            return india_news


    def __init__(self):
        # just for the sake of information
        self.db_conn = _DBConnSingleton.__DBConnection()


_db_singleton = _DBConnSingleton()


def DBConnection():
    return _db_singleton
