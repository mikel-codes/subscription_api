from flask import Blueprint, jsonify, request
from db import db
from models import Subscription
from sqlalchemy import text

sub_bp = Blueprint("subscriptions", __name__)

@sub_bp.route("/<int:user_id>/active", methods=["GET"])
def get_active_subscription(user_id):
    # Optimized raw SQL for active subscription lookup
    sql = text("""
        SELECT s.id, s.plan_id, s.status, s.start_date
        FROM subscriptions s
        WHERE s.user_id = :uid AND s.status = 'active'
        ORDER BY s.start_date DESC
        LIMIT 1
    """)
    result = db.session.execute(sql, {"uid": user_id}).fetchone()
    return jsonify(dict(result)) if result else jsonify({"message": "No active subscription"})

@sub_bp.route("/", methods=["POST"])
def subscribe():
    data = request.json
    # Cancel previous active subscription
    db.session.execute(text("""
        UPDATE subscriptions
        SET status = 'canceled', end_date = CURRENT_TIMESTAMP
        WHERE user_id = :uid AND status = 'active'
    """), {"uid": data["user_id"]})
    db.session.commit()
    
    new_sub = Subscription(user_id=data["user_id"], plan_id=data["plan_id"])
    db.session.add(new_sub)
    db.session.commit()
    return jsonify({"message": "Subscribed successfully"})
