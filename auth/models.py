from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .. import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    appliance = relationship("Appliance", uselist=False, back_populates="user")
    scheduler = relationship("Scheduler", uselist=False, back_populates="user")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<User name={self.name}, email={self.email}, appliance={self.appliance}, scheduler={self.scheduler}, created_at={self.created_at}, updated_at={self.updated_at}>'

