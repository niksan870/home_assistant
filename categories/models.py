from sqlalchemy.orm import relationship

from .. import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    image = db.Column(db.String(500))
    appliances = db.relationship("Appliance", backref="category", lazy=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )

    def __repr__(self):
        return f"<Category name={self.name}, description={self.description}, image={self.image}, appliances={self.appliances}, created_at={self.created_at}, updated_at={self.updated_at}>"
