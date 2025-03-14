from flask import Blueprint, request, jsonify
from extensions import bcrypt
from supabase import create_client, Client
import os

auth_bp = Blueprint('auth', __name__)

# Initialize Supabase client
supabase: Client = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_KEY'))

# User Signup
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing fields"}), 400

    # Check if username already exists
    user = supabase.table('users').select('*').eq('username', data['username']).execute()
    if user.data:
        return jsonify({"error": "Username already exists"}), 400

    # Hash password and create new user
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = {
        "username": data['username'],
        "password": hashed_password
    }

    # Insert into Supabase
    supabase.table('users').insert(new_user).execute()
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing fields"}), 400

    # Fetch user from Supabase
    user = supabase.table('users').select('*').eq('username', data['username']).execute()
    if user.data and bcrypt.check_password_hash(user.data[0]['password'], data['password']):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401