
from flask import Blueprint, jsonify, request
from db import db
from models import Plan

plans_bp = Blueprint("plans", __name__)

@plans_bp.route("/", methods=["GET"])
def list_plans():
    """ Display all availble plans"""
    plans = Plan.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": float(p.price)} for p in plans])

@plans_bp.route("/", methods=["POST"])
def create_plan():
    """ Add a new subscription Plan """
    data = request.json
    plan = Plan(name=data["name"], price=data["price"])
    db.session.add(plan)
    db.session.commit()
    return jsonify({"message": "Plan created"})
