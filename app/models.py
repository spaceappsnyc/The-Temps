from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_contact = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_contact = db.Column(db.DateTime)

    def __repr__(self):
        return '<Party {}>'.format(self.id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    location = db.Column(db.Integer, db.ForeignKey('location.id'))
    is_mobile = db.Column(db.Boolean)
    is_safe = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128))
    zip = db.Column(db.Integer)

    def __repr__(self):
        return '<Location {}>'.format(self.id)


class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)


class PartySupply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'))
    have = db.Column(db.Boolean)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
