# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Inwoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bsn = db.Column(db.String(9), unique=True, nullable=False)
    trajecten = db.relationship('Traject', backref='inwoner', lazy=True)

class Werknemer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(50), nullable=False)
    achternaam = db.Column(db.String(50), nullable=False)
    datum_in_dienst = db.Column(db.Date, nullable=False)
    datum_uit_dienst = db.Column(db.Date, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    trajecten = db.relationship('Traject', backref='casushouder', lazy=True)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100), unique=True, nullable=False)
    gebied = db.Column(db.String(50), nullable=False)
    werknemers = db.relationship('Werknemer', backref='team', lazy=True)
    trajecten = db.relationship('Traject', backref='team', lazy=True)

class Traject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registratiedatum = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    trajectsoort = db.Column(db.String(50), nullable=False)
    inwoner_id = db.Column(db.Integer, db.ForeignKey('inwoner.id'), nullable=False)
    casushouder_id = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

class Toewijzing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startdatum = db.Column(db.Date, nullable=False)
    einddatum = db.Column(db.Date, nullable=True)
    product = db.Column(db.String(50), nullable=False)
    traject_id = db.Column(db.Integer, db.ForeignKey('traject.id'), nullable=False)
    werknemer_id = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=False)

# Other models such as Plan can be defined similarly
