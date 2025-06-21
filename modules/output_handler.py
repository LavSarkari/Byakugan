import os

def save_recon_results(domain: str, subdomains: list, live_subdomains: list) -> None:
    """
    Save reconnaissance results to organized output files.
    
    Args:
        domain (str): The target domain
        subdomains (list): List of all discovered subdomains
        live_subdomains (list): List of live subdomains
    """
    # Create output directory
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save all subdomains
    subdomains_file = os.path.join(output_dir, "subdomains.txt")
    with open(subdomains_file, 'w') as f:
        for subdomain in subdomains:
            f.write(f"{subdomain}\n")
    
    # Save live subdomains
    live_file = os.path.join(output_dir, "live.txt")
    with open(live_file, 'w') as f:
        for subdomain in live_subdomains:
            f.write(f"{subdomain}\n")
    
    print(f"\n📁 Results saved to: {output_dir}/")
    print(f"   • subdomains.txt ({len(subdomains)} entries)")
    print(f"   • live.txt ({len(live_subdomains)} entries)") 