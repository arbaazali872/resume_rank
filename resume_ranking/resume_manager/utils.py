# resumes/utils.py
from .models import JobDescription, Resume, RankingResult

def rank_resumes(session_id):
    jd = JobDescription.objects.get(session_id=session_id)
    resumes = Resume.objects.filter(session_id=session_id)
    
    ranked_resumes = []
    for resume in resumes:
        score = calculate_similarity(jd.description, resume.file.path)
        ranked_resumes.append((resume, score))
    
    ranked_resumes.sort(key=lambda x: x[1], reverse=True)
    
    for resume, score in ranked_resumes:
        RankingResult.objects.create(session_id=session_id, resume=resume, score=score)

def calculate_similarity(jd_text, resume_path):
    with open(resume_path, 'r') as f:
        resume_text = f.read()
    score = len(set(jd_text.split()) & set(resume_text.split()))
    return score
