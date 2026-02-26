import google.generativeai as genai
import os
import sys
import requests
import time
from bs4 import BeautifulSoup

# --- [ الإعدادات - SETTINGS ] ---
# ضع مفتاح الـ API الجديد الخاص بك هنا
API_KEY = "AIzaSyDmm3sH2JC4PJDLJwUP47DQbX3zqCrcNDA"
COOKIES = {"connect.sid": "ضـع_الـكوكـي_هنـا_اختياري"}

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
#            {Colors.YELLOW}--- GHENA AI: THE ULTIMATE CTF SOLVER ---{Colors.CYAN}         #
###############################################################{Colors.ENDC}
"""

def initialize_engine():
    """تفعيل محرك Gemini وتخطي مشاكل الاتصال"""
    print(f"{Colors.YELLOW}[*] جاري فحص الاتصال بالمفتاح وتفعيل المحرك...{Colors.ENDC}")
    try:
        genai.configure(api_key=API_KEY)
        # استخدام flash حصرياً لتجنب أخطاء 404 التي ظهرت في الصور
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # اختبار بسيط للتأكد من الاستجابة
        test = model.generate_content("ping", generation_config={"max_output_tokens": 5})
        print(f"{Colors.GREEN}[+] تم التفعيل بنجاح! المحرك مستعد للعمل.{Colors.ENDC}")
        return model
    except Exception as e:
        print(f"{Colors.FAIL}[!] خطأ في التشغيل: {e}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[i] تأكد من ضبط الوقت (Asia/Amman) ووضع مفتاح صحيح.{Colors.ENDC}")
        sys.exit()

def fetch_lab_context(url):
    """سحب الأسئلة والمهام من رابط اللاب"""
    print(f"{Colors.YELLOW}[*] جاري قراءة تعليمات اللاب من الرابط...{Colors.ENDC}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, cookies=COOKIES, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        content = "\n".join([el.get_text() for el in soup.find_all(['h3', 'h4', 'p', 'li', 'code'])])
        return content[:7000]
    except:
        return "Manual Mode: Context not found."

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

    # تشغيل المحرك
    model = initialize_engine()

    lab_url = input(f"\n{Colors.BOLD}[?] رابط اللاب (Lab URL): {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] IP الهدف (Target IP): {Colors.ENDC}")
    
    lab_context = fetch_lab_context(lab_url)
    print(f"{Colors.GREEN}[+] GHENA جاهزة تماماً للحل وفقاً لمتطلبات المؤلف.{Colors.ENDC}")

    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        
        # 1. تحليل المهمة التالية بناءً على اللاب
        prompt_step = f"""
        أنت مساعد خبير في حل لابات CTF. 
        تعليمات اللاب الحالية: {lab_context}
        الهدف الحالي: {target_ip}
        ما هو الأمر الذي يجب تنفيذه الآن بناءً على ترتيب المهام في اللاب؟
        ابدأ إجابتك بـ 'NEXT_STEP:' متبوعاً بالأمر فقط.
        """
        
        try:
            ai_step = model.generate_content(prompt_step).text
            if "NEXT_STEP:" in ai_step:
                cmd = ai_step.split("NEXT_STEP:")[1].split("\n")[0].strip()
                print(f"{Colors.HEADER}🤖 تعليمات اللاب الحالية:{Colors.ENDC}\n{ai_step}")
                choice = input(f"\n{Colors.WARNING}[!] هل تريد تنفيذ الأمر المقترح؟ (y/n): {Colors.ENDC}")
                if choice.lower() == 'y': os.system(cmd)
        except Exception as e:
            print(f"Error suggesting step: {e}")

        # 2. استقبال المخرجات وحل الأسئلة واستخراج الباسوردات
        print(f"\n{Colors.YELLOW}الصق مخرجات الأداة (Nmap, Gobuster, إلخ) للتحليل (Enter مرتين):{Colors.ENDC}")
        lines = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break
            lines.append(line)
        
        user_output = "\n".join(lines)
        if not user_output.strip(): continue

        print(f"\n{Colors.CYAN}[⚡] GHENA AI is extracting answers & passwords...{Colors.ENDC}")

        prompt_solve = f"""
        سياق اللاب: {lab_context}
        مخرجات الأدوات: {user_output}
        
        مهمتك:
        1. ابحث عن أي (Password, Username, Flag) في المخرجات.
        2. حل الأسئلة الموجودة في سياق اللاب بناءً على النتائج.
        3. إذا كان هناك FTP Anonymous، أخبرني فوراً.
        
        التنسيق:
        ✅ جواب السؤال (رقم): [الإجابة المباشرة]
        🔑 Credentials: [يوزر:باسورد إن وجد]
        ⚠️ Alert: [تنبيهات أمنية]
        👉 الخطوة التالية: [ماذا نفعل الآن؟]
        """
        
        try:
            solution = model.generate_content(prompt_solve).text
            print(f"\n{Colors.OKGREEN}🎯 الحلول المستخرجة:{Colors.ENDC}\n")
            print(solution)
        except Exception as e:
            print(f"Analysis Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] إغلاق البرنامج...{Colors.ENDC}")
