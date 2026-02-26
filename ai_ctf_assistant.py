import os
import sys
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# --- [ الإعدادات - SETTINGS ] ---
# ضع مفتاح الـ API الخاص بك من OpenAI هنا
API_KEY = "sk-your-openai-api-key-here"

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
    print(f"{Colors.YELLOW}[*] جاري الاتصال بمحرك الذكاء الاصطناعي (OpenAI) وتفعيل المفتاح...{Colors.ENDC}")
    try:
        client = OpenAI(api_key=API_KEY)
        # اختبار استجابة سريع للتأكد من صحة المفتاح
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=10
        )
        print(f"{Colors.GREEN}[+] تم التفعيل بنجاح! المحرك مستعد لحل اللاب.{Colors.ENDC}")
        return client
    except Exception as e:
        print(f"{Colors.FAIL}[!] خطأ في التشغيل: {e}{Colors.ENDC}")
        print(f"{Colors.CYAN}[i] تأكد من مفتاح الـ API ومن تنفيذ: pip install openai{Colors.ENDC}")
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

    client = initialize_ghena()

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
        
        while True:
            try:
                line = input()
                if line.strip().lower() == 'exit': 
                    sys.exit()
                
                if line == '':
                    empty_lines_count += 1
                    if empty_lines_count >= 2:
                        break
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
            response = client.chat.completions.create(
                model="gpt-4o", # يمكنك تغييره إلى gpt-3.5-turbo إذا أردت
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي ومحترف في حل تحديات الأمن السيبراني."},
                    {"role": "user", "content": prompt}
                ]
            )
            print(response.choices[0].message.content)
        except Exception as e:
            print(f"{Colors
