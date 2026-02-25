import os
import subprocess
import sys
import time

# التحقق من وجود المكتبة وتنبيهك
try:
    import google.generativeai as genai
except ImportError:
    print("\n\033[91m[!] المكتبة غير مثبتة. نفذ الأمر التالي أولاً:")
    print("\033[92mpip install google-generativeai --break-system-packages\033[0m\n")
    sys.exit()

import requests
from bs4 import BeautifulSoup

# --- [ إعدادات المحرك ] ---
API_KEY = "ضـع_مفـتاحك_هنـا" # استبدله بمفتاحك الخاص

BANNER = r"""
  ________  ___  ___  _______   ________   ________     
 |\   ____\|\  \|\  \|\  ___ \ |\   ___  \|\   __  \    
 \ \  \___|\ \  \\\  \ \   __/|\ \  \\ \  \ \  \|\  \   
  \ \  \  __\ \   __  \ \  \_|/_\ \  \\ \  \ \   __  \  
   \ \  \|\  \ \  \ \  \ \  \_|\ \ \  \\ \  \ \  \ \  \ 
    \ \_______\ \__\ \__\ \_______\ \__\\ \__\ \__\ \__\
     \|_______|\|__|\|__|\|_______|\|__| \|__|\|__|\|__|
           GHENA AI | FIXED & STABLE EDITION
"""

def run_tools(target_ip):
    results = ""
    print(f"\033[94m[*] Phase 1: Nmap Scanning...\033[0m")
    try:
        # فحص سريع لعدم تعليق الأداة
        nmap_res = subprocess.check_output(f"nmap -F {target_ip}", shell=True, text=True)
        results += f"\n--- NMAP ---\n{nmap_res}"
    except: results += "\n--- NMAP FAILED ---"

    if "80" in results or "443" in results:
        print(f"\033[94m[*] Phase 2: Gobuster (Web Enumeration)...\033[0m")
        # تم حذف -z ليتوافق مع نسختك
        cmd = f"gobuster dir -u http://{target_ip} -w /usr/share/wordlists/dirb/common.txt -q"
        try:
            gob_res = subprocess.check_output(cmd, shell=True, text=True, timeout=30)
            results += f"\n--- GOBUSTER ---\n{gob_res}"
        except: results += "\n--- GOBUSTER SKIPPED ---"
    return results

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\033[96m{BANNER}\033[0m")

    if API_KEY == "ضـع_مفـتاحك_هنـا":
        print("\033[91m[!] خطأ: يجب وضع الـ API KEY داخل الكود!\033[0m")
        return

    # تهيئة الذكاء الاصطناعي مع معالجة أخطاء الاتصال
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')

    lab_url = input("\033[1m[?] Lab/Room URL: \033[0m")
    target_ip = input("\033[1m[?] Target IP: \033[0m")

    print("\n\033[92m[+] Starting GHENA Strategic Analysis...\033[0m")
    
    # تنفيذ الفحص
    field_data = run_tools(target_ip)

    print("\033[93m[⚡] Sending data to Gemini Neural Engine...\033[0m")
    
    prompt = f"Target IP: {target_ip}\nLab Link: {lab_url}\nScan Data:\n{field_data}\nAnalyze and give the solution."
    
    try:
        response = model.generate_content(prompt)
        print(f"\n\033[92m🎯 GHENA AI SOLUTION:\033[0m\n{response.text}")
    except Exception as e:
        print(f"\033[91m[!] AI Connection Error: {e}\033[0m")

if __name__ == "__main__":
    main()
