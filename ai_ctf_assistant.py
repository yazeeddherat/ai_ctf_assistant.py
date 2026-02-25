import google.generativeai as genai
import os
import datetime
import sys

# --- الإعدادات (Settings) ---
# ضع مفتاح API الخاص بك هنا
API_KEY = "ضع_مفتاحك_هنا"

# إعداد الألوان للـ Terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- إعداد الذكاء الاصطناعي (نسخة البحث التلقائي) ---
try:
    genai.configure(api_key=API_KEY)
    
    # البحث عن الموديلات المتاحة في حسابك لتجنب خطأ 404
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_models:
        print(f"{Colors.FAIL}[!] لا توجد موديلات متاحة لهذا المفتاح.{Colors.ENDC}")
        sys.exit()
    
    # اختيار الموديل المتاح (يفضل flash إذا وجد وإلا يأخذ المتاح)
    selected_model = next((m for m in available_models if "flash" in m), available_models[0])
    model = genai.GenerativeModel(selected_model)
    
except Exception as e:
    print(f"{Colors.FAIL}[!] خطأ في الاتصال: {e}{Colors.ENDC}")
    sys.exit()

def save_to_report(data):
    with open("ctf_report.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.datetime.now()} ---\n")
        f.write(data + "\n")

def get_ai_guidance(user_input, target_info):
    prompt = f"""
    أنت خبير Pentesting في تحديات CTF.
    بيانات الهدف الحالية: {target_info}
    قم بتحليل المخرجات التالية واقترح الخطوة القادمة بأمر محدد '👉 اكتب هذا الأمر:'.
    المخرجات:
    {user_input}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"خطأ أثناء توليد الرد: {e}"

def main():
    os.system('clear')
    print(f"{Colors.HEADER}{Colors.BOLD}=== 🛡️ AI CTF MENTOR (Auto-Model Version) ==={Colors.ENDC}")
    print(f"{Colors.OKGREEN}[+] تم استخدام الموديل: {selected_model}{Colors.ENDC}\n")

    target_ip = input(f"{Colors.BOLD}[?] أدخل IP الهدف: {Colors.ENDC}")
    platform = input(f"{Colors.BOLD}[?] المنصة (THM / HTB): {Colors.ENDC}")
    
    target_info = f"IP: {target_ip}, Platform: {platform}"
    
    print(f"\n{Colors.OKGREEN}[*] الخطوة الأولى:{Colors.ENDC}")
    print(f"👉 اكتب هذا الأمر: {Colors.BOLD}nmap -sV -sC -Pn {target_ip}{Colors.ENDC}")

    while True:
        print(f"\n{Colors.WARNING}--------------------------------------------------{Colors.ENDC}")
        print(f"الصق مخرجات الأمر هنا (اضغط Enter مرتين للتحليل):")
        
        user_output = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break 
            user_output.append(line)
        
        full_output = "\n".join(user_output)
        if not full_output.strip(): continue

        print(f"\n{Colors.OKBLUE}[*] جاري التحليل الذكي...{Colors.ENDC}")
        guidance = get_ai_guidance(full_output, target_info)
        print(f"\n{Colors.OKGREEN}🤖 توجيهات المدرب:{Colors.ENDC}\n{guidance}")
        save_to_report(f"Analysis for {target_ip}:\n{guidance}")

if __name__ == "__main__":
    main()
