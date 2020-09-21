from flask import Flask, render_template, request
import random 
from _collections import defaultdict
import pandas as pd
import requests
from flask_frozen import Freezer


Nick_text = pd.read_pickle('Splice_In_Time.pkl')
Shakespeare = pd.read_pickle("Shakespeare.pkl")

def markov_chain(text):
    words = text.split()
    dictionary = defaultdict(list)
    for current_word, next_word in zip(words[0:], words[1:]):
        dictionary[current_word].append(next_word)
    dictionary = dict(dictionary)
    return dictionary
Nick_Dict = markov_chain(Nick_text)
Shakespeare_Dict = markov_chain(Shakespeare)

def generator(chain, count):
    w1 = random.choice(list(chain.keys()))
    sentence = w1.capitalize()
    for i in range(count - 1):
        w1 = random.choice(chain[w1])
        w2 = w1
        sentence += ' ' + w2 
    sentence += random.choice(['.', '?', '!', ';', '...'])
    return sentence

app = Flask(__name__)
freezer = Freezer(app)
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get("Generate") == "Generate":
                return render_template("index.html", text=generator(Nick_Dict, 25))
    else:
        return render_template("index.html",text = generator(Nick_Dict, random.randint(10, 50)))


if __name__ == '__main__':
    freezer.freeze()
