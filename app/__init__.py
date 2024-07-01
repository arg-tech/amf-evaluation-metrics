from flask import Flask

application = Flask(__name__, template_folder='../app/templates')

from app import routes


