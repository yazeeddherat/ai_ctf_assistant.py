import google.generativeai as genai
import os
import sys
import requests
import subprocess
import time
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
#            {Colors.YELLOW}--- GHENA AI: MULTI-ENGINE AUTO-SOLVER ---{Colors.CYAN}        #
###############################################################{Colors.ENDC}
"""

def initialize_engine():
    """وظيفة فحص وتجربة نسخ جيميني حتى إيجاد نسخة شغالة"""
    print(f"{Colors.YELLOW}[*] جاري فحص نسخ Gemini المتاحة في حسابك...{Colors.ENDC}")
    genai.configure(api_key=API_KEY)
    
    # قائمة النسخ التي نريد تجربتها بالترتيب
    model_candidates = [
        'gemini-1.5-flash', 
        'gemini-1.5-pro', 
        'gemini-1.0-pro'
    ]
    
    selected_model = None
    
    for model_name in model_candidates:
        try:
            print(f"{Colors.CYAN}[?] تجربة النسخة: {model_name}...{Colors.ENDC}", end="\r")
            test_model = genai.GenerativeModel(model_name)
            # تجربة إرسال نص بسيط جداً للتأكد من الشغال
            test_model.generate_content("ping", generation_config={"max_output_tokens": 1})
            selected_model = test_model
            print(f"{Colors.GREEN}[+] تم العثور على نسخة شغالة: {model_name}          {Colors.ENDC}")
            return selected_model, model_name
        except Exception:
            continue
            
    if not selected_model:
        print(f"{Colors.FAIL}\n[!] لم يتم العثور على أي نسخة شغالة. تأكد من الـ API KEY ومن الإنترنت.{Colors.ENDC}")
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

    # 1. اختيار المحرك تلقائياً
    model, engine_name = initialize_engine()

    lab_url = input(f"\n{Colors.BOLD}[?] رابط اللاب (Lab URL): {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] IP الهدف (Target IP): {Colors.ENDC}")
    
    print(f"{Colors.YELLOW}[*] قراءة متطلبات اللاب من الرابط...{Colors.ENDC}")
    lab_context = fetch_lab_context(lab_url)

    print(f"{Colors.GREEN}[+] تم الربط بنجاح. سألتزم بتعليمات اللاب وأحل الأسئلة تلقائياً.{Colors.ENDC}")

    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        
        # برومبت تعليمات اللاب
        prompt_instruction = f"بناءً على تعليمات اللاب: {lab_context}\nما هو الأمر التالي الذي يطلبه اللاب للهدف {target_ip}؟ ابدأ بـ NEXT_STEP:"
        
        try:
            ai_instruction = model.generate_content(prompt_instruction).text
            if "NEXT_STEP:" in ai_instruction:
                cmd = ai_instruction.split("NEXT_STEP:")[1].split("\n")[0].strip()
                print(f"{Colors.HEADER}🤖 المهمة المطلوبة حالياً:{Colors.ENDC}\n{ai_instruction}")
                choice = input(f"\n{Colors.WARNING}[!] هل تريد تنفيذ {cmd}؟ (y/n): {Colors.ENDC}")
                if choice.lower() == 'y': os.system(cmd)
        except Exception as e: print(f"Error: {e}")

        print(f"\n{Colors.YELLOW}الصق مخرجات الأمر لتحليلها وحل السؤال (Enter مرتين):{Colors.ENDC}")
        lines = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break
            lines.append(line)
        
        user_output = "\n".join(lines)
        
        # برومبت حل الأسئلة
        prompt_solve = f"تعليمات اللاب: {lab_context}\nالمخرجات: {user_output}\nاستخرج جواب السؤال المطلوب في اللاب الآن بصيغة ✅ جواب السؤال:"
        
        try:
            analysis = model.generate_content(prompt_solve).text
            print(f"\n{Colors.OKGREEN}🎯 تحليل غنى واستخراج الأجوبة:{Colors.ENDC}\n")
            print(analysis)
        except Exception as e: print(f"Analysis Error: {e}")

if __name__ == "__main__":
    main()
