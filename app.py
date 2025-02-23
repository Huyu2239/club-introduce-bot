
from flask import Flask, render_template

from pathlib import Path
import requests
# os内のenvironmentを扱うライブラリ
import os




app = Flask(__name__, static_folder='./templates/img')



@app.route("/")
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
