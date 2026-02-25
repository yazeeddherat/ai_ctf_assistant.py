import google.generativeai as genai
import os
import sys
import time
import datetime

# ==========================================
# --- إعدادات المحرك (Configuration) ---
# ==========================================
API_KEY = "ضـع_مفـتاحك_هنـا"  # استبدله بمفتاح API الخاص بك

# شعار GHENA المخصص (ASCII ART)
BANNER = r"""
  ________  ___  ___  _______   ________   ________     
 |\   ____\|\  \|\  \|\  ___ \ |\   ___  \|\   __  \    
 \ \  \___|\ \  \\\  \ \   __/|\ \  \\ \  \ \  \|\  \   
  \ \  \  __\ \   __  \ \  \_|/_\ \  \\ \  \ \   __  \  
   \ \  \|\  \ \  \ \  \ \  \_|\ \ \  \\ \  \ \  \ \  \ 
    \ \_______\ \__\ \__\ \_______\ \__\\ \__\ \__\ \__\
     \|_______|\|__|\|__|\|_______|\|__| \|__|\|__|\|__|
            GHENA AI - NEURAL STRATEGIC ENGINE
"""

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

# ==========================================
# --- الوظائف الحركية والبصرية ---
# ==========================================

def loading_animation():
    """تأثير بصري لبدء تشغيل النظام"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.MAGENTA}{Colors.BOLD}Initializing GHENA AI Strategic Modules...{Colors.ENDC}")
    animation = ["□□□□□", "■□□□□", "■■□□□", "■■■□□", "■■■■□", "■■■■■"]
    for i in range(len(animation)):
        time.sleep(0.3)
        sys.stdout.write(f"\r{Colors.CYAN}[{animation[i]}] Booting Neural Pathways...{Colors.ENDC}")
        sys.stdout.flush()
    print("\n")

def get_strategy(chat_session, output, target_info):
    """إرسال البيانات للمحرك العصبي وتحليلها"""
    system_instruction = f"""
    أنت الآن 'GHENA AI' مساعد خبير في الأمن السيبراني وتحديات CTF.
    الهدف الحالي: {target_info}
    
    مهمتك:
    1. تحليل المخرجات تقنياً واستخراج الثغرات (CVEs).
    2. ربط المعلومات ببعضها (Correlation).
    3. اقتراح الخطوات القادمة بأوامر جاهزة تبدأ بـ 👉.
    4. شرح مبسط باللغة العربية بجانب كل أمر تقني.
    """
    try:
        response = chat_session.send_message(f"{system_instruction}\n\nالمخرجات الجديدة:\n{output}")
        return response.text
    except Exception as e:
        return f"{Colors.RED}Error in Neural Engine: {e}{Colors.ENDC}"

# ==========================================
# --- الدورة الأساسية للبرنامج ---
# ==========================================

def main():
    # 1. تشغيل المؤثرات البصرية
    loading_animation()
    print(f"{Colors.CYAN}{Colors.BOLD}{BANNER}{Colors.ENDC}")
    print(f"{Colors.MAGENTA}{'='*65}{Colors.ENDC}")

    # 2. تهيئة الاتصال بـ Gemini
    try:
        if API_KEY == "ضـع_مفـتاحك_هنـا":
            print(f"{Colors.RED}[!] Error: Please set your API_KEY in the script!{Colors.ENDC}")
            return
        
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={"temperature": 0.2, "max_output_tokens": 4096}
        )
        chat = model.start_chat(history=[])
    except Exception as e:
        print(f"{Colors.RED}[!] Connection Failed: {e}{Colors.ENDC}")
        return

    # 3. إدخال بيانات الهدف
    target_ip = input(f"{Colors.YELLOW}{Colors.BOLD}[?] Target IP/Domain: {Colors.ENDC}")
    platform = input(f"{Colors.YELLOW}{Colors.BOLD}[?] Platform (HTB/THM): {Colors.ENDC}")
    target_info = f"IP: {target_ip}, Platform: {platform}"

    print(f"\n{Colors.GREEN}[+] GHENA Engine is LIVE. Send your tool outputs.{Colors.ENDC}")

    while True:
        print(f"\n{Colors.CYAN}📥 Paste tool output below (Press Enter twice to analyze):{Colors.ENDC}")
        
        user_input = []
        while True:
            line = sys.stdin.readline().rstrip()
            if line == '': break
            user_input.append(line)
        
        full_output = "\n".join(user_input)
        
        if full_output.lower() == 'exit': 
            print(f"{Colors.MAGENTA}Shutting down GHENA AI... Goodbye!{Colors.ENDC}")
            break
            
        if not full_output.strip(): continue

        print(f"\n{Colors.MAGENTA}[⚡] GHENA is calculating attack vectors...{Colors.ENDC}")
        
        # 4. الحصول على التحليل
        start_time = time.time()
        analysis = get_strategy(chat, full_output, target_info)
        end_time = time.time()

        # 5. عرض النتائج بتنسيق احترافي
        print(f"\n{Colors.BOLD}{'—'*65}{Colors.ENDC}")
        # تلوين الأوامر المقترحة لجعلها بارزة
        formatted_analysis = analysis.replace("👉", f"{Colors.GREEN}{Colors.BOLD}👉{Colors.ENDC}{Colors.BOLD}")
        print(formatted_analysis)
        print(f"\n{Colors.BOLD}{'—'*65}{Colors.ENDC}")
        print(f"{Colors.CYAN}Processing Time: {round(end_time - start_time, 2)}s | Model: Gemini 1.5 Pro{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Session Terminated.{Colors.ENDC}")
