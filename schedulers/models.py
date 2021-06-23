from sqlalchemy.orm import relationship
from .. import db


class Scheduler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cron = db.Column(db.String(500))
    state = db.Column(db.Integer)
    appliance_state = db.Column(db.Integer)
    appliances = db.relationship('Appliance', backref='scheduler', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="scheduler")

    def __repr__(self):
        return f'<Scheduler name={self.name}, cron={self.cron}, appliances={self.appliances} appliance_state={self.appliance_state}, state={self.state}>'