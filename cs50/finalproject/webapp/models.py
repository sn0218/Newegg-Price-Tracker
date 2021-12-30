# from webapp import db is equivalent to the below line which . means the current python package folder
from . import db 
# Import UserMixin from flask_login library to provide boilerplate methods for managing users 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative, DeclarativeMeta

class Tracks(db.Model):
    """"Track record model"""
    id = db.Column(db.Integer, primary_key=True)
    # associate foreign key from user
    """one-to-many relation that one user can have many notes"""
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    url = db.Column(db.Text)
    productname = db.Column(db.String(1000))
    trackedprice = db.Column(db.Float)
    targetprice = db.Column(db.Float)
    # add current datetime 
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # create method to the class to convert sqlalchemy object to dict
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
    

class Users(db.Model, UserMixin):
    """User account model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(150), unique=False)
    password = db.Column(db.String(150))
    # store all notes of the user owned referenced from the class Note
    track = db.relationship("Tracks")

    
   