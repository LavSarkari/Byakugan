import google.generativeai as genai
import os
import sys

# Add parent directory to path to import secrets
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from secrets import GEMINI_API_KEY
except ImportError:
    print("❌ Error: secrets.py not found. Please create it with your GEMINI_API_KEY.")
    GEMINI_API_KEY = None

def analyze_subdomain(domain: str, content: str) -> dict:
    """
    Analyze a subdomain using Gemini AI for security risks and bounty worthiness.
    
    Args:
        domain (str): The subdomain to analyze
        content (str): HTTP content/response from the subdomain
        
    Returns:
        dict: Analysis results with risk summary, exploit hint, and bounty tag
    """
    if not GEMINI_API_KEY:
        return {
            "subdomain": domain,
            "risk_summary": "API key not configured",
            "exploit_hint": "Configure GEMINI_API_KEY in secrets.py",
            "bounty_tag": "🧪"
        }
    
    if not content or content.strip() == "":
        return {
            "subdomain": domain,
            "risk_summary": "No content available for analysis",
            "exploit_hint": "Subdomain may be down or returning empty response",
            "bounty_tag": "🧪"
        }
    
    try:
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Create the prompt
        prompt = f"""Given this subdomain: {domain}, and HTTP content: {content[:2000]}..., suggest:
1. Potential risk or vulnerability
2. How to exploit it
3. Tag the bounty worthiness as one of: 🧪 (Low), 🔐 (Medium), 💰 (High)

Please respond in a structured format:
Risk: [your risk assessment]
Exploit: [how to exploit]
Bounty: [bounty tag]"""
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Parse the response
        response_text = response.text
        
        # Extract components (simple parsing)
        risk_summary = "Analysis completed"
        exploit_hint = "Review the response for details"
        bounty_tag = "🧪"  # Default to low
        
        # Try to parse structured response
        if "Risk:" in response_text:
            risk_parts = response_text.split("Risk:")
            if len(risk_parts) > 1:
                risk_exploit = risk_parts[1].split("Exploit:")
                if len(risk_exploit) > 1:
                    risk_summary = risk_exploit[0].strip()
                    exploit_bounty = risk_exploit[1].split("Bounty:")
                    if len(exploit_bounty) > 1:
                        exploit_hint = exploit_bounty[0].strip()
                        bounty_part = exploit_bounty[1].strip()
                        if "💰" in bounty_part:
                            bounty_tag = "💰"
                        elif "🔐" in bounty_part:
                            bounty_tag = "🔐"
                        elif "🧪" in bounty_part:
                            bounty_tag = "🧪"
        
        return {
            "subdomain": domain,
            "risk_summary": risk_summary,
            "exploit_hint": exploit_hint,
            "bounty_tag": bounty_tag
        }
        
    except Exception as e:
        return {
            "subdomain": domain,
            "risk_summary": f"AI analysis failed: {str(e)}",
            "exploit_hint": "Manual review recommended",
            "bounty_tag": "🧪"
        } 