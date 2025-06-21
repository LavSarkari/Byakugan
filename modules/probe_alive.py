import subprocess
import os
import tempfile

def run_httpx_probe(subdomains: list) -> list:
    """
    Probe subdomains using httpx to find live ones.
    
    Args:
        subdomains (list): List of subdomains to probe
        
    Returns:
        list: List of live subdomains
    """
    if not subdomains:
        return []
    
    # High-value keywords to check for
    high_value_keywords = ["admin", "login", "staging", "test", "dev"]
    
    # Create temporary file
    temp_file = "subdomains.txt"
    
    try:
        # Write subdomains to temporary file
        with open(temp_file, 'w') as f:
            for subdomain in subdomains:
                f.write(f"{subdomain}\n")
        
        # Run httpx
        result = subprocess.run(
            ['httpx', '-silent', '-l', temp_file],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Split output into lines and filter out empty lines
        live_subdomains = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        # Check for high-value targets
        print("\n🔍 Checking for high-value targets...")
        for subdomain in live_subdomains:
            for keyword in high_value_keywords:
                if keyword in subdomain.lower():
                    print(f"\033[91m🚨 High-value target found:\033[0m \033[1m{subdomain}\033[0m")
                    break
        
        return live_subdomains
        
    except subprocess.CalledProcessError as e:
        print(f"Error running httpx: {e}")
        return []
    except FileNotFoundError:
        print("Error: httpx not found. Please install httpx first.")
        return []
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file) 