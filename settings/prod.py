MONGODB_HOST = 'localhost'
BROKER_URL = 'mongodb://localhost:27017/corona_india'

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "corona_india",
    "taskmeta_collection": "corona_taskmeta_collection",
}