from flask import Flask

from db.setup import DBConnection
from settings import settings
from celery import Celery


def init_celery(celery_appl, app):
    celery_appl.config_from_object(app.config)
    TaskBase = celery_appl.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_appl.Task = ContextTask


def make_celery(app_name=__name__):
    backend = settings.CELERY_RESULT_BACKEND
    broker = settings.BROKER_URL
    celery_appl = Celery(app_name, backend=backend, broker=broker)
    return celery_appl


celery_app = make_celery()

app = None


def create_app(app_name=__name__, **kwargs):
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static', )
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)
    from api import api
    app.register_blueprint(api)
    app.config.from_object(settings)
    db_conn = DBConnection()
    return app


if __name__ == '__main__':
    app = create_app(celery_app=celery_app)
    app.run()
