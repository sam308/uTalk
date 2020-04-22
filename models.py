from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin

db=SQLAlchemy()

#class User(UserMixin, db.Model):
class User(db.Model):
    """ Users Model """
    __tablename__ = "tryusers"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
