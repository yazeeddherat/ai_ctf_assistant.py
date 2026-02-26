import google.generativeai as genai
import os
import sys
import requests
from bs4 import BeautifulSoup

# --- [ الإعدادات - SETTINGS ] ---
# ضع مفتاحك الجديد هنا الذي استخرجته من Google AI Studio
API_KEY = "AIzaSyCf6jw6eM5kqTPwfRnHNZiR1i0dMcH_4gY" 

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

def initialize_engine():
    """تهيئة المحرك وتجربة الاتصال لتجنب خطأ 404"""
    print(f"{Colors.YELLOW}[*] جاري فحص الاتصال بالمفتاح والموديل...{Colors.ENDC}")
    genai.configure(api_key=API_KEY)
    
    # قائمة الموديلات المتاحة (نبدأ بـ flash لأنه الأكثر استقراراً للمجاني)
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash']
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            # اختبار استجابة سريع
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            print(f"{Colors.GREEN}[+] تم التفعيل بنجاح! الموديل المستخدم: {name}{Colors.ENDC}")
            return model
        except Exception:
            continue
    
    print(f"{Colors.FAIL}[!] خطأ: لم ينجح الاتصال. تأكد من تحديث المكتبة عبر الأمر:\n    pip install -U google-generativeai --break-system-packages{Colors.ENDC}")
    sys.exit()

def fetch_lab_context(url):
    print(f"{Colors.YELLOW}[*] سحب تعليمات اللاب من الرابط...{Colors.ENDC}")
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        return "\n".join([el.get_text() for el in soup.find_all(['h3', 'h4', 'p', 'li', 'code'])])[:6000]
    except:
        return "Manual Mode: Context fetching failed."

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

    active_model = initialize_engine()

    lab_url = input(f"\n{Colors.BOLD}[?] رابط اللاب: {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] IP الهدف: {Colors.ENDC}")
    
    lab_context = fetch_lab_context(lab_url)
    print(f"{Colors.GREEN}[+] غنى جاهزة. سألتزم بتعليمات اللاب وأستخرج الباسوردات.{Colors.ENDC}")

    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        
        # 1. تحديد الخطوة التالية بناءً على اللاب
        prompt_step = f"تعليمات اللاب: {lab_context}\nالهدف: {target_ip}\nبناءً على اللاب، ما هو الأمر التقني المطلوب تنفيذه الآن؟ ابدأ بـ 'NEXT_STEP:'"
        
        try:
            ai_step = active_model.generate_content(prompt_step).text
            if "NEXT_STEP:" in ai_step:
                cmd = ai_step.split("NEXT_STEP:")[1].split("\n")[0].strip()
                print(f"{Colors.HEADER}🤖 المهمة القادمة حسب اللاب:{Colors.ENDC}\n{ai_step}")
                choice = input(f"\n{Colors.WARNING}[!] هل تريد تنفيذ {cmd}؟ (y/n): {Colors.ENDC}")
                if choice.lower() == 'y': os.system(cmd)
        except Exception as e:
            print(f"Error identifying step: {e}")

        # 2. تحليل النتائج وحل الأسئلة
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
        المخرجات: {user_output}
        
        مهمتك:
        1. استخرج الأجوبة لأسئلة اللاب.
        2. إذا وجدت باسوورد أو يوزر، أبرزه بوضوح.
        3. إذا اكتشفت FTP Anonymous، نبهني.
        
        التنسيق:
        ✅ جواب السؤال (رقم): [الإجابة]
        🔑 Credentials: [يوزر:باسورد]
        ⚠️ Alert: [أي ثغرة مكتشفة]
        """
        
        try:
            print(f"\n{Colors.OKGREEN}[⚡] جاري استخراج الحلول...{Colors.ENDC}")
            solution = active_model.generate_content(prompt_solve).text
            print(f"\n{Colors.HEADER}🎯 تحليل النتائج:{Colors.ENDC}\n")
            print(solution)
        except Exception as e:
            print(f"Analysis Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] إغلاق.{Colors.ENDC}")
