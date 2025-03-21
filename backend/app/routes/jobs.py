from flask import Blueprint, request, jsonify
from ..models import Job, Application, db
from ..services.file_processing import extract_text_from_file, save_resume_to_s3
from ..services.ai_processing import generate_ai_summary
import uuid
from datetime import datetime

bp = Blueprint('jobs', __name__)

@bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job_title = data.get('title')
    department = data.get('department')
    location = data.get('location')
    job_desc = data.get('description')
    skills = data.get('skills')
    salary_min = data.get('salary_min')
    salary_max = data.get('salary_max')
    created_by = data.get('created_by')

    if not job_title or not job_desc:
        return jsonify({"error": "Job title and description are required!"}), 400

    job_id = str(uuid.uuid4())
    new_job = Job(
        id=job_id,
        title=job_title,
        department=department,
        location=location,
        description=job_desc,
        skills=skills,
        salary_min=salary_min,
        salary_max=salary_max,
        created_by=created_by,
        created_at=datetime.utcnow()
    )
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Job posted successfully!", "job_id": job_id}), 201

@bp.route('/jobs/<job_id>/apply', methods=['POST'])
def apply_for_job(job_id):
    file = request.files.get('resume')
    candidate_email = request.form.get('email')

    if not file or not candidate_email:
        return jsonify({"error": "Resume and email are required!"}), 400

    resume_text = extract_text_from_file(file)
    if not resume_text:
        return jsonify({"error": "Failed to extract text from resume!"}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found!"}), 404

    ai_summary, match_score = generate_ai_summary(resume_text, job.description)
    file_url = save_resume_to_s3(file, job_id, candidate_email)
    if not file_url:
        return jsonify({"error": "Failed to save resume!"}), 500

    application_id = str(uuid.uuid4())
    new_application = Application(
        id=application_id,
        job_id=job_id,
        candidate_id=candidate_email,
        resume_text=resume_text,
        match_score=match_score,
        applied_at=datetime.utcnow(),
        resume_url=file_url
    )
    db.session.add(new_application)
    db.session.commit()

    return jsonify({"message": "Application submitted successfully!", "match_score": match_score}), 201