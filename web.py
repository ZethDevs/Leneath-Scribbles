from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
import os
from threading import Thread

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()