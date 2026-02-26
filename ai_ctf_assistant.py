import google.generativeai as genai
import os
import sys
import requests
from bs4 import BeautifulSoup

# --- [ الإعدادات - SETTINGS ] ---
# ضع مفتاح الـ API الخاص بك هنا
API_KEY = "AIzaSyDmm3sH2JC4PJDLJwUP47DQbX3zqCrcNDA"

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

BANNER = f"""
{Colors.CYAN}###############################################################
#                                                             #
#   {Colors.GREEN}  ██████╗ ██╗  ██╗███████╗███╗   ██╗ █████╗  ██╗  {Colors.CYAN}       #
#   {Colors.GREEN} ██╔════╝ ██║  ██║██╔════╝████╗  ██║██╔══██╗ ██║  {Colors.CYAN}       #
#   {Colors.GREEN} ██║  ███╗███████║█████╗  ██╔██╗ ██║███████║ ██║  {Colors.CYAN}       #
#   {Colors.GREEN} ██║   ██║██╔══██║██╔══╝  ██║╚██╗██║██╔══██║ ██║  {Colors.CYAN}       #
#   {Colors.GREEN} ╚██████╔╝██║  ██║███████╗██║ ╚████║██║  ██║ ██║  {Colors.CYAN}       #
#   {Colors.GREEN}  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═╝  {Colors.CYAN}       #
#                                                             #
#            {Colors.YELLOW}--- GHENA AI: THE FINAL LAB SOLVER ---{Colors.CYAN}           #
###############################################################{Colors.ENDC}
"""

def initialize_ghena():
    print(f"{Colors.YELLOW}[*] جاري الاتصال بمحرك جوجل وتفعيل المفتاح...{Colors.ENDC}")
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # إصلاح تمرير الإعدادات لتتوافق مع جميع إصدارات المكتبة
        response = model.generate_content("Ping", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
        print(f"{Colors.GREEN}[+] تم التفعيل بنجاح! المحرك مستعد لحل اللاب.{Colors.ENDC}")
        return model
    except Exception as e:
        print(f"{Colors.FAIL}[!] خطأ في التشغيل: {e}{Colors.ENDC}")
        print(f"{Colors.CYAN}[i] تأكد من تنفيذ: pip install -U google-generativeai --break-system-packages{Colors.ENDC}")
        sys.exit()

def fetch_lab_task(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        return "\n".join([el.get_text() for el in soup.find_all(['h3', 'p', 'li', 'code'])])[:5000]
    except: return "Manual Context"

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

    model = initialize_ghena()

    try:
        lab_url = input(f"\n{Colors.BOLD}[?] رابط اللاب: {Colors.ENDC}")
        target_ip = input(f"{Colors.BOLD}[?] IP الهدف: {Colors.ENDC}")
    except (KeyboardInterrupt, EOFError):
        sys.exit()
    
    print(f"{Colors.YELLOW}[*] جاري قراءة سيناريو اللاب...{Colors.ENDC}")
    context = fetch_lab_task(lab_url)

    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}الصق مخرج الأداة (Nmap, Gobuster, إلخ) لتحليلها (Enter مرتين للمتابعة):{Colors.ENDC}")
        
        lines = []
        empty_lines_count = 0
        
        # --- [ تم إصلاح مشكلة قراءة الأسطر المتعددة هنا ] ---
        while True:
            try:
                line = input()
                if line.strip().lower() == 'exit': 
                    sys.exit()
                
                if line == '':
                    empty_lines_count += 1
                    if empty_lines_count >= 2:
                        break # الخروج فقط عند وجود سطرين فارغين متتاليين (Enter مرتين)
                else:
                    empty_lines_count = 0
                
                lines.append(line)
            except (KeyboardInterrupt, EOFError):
                sys.exit()
        
        user_output = "\n".join(lines).strip()
        if not user_output: 
            continue

        prompt = f"""
        أنت GHENA AI، خبير حل لابات CTF.
        سياق اللاب: {context}
        الهدف: {target_ip}
        المخرجات التقنية: {user_output}

        بناءً على تعليمات اللاب والمخرجات:
        1. استخرج الأجوبة المباشرة للأسئلة.
        2. إذا وجد FTP Anonymous، أخبر المستخدم فوراً بكيفية الدخول.
        3. اقترح الأمر التالي الذي يجب تنفيذه حرفياً.

        التنسيق:
        ✅ جواب السؤال: [الإجابة]
        ⚠️ تنبيه أمني: [إن وجد]
        👉 الخطوة التالية: [الأمر البرمجي]
        """

        try:
            print(f"\n{Colors.HEADER}🤖 تحليل غنى الذكي:{Colors.ENDC}")
            result = model.generate_content(prompt)
            print(result.text)
        except Exception as e:
            print(f"{Colors.FAIL}[!] فشل التحليل: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()
