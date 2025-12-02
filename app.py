# app.py

from flask import Flask
from config import Config
from models import db
from flask_login import LoginManager
from flask_migrate import Migrate
from routes import routes_blueprint  # Import de blueprint

# Maak de app via een factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialiseer extensie
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    migrate = Migrate(app, db)  # Voeg Flask-Migrate toe
    
    # Configureer login
    login_manager.login_view = 'routes.login'
    login_manager.login_message = "Je moet ingelogd zijn om deze pagina te bekijken."
    login_manager.login_message_category = "info"

    # Voeg user_loader toe
    from models import Werknemer

    @login_manager.user_loader
    def load_user(user_id):
        return Werknemer.query.get(int(user_id))

    # Registreer blueprints
    app.register_blueprint(routes_blueprint)

    return app


# Main entry point
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Maak database-tabellen aan als ze nog niet bestaan
    app.run(debug=True)
