import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(test_config=None):
    """Application factory for Flask + HTMX + SQLite."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secure-change-me-32byte-min"),
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
        WTF_CSRF_TIME_LIMIT=7200,
        WTF_CSRF_HEADERS=["X-CSRFToken", "X-CSRF-Token"],
    )
    
    if test_config is not None:
        app.config.update(test_config)
        
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
        
    # Initialize extensions
    csrf.init_app(app)
    
    from app import db
    db.init_app(app)

    from app import observability
    observability.init_app(app)
    
    # Auto-initialize database tables if file doesn't exist yet
    with app.app_context():
        if not os.path.exists(app.config["DATABASE"]):
            try:
                db.init_db()
            except Exception as e:
                app.logger.warning("Auto-init db deferred: %s", e)
                
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response
        
    return app
