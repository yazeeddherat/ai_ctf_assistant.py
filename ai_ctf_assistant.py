import os
import subprocess
import sys
import time

# التحقق من المكتبة
try:
    import google.generativeai as genai
except ImportError:
    print("\n\033[91m[!] المكتبة غير موجودة. اكتب هذا الأمر في التيرمينال أولاً:")
    print("\033[92mpip install google-generativeai --break-system-packages\033[0m\n")
    sys.exit()

import requests
from bs4 import BeautifulSoup

# --- [ الإعدادات ] ---
API_KEY = "ضـع_مفـتاحك_هنـا"

BANNER = r"""
  ________  ___  ___  _______   ________   ________     
 |\   ____\|\  \|\  \|\  ___ \ |\   ___  \|\   __  \    
 \ \  \___|\ \  \\\  \ \   __/|\ \  \\ \  \ \  \|\  \   
  \ \  \  __\ \   __  \ \  \_|/_\ \  \\ \  \ \   __  \  
   \ \  \|\  \ \  \ \  \ \  \_|\ \ \  \\ \  \ \  \ \  \ 
    \ \_______\ \__\ \__\ \_______\ \__\\ \__\ \__\ \__\
     \|_______|\|__|\|__|\|_______|\|__| \|__|\|__|\|__|
            GHENA AI | THE FINAL REPAIR v5.2
"""

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\033[96m{BANNER}\033[0m")

    if API_KEY == "ضـع_مفـتاحك_هنـا":
        print("\033[91m[!] تنبيه: لم تضع مفتاح الـ API داخل الكود.\033[0m")
        return

    # إعداد المحرك
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')

    lab_url = input("\033[1m[?] Lab/Room URL: \033[0m")
    target_ip = input("\033[1m[?] Target IP: \033[0m")

    print("\n\033[94m[*] Phase 1: Nmap Scanning...\033[0m")
    try:
        # فحص سريع لضمان عدم حدوث Timeout
        scan = subprocess.check_output(f"nmap -F {target_ip}", shell=True, text=True)
    except:
        scan = "Nmap scan failed."

    print("\033[93m[⚡] Analyzing with GHENA Neural Engine...\033[0m")
    
    prompt = f"Target: {target_ip}\nLab: {lab_url}\nScan Results:\n{scan}\nSolve the lab questions."

    try:
        response = model.generate_content(prompt)
        print(f"\n\033[92m🎯 GHENA SOLUTION:\033[0m\n{response.text}")
    except Exception as e:
        print(f"\n\033[91m[!] حدث خطأ في الاتصال: {e}")
        print("\033[93m[i] تأكد من ضبط وقت وساعة النظام، ومن صحة مفتاح الـ API.\033[0m")

if __name__ == "__main__":
    main()
