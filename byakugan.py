import argparse
from pathlib import Path
from dotenv import load_dotenv
from modules.subdomain_enum import run_subdomain_enum
from modules.probe_alive import run_httpx_probe
from modules.output_handler import save_recon_results
from modules.screenshot import capture_screenshots
from modules.ai_analysis import run_ai_analysis
from setup import check_and_install_tools

# Load environment variables from .env file
load_dotenv()

def check_existing_output(domain: str) -> dict:
    """
    Check what output files already exist for the domain.
    
    Args:
        domain (str): The target domain
        
    Returns:
        dict: Status of existing output files
    """
    output_dir = Path(f"output/{domain}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    status = {
        'subdomains': output_dir / "subdomains.txt",
        'live': output_dir / "live.txt",
        'analysis': output_dir / "analysis.json",
        'screenshots': output_dir / "screenshots"
    }
    
    # Check if files exist and have content
    existing = {}
    for key, path in status.items():
        if key == 'screenshots':
            # Check if screenshots directory exists and has image files
            existing[key] = path.exists() and any(path.glob("*.png"))
        else:
            # Check if file exists and has content
            existing[key] = path.exists() and path.stat().st_size > 0
    
    return existing

def load_existing_data(domain: str, file_type: str) -> list:
    """
    Load existing data from output files.
    
    Args:
        domain (str): The target domain
        file_type (str): Type of data to load ('subdomains' or 'live')
        
    Returns:
        list: Loaded data
    """
    file_path = Path(f"output/{domain}/{file_type}.txt")
    if file_path.exists():
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def run_recon(domain):
    """
    Run reconnaissance on the specified domain with resume capability.
    """
    print(f"Running recon on: {domain}")
    
    # Check existing output
    existing = check_existing_output(domain)
    
    # Subdomain enumeration
    if existing['subdomains']:
        print(f"[!] Found previous subdomain scan for {domain}, skipping...")
        subdomains = load_existing_data(domain, 'subdomains')
        print(f"Loaded {len(subdomains)} existing subdomains")
    else:
        print("Starting subdomain enumeration...")
        subdomains = run_subdomain_enum(domain)
        print(f"Found {len(subdomains)} subdomains")
    
    # Print all subdomains found
    print("\n🔍 Subdomains found:")
    print("─" * 50)
    for subdomain in subdomains:
        print(f"  • {subdomain}")
    
    # Live subdomain probing
    if existing['live']:
        print(f"[!] Found previous live subdomain scan for {domain}, skipping...")
        live_subdomains = load_existing_data(domain, 'live')
        print(f"Loaded {len(live_subdomains)} existing live subdomains")
    else:
        print("Starting live subdomain probing...")
        live_subdomains = run_httpx_probe(subdomains)
        print(f"Found {len(live_subdomains)} live subdomains")
    
    # Print live subdomains
    print("\n✅ Live subdomains:")
    print("─" * 50)
    for subdomain in live_subdomains:
        print(f"  • {subdomain}")
    
    # Save results to files (only if we have new data)
    if not existing['subdomains'] or not existing['live']:
        save_recon_results(domain, subdomains, live_subdomains)
    
    # Screenshot capture
    if existing['screenshots']:
        print(f"[!] Found previous screenshots for {domain}, skipping...")
    else:
        print("Starting screenshot capture...")
        capture_screenshots(domain, live_subdomains)
    
    # AI analysis
    if existing['analysis']:
        print(f"[!] Found previous AI analysis for {domain}, skipping...")
    else:
        print("Starting AI analysis...")
        run_ai_analysis(live_subdomains, domain)

def main():
    """
    Main function to parse arguments and run the tool.
    """
    banner = r"""
    ____              __                         
   / __ )__  ______ _/ /____  ______ _____ _____ 
  / __  / / / / __ `/ //_/ / / / __ `/ __ `/ __ \
 / /_/ / /_/ / /_/ / ,< / /_/ / /_/ / /_/ / / / /
/_____/\__, /\__,_/_/|_|\__,_/\__, /\__,_/_/ /_/ 
      /____/                 /____/ — 0.1     

   👁️  The All-Seeing Recon AI Tool for Hackers 👁️
    """
    print(banner)

    parser = argparse.ArgumentParser(description="Byakugan - The All-Seeing Recon AI Tool")
    parser.add_argument("-d", "--domain", required=True, help="Domain to run recon on")
    
    args = parser.parse_args()
    
    # Check and install required tools before starting recon
    print("Checking required tools...")
    check_and_install_tools()
    print()
    
    run_recon(args.domain)

if __name__ == "__main__":
    main() 