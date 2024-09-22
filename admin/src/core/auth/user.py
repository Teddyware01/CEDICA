from src.core.database import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

   
    issues = db.relationship("Issue", back_populates="user")

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    update_at =  db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<User #{self.id} email = {self.email}"