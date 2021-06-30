from sqlalchemy.orm import relationship
from .. import db


appliances = db.Table('appliances',
    db.Column('appliance_id', db.Integer, db.ForeignKey('appliance.id'), primary_key=True),
    db.Column('scheduler_id', db.Integer, db.ForeignKey('scheduler.id'), primary_key=True)
)

class Scheduler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cron = db.Column(db.String(500))
    state = db.Column(db.Integer)
    appliance_state = db.Column(db.Integer)
    appliances = db.relationship('Appliance', secondary=appliances, lazy='subquery',
        backref=db.backref('schedulers', lazy=True))
    # appliances = db.relationship('Appliance', backref='scheduler', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="scheduler")

    def __repr__(self):
        return f'<Scheduler name={self.name}, cron={self.cron}, appliances={self.appliances} appliance_state={self.appliance_state}, state={self.state}>'