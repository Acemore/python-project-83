from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
