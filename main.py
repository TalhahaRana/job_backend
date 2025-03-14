import os
from flask import Flask
from extensions import db, init_extensions
from routes.auth_routes import auth_bp
from routes.job_routes import job_bp

app = Flask(__name__)

# Supabase PostgreSQL connection string
database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db.mmwaubrgkbcjhazsjjpm.supabase.co:5432/postgres')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_extensions(app)

# Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(job_bp, url_prefix='/api')

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)