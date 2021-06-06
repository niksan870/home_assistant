from sqlalchemy.orm import relationship
from .. import db


class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    discription = db.Column(db.String(200))

    def __init__(self, name, discription):
        self.name = name
        self.discription = discription

    def save(self):
        """Save a student to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a user from the database.
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Light %s>' % self.discription
