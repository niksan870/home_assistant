from sqlalchemy.orm import relationship
from .. import db

class Appliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    pin_num = db.Column(db.Integer)
    state = db.Column(db.Integer)
    previous_state = db.Column(db.Integer)
    running_state = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    scheduler_id = db.Column(db.Integer, db.ForeignKey('scheduler.id'),
        nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="appliance")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Appliance name={self.name}, pin_num={self.pin_num}, state={self.state}, category_id={self.category_id}, user_id={self.user_id}, scheduler_id={self.scheduler_id}, created_at={self.created_at}, updated_at={self.updated_at}>'

