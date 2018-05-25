import time
from flask import Flask, render_template, request
from itertools import permutations

from celery import Celery
import redis
r = redis.Redis(
        host='localhost',
        port=6379,
        )

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

## --- Celery Worker
@celery.task
def permutation_count(s):
    count = 0
    for p in permutations(s):
        count += 1
    r.set(s, count)

## --- Web Server
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/permute", methods=["POST"])
def permute():
    text_input = request.form['text']

    was_cached = True
    if r.get(text_input) is None:
        permutation_count.delay(text_input)
        was_cached = False

    count = None
    while True:
        count = r.get(text_input)
        if count is not None:
            count = int(count)
            break
        time.sleep(.3)

    return render_template(
            'permute.html',
            number_of_permutations=count,
            text_input=text_input,
            was_cached=was_cached
            )
