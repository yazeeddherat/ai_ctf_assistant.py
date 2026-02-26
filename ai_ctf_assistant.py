import google.generativeai as genai
import os
import sys
import requests
from bs4 import BeautifulSoup

# --- [ الإعدادات - SETTINGS ] ---
# ضع مفتاحك الجديد الذي ظهر في الصورة الأخيرة هنا
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
#            {Colors.YELLOW}--- GHENA AI: THE FULL LAB SCENARIO ---{Colors.CYAN}          #
###############################################################{Colors.ENDC}
"""

def initialize_engine():
    print(f"{Colors.YELLOW}[*] جاري فحص الاتصال بالمفتاح وتفعيل الموديل...{Colors.ENDC}")
    try:
        genai.configure(api_key=API_KEY)
        # استخدام المسار الكامل للموديل لتجنب خطأ 404 الذي ظهر في الصور
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        # اختبار استجابة سريع
        model.generate_content("ping", generation_config={"max_output_tokens": 1})
        print(f"{Colors.GREEN}[+] تم التفعيل بنجاح! المحرك جاهز للعمل وفق توقيت Amman.{Colors.ENDC}")
        return model
    except Exception as e:
        print(f"{Colors.FAIL}\n[!] فشل: {e}. تأكد من وضع المفتاح الصحيح وتغيير الموديل لـ flash.{Colors.ENDC}")
        sys.exit()

def fetch_lab_context(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, cookies=COOKIES, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        return "\n".join([el.get_text() for el in soup.find_all(['h3', 'h4', 'p', 'li', 'code'])])[:6000]
    except: return "Manual Mode"

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

    active_model = initialize_engine()

    lab_url = input(f"\n{Colors.BOLD}[?] رابط اللاب: {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] IP الهدف: {Colors.ENDC}")
    
    print(f"{Colors.YELLOW}[*] جاري قراءة سيناريو اللاب والأسئلة...{Colors.ENDC}")
    lab_context = fetch_lab_context(lab_url)

    print(f"{Colors.GREEN}[+] GHENA ستلتزم الآن بتعليمات اللاب حرفياً.{Colors.ENDC}")

    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        
        # 1. تحديد الخطوة التالية بناءً على اللاب فقط
        prompt_instruction = f"""
        أنت مساعد لابات CTF. تعليمات اللاب: {lab_context}
        بناءً على هذه التعليمات والهدف {target_ip}، ما هو الأمر التقني الذي يجب تنفيذه الآن؟
        (ملاحظة: إذا طلب اللاب Nmap استخدمه، إذا طلب Gobuster استخدمه).
        ابدأ بـ 'NEXT_STEP:'
        """
        
        try:
            ai_instruction = active_model.generate_content(prompt_instruction).text
            print(f"{Colors.HEADER}🤖 تعليمات اللاب الحالية:{Colors.ENDC}\n{ai_instruction}")
            
            if "NEXT_STEP:" in ai_instruction:
                cmd = ai_instruction.split("NEXT_STEP:")[1].split("\n")[0].strip()
                choice = input(f"\n{Colors.WARNING}[!] تنفيذ {cmd}؟ (y/n): {Colors.ENDC}")
                if choice.lower() == 'y': os.system(cmd)
        except Exception as e: print(f"Error: {e}")

        # 2. تحليل النتائج واستخراج الباسوردات والحلول
        print(f"\n{Colors.YELLOW}الصق مخرجات الأداة هنا (Enter مرتين):{Colors.ENDC}")
        lines = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break
            lines.append(line)
        
        user_output = "\n".join(lines)
        if not user_output.strip(): continue

        prompt_solve = f"""
        سياق اللاب: {lab_context}
        المخرجات التقنية الحالية: {user_output}
        
        مهمتك كـ GHENA AI:
        1. استخرج أي Password أو Flag أو Username ظهر في المخرجات.
        2. اربط النتائج بأسئلة اللاب المذكورة في السياق.
        3. إذا كان هناك FTP يسمح بـ Anonymous، أخبر المستخدم فوراً.
        
        التنسيق:
        ✅ جواب السؤال (رقم X): [الحل]
        🔑 Credentials: [يوزر:باسورد إن وجد]
        ⚠️ Alert: [تنبيهات أمنية]
        """
        
        try:
            analysis = active_model.generate_content(prompt_solve).text
            print(f"\n{Colors.OKGREEN}🎯 تحليل غنى وحل الأسئلة:{Colors.ENDC}\n")
            print(analysis)
        except Exception as e: print(f"Analysis Error: {e}")

if __name__ == "__main__":
    main()
