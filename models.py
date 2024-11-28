from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Inwoner(db.Model):
    __tablename__ = 'inwoner' 
    id = db.Column(db.Integer, primary_key=True)
    bsn = db.Column(db.String(9), unique=True, nullable=False)
    voornaam = db.Column(db.String(50), nullable=True)
    achternaam = db.Column(db.String(50), nullable=True)   
    adres = db.Column(db.String(100), nullable=True)   
    woonplaats = db.Column(db.String(50), nullable=True)    
    geboortedatum = db.Column(db.Date, nullable=True)
    casussen = db.relationship('Casus', backref='inwoner', lazy=True)

class Werknemer(db.Model, UserMixin):
    __tablename__ = 'werknemer' 
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(50), nullable=False)
    achternaam = db.Column(db.String(50), nullable=False)
    datum_in_dienst = db.Column(db.Date, nullable=False)
    datum_uit_dienst = db.Column(db.Date, nullable=True)
    
    # Relaties met expliciete foreign_keys
    geregistreerde_casussen = db.relationship(
        'Casus',
        foreign_keys='Casus.geregistreerd_door',
        backref='geregistreerd_door_werknemer',
        lazy=True
    )
    casushouder_casussen = db.relationship(
        'Casus',
        foreign_keys='Casus.casushouder_id',
        backref='casushouder_werknemer',
        lazy=True
    )
    tweede_casushouder_casussen = db.relationship(
        'Casus',
        foreign_keys='Casus.tweede_casushouder_id',
        backref='tweede_casushouder_werknemer',
        lazy=True
    )
    interne_inzet_werknemer = db.relationship(
        'InterneInzet',
        foreign_keys='InterneInzet.werknemer_id',
        backref='interne_inzet_werknemer',
        lazy=True
    )
    
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Functie(db.Model):
    __tablename__ = 'functie' 
    id = db.Column(db.Integer, primary_key=True)
    functienaam = db.Column(db.String(50), nullable=False) 

class Gebied(db.Model):
    __tablename__ = 'gebied' 
    id = db.Column(db.Integer, primary_key=True)
    gebiednaam = db.Column(db.String(100), unique=True, nullable=False)
    teams = db.relationship('Team', backref='gebied', lazy=True)  
    
class Team(db.Model):
    __tablename__ = 'team' 
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100), unique=True, nullable=False)
    gebied_id = db.Column(db.Integer, db.ForeignKey('gebied.id', ondelete="SET NULL"), nullable=True)
    casussen = db.relationship('Casus', backref='team', lazy=True)

class Frequentie(db.Model):
    __tablename__ = 'frequentie' 
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False)
    omschrijving = db.Column(db.String(100), nullable=True)

class Status(db.Model):
    __tablename__ = 'status' 
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False, unique=True)
    omschrijving = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Status {self.naam}>"

class MelderSoort(db.Model):
    __tablename__ = 'meldersoort'  
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False)
    omschrijving = db.Column(db.String(100), nullable=True)
    
class CasusSoort(db.Model):
    __tablename__ = 'casussoort'  
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False)
    omschrijving = db.Column(db.String(100), nullable=True)

class InternProduct(db.Model):
    __tablename__ = 'internproduct' 
    id = db.Column(db.Integer, primary_key=True)
    productnaam = db.Column(db.String(100), nullable=False)
    startdatum = db.Column(db.Date, nullable=True)
    einddatum = db.Column(db.Date, nullable=True)
    inzet = db.relationship('InterneInzet', backref='inzet', lazy=True)

class InterneInzet(db.Model):
    __tablename__ = 'interneinzet' 
    id = db.Column(db.Integer, primary_key=True)
    startdatum = db.Column(db.Date, nullable=False)
    einddatum = db.Column(db.Date, nullable=True)
    casus_id = db.Column(db.Integer, db.ForeignKey('casus.id'), nullable=False)
    werknemer_id = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('internproduct.id'), nullable=False)  
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    volume = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    frequentie = db.Column(db.String(50), nullable=True)

class Casus(db.Model):
    __tablename__ = 'casus' 
    id = db.Column(db.Integer, primary_key=True)
    registratiedatum = db.Column(db.Date, default=datetime.utcnow)
    casus_naam = db.Column(db.String(255), nullable=True)  # Casusnaam optioneel
    einde_wettelijke_termijn = db.Column(db.Date, nullable=True)
    geregistreerd_door = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=True)
    casussoort_id = db.Column(db.Integer, db.ForeignKey('casussoort.id'), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    inwoner_id = db.Column(db.Integer, db.ForeignKey('inwoner.id'), nullable=False)
    meldersoort_id = db.Column(db.Integer, db.ForeignKey('meldersoort.id'), nullable=False)
    casushouder_id = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=True)
    tweede_casushouder_id = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    soort = db.relationship('CasusSoort', backref='casussen', lazy=True)    
    interne_inzet = db.relationship('InterneInzet', backref='casus', lazy=True)
    toelichting = db.Column(db.Text, nullable=True)

# class Casus(db.Model):
#     __tablename__ = 'casus' 
#     id = db.Column(db.Integer, primary_key=True)
#     registratiedatum = db.Column(db.Date, default=datetime.utcnow)
#     casus_naam = db.Column(db.String(80), nullable=False)
#     einde_wettelijke_termijn = db.Column(db.Date, nullable=True)
#     geregistreerd_door = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=True)
#     casussoort_id = db.Column(db.Integer, db.ForeignKey('casussoort.id'), nullable=True)  # Correcte verwijzing
#     status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
#     inwoner_id = db.Column(db.Integer, db.ForeignKey('inwoner.id'), nullable=False)
#     meldersoort_id = db.Column(db.Integer, db.ForeignKey('meldersoort.id'), nullable=False)
#     casushouder_id = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=True)
#     tweede_casushouder_id = db.Column(db.Integer, db.ForeignKey('werknemer.id'), nullable=True)
#     team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
#     soort = db.relationship('CasusSoort', backref='casussen', lazy=True)
#     interne_inzet = db.relationship('InterneInzet', backref='casus', lazy=True)
#     toelichting = db.Column(db.Text, nullable=True)