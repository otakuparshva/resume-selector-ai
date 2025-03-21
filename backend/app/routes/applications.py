from flask import Blueprint, jsonify
from ..models import Application, db

bp = Blueprint('applications', __name__)

@bp.route('/applications/<job_id>', methods=['GET'])
def get_applications(job_id):
    applications = Application.query.filter_by(job_id=job_id).all()
    applications_data = [{
        "id": app.id,
        "candidate_id": app.candidate_id,
        "resume_text": app.resume_text,
        "match_score": app.match_score,
        "applied_at": app.applied_at
    } for app in applications]

    return jsonify(applications_data), 200