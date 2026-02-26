import google.generativeai as genai
import os
import sys
import requests
import subprocess
from bs4 import BeautifulSoup

# --- [ الإعدادات - SETTINGS ] ---
API_KEY = "AIzaSyBe_ZTiXXbCy_t_OqURaR11NHr4C-Nz9F8"
COOKIES = {"connect.sid": "ضـع_الـكوكـي_هنـا_اختياري"}

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# واجهة الأداة عند التشغيل
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
#            {Colors.YELLOW}--- GHENA AI: THE LAB-DRIVEN SOLVER ---{Colors.CYAN}          #
###############################################################{Colors.ENDC}
"""

# إعداد الموديل
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        safety_settings=[{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}],
        generation_config={"temperature": 0.1}
    )
except Exception as e:
    print(f"Error: {e}"); sys.exit()

def fetch_lab_context(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, cookies=COOKIES, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        # تركيز البحث على "Tasks" و "Instructions"
        return "\n".join([el.get_text() for el in soup.find_all(['h3', 'h4', 'p', 'li', 'code'])])[:6000]
    except: return "Manual Mode: Please provide lab instructions."

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

    lab_url = input(f"{Colors.BOLD}[?] رابط اللاب (Lab URL): {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] IP الهدف (Target IP): {Colors.ENDC}")
    
    print(f"{Colors.YELLOW}[*] GHENA is reading lab requirements...{Colors.ENDC}")
    lab_context = fetch_lab_context(lab_url)

    print(f"{Colors.GREEN}[+] تمت قراءة السيناريو. سألتزم بالأدوات والخطوات التي يطلبها اللاب فقط.{Colors.ENDC}")

    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        
        # برومبت يطلب من AI تحديد الخطوة القادمة بناءً على "تعليمات اللاب"
        instruction_prompt = f"""
        أنت مساعد خبير في حل لابات CTF. التزم حرفياً بتعليمات اللاب المقدمة لك.
        تعليمات اللاب: {lab_context}
        الهدف: {target_ip}

        بناءً على ما يطلبه اللاب في هذه المرحلة، ما هو الأمر الذي يجب تنفيذه الآن؟ 
        اجعل إجابتك تبدأ بـ 'NEXT_STEP:' متبوعاً بالأمر.
        """
        
        try:
            ai_instruction = model.generate_content(instruction_prompt).text
            print(f"{Colors.HEADER}🤖 تعليمات اللاب الحالية:{Colors.ENDC}")
            print(ai_instruction)
            
            # استخراج الأمر المقترح من اللاب
            if "NEXT_STEP:" in ai_instruction:
                suggested_cmd = ai_instruction.split("NEXT_STEP:")[1].split("\n")[0].strip()
                choice = input(f"\n{Colors.WARNING}[!] اللاب يطلب تنفيذ: {Colors.BOLD}{suggested_cmd}{Colors.ENDC}\nهل تريد التنفيذ؟ (y/n): ")
                if choice.lower() == 'y':
                    os.system(suggested_cmd)
        
        except Exception as e:
            print(f"Error: {e}")

        print(f"\n{Colors.YELLOW}الصق مخرجات الأمر هنا لتحليل النتائج وحل الأسئلة (Enter مرتين):{Colors.ENDC}")
        lines = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break
            lines.append(line)
        
        user_output = "\n".join(lines)
        
        # تحليل النتائج واستخراج الأجوبة
        analysis_prompt = f"""
        بناءً على تعليمات اللاب: {lab_context}
        ومخرجات الأداة: {user_output}
        
        استخرج الإجابة المطلوبة للسؤال الحالي في اللاب.
        إذا وجدت كلمة مرور أو Flag، حدد أي سؤال يحل.
        التنسيق:
        ✅ جواب السؤال (X): [الإجابة]
        🔑 Credentials: [يوزر:باسورد إن وجد]
        👉 الخطوة القادمة حسب اللاب: [وصف]
        """
        
        try:
            analysis_res = model.generate_content(analysis_prompt).text
            print(f"\n{Colors.OKGREEN}🎯 تحليل النتائج وحل الأسئلة:{Colors.ENDC}\n")
            print(analysis_res)
        except Exception as e:
            print(f"Analysis Error: {e}")

if __name__ == "__main__":
    main()
