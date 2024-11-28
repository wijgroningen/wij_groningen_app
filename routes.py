# # routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from models import db, Inwoner, Casus, Werknemer, Team, InterneInzet, InternProduct, Status, MelderSoort, CasusSoort
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
    casussoort_filter = request.args.get('casussoort')
    casusstatus_filter = request.args.get('casusstatus')
    casushouder_filter = request.args.get('casushouder')
    team_filter = request.args.get('team')

    # Base query voor Casus
    query = Casus.query

    # Pas filters toe als ze zijn ingesteld
    if casussoort_filter:
        query = query.filter(Casus.casussoort_id == casussoort_filter)
    if casusstatus_filter:
        query = query.filter(Casus.status_id == casusstatus_filter)
    if casushouder_filter:
        query = query.filter(Casus.casushouder_id == casushouder_filter)
    if team_filter:
        query = query.filter(Casus.team_id == team_filter)

    # Debugging: Print de query en resultaten
    print(query)  # Hiermee zie je de query in de terminal
    triagecasussen = query.all()
    print(triagecasussen)  # Hiermee zie je de opgehaalde casussen

    # Haal opties voor de filters op
    casussoorten = CasusSoort.query.all()
    casusstatussen = Status.query.all()
    casushouders = Werknemer.query.all()  # Neem aan dat casushouders werknemers zijn
    teams = Team.query.all()

    # Render de pagina met de gefilterde casussen en filteropties
    return render_template(
        'index.html',
        triagecasussen=triagecasussen,
        casussoorten=casussoorten,
        casusstatussen=casusstatussen,
        casushouders=casushouders,
        teams=teams
    )

@routes_blueprint.route('/Casus/new', methods=['GET', 'POST'])
def new_casus():
    if request.method == 'POST':
        status_id = request.form['status_id']
        meldersoort_id = request.form['meldersoort_id']
        casussoort_id = request.form['casussoort_id']
        inwoner_id = request.form['inwoner_id']  # Correct veld gebruiken
        casushouder_id = request.form['casushouder_id']
        team_id = request.form['team_id']
        casus_naam = request.form.get('casus_naam')  # Optioneel veld
        toelichting = request.form.get('toelichting')  # Optioneel veld
        tweede_casushouder_id = request.form.get('tweede_casushouder_id')

        # Controleer of de inwoner bestaat
        inwoner = Inwoner.query.get(inwoner_id)
        if not inwoner:
            flash('Geselecteerde inwoner bestaat niet.', 'error')
            return redirect(url_for('routes.new_casus'))

        # Automatische naamgeving indien casus_naam leeg is
        if not casus_naam:
            casussoort = CasusSoort.query.get(casussoort_id)
            registratiedatum = datetime.utcnow().strftime('%Y-%m-%d')
            casus_naam = f"{inwoner.achternaam} - {casussoort.naam} - {registratiedatum}"

        # Maak een nieuw Casus
        nieuwe_casus = Casus(
            status_id=status_id,
            casussoort_id=casussoort_id,
            meldersoort_id=meldersoort_id,
            inwoner_id=inwoner.id,
            casushouder_id=casushouder_id,
            tweede_casushouder_id=tweede_casushouder_id,
            team_id=team_id,
            casus_naam=casus_naam,
            toelichting=toelichting
        )
        db.session.add(nieuwe_casus)
        db.session.commit()

        # Voeg toewijzingen toe
        toewijzing_producten = request.form.getlist('toewijzing_product[]')
        toewijzing_startdatums = request.form.getlist('toewijzing_startdatum[]')
        toewijzing_einddatums = request.form.getlist('toewijzing_einddatum[]')
        toewijzing_statussen = request.form.getlist('toewijzing_status[]')

        for product, startdatum, einddatum, status_id in zip(
            toewijzing_producten, toewijzing_startdatums, toewijzing_einddatums, toewijzing_statussen
        ):
            startdatum_obj = datetime.strptime(startdatum, '%Y-%m-%d').date()
            einddatum_obj = datetime.strptime(einddatum, '%Y-%m-%d').date() if einddatum else None

            toewijzing = InterneInzet(
                product_id=product,
                startdatum=startdatum_obj,
                einddatum=einddatum_obj,
                casus_id=nieuwe_casus.id,
                werknemer_id=casushouder_id,
                status_id=status_id
            )
            db.session.add(toewijzing)

        db.session.commit()
        flash('Nieuwe casus succesvol opgeslagen.', 'success')
        return redirect(url_for('routes.home'))

    statussen = Status.query.all()
    casussoorten = CasusSoort.query.all()
    meldersoorten = MelderSoort.query.all()
    werknemers = Werknemer.query.order_by(Werknemer.achternaam).all()
    teams = Team.query.all()

    return render_template(
        'casus_form.html',
        statussen=statussen,
        werknemers=werknemers,
        teams=teams,
        meldersoorten=meldersoorten,
        casussoorten=casussoorten
    )

@routes_blueprint.route('/zoek_inwoner')
def zoek_inwoner():
    zoekterm = request.args.get('zoekterm', '').strip()

    if not zoekterm or len(zoekterm) < 3:
        return jsonify([])  # Geen resultaten als de zoekterm te kort is

    # Zoek inwoners op BSN of achternaam
    inwoners = Inwoner.query.filter(
        (Inwoner.bsn.like(f"%{zoekterm}%")) | (Inwoner.achternaam.ilike(f"%{zoekterm}%"))
    ).all()

    # Retourneer de resultaten als JSON
    return jsonify([{
        'id': inwoner.id,
        'bsn': inwoner.bsn,
        'voornaam': inwoner.voornaam,
        'achternaam': inwoner.achternaam
    } for inwoner in inwoners])

# @routes_blueprint.route('/Casus/new', methods=['GET', 'POST'])
# def new_casus():
#     if request.method == 'POST':
#         status_id = request.form['status_id']
#         meldersoort_id = request.form['meldersoort_id']
#         casussoort_id = request.form['casussoort_id']
#         bsn = request.form['bsn']
#         casushouder_id = request.form['casushouder_id']
#         team_id = request.form['team_id']

#         # Haal of maak de inwoner
#         inwoner = Inwoner.query.filter_by(bsn=bsn).first()
#         if not inwoner:
#             inwoner = Inwoner(bsn=bsn)
#             db.session.add(inwoner)
#             db.session.commit()

#         # Maak een nieuw Casus
#         Nieuwe_casus = Casus(
#             status_id=status_id,
#             casussoort_id=casussoort_id,
#             meldersoort_id = meldersoort_id,
#             inwoner_id=inwoner.id,
#             casushouder_id=casushouder_id,
#             team_id=team_id
#         )
#         db.session.add(Nieuwe_casus)
#         db.session.commit()

#         # Voeg toewijzingen toe
#         toewijzing_producten = request.form.getlist('toewijzing_product[]')
#         toewijzing_startdatums = request.form.getlist('toewijzing_startdatum[]')
#         toewijzing_einddatums = request.form.getlist('toewijzing_einddatum[]')

#         for product, startdatum, einddatum in zip(toewijzing_producten, toewijzing_startdatums, toewijzing_einddatums):
#             # Converteer de string naar datetime.date objecten
#             startdatum_obj = datetime.strptime(startdatum, '%Y-%m-%d').date()
#             einddatum_obj = datetime.strptime(einddatum, '%Y-%m-%d').date() if einddatum else None

#             toewijzing = InterneInzet(
#                 product=product,
#                 startdatum=startdatum_obj,
#                 einddatum=einddatum_obj,
#                 Casus_id=Casus.id,
#                 werknemer_id=casushouder_id
#             )
#             db.session.add(toewijzing)

#         db.session.commit()
#         return redirect(url_for('routes.home'))

#     statussen = Status.query.all()
#     casussoorten = CasusSoort.query.all()
#     meldersoorten = MelderSoort.query.all()
#     werknemers = Werknemer.query.order_by(Werknemer.achternaam).all()
#     teams = Team.query.all()

#     return render_template('Casus_form.html', statussen=statussen, werknemers=werknemers, teams=teams, meldersoorten=meldersoorten, casussoorten=casussoorten)


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