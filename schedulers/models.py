from sqlalchemy.orm import relationship
from .. import db


class Scheduler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cron = db.Column(db.String(500))
    appliances = db.relationship('Appliance', backref='scheduler', lazy=True)

    def __repr__(self):
        return f'<Scheduler name={self.name}, cron={self.cron}, appliances={self.appliances}>'