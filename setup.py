import shutil
import subprocess

def check_and_install_tools() -> None:
    """
    Check if required tools are installed and install them if missing.
    """
    tools = {
        'subfinder': {
            'install_cmd': 'go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
            'manual_install': False
        },
        'httpx': {
            'install_cmd': 'go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest',
            'manual_install': False
        },
        'assetfinder': {
            'install_cmd': 'go install -v github.com/tomnomnom/assetfinder@latest',
            'manual_install': False
        },
        'amass': {
            'install_cmd': 'go install -v github.com/owasp-amass/amass/v4/...@master',
            'manual_install': False
        },
        'gowitness': {
            'install_cmd': None,
            'manual_install': True,
            'manual_url': 'https://github.com/sensepost/gowitness'
        }
    }
    
    for tool, config in tools.items():
        if shutil.which(tool):
            print(f"✅ {tool} is installed")
        else:
            print(f"❌ {tool} not found")
            
            if config['manual_install']:
                print(f"   Install manually from {config['manual_url']}")
            else:
                print(f"   Installing {tool}...")
                try:
                    subprocess.run(config['install_cmd'].split(), check=True)
                    print(f"   ✅ {tool} installed successfully")
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Failed to install {tool}: {e}")
                except FileNotFoundError:
                    print(f"   ❌ Go not found. Please install Go first to install {tool}") 