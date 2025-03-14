from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os

job_bp = Blueprint("job_bp", __name__)

# Initialize Supabase client
supabase: Client = create_client(os.environ.get('https://mmwaubrgkbcjhazsjjpm.supabase.co'), os.environ.get('SUPABASE_KEY'))

# Fetch all jobs
@job_bp.route("/jobs", methods=["GET"])
def get_jobs():
    category = request.args.get("category")
    location = request.args.get("location")
    company = request.args.get("company")
    sort_by = request.args.get("sort_by", "date_posted")

    query = supabase.table('jobs').select('*')

    # Filtering
    if category:
        query = query.ilike('category', f"%{category}%")
    if location:
        query = query.ilike('location', f"%{location}%")
    if company:
        query = query.ilike('company', f"%{company}%")

    # Sorting
    if sort_by == "company":
        query = query.order('company', ascending=True)
    elif sort_by == "title":
        query = query.order('title', ascending=True)
    else:
        query = query.order('date_posted', ascending=False)

    jobs = query.execute()
    return jsonify(jobs.data)

# Add a new job
@job_bp.route("/jobs", methods=["POST"])
def add_job():
    data = request.get_json()
    if not data or "title" not in data or "company" not in data or "location" not in data or "category" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_job = {
        "title": data["title"],
        "company": data["company"],
        "location": data["location"],
        "category": data["category"]
    }

    # Insert into Supabase
    supabase.table('jobs').insert(new_job).execute()
    return jsonify({"message": "Job added successfully"}), 201

# Delete a job
@job_bp.route("/jobs/<string:job_id>", methods=["DELETE"])
def delete_job(job_id):
    supabase.table('jobs').delete().eq('id', job_id).execute()
    return jsonify({"message": "Job deleted successfully"}), 200