import subprocess
import requests
import json

def run_subdomain_enum(domain: str) -> list:
    """
    Run multiple subdomain enumeration tools and combine results.
    
    Args:
        domain (str): The domain to enumerate subdomains for
        
    Returns:
        list: List of discovered subdomains
    """
    all_subdomains = set()
    tool_results = {}
    
    # 1. Subfinder
    try:
        result = subprocess.run(
            ['subfinder', '-d', domain, '-silent'],
            capture_output=True,
            text=True,
            check=True
        )
        subfinder_domains = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        all_subdomains.update(subfinder_domains)
        tool_results['subfinder'] = len(subfinder_domains)
        print(f"[+] subfinder found {len(subfinder_domains)}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] subfinder not found or failed")
        tool_results['subfinder'] = 0
    
    # 2. Assetfinder
    try:
        result = subprocess.run(
            ['assetfinder', domain],
            capture_output=True,
            text=True,
            check=True
        )
        assetfinder_domains = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        all_subdomains.update(assetfinder_domains)
        tool_results['assetfinder'] = len(assetfinder_domains)
        print(f"[+] assetfinder found {len(assetfinder_domains)}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] assetfinder not found or failed")
        tool_results['assetfinder'] = 0
    
    # 3. Amass (passive mode)
    try:
        result = subprocess.run(
            ['amass', 'enum', '-passive', '-d', domain],
            capture_output=True,
            text=True,
            check=True
        )
        amass_domains = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        all_subdomains.update(amass_domains)
        tool_results['amass'] = len(amass_domains)
        print(f"[+] amass found {len(amass_domains)}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] amass not found or failed")
        tool_results['amass'] = 0
    
    # 4. crt.sh
    try:
        url = f"https://crt.sh/?q={domain}&output=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        crt_data = response.json()
        crt_domains = set()
        
        for entry in crt_data:
            if 'name_value' in entry:
                # Split by newlines in case multiple domains are in one entry
                domains = entry['name_value'].split('\n')
                for d in domains:
                    d = d.strip()
                    if d and domain in d:  # Ensure it's related to our target domain
                        crt_domains.add(d)
        
        all_subdomains.update(crt_domains)
        tool_results['crt.sh'] = len(crt_domains)
        print(f"[+] crt.sh found {len(crt_domains)}")
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"[-] crt.sh failed: {e}")
        tool_results['crt.sh'] = 0
    
    # Return sorted list of unique subdomains
    final_subdomains = sorted(list(all_subdomains))
    
    print(f"\n[+] Total unique subdomains found: {len(final_subdomains)}")
    print(f"[+] Combined results from {sum(1 for count in tool_results.values() if count > 0)} tools")
    
    return final_subdomains 