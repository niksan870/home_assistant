from sqlalchemy.orm import relationship
from .. import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    image = db.Column(db.String(500))
    appliances = db.relationship('Appliance', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category name={self.name}, description={self.description}, image={self.image}, appliances={self.appliances}>'