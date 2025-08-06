import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) #Ensures files path are accessible to tests

import pytest
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Plan, Subscription

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///:memory:'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
            hash = generate_password_hash('pws111')
            user = User(username="username01", password_hash=hash)  
            db.session.add(user)
            db.session.commit()    
        yield client

        with app.app_context():
            db.drop_all()
    

@pytest.fixture
def sample_users_and_plans(client):
    with app.app_context():


        user1 = User(username="example_user", password_hash="passhw")
        free_plan = Plan(name="Free", price=0.0)
        paid_plan = Plan(name="Pro", price=1000.0)
        db.session.add_all([ user1, free_plan,paid_plan])
        db.session.commit()
        
        yield  user1, free_plan, paid_plan
    
@pytest.fixture
def subscription():
    with app.app_context():
        user =  User(username="A1_user", password_hash="passhwd")
        free_plan = Plan(name="Free", price=0.0)
        db.session.add_all([user, free_plan])
        db.session.commit()
        subscription = Subscription(user_id=user.id, plan_id=free_plan.id)
        db.session.add(subscription)
        db.session.commit()
        yield user, subscription

        db.session.query(Subscription).delete()
        db.session.query(Plan).delete()
        db.session.query(User).delete()
        db.session.commit()

@pytest.fixture
def pro_plan():
    pro_plan = Plan(name="Pro", price=90000)
    db.session.add(pro_plan)
    db.session.commit()

    yield pro_plan
    db.session.query(Plan).delete()
    db.session.commit()
    