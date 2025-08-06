from flask import Flask
from flask_migrate import Migrate
from db import db, init_db
from routes import auth_bp, sub_bp, plans_bp


app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app) 
migrate = Migrate(app, db)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(plans_bp, url_prefix="/plans")
app.register_blueprint(sub_bp, url_prefix="/subscriptions")

if app.config["ENVIRONMENT"] == "development":
    with app.app_context():
        init_db()

if __name__ == "__main__":
    app.run(debug=True)
