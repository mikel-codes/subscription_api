import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) #Ensures files path are accessible to tests

import pytest
from app import app, db
from models import Subscription, User, Plan, Status

@pytest.fixture
def app_context():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

    
def test_user_model(app_context):
    user = User(username="example_user", password_hash="passw_hash")
    db.session.add(user)
    db.session.commit()

    assert User.query.count() == 1
    assert User.query.first().username == 'example_user'


def test_plan_model(app_context):
    plan = Plan(name="Pro", price=10900.00)
    db.session.add(plan)
    db.session.commit()

    assert Plan.query.count() == 1
    fetched_plan = Plan.query.first()
    assert fetched_plan.name == 'Pro'
    assert fetched_plan.name != 'pro'
    assert fetched_plan.price == 10900.00


def test_subscription_model(app_context):
    user = User(username="username_", password_hash="pwhash")
    plan = Plan(name="Free", price=0.0)

    db.session.add_all([user, plan])
    db.session.commit()
    sub = Subscription(user_id=user.id, plan_id=plan.id)
    db.session.add(sub)
    db.session.commit()

    fetched_sub = Subscription.query.filter_by(user_id=user.id).first()
    assert fetched_sub.status.value.lower() == 'active', 'should show default status is active'
    assert isinstance(fetched_sub.status, Status), 'should match types as enum'

    fetched_sub.cancel()
    assert fetched_sub.status.value.lower() == 'cancelled', 'should show default status is active'


