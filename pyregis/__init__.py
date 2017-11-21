from flask import Flask


app = Flask(__name__, template_folder='dist', static_folder='dist')
