import google.generativeai as genai
import os
import sys
import datetime

# --- الإعدادات (Settings) ---
# ضع مفتاح API الخاص بك هنا
API_KEY = "ضع_مفتاحك_هنا"

# إعداد الألوان والواجهة
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'

# --- تهيئة الاتصال الذكي ---
try:
    genai.configure(api_key=API_KEY)
    
    # البحث التلقائي عن الموديلات المتاحة في حسابك لتجنب خطأ 404
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_models:
        print(f"{Colors.FAIL}[!] خطأ: لا توجد موديلات متاحة لهذا المفتاح.{Colors.ENDC}")
        sys.exit()
    
    # اختيار أفضل موديل متاح (يفضل flash لأنه الأنسب لمهام الـ CTF السريعة)
    selected_model = next((m for m in available_models if "flash" in m), available_models[0])
    model = genai.GenerativeModel(selected_model)
    
except Exception as e:
    print(f"{Colors.FAIL}[!] فشل الاتصال بـ Gemini API: {e}{Colors.ENDC}")
    sys.exit()

def get_ai_analysis(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return f"{Colors.WARNING}[!] تم تجاوز حد الطلبات (Quota). انتظر 20 ثانية وحاول مجدداً.{Colors.ENDC}"
        return f"{Colors.FAIL}[!] حدث خطأ أثناء التحليل: {e}{Colors.ENDC}"

def main_interface():
    os.system('clear')
    banner = f"""
{Colors.CYAN}    ________  __________   _____    ___    ____
   / ____/ / / / ____/ | / /   |  /   |  /  _/
  / / __/ /_/ / __/ /  |/ / /| | / /| |  / /  
 / /_/ / __  / /___/ /|  / ___ |/ ___ |_/ /   
 \____/_/ /_/_____/_/ |_/_/  |_/_/  |_/___/   
{Colors.OKGREEN}       GHENA AI | REPAIRED & STABLE EDITION{Colors.ENDC}
    """
    print(banner)
    print(f"{Colors.OKBLUE}[+] الموديل النشط حالياً: {selected_model}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}[+] الوقت: {datetime.datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}\n")

    lab_url = input(f"{Colors.BOLD}[?] رابط المختبر (URL): {Colors.ENDC}")
    target_ip = input(f"{Colors.BOLD}[?] عنوان الهدف (IP): {Colors.ENDC}")

    while True:
        print(f"\n{Colors.WARNING}--------------------------------------------------{Colors.ENDC}")
        print(f"{Colors.BOLD}الصق مخرجات الأداة (Nmap, Gobuster, etc.) واضغط Enter مرتين للتحليل:{Colors.ENDC}")
        
        user_input = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break 
            user_input.append(line)
        
        raw_data = "\n".join(user_input)
        if not raw_data.strip(): continue

        full_prompt = f"""
        أنت خبير Pentesting ومساعد في تحديات CTF.
        الهدف الحالي: {target_ip}
        رابط التحدي: {lab_url}
        المخرجات التقنية المطلوبة منك تحليلها:
        {raw_data}
        
        بناءً على هذه المعطيات، قدم لي:
        1. تحليل سريع لأهم الثغرات المحتملة.
        2. الخطوة العملية القادمة (أمر محدد للتنفيذ).
        3. نصيحة "خبير" لتجاوز أي جدار حماية محتمل.
        """

        print(f"\n{Colors.CYAN}[*] جاري التفكير والتحليل الذكي...{Colors.ENDC}")
        analysis = get_ai_analysis(full_prompt)
        print(f"\n{Colors.OKGREEN}🤖 توجيهات GHENA AI:{Colors.ENDC}\n{analysis}")

if __name__ == "__main__":
    main_interface()
