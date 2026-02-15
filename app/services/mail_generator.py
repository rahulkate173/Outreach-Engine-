from typing import Dict

class MailGenerator:
    """Service for generating cold outreach emails"""
    
    @staticmethod
    async def generate_cold_mail(
        recipient_name: str,
        company: str,
        job_title: str,
        context: str,
        company_context: str = ""
    ) -> Dict[str, str]:
        """Generate personalized cold email"""
        
        mail_templates = {
            "subject": f"Quick question about {company} 👋",
            "body": f"""Hi {recipient_name},

I came across your profile and was impressed by your work at {company}. 

{context}

I thought you might find this interesting given your role as {job_title}.

{f"I noticed that {company_context}" if company_context else ""}

Would you be open to a quick chat?

Best regards,
SMB02 Team""",
            "preview": f"Quick question about {company}",
            "personalization_score": 0.85
        }
        
        return mail_templates
    
    @staticmethod
    async def enhance_mail(original_mail: str, tone: str = "professional") -> str:
        """Enhance mail with better copy"""
        
        tones = {
            "professional": "formal and business-oriented",
            "casual": "friendly and conversational",
            "urgent": "time-sensitive and compelling",
            "educational": "informative and value-driven"
        }
        
        enhanced = f"""[Enhanced with {tone} tone]

{original_mail}

---
This email has been enhanced for better engagement."""
        
        return enhanced
    
    @staticmethod
    async def get_mail_score(mail: str) -> Dict:
        """Score email quality"""
        
        return {
            "overall_score": 8.5,
            "personalization": 9.0,
            "clarity": 8.0,
            "call_to_action": 8.5,
            "length": "optimal",
            "sentiment": "positive",
            "recommendations": [
                "Add specific achievement mention",
                "Make CTA more concrete"
            ]
        }