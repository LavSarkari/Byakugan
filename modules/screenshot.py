import subprocess
import os

def capture_screenshots(domain: str, live_subdomains: list) -> None:
    """
    Capture screenshots of live subdomains using gowitness.
    
    Args:
        domain (str): The target domain
        live_subdomains (list): List of live subdomains to screenshot
    """
    if not live_subdomains:
        print("No live subdomains to screenshot.")
        return
    
    # Create screenshots directory
    screenshots_dir = f"output/{domain}/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # Write live subdomains to file with http/https prefixes
    live_file = "live.txt"
    try:
        with open(live_file, 'w') as f:
            for subdomain in live_subdomains:
                # Ensure subdomain has http:// or https:// prefix
                if not subdomain.startswith(('http://', 'https://')):
                    subdomain = f"https://{subdomain}"
                f.write(f"{subdomain}\n")
        
        print(f"\n📸 Capturing screenshots of {len(live_subdomains)} live subdomains...")
        
        # Run gowitness with the correct command
        result = subprocess.run([
            'gowitness', 'scan', 'file', '-f', live_file, '-s', screenshots_dir
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Screenshots saved to {screenshots_dir}/")
        else:
            print(f"❌ Error capturing screenshots: {result.stderr}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running gowitness: {e}")
    except FileNotFoundError:
        print("❌ Error: gowitness not found. Please install gowitness first.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Clean up temporary file
        if os.path.exists(live_file):
            os.remove(live_file) 