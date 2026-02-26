import google.generativeai as genai
import os
import sys
import requests
import time
from bs4 import BeautifulSoup

# --- [ الإعدادات - SETTINGS ] ---
# تم وضع مفتاح الـ API الخاص بك هنا
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
#            {Colors.YELLOW}--- GHENA AI: API ACTIVATED EDITION ---{Colors.CYAN}           #
###############################################################{Colors.ENDC}
"""

def initialize_engine():
    """فحص النسخ المتاحة للمفتاح الحالي"""
    print(f"{Colors.YELLOW}[*] جاري تهيئة المحرك باستخدام المفتاح المقدم...{Colors.ENDC}")
    genai.configure(api_key=API_KEY)
    
    # القائمة المفضلة للعمل في لابات الـ CTF
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
    
    for m_name in models_to_try:
        try:
            print(f"{Colors.CYAN}[?] فحص صلاحية {m_name}...{Colors.ENDC}", end="\r")
            m = genai.GenerativeModel(m_name)
            # اختبار استجابة سريع
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            print(f"{Colors.GREEN}[+] تم التفعيل بنجاح على نسخة: {m_name}          {Colors.ENDC}")
            return m
        except Exception:
            continue
    
    print(f"{Colors.FAIL}\n[!] خطأ: يبدو أن المفتاح غير مفعل أو انتهت صلاحيته.{Colors.ENDC}")
    sys.exit()

def fetch_lab_context(url):
    print(f"{Colors.YELLOW}[*] جاري سحب متطلبات اللاب من الرابط...{Colors.ENDC}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, cookies=COOKIES, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        # استخراج المهام والأسئلة (Tasks & Questions)
        content = "\n".join([el.get_text() for el in soup.find_all(['h3', 'h4', 'p', 'li', 'code'])])
        return content[:7000]
    except:
        return "Manual Mode: Context fetching failed."

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

    # تشغيل المحرك بالمفتاح المدمج
    active_model = initialize_engine()

    lab_url = input(f"\n{Colors.BOLD}[?] رابط اللاب (Lab URL): {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] IP الهدف (Target IP): {Colors.ENDC}")
    
    lab_context = fetch_lab_context(lab_url)
    print(f"{Colors.GREEN}[+] GHENA جاهزة للعمل وفق سيناريو اللاب.{Colors.ENDC}")

    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        
        # 1. طلب الخطوة التالية من الذكاء الاصطناعي بناءً على اللاب
        prompt_step = f"تعليمات اللاب: {lab_context}\nالهدف: {target_ip}\nبناءً على اللاب، ما هو الأمر التقني المطلوب تنفيذه الآن؟ ابدأ بـ 'NEXT_STEP:'"
        
        try:
            ai_step = active_model.generate_content(prompt_step).text
            if "NEXT_STEP:" in ai_step:
                cmd = ai_step.split("NEXT_STEP:")[1].split("\n")[0].strip()
                print(f"{Colors.HEADER}🤖 تعليمات اللاب الحالية:{Colors.ENDC}\n{ai_step}")
                choice = input(f"\n{Colors.WARNING}[!] تنفيذ {cmd}؟ (y/n): {Colors.ENDC}")
                if choice.lower() == 'y': os.system(cmd)
        except Exception as e:
            print(f"Error: {e}")

        # 2. استقبال النتائج وحل الأسئلة
        print(f"\n{Colors.YELLOW}الصق مخرجات الأداة هنا لحل الأسئلة (Enter مرتين):{Colors.ENDC}")
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
        المخرجات التقنية: {user_output}
        
        مهمتك: استخرج الأجوبة المباشرة لأسئلة اللاب بناءً على هذه المخرجات فقط.
        التنسيق:
        ✅ جواب السؤال (رقم): [الإجابة المباشرة]
        🔑 Credentials: [يوزر:باسورد إن وجد]
        👉 الخطوة القادمة: [حسب اللاب]
        """
        
        try:
            solution = active_model.generate_content(prompt_solve).text
            print(f"\n{Colors.OKGREEN}🎯 استخراج الأجوبة الذكي:{Colors.ENDC}\n")
            print(solution)
        except Exception as e:
            print(f"Analysis Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] تم إغلاق النظام.{Colors.ENDC}")
