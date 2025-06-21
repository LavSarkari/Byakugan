import google.generativeai as genai
import os
import json
import time
import sys
import requests
from typing import List, Dict, Any

# Get API keys from environment variables
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GORK_API_KEY = os.environ.get('GORK_API_KEY')

def init_gemini():
    """
    Initialize Gemini API with the API key from environment variables
    """
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not configured in environment variables")
        return None
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        return model
    except Exception as e:
        print(f"❌ Failed to initialize Gemini: {e}")
        return None

def analyze_with_gork(subdomain: str) -> Dict[str, Any]:
    """
    Analyze subdomain using Gork AI API
    
    Args:
        subdomain (str): The subdomain to analyze
        
    Returns:
        dict: Analysis results or None if failed
    """
    if not GORK_API_KEY:
        print("    ⚠️  GORK_API_KEY not configured")
        return None
    
    try:
        # Ensure proper URL format
        if subdomain.startswith(('http://', 'https://')):
            target_url = subdomain
        else:
            target_url = f"https://{subdomain}"
        
        # Use Gork AI API
        url = "https://api.gork.ai/v1/analyze"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GORK_API_KEY}"
        }
        
        data = {
            "url": target_url,
            "analysis_type": "security"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        
        # Convert Gork AI response to our format
        if result and 'analysis' in result:
            analysis = result['analysis']
            
            # Extract risk level from Gork's scoring
            risk_score = analysis.get('risk_score', 0)
            risk_level = 'high' if risk_score > 7 else 'medium' if risk_score > 4 else 'low'
            
            return {
                'tech_stack': analysis.get('technologies', []),
                'likely_issues': analysis.get('vulnerabilities', []),
                'risk_level': risk_level,
                'bug_bounty_potential': risk_score > 5,
                'summary': analysis.get('summary', 'Analyzed by Gork AI'),
                'source': 'gork_ai'
            }
    except Exception as e:
        print(f"    ⚠️  Gork AI failed: {e}")
    
    return None

def analyze_with_openai(subdomain: str) -> Dict[str, Any]:
    """
    Analyze subdomain using OpenAI API as fallback
    
    Args:
        subdomain (str): The subdomain to analyze
        
    Returns:
        dict: Analysis results or None if failed
    """
    if not OPENAI_API_KEY:
        return None
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Analyze this subdomain: https://{subdomain} — Return JSON with:
  - tech_stack: List of technologies detected
  - risk_level: "high", "medium", or "low"
  - bug_bounty_potential: true or false
  - summary: One-line security assessment

Respond only with valid JSON, no additional text."""
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a cybersecurity expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        # Clean up response if it has markdown formatting
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        
        analysis = json.loads(content)
        
        # Add missing fields with defaults
        analysis['likely_issues'] = analysis.get('likely_issues', [])
        analysis['source'] = 'openai'
        
        return analysis
        
    except Exception as e:
        print(f"    ⚠️  OpenAI failed: {e}")
    
    return None

def run_ai_analysis(live_subdomains: List[str], domain: str) -> None:
    """
    Run hybrid AI analysis on live subdomains with fallback chain
    
    Args:
        live_subdomains (List[str]): List of live subdomains to analyze
        domain (str): The target domain
    """
    if not live_subdomains:
        print("No live subdomains to analyze.")
        return
    
    print(f"\n🧠 Running hybrid AI analysis on {len(live_subdomains)} live subdomains...")
    print("   🔄 Using Gork AI → OpenAI (fallback) → skip")
    
    analysis_results = []
    high_risk_subdomains = []
    
    # Analyze each subdomain
    for i, subdomain in enumerate(live_subdomains, 1):
        print(f"  [{i}/{len(live_subdomains)}] Analyzing {subdomain}...")
        
        # Try gork first (free)
        analysis = analyze_with_gork(subdomain)
        
        # If gork fails, try OpenAI
        if not analysis:
            analysis = analyze_with_openai(subdomain)
        
        # If both fail, create unscored entry
        if not analysis:
            analysis = {
                'subdomain': subdomain,
                'tech_stack': [],
                'likely_issues': [],
                'risk_level': 'low',
                'bug_bounty_potential': False,
                'summary': 'Analysis failed - manual review needed',
                'source': 'unscored'
            }
            print(f"    ❌ All analyzers failed")
        else:
            # Add subdomain to the analysis
            analysis['subdomain'] = subdomain
            
            # Validate required fields
            required_fields = ['tech_stack', 'likely_issues', 'risk_level', 'bug_bounty_potential', 'summary']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = [] if field in ['tech_stack', 'likely_issues'] else 'low' if field == 'risk_level' else False if field == 'bug_bounty_potential' else 'No analysis available'
            
            # Track high-risk subdomains
            if analysis.get('risk_level') == 'high':
                high_risk_subdomains.append(analysis)
            
            source = analysis.get('source', 'unknown')
            print(f"    ✅ {analysis.get('risk_level', 'unknown').upper()} risk ({source})")
        
        analysis_results.append(analysis)
        
        # Rate limiting - be nice to the APIs
        time.sleep(1)
    
    # Save results to file
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    
    analysis_file = os.path.join(output_dir, "analysis.json")
    with open(analysis_file, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\n📊 Hybrid AI Analysis Results:")
    print(f"   • Analyzed {len(analysis_results)} subdomains")
    print(f"   • Found {len(high_risk_subdomains)} high-risk targets")
    print(f"   • Results saved to: {analysis_file}")
    
    # Show only high-risk subdomains
    if high_risk_subdomains:
        print(f"\n🔥 High-Risk Targets:")
        for i, analysis in enumerate(high_risk_subdomains, 1):
            print(f"   {i}. {analysis['subdomain']}")
            print(f"      Summary: {analysis.get('summary', 'No summary')}")
            print(f"      Source: {analysis.get('source', 'unknown')}")
            print(f"      Bounty Potential: {'💰' if analysis.get('bug_bounty_potential') else '❌'}")
            print()
    else:
        print("\n✅ No high-risk targets found") 