MONGODB_HOST = 'localhost'
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0
BROKER_URL = "redis://localhost:6379/0"
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 1500}