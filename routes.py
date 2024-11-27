# # routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from models import db, Inwoner, Casus, Werknemer, Team, InterneInzet, InternProduct, Status
from datetime import datetime

# Define the blueprint
routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # Aangenomen dat gebruikers hun achternaam gebruiken
        password = request.form['password']

        # Zoek werknemer op basis van achternaam
        werknemer = Werknemer.query.filter_by(achternaam=username).first()

        if werknemer and werknemer.check_password(password):
            # Succesvolle login
            login_user(werknemer)
            flash('Welkom terug, {}!'.format(werknemer.voornaam), 'success')
            return redirect(url_for('routes.home'))
        else:
            # Mislukte login
            flash('Ongeldige gebruikersnaam of wachtwoord', 'danger')
    
    return render_template('login.html')


@routes_blueprint.route('/logout')
def logout():
    logout_user()
    flash('Je bent uitgelogd.', 'info')
    return redirect(url_for('routes.login'))


@routes_blueprint.route('/')
@login_required
def home():
    # Haal filters uit de query parameters
    Casussoort_filter = request.args.get('Casussoort')
    Casusstatus_filter = request.args.get('Casusstatus')
    casushouder_filter = request.args.get('casushouder')
    team_filter = request.args.get('team')

    # Base query voor Casusen
    query = Casus.query

    # Pas filters toe als ze zijn ingesteld
    if Casussoort_filter:
        query = query.filter_by(Casussoort=Casussoort_filter)
    if Casusstatus_filter:
        query = query.filter_by(status_id=Casusstatus_filter)
        print(query)
    if casushouder_filter:
        query = query.filter_by(casushouder_id=casushouder_filter)
    if team_filter:
        query = query.filter_by(team_id=team_filter)

    # Voer de query uit
    triageCasusen = query.all()

    # Haal opties voor de filters op
    Casussoorten = Casus.query.with_entities(Casus.soort).distinct().all()
    Casusstatussen = Status.query.all()
    casushouders = Werknemer.query.all()  # Neem aan dat casushouders werknemers zijn
    teams = Team.query.all()

    # Render de pagina met de gefilterde Casusen en filteropties
    return render_template(
        'index.html',
        triageCasusen=triageCasusen,
        Casussoorten=[t[0] for t in Casussoorten],
        Casusstatussen=Casusstatussen,
        casushouders=casushouders,
        teams=teams
    )


@routes_blueprint.route('/Casus/new', methods=['GET', 'POST'])
def new_casus():
    if request.method == 'POST':
        status_id = request.form['status_id']
        Casussoort = request.form['Casussoort']
        bsn = request.form['bsn']
        casushouder_id = request.form['casushouder_id']
        team_id = request.form['team_id']

        # Haal of maak de inwoner
        inwoner = Inwoner.query.filter_by(bsn=bsn).first()
        if not inwoner:
            inwoner = Inwoner(bsn=bsn)
            db.session.add(inwoner)
            db.session.commit()

        # Maak een nieuw Casus
        Casus = Casus(
            status_id=status_id,
            Casussoort=Casussoort,
            inwoner_id=inwoner.id,
            casushouder_id=casushouder_id,
            team_id=team_id
        )
        db.session.add(Casus)
        db.session.commit()

        # Voeg toewijzingen toe
        toewijzing_producten = request.form.getlist('toewijzing_product[]')
        toewijzing_startdatums = request.form.getlist('toewijzing_startdatum[]')
        toewijzing_einddatums = request.form.getlist('toewijzing_einddatum[]')

        for product, startdatum, einddatum in zip(toewijzing_producten, toewijzing_startdatums, toewijzing_einddatums):
            # Converteer de string naar datetime.date objecten
            startdatum_obj = datetime.strptime(startdatum, '%Y-%m-%d').date()
            einddatum_obj = datetime.strptime(einddatum, '%Y-%m-%d').date() if einddatum else None

            toewijzing = Toewijzing(
                product=product,
                startdatum=startdatum_obj,
                einddatum=einddatum_obj,
                Casus_id=Casus.id,
                werknemer_id=casushouder_id
            )
            db.session.add(toewijzing)

        db.session.commit()
        return redirect(url_for('routes.home'))

    statussen = Status.query.all()
    werknemers = Werknemer.query.order_by(Werknemer.achternaam).all()
    teams = Team.query.all()

    return render_template('Casus_form.html', statussen=statussen, werknemers=werknemers, teams=teams)


@routes_blueprint.route('/pending-changes')
def pending_changes():
    return render_template('pending_changes.html')

@routes_blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Controleer of het huidige wachtwoord klopt
        if not current_user.check_password(current_password):
            flash('Huidig wachtwoord is onjuist.', 'error')
            return redirect(url_for('routes.change_password'))

        # Controleer of de nieuwe wachtwoorden overeenkomen
        if new_password != confirm_password:
            flash('De nieuwe wachtwoorden komen niet overeen.', 'error')
            return redirect(url_for('routes.change_password'))

        # Update het wachtwoord
        current_user.set_password(new_password)
        db.session.commit()

        flash('Wachtwoord succesvol gewijzigd!', 'success')
        return redirect(url_for('routes.home'))

    return render_template('change_password.html')