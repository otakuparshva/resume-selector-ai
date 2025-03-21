import ollama
import re

def generate_ai_summary(resume_text, job_desc):
    try:
        if not resume_text or not job_desc:
            return "Error: Missing resume text or job description", 0

        prompt = f"""
        ## Resume Analysis Task
        
        ### Resume Text:
        {resume_text[:3000]}  # Limiting to first 3000 chars for performance
        
        ### Job Description:
        {job_desc[:1000]}  # Limiting to first 1000 chars for performance
        
        ### Instructions:
        1. Analyze the candidate's skills, experience, and qualifications
        2. Compare them against the job requirements
        3. Provide a brief summary of the candidate (2-3 sentences)
        4. List the top 3 matching skills
        5. List the top 3 missing skills or gaps
        6. Give a numerical match score (0-100)
        """
        
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_response = response["message"]["content"]
        match_score = extract_match_score(ai_response)
        
        return ai_response, match_score
        
    except Exception as e:
        return f"Error generating AI summary: {str(e)}", 0

def extract_match_score(ai_response):
    try:
        score_match = re.search(r"\b(\d{1,3})\b", ai_response)
        if score_match:
            return int(score_match.group(1))
        return 0
    except Exception as e:
        return 0