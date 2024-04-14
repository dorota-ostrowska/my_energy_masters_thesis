from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Client(db.Model, UserMixin):
    __tablename__ = "client"
    id_client = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    pesel = db.Column(db.String(11), unique=True)
    address_id_address = db.Column(db.Integer, db.ForeignKey('address.id_address'))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.Text)

    def __repr__(self):
        return f'<Client "{self.name} {self.surname}">'
    
class Address(db.Model, UserMixin):
    __tablename__ = "address"
    id_address = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    house_number = db.Column(db.String(5))
    zip_code = db.Column(db.String(6))
    city = db.Column(db.String(50))
    additional_info = db.Column(db.String(50))
    clients = db.relationship('Client', backref='address')

    def __repr__(self):
        return f'<Address "{self.street}">'