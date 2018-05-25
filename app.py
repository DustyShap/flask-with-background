from flask import Flask, render_template, request
from itertools import permutations

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
    count = permutation_count(text_input)
    return render_template('permute.html', number_of_permutations=count, text_input=text_input)
