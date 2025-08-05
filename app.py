from flask import Flask
from db import db, init_db


app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app) 
with app.app_context():
    init_db()




if __name__ == "__main__":
    app.run(debug=True)
