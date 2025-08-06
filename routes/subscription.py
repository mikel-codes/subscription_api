from flask import Blueprint, jsonify, request
from db import db
from models import Subscription, Plan, Status
from sqlalchemy import text

from datetime import datetime
sub_bp = Blueprint("subscriptions", __name__)



@sub_bp.route("/<int:user_id>/active", methods=["GET"])
def get_active_user_subscription(user_id):
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

@sub_bp.route("/", methods=["GET"])
def list_subscriptions():
    # I omitted pagination for the sake of brevity
    sql = text("SELECT * FROM subscriptions")
    subs = db.session.execute(sql).mappings().all()
    subs_list =  [dict(row) for row in subs]
    return jsonify(subs_list) 

def get_plan_price(plan_id):
    """Fetch plan price efficiently"""
    plan = db.session.get(Plan, plan_id)
    return plan.price if plan else 0.0


def get_user_active_subscription(user_id):
    """Fetch user's active subscription using ORM"""
    return Subscription.query.filter_by(user_id=user_id, status='active').first() 


def get_user_active_subscription_price(user_id):
    """Return current subscription price"""
    sub = get_user_active_subscription(user_id)
    return get_plan_price(sub.plan_id) if sub else 0.0

@sub_bp.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    user_id = data["user_id"]
    plan_id = data["plan_id"]

    with db.engine.connect() as conn:

        # Validate user as registered 
        user_exists = conn.execute(
            text("SELECT 1 FROM users WHERE id = :user_id LIMIT 1"), {"user_id": user_id}
        ).fetchone()
        if not user_exists:
            return jsonify({"error": "User not found"}), 404
        user_id = user_exists[0] # Here we retrieve the requested id of user found
 
        # Validate this as an exisiting plan
        plan_exists = conn.execute(
            text("SELECT id FROM plans WHERE id = :plan_id LIMIT 1"),
            {"plan_id": plan_id}
        ).fetchone()
        if not plan_exists:
            return jsonify({"error": "Plan not found"}), 404

        conn.execute(
            text("""
                UPDATE subscriptions
                SET status = 'cancelled', end_date = CURRENT_TIMESTAMP
                WHERE user_id = :user_id AND status = 'active'
            """), {"user_id": user_id}
        ) # Here ensure any existing active subscriptions is first cancelled

     
        conn.execute(
            text("""
                INSERT INTO subscriptions (user_id, plan_id, status, start_date)
                VALUES (:uid, :plan, 'active', CURRENT_TIMESTAMP)
            """),
            {"uid": user_id, "plan": plan_id}
        ) # Finally ensure that we can activate the user_subscriptions per plan selected
        conn.commit()

    return jsonify({"message": "Subscribed successfully", "plan_id": plan_id}), 201

@sub_bp.route("/<int:user_id>/upgrade", methods=["PUT"])
def upgrade_subscription(user_id):
    data = request.get_json()
    next_plan_id = data["plan_id"]

    current_price = get_user_active_subscription_price(user_id)
    next_price = get_plan_price(next_plan_id)

    # Ensure request is valid input
    if next_price <= current_price:
        return jsonify({"error": "Upgrade must be to a higher plan"}), 400

    with db.engine.connect() as conn:
        # Cancel old subscription
        conn.execute(
            text("""
                UPDATE subscriptions
                SET status = :canceled_status, end_date = CURRENT_TIMESTAMP
                WHERE user_id = :uid AND status = :active_stats
            """),
            {"uid": user_id, 
             "canceled_status": Status.CANCELLED.value,
             "active_stats": Status.ACTIVE.value
             }
        )

        # Insert new subscription
        conn.execute(
            text("""
                INSERT INTO subscriptions (user_id, plan_id, status, start_date)
                VALUES (:uid, :plan, 'active', CURRENT_TIMESTAMP)
            """),
            {"uid": user_id, "plan": next_plan_id}
        )
        conn.commit()

    return jsonify({
        "message": "Subscription upgraded",
        "new_plan_id": next_plan_id,
        "old_price": current_price,
        "new_price": next_price
    }), 200




@sub_bp.route("/<int:user_id>/cancel", methods=["DELETE"])
def cancel(user_id):
    with db.engine.connect() as conn:
        
        user = conn.execute(
            text("SELECT id FROM users WHERE id = :user_id"), {"user_id": user_id}
        ).fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_id = user[0]


        result = conn.execute(
            text("""
                UPDATE subscriptions
                SET status = 'cancelled', end_date = CURRENT_TIMESTAMP
                WHERE user_id = :uid AND status = 'active'
            """),
            {"uid": user_id}
        )
        conn.commit()

        if result.rowcount == 0:
            return jsonify({"message": "No active subscription to cancel"}), 200

    return jsonify({"message": "Subscription cancelled"}), 200
