import os
import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import re

# =======================
# Configuration
# =======================
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =======================
# Utils
# =======================
def run_cmd(cmd_list, timeout=30):
    try:
        return subprocess.check_output(
            cmd_list,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout
        )
    except Exception as e:
        return f"[ERROR] {e}"

# =======================
# 1) Scrape lab questions
# =======================
def extract_questions(lab_url):
    res = requests.get(lab_url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    questions = []
    for tag in soup.find_all(["li", "p", "h3", "h4"]):
        text = tag.get_text(strip=True)
        if "?" in text:
            questions.append(text)

    # تنظيف
    cleaned = []
    for q in questions:
        if len(q) > 10 and len(q) < 200:
            cleaned.append(q)

    return cleaned

# =======================
# 2) Nmap Recon
# =======================
def run_nmap(target):
    return run_cmd(["nmap", "-sV", "--top-ports", "1000", target])

def parse_open_ports(nmap_out):
    ports = []
    for line in nmap_out.splitlines():
        if "/tcp" in line and "open" in line:
            ports.append(line.split()[0])
    return ports

def service_on_port(nmap_out, port):
    for line in nmap_out.splitlines():
        if line.startswith(f"{port}/tcp"):
            return line
    return "Unknown"

# =======================
# 3) FTP Anonymous Check
# =======================
def ftp_anonymous_enabled(target):
    try:
        cmd = (
            f'echo -e "USER anonymous\\nPASS anonymous\\nQUIT" | '
            f'ftp -n {target}'
        )
        out = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
        return "230" in out, out
    except:
        return False, ""

def ftp_list_files(target):
    cmd = (
        f'echo -e "USER anonymous\\nPASS anonymous\\nls\\nQUIT" | '
        f'ftp -n {target}'
    )
    return subprocess.check_output(cmd, shell=True, text=True)

# =======================
# 4) Hydra Output Parser
# =======================
def parse_hydra_output(path):
    creds = []
    if not os.path.exists(path):
        return creds

    with open(path, "r", errors="ignore") as f:
        for line in f:
            if "login:" in line and "password:" in line:
                user = re.search(r"login:\s*(\S+)", line)
                pwd = re.search(r"password:\s*(\S+)", line)
                if user and pwd:
                    creds.append({
                        "user": user.group(1),
                        "password": pwd.group(1)
                    })
    return creds

# =======================
# 5) Answer Engine
# =======================
def answer_questions(questions, nmap_out, ftp_info, hydra_creds):
    answers = []
    open_ports = parse_open_ports(nmap_out)

    for idx, q in enumerate(questions, 1):
        ql = q.lower()
        ans = "Not found"

        # عدد البورتات
        if "how many" in ql and "port" in ql:
            ans = str(len(open_ports))

        # سيرفس على بورت
        elif "service" in ql and "port" in ql:
            p = re.search(r"port\s+(\d+)", ql)
            if p:
                ans = service_on_port(nmap_out, p.group(1))

        # FTP Anonymous
        elif "ftp" in ql and "anonymous" in ql:
            ans = "Enabled" if ftp_info["anon"] else "Disabled"

        # Password
        elif "password" in ql:
            if hydra_creds:
                ans = hydra_creds[0]["password"]
            else:
                ans = "Not found"

        answers.append((idx, q, ans))

    return answers

# =======================
# MAIN
# =======================
def main():
    print("=== GHENA CTF LAB SOLVER ===\n")

    lab_url = input("[?] Lab URL: ").strip()
    target = input("[?] Target IP: ").strip()

    print("\n[*] Extracting lab questions...")
    questions = extract_questions(lab_url)

    print("[*] Running Nmap...")
    nmap_out = run_nmap(target)

    print("[*] Checking FTP anonymous access...")
    anon, ftp_raw = ftp_anonymous_enabled(target)
    ftp_files = ftp_list_files(target) if anon else ""

    print("\n[?] Enter Hydra command you used (for reference only):")
    hydra_cmd = input("> ")

    print("[?] Enter Hydra output file path (or leave empty):")
    hydra_path = input("> ").strip()

    hydra_creds = parse_hydra_output(hydra_path) if hydra_path else []

    ftp_info = {
        "anon": anon,
        "files": ftp_files
    }

    answers = answer_questions(
        questions,
        nmap_out,
        ftp_info,
        hydra_creds
    )

    # =======================
    # OUTPUT
    # =======================
    print("\n==============================")
    print("LAB ANSWERS")
    print("==============================\n")

    for idx, q, ans in answers:
        print(f"Question {idx}:")
        print(q)
        print(f"→ Answer: {ans}\n")

    if anon:
        print("[FTP Anonymous Files]")
        print(ftp_files)

    print("==============================")

if __name__ == "__main__":
    main()
