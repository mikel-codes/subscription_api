from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#Explicity define fields here to simplify model definition
Model = db.Model
Column = db.Column
Integer = db.Integer
String = db.String
DateTime = db.DateTime
Numeric = db.Numeric
ForeignKey = db.ForeignKey
Enum = db.Enum
relationship = db.relationship
JSON = db.JSON
Index = db.Index


def init_db():
    from models import User, Plan, Subscription  # to avoid circular imports
    db.create_all()
