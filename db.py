from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


Model = db.Model
Column = db.Column
Integer = db.Integer
String = db.String
DateTime = db.DateTime
Numeric = db.Numeric
ForeignKey = db.ForeignKey
Enum = db.Enum
relationship = db.relationship
Index = db.Index

def init_db():
    import models  
    db.create_all()
