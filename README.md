<h1 align="center">
  🥷 Byakugan
</h1>
<p align="center">
  <i>The hacker’s all-seeing eye — a dark-themed, AI-powered recon tool</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge" />
</p>

---

## 🌌 What is Byakugan?

**Byakugan** is a dark-themed, AI-augmented recon framework for ethical hackers and bug bounty hunters.

It automates:
- 🔍 Subdomain enumeration
- 🌐 Live host discovery
- 📸 Screenshot capture
- 🧠 AI-driven risk summaries, exploit suggestions, and bounty tagging

Inspired by the legendary *dojutsu*, Byakugan gives hackers **clairvoyant recon power**.

---

## ⚙️ Features

- 🔗 Subdomain enum via `subfinder`, `amass`, `crt.sh`, and more
- ☠️ Live probing with `httpx`
- 📷 Screenshots with `gowitness`
- 🤖 AI analysis using **Gemini API**, optional fallback to GPT
- 📁 Organized outputs: `subdomains.txt`, `live.txt`, `screenshots/`, `analysis.json`
- 🔄 Continues from previous scans — smart caching
- 💻 CLI-first, optional FastAPI + Tailwind web dashboard
- 🧪 Designed for real bug bounty workflows

---

## 📦 Install

```bash
# Clone the repo
git clone https://github.com/lavsarkari/byakugan
cd byakugan

# Create and activate virtual environment
python3 -m venv Byakugan
source Byakugan/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python byakugan.py -d example.com
```

Options coming soon:

```bash
--resume           Continue if scan already exists
--no-ai            Skip AI analysis
--dashboard        Launch web UI (WIP)
```

---

## 🔐 API Keys

Create `secrets.py` like this:

```python
OPENAI_API_KEY = "sk-..."
GEMINI_API_KEY = "AIzaSy..."
```

---

## 📁 Output Structure

```
output/
└── example.com/
    ├── subdomains.txt
    ├── live.txt
    ├── screenshots/
    └── analysis.json
```

---

## 💀 Example Output

> “Scanning `nmap.com` with Byakugan…”

```shell
Found 8 subdomains
Found 8 live hosts
Captured 8 screenshots

📊 AI Analysis:
- 2 High-Risk Targets
- 3 Potential for Bounties
```

---

## 🧠 Powered By

* [subfinder](https://github.com/projectdiscovery/subfinder)
* [httpx](https://github.com/projectdiscovery/httpx)
* [gowitness](https://github.com/sensepost/gowitness)
* [Gemini API](https://ai.google.dev)
* [OpenAI GPT-3.5](https://platform.openai.com)

<br>

---
## 🛡️ Disclaimer

For educational and authorized testing purposes only. You are responsible for your actions. 