from flask import Flask
from flask_restful import Api
from flask_talisman import Talisman
from flask_cors import CORS
from db import db
import os

from resources.stock import Stock

app = Flask(__name__)
Talisman(app)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///stock-prices"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Stock, "/api/stock-prices")

if __name__ == "__main__":
    app.run(debug=True)
