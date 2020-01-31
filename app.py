from flask import Flask
from celery import Celery
from scripts.print import print_test


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def test():
    print_test()


@app.route('/', methods=['GET'])
def index():
    test.delay()
    return 'hey there'


if __name__ == '__main__':
    app.run(debug=True)
