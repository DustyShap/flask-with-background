from flask import Flask, render_template, request
from itertools import permutations

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/permute", methods=["POST"])
def permute():
    text_input = request.form['text']
    return render_template('permute.html', permutations=permutations(text_input))
