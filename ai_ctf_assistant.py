import google.generativeai as genai
import os
import subprocess
import sys
import time
import requests
from bs4 import BeautifulSoup

# --- [ إعدادات المحرك العصبي ] ---
API_KEY = "ضـع_مفـتاحك_هنـا"
# الكوكيز الخاصة بمتصفحك (اختياري لقراءة الغرف الخاصة)
SESSION_COOKIES = {
    "connect.sid": "ضـع_الـكوكـي_هنـا_إذا_لزم_الأمـر" 
}

BANNER = r"""
  ________  ___  ___  _______   ________   ________     
 |\   ____\|\  \|\  \|\  ___ \ |\   ___  \|\   __  \    
 \ \  \___|\ \  \\\  \ \   __/|\ \  \\ \  \ \  \|\  \   
  \ \  \  __\ \   __  \ \  \_|/_\ \  \\ \  \ \   __  \  
   \ \  \|\  \ \  \ \  \ \  \_|\ \ \  \\ \  \ \  \ \  \ 
    \ \_______\ \__\ \__\ \_______\ \__\\ \__\ \__\ \__\
     \|_______|\|__|\|__|\|_______|\|__| \|__|\|__|\|__|
           GHENA AI | FULL AUTONOMOUS SOLUTION
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
    """سحب الأسئلة والمهام من رابط المختبر"""
    print(f"{Colors.YELLOW}[*] GHENA is accessing Lab Intelligence...{Colors.ENDC}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # محاولة الدخول بالكوكيز إذا كانت متوفرة
        res = requests.get(url, headers=headers, cookies=SESSION_COOKIES, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # استخراج العناوين والأسئلة (تخصيص لمنصات الـ CTF)
        tasks = [t.get_text() for t in soup.find_all(['h3', 'h4', 'p'])]
        return "\n".join(tasks[:20]) # نكتفي بأهم الأجزاء لفهم الأهداف
    except Exception as e:
        return f"Scraping Error: {e}"

def execute_smart_tools(target_ip):
    """تشغيل الأدوات بشكل تسلسلي ذكي"""
    logs = ""
    
    # 1. Nmap (أساسي دائماً)
    print(f"{Colors.CYAN}[*] Step 1: Broad Reconnaissance (Nmap)...{Colors.ENDC}")
    nmap_cmd = f"nmap -sV --top-ports 1000 {target_ip}"
    nmap_out = subprocess.check_output(nmap_cmd, shell=True, text=True)
    logs += f"\n--- NMAP ---\n{nmap_out}"

    # 2. اتخاذ قرار ذكي بناءً على المنافذ
    if "80" in nmap_out or "443" in nmap_out:
        print(f"{Colors.CYAN}[*] Step 2: Web Path Discovery (Gobuster)...{Colors.ENDC}")
        gobuster_cmd = f"gobuster dir -u http://{target_ip} -w /usr/share/wordlists/dirb/common.txt -z -q"
        try:
            gobuster_out = subprocess.check_output(gobuster_cmd, shell=True, text=True)
            logs += f"\n--- GOBUSTER ---\n{gobuster_out}"
        except: logs += "\n--- GOBUSTER: No directories found ---"

    return logs

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.CYAN}{BANNER}{Colors.ENDC}")

    # تهيئة Gemini 1.5 Pro
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    chat = model.start_chat(history=[])

    # مدخلات المستخدم
    lab_url = input(f"{Colors.BOLD}[?] Lab URL: {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] Target IP: {Colors.ENDC}")

    # التنفيذ
    print(f"\n{Colors.GREEN}[+] GHENA Intelligence Cycle Started...{Colors.ENDC}")
    
    # جلب الأهداف من الرابط
    goals = scrape_lab_goals(lab_url)
    
    # تنفيذ الفحص الميداني
    field_data = execute_smart_tools(target_ip)

    # التحليل النهائي والحل
    print(f"{Colors.YELLOW}[⚡] Mapping Lab Goals to Field Data...{Colors.ENDC}")
    
    final_prompt = f"""
    أنت GHENA AI. هدفك هو حل هذا المختبر (CTF Solver).
    
    [أهداف المختبر من الرابط]:
    {goals}
    
    [نتائج الفحص الفني]:
    {field_data}
    
    بناءً على ما سبق، قدم لي تقريراً نهائياً يتضمن:
    1. الإجابة المباشرة على كل سؤال ظهر في الرابط.
    2. تسلسل الخطوات (Exploit Chain) التي يجب أن أقوم بها للحصول على الـ Flag.
    3. أي ثغرات حرجة لاحظتها في مخرجات الأدوات.
    """

    response = chat.send_message(final_prompt)
    
    print(f"\n{Colors.BOLD}{'='*65}{Colors.ENDC}")
    print(f"{Colors.GREEN}🎯 GHENA'S FINAL SOLUTION & ANSWERS:{Colors.ENDC}")
    print(response.text)
    print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")

if __name__ == "__main__":
    main()
