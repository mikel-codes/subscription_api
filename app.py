from flask import Flask
from db import db, init_db
from routes.auth import auth_bp
from routes.subscription import sub_bp
from routes.plans import plans_bp

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app) 
with app.app_context():
    init_db()


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(plans_bp, url_prefix="/plans")
app.register_blueprint(sub_bp, url_prefix="/subscriptions")

if __name__ == "__main__":
    app.run(debug=True)
