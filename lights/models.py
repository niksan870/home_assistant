from sqlalchemy.orm import relationship
from .. import db


class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    status = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="light")

    def __init__(self, name, description, user_id, status):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.status = status

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
        return f'<Light name={self.name}, description={self.description}, status={self.status}, user_id={self.user_id}>'
