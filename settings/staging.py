from celery.schedules import crontab

CELERY_DEFAULT_QUEUE = 'default'
CELERY_ROUTES = {
    'runner.tasks.dummy_task': {'queue': 'default'},
    'runner.tasks.dummy_periodic_task': {'queue': 'default'},
}

CELERYBEAT_SCHEDULE = {
    'minda-vehicle-details-task': {
        'task': 'runner.tasks.minda_vehicle_details',
        # Every minute
        'schedule': crontab(minute="*"),
    }
}

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0
BROKER_URL = "redis://localhost:6379/0"
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 1500}

MONGODB_HOST = 'localhost'