import google.generativeai as genai
import os
import sys
import requests
import datetime
import subprocess
from bs4 import BeautifulSoup

# --- [ الإعدادات - SETTINGS ] ---
API_KEY = "ضـع_مفـتاحك_هنـا"

COOKIES = {"connect.sid": "ضـع_الـكوكـي_هنـا_اختياري"}

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

BANNER = r"""
  ________  ___  ___  _______   ________   ________     
 |\   ____\|\  \|\  \|\  ___ \ |\   ___  \|\   __  \    
 \ \  \___|\ \  \\\  \ \   __/|\ \  \\ \  \ \  \|\  \   
  \ \  \  __\ \   __  \ \  \_|/_\ \  \\ \  \ \   __  \  
   \ \  \|\  \ \  \ \  \ \  \_|\ \ \  \\ \  \ \  \ \  \ 
    \ \_______\ \__\ \__\ \_______\ \__\\ \__\ \__\ \__\
     \|_______|\|__|\|__|\|_______|\|__| \|__|\|__|\|__|
            GHENA AI | FTP & ANONYMOUS DETECTOR
"""

# --- [ إعداد المحرك الذكي ] ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        safety_settings=[{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}],
        generation_config={"temperature": 0.1}
    )
except Exception as e:
    print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}"); sys.exit()

def fetch_lab_content(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, cookies=COOKIES, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        return "\n".join([el.get_text() for el in soup.find_all(['h3', 'h4', 'p', 'li', 'code'])])[:5000]
    except: return "Manual Context"

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.CYAN}{Colors.BOLD}{BANNER}{Colors.ENDC}")

    lab_url = input(f"{Colors.BOLD}[?] رابط اللاب: {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] IP الهدف: {Colors.ENDC}")
    lab_context = fetch_lab_content(lab_url)

    print(f"\n{Colors.GREEN}[+] تم تحميل الأهداف. GHENA تراقب الآن منافذ FTP والـ Anonymous...{Colors.ENDC}")

    while True:
        print(f"\n{Colors.YELLOW}{'—'*60}{Colors.ENDC}")
        print(f"الصق مخرج الأداة (Nmap مثلاً):")
        
        lines = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break
            lines.append(line)
        
        user_output = "\n".join(lines)
        if not user_output.strip(): continue

        # تحليل إضافي من "غنى" للبحث عن FTP Anonymous
        print(f"\n{Colors.CYAN}[⚡] GHENA AI is analyzing service configurations...{Colors.ENDC}")

        prompt = f"""
        أنت GHENA AI، خبير اختراق متقدم.
        الأسئلة المطلوبة: {lab_context}
        المخرجات: {user_output}
        الهدف: {target_ip}

        مهمتك الخاصة:
        1. إذا رأيت بورت 21 مفتوحاً (FTP)، تحقق من مخرج Nmap إذا كان يذكر 'Anonymous FTP login allowed'.
        2. إذا كان مسموحاً، أخبر المستخدم فوراً: "⚠️ تنبيه: منفذ FTP يسمح بالدخول المجهول!" واعطه الجواب إذا كان هناك سؤال متعلق بذلك.
        3. استخرج أي باسوردات أو يوزرات تظهر في المخرجات.
        
        التنسيق:
        ✅ جواب السؤال (رقم X): [الحل]
        🔓 حالة الخدمة: [مثال: FTP Anonymous Allowed]
        👉 اكتب هذا الأمر: [الأمر اللازم للدخول أو الفحص]
        🔑 Credentials: [أي يوزر أو باسورد مستخرج]
        """

        try:
            response = model.generate_content(prompt)
            print(f"\n{Colors.HEADER}🤖 تحليل غنى الذكي:{Colors.ENDC}\n")
            print(response.text)
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()
