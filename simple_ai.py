import json
import random
from typing import Dict, Any

class SimpleAI:
    """A simple AI model that provides free resume analysis without external dependencies"""
    
    def __init__(self):
        self.name = "SimpleAI"
    
    def analyze_resume(self, resume_text: str, job_requirements: Dict[str, Any], role: str) -> tuple[bool, str]:
        """
        Analyze resume and return selection decision with feedback
        """
        # Simple keyword-based analysis
        keywords = {
            "python": 3,
            "java": 2,
            "javascript": 2,
            "react": 2,
            "node": 2,
            "sql": 2,
            "aws": 2,
            "docker": 2,
            "kubernetes": 2,
            "machine learning": 3,
            "ai": 2,
            "data": 2,
            "experience": 1,
            "project": 1,
            "education": 1,
            "bachelor": 1,
            "master": 2,
            "phd": 3,
            "certification": 1,
            "github": 1,
            "portfolio": 1
        }
        
        resume_lower = resume_text.lower()
        score = 0
        
        # Calculate score based on keywords
        for keyword, weight in keywords.items():
            if keyword in resume_lower:
                score += weight
        
        # Additional scoring based on content length and structure
        if len(resume_text) > 500:
            score += 2
        if "experience" in resume_lower:
            score += 1
        if "education" in resume_lower:
            score += 1
        if "skills" in resume_lower:
            score += 1
            
        # Random factor for variety (but still deterministic)
        random.seed(hash(resume_text) % 1000)
        score += random.randint(-2, 2)
        
        # Decision threshold
        is_selected = score >= 8
        
        # Generate feedback
        if is_selected:
            feedback = f"""
🎉 **Congratulations! You've been selected for the {role} position!**

**Analysis Score: {score}/15**

**Strengths:**
✅ Strong technical background
✅ Relevant experience and skills
✅ Good educational foundation
✅ Professional presentation

**Next Steps:**
1. We'll schedule an interview within 24 hours
2. Prepare for technical discussion
3. Bring examples of your work

**Interview Preparation Tips:**
- Review the job requirements
- Prepare to discuss your projects
- Have questions ready about the role
- Be ready for technical questions

We're excited to have you join our team!
            """
        else:
            feedback = f"""
📝 **Thank you for your application for the {role} position**

**Analysis Score: {score}/15**

**Areas for Improvement:**
🔸 Consider adding more relevant technical skills
🔸 Include specific project examples
🔸 Highlight quantifiable achievements
🔸 Add certifications if applicable

**Suggestions:**
- Update your resume with recent projects
- Include GitHub portfolio if available
- Add relevant certifications
- Emphasize technical skills

**Keep Learning:**
- Continue building projects
- Stay updated with industry trends
- Consider additional certifications
- Network with professionals in the field

We encourage you to apply again in the future!
            """
        
        return is_selected, feedback
    
    def generate_email(self, is_selected: bool, candidate_email: str, company_name: str, role: str) -> str:
        """Generate email content based on selection decision"""
        
        if is_selected:
            subject = f"Congratulations! You've been selected for {role} position"
            body = f"""
Dear Candidate,

We are pleased to inform you that you have been selected for the {role} position at {company_name}!

Your application stood out among many qualified candidates, and we are excited about the possibility of you joining our team.

**Next Steps:**
- We will contact you within 24 hours to schedule an interview
- Please prepare for a technical discussion
- Bring examples of your work and projects
- Have questions ready about the role and company

**Interview Details:**
- Format: Technical interview via Zoom
- Duration: Approximately 45-60 minutes
- Topics: Technical skills, project discussion, role-specific questions

We look forward to meeting you!

Best regards,
The AI Recruiting Team
{company_name}
            """
        else:
            subject = f"Application Update - {role} Position"
            body = f"""
Dear Candidate,

Thank you for your interest in the {role} position at {company_name}.

After careful review of your application, we regret to inform you that we have decided to move forward with other candidates whose qualifications more closely match our current needs.

**Feedback:**
- Your application was reviewed thoroughly
- We appreciate the time you invested in applying
- We encourage you to apply for future opportunities

**Suggestions for Future Applications:**
- Continue developing relevant technical skills
- Include specific project examples in your resume
- Consider obtaining relevant certifications
- Stay updated with industry trends

We wish you the best in your job search and future endeavors.

Best regards,
The AI Recruiting Team
{company_name}
            """
        
        return subject, body 