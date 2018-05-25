import time
import json
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
    job_state = json.loads(r.get(s).decode('utf-8'))

    job_state["status"] = "in progress"
    r.set(s, json.dumps(job_state))

    count = 0
    for p in permutations(s):
        count += 1

    job_state["status"] = "complete"
    job_state["count"] = count
    r.set(s, json.dumps(job_state))

## --- Web Server
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/permute", methods=["POST"])
def permute():
    text_input = request.form['text']

    was_cached = True
    if r.get(text_input) is None:
        r.set(text_input, json.dumps({
            "status": "not started",
            "count": "0"
        }))
        permutation_count.delay(text_input)
        was_cached = False

    count = None
    while True:
        message = r.get(text_input)
        status = None
        if message is not None:
            job_state = json.loads(message.decode('utf-8'))
            count = int(job_state["count"])
            status = job_state["status"]
            break
        time.sleep(.3)

    return render_template(
            'permute.html',
            number_of_permutations=count,
            text_input=text_input,
            job_state=status
            )
