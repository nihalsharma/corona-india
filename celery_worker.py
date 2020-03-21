

from app import create_app, init_celery, celery_instance

app = create_app()
init_celery(celery_instance, app)

