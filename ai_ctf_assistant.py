import google.generativeai as genai
import os
import subprocess
import sys
import time
import requests
from bs4 import BeautifulSoup

# --- [ إعدادات المحرك العصبي ] ---
API_KEY = "ضـع_مفـتاحك_هنـا" # تأكد من وضع المفتاح الصحيح هنا

BANNER = r"""
  ________  ___  ___  _______   ________   ________     
 |\   ____\|\  \|\  \|\  ___ \ |\   ___  \|\   __  \    
 \ \  \___|\ \  \\\  \ \   __/|\ \  \\ \  \ \  \|\  \   
  \ \  \  __\ \   __  \ \  \_|/_\ \  \\ \  \ \   __  \  
   \ \  \|\  \ \  \ \  \ \  \_|\ \ \  \\ \  \ \  \ \  \ 
    \ \_______\ \__\ \__\ \_______\ \__\\ \__\ \__\ \__\
     \|_______|\|__|\|__|\|_______|\|__| \|__|\|__|\|__|
           GHENA AI | REPAIRED & STABLE EDITION
"""

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

# --- [ وظائف جلب البيانات والتحليل ] ---

def scrape_lab_goals(url):
    print(f"{Colors.YELLOW}[*] GHENA is accessing Lab Intelligence...{Colors.ENDC}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.content, 'html.parser')
        tasks = [t.get_text() for t in soup.find_all(['h3', 'h4', 'p'])]
        return "\n".join(tasks[:20])
    except Exception as e:
        return f"Scraping Error: {e}"

def execute_smart_tools(target_ip):
    logs = ""
    # 1. Nmap
    print(f"{Colors.CYAN}[*] Step 1: Broad Reconnaissance (Nmap)...{Colors.ENDC}")
    try:
        nmap_cmd = f"nmap -sV --top-ports 1000 {target_ip}"
        nmap_out = subprocess.check_output(nmap_cmd, shell=True, text=True)
        logs += f"\n--- NMAP ---\n{nmap_out}"
    except: logs += "\n--- NMAP: Failed ---"

    # 2. Gobuster (تم إصلاح الفلاج -z ليتناسب مع نسختك)
    if "80" in logs or "443" in logs:
        print(f"{Colors.CYAN}[*] Step 2: Web Path Discovery (Gobuster)...{Colors.ENDC}")
        # أزلنا فلاج -z الذي سبب لك الخطأ في الصورة
        gobuster_cmd = f"gobuster dir -u http://{target_ip} -w /usr/share/wordlists/dirb/common.txt -q"
        try:
            gobuster_out = subprocess.check_output(gobuster_cmd, shell=True, text=True)
            logs += f"\n--- GOBUSTER ---\n{gobuster_out}"
        except: logs += "\n--- GOBUSTER: No directories found or failed ---"

    return logs

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.CYAN}{BANNER}{Colors.ENDC}")

    # تهيئة Gemini مع معالجة أخطاء الاتصال
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        chat = model.start_chat(history=[])
    except Exception as e:
        print(f"{Colors.RED}[!] Initialization Error: {e}{Colors.ENDC}")
        return

    lab_url = input(f"{Colors.BOLD}[?] Lab URL: {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] Target IP: {Colors.ENDC}")

    print(f"\n{Colors.GREEN}[+] GHENA Intelligence Cycle Started...{Colors.ENDC}")
    
    goals = scrape_lab_goals(lab_url)
    field_data = execute_smart_tools(target_ip)

    print(f"{Colors.YELLOW}[⚡] Mapping Lab Goals to Field Data...{Colors.ENDC}")
    
    final_prompt = f"Target IP: {target_ip}\nLab Goals: {goals}\nTools Output: {field_data}\nAnalyze and solve."

    # محاولة إرسال البيانات مع معالجة خطأ RpcError (مشكلة الإنترنت)
    try:
        response = chat.send_message(final_prompt)
        print(f"\n{Colors.BOLD}{'='*65}{Colors.ENDC}")
        print(f"{Colors.GREEN}🎯 GHENA'S FINAL SOLUTION & ANSWERS:{Colors.ENDC}")
        print(response.text)
        print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}[!] API Error: {e}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[i] نصيحة: تأكد من اتصال الـ Kali بالإنترنت ومن صحة مفتاح الـ API.{Colors.ENDC}")

if __name__ == "__main__":
    main()
