from flask import Flask
from .metrics import bp as metrics_bp, setup_metrics  #
from .config import get_config

def create_app() -> Flask:
    app = Flask(__name__)
    cofig_Class = get_config()
    app.config.from_object(cofig_Class)

    # Lazy imports to avoid circular deps during app init
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    # mterics 
    app.register_blueprint(metrics_bp)
    setup_metrics(app)

    if cofig_Class.FLASK_ENV == 'development':
        print("Running in Dev mode (Development)")

    if cofig_Class.FLASK_ENV == 'staging':
        print("Running in Stage mode (Staging)")

    if cofig_Class.FLASK_ENV == 'production':
        print("Running in Prod mode (Production)")
    


    return app
