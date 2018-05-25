from flask import Flask, render_template, request
from itertools import permutations

import redis
r = redis.Redis(
        host='localhost',
        port=6379,
        )

app = Flask(__name__)

def permutation_count(s):
    count = 0
    for p in permutations(s):
        count += 1
    return count

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/permute", methods=["POST"])
def permute():
    text_input = request.form['text']
    cached_answer = r.get(text_input)
    if cached_answer:
        count = int(cached_answer)
    else:
        count = permutation_count(text_input)
        r.set(text_input, count)

    return render_template(
            'permute.html',
            number_of_permutations=count,
            text_input=text_input,
            was_cached=(cached_answer is not None)
            )
