from datetime import datetime, timezone
from enum import Enum as PyEnum
from db import *
from sqlalchemy import Enum as SQLEnum


class Status(PyEnum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'

    



class User(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    subscriptions = relationship("Subscription", back_populates="user", lazy="dynamic")


class Plan(Model):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime,  default=lambda: datetime.now(timezone.utc))
    features = Column(JSON)
    subscriptions = relationship("Subscription", back_populates="plan", lazy="dynamic")


class Subscription(Model):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    start_date = Column(DateTime,  default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime)
    status = Column(SQLEnum(Status), default=Status.ACTIVE, index=True)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")

    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
    )

    def cancel(self):
        self.status = Status.CANCELLED
        db.session.commit()
