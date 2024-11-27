# routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import db, Inwoner, Traject, Werknemer, Team, Toewijzing

# Define the blueprint
routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
def home():
    return render_template('index.html')

# Add additional route definitions here as needed, for example:
@routes_blueprint.route('/inwoner', methods=['POST'])
def create_inwoner():
    # Logic to create a new Inwoner
    pass

@routes_blueprint.route('/traject/new', methods=['GET', 'POST'])
def new_traject():
    if request.method == 'POST':
        # Retrieve form data
        status = request.form['status']
        trajectsoort = request.form['trajectsoort']
        bsn = request.form['bsn']
        casushouder_id = request.form['casushouder_id']
        team_id = request.form['team_id']

        # Fetch or create Inwoner
        inwoner = Inwoner.query.filter_by(bsn=bsn).first()
        if not inwoner:
            inwoner = Inwoner(bsn=bsn)
            db.session.add(inwoner)
            db.session.commit()

        # Create a new Traject
        traject = Traject(status=status, trajectsoort=trajectsoort,
                          inwoner_id=inwoner.id, casushouder_id=casushouder_id,
                          team_id=team_id)
        db.session.add(traject)
        db.session.commit()
        return redirect(url_for('index'))
    
    werknemers = Werknemer.query.order_by(Werknemer.achternaam).all()
    teams = Team.query.all()
    return render_template('traject_form.html', werknemers=werknemers, teams=teams)

# Additional routes for viewing and editing data would go here
