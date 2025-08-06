import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) #Ensures files path are accessible to tests

import json
from models import Plan

def test_list_plans(client, sample_users_and_plans): # we inject the fixture
    res = client.get('/plans/')
    assert res.status_code == 200

    json_ = res.get_json()
    assert json_.__len__() == 2, 'should have 2 instances of Plan'
    assert any(plan['name'] == 'Free' for plan in json_), 'one plan must have a "Free" name'
    assert any(plan['price'] == 0. for plan in json_), "one plan 'Free plan' must be 0 priced"


def test_create_plan(client):
    payload1 = json.dumps({'name': 'Free1',  'price': 0.0})
    payload2 = json.dumps({'name': 'Basic', 'price': 600})
    payload3 = json.dumps({'name': 'Pro1',   'price': 10000})

    """ we test to see each plan is created and so validate the endpoint """
    res1 = client.post('/plans/', data=payload1, content_type="application/json")
    res2 = client.post('/plans/', data=payload2, content_type="application/json")
    res3 = client.post('/plans/', data=payload3, content_type="application/json")

    assert  res1.status_code ==  res2.status_code ==  res3.status_code == 200
    assert  Plan.query.count() == 3, 'Total plans now 3'

