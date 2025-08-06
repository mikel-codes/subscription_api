
import pytest
from app import app
from models import User, Plan, Subscription, Status

@pytest.fixture
def subscribe_user(client, sample_users_and_plans):
   user1, free_plan, paid_plan = sample_users_and_plans
   payload = {'user_id': user1.id, 'plan_id': free_plan.id}
   res = client.post('/subscriptions/subscribe', json=payload)
   yield res, user1, free_plan, paid_plan

def test_subscription_activation(subscribe_user):
    res, user1, free_plan, paid_plan = subscribe_user
    assert res.status_code == 201
   
    res_json = res.get_json()
    assert res_json['message'] == 'Subscribed successfully', 'Should match the message'
    assert res_json['plan_id'] == free_plan.id
    assert res_json['plan_id'] != paid_plan.id
    with app.app_context():
        assert Subscription.query.filter_by(status=Status.ACTIVE).count() == 1, "Should confirm one active subscription"
        assert Subscription.query.filter_by(status=Status.CANCELLED).count() == 0, "No existing cancelled subscriptions"


def test_subscriptions_active_listing(client):
    res = client.get('/subscriptions/')
    assert res.status_code == 200



def test_subscription_valid_upgrade(client, subscription, pro_plan):
    user, subscription = subscription
    
    _res = client.put(f'/subscriptions/{user.id}/upgrade', json={'user_id': user.id, 'plan_id': pro_plan.id})
    assert _res.status_code == 200
    with app.app_context():
        assert Subscription.query.filter_by(status='active', user_id=user.id).count() == 1, "Should confirm one active subscription"
        assert Subscription.query.filter_by(status='cancelled', user_id=user.id).count() == 1, "Should confirm previous subscription as cancelled"
    




def test_subscription_cancellation_for_subscribed_user(client, subscription):
    user, subscription = subscription
    res_ = client.delete(f'subscriptions/{user.id}/cancel')
    assert res_.status_code == 200

    ctx = res_.get_json()
    assert ctx['message'] == "Subscription cancelled", "Should match no active subs to cancel message"
    assert not ctx['message'] == "subscription cancelled by you", "Should not match this message"

def test_subscription_cancellation_for_unscribed_user_or_new_user(client, sample_users_and_plans):
    user1, *rest = sample_users_and_plans
    res_ = client.delete(f'subscriptions/{user1.id}/cancel')
    assert res_.status_code == 200

    ctx = res_.get_json()
    assert ctx['message'] == "No active subscription to cancel", "Should match no active subs to cancel message"