import google.generativeai as genai
import os
import datetime
import sys
import time
import subprocess

# --- الإعدادات (Settings) ---
# ضع مفتاح API الخاص بك هنا
API_KEY = "ضـع_مفـتاحك_هنـا"

# إعداد الألوان للـ Terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'

# الشعار المخصص باسم GHENA
BANNER = r"""
  ________  ___  ___  _______   ________   ________     
 |\   ____\|\  \|\  \|\  ___ \ |\   ___  \|\   __  \    
 \ \  \___|\ \  \\\  \ \   __/|\ \  \\ \  \ \  \|\  \   
  \ \  \  __\ \   __  \ \  \_|/_\ \  \\ \  \ \   __  \  
   \ \  \|\  \ \  \ \  \ \  \_|\ \ \  \\ \  \ \  \ \  \ 
    \ \_______\ \__\ \__\ \_______\ \__\\ \__\ \__\ \__\
     \|_______|\|__|\|__|\|_______|\|__| \|__|\|__|\|__|
            GHENA AI | ULTIMATE PENTEST STRATEGIST
"""

# --- إعداد الذكاء الاصطناعي مع الضبط المتقدم ---
try:
    genai.configure(api_key=API_KEY)
    
    # 1. إعدادات التوليد (Generation Config) لضمان الدقة التقنية
    generation_config = {
        "temperature": 0.2,       # تقليل العشوائية للحصول على أوامر دقيقة
        "top_p": 0.95,
        "max_output_tokens": 4096,
    }

    # 2. إعدادات الأمان (Safety Settings) لمنع حظر محتوى الأمن السيبراني
    safety_settings = [
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    ]
    
    # البحث عن الموديلات المتاحة تلقائياً
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if not available_models:
        print(f"{Colors.FAIL}[!] لا توجد موديلات متاحة لهذا المفتاح.{Colors.ENDC}")
        sys.exit()
    
    selected_model = next((m for m in available_models if "flash" in m), available_models[0])
    
    # بناء الموديل بالإعدادات المتقدمة
    model = genai.GenerativeModel(
        model_name=selected_model,
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
except Exception as e:
    print(f"{Colors.FAIL}[!] خطأ في التهيئة: {e}{Colors.ENDC}")
    sys.exit()

def save_to_report(data):
    with open("ghena_report.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.datetime.now()} ---\n")
        f.write(data + "\n")

def get_ai_guidance(user_input, target_info):
    prompt = f"""
    [ROLE: GHENA AI PENTEST EXPERT]
    بيانات الهدف: {target_info}
    حلل مخرجات الأدوات التالية بدقة عالية:
    {user_input}
    
    المطلوب:
    1. استخراج المنافذ والخدمات المكتشفة.
    2. اقتراح الخطوة القادمة بأمر محدد يبدأ بـ '👉 اكتب هذا الأمر:'.
    3. شرح سبب اختيار هذا الهجوم باللغة العربية.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالدماغ العصبي: {e}"

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.CYAN}{Colors.BOLD}{BANNER}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[+] تم تفعيل المحرك الذكي: {selected_model}{Colors.ENDC}\n")

    target_ip = input(f"{Colors.BOLD}[?] أدخل IP الهدف: {Colors.ENDC}")
    platform = input(f"{Colors.BOLD}[?] المنصة (THM / HTB): {Colors.ENDC}")
    target_info
