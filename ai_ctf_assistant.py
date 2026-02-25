import google.generativeai as genai
import os
import datetime
import sys

# --- الإعدادات (Settings) ---
# استبدل هذا بمفتاح API الخاص بك أو ضعه كمتغير بيئة
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# إعداد الألوان للـ Terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- إعداد الذكاء الاصطناعي ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"{Colors.FAIL}[!] خطأ في إعداد API: {e}{Colors.ENDC}")
    sys.exit()

def save_to_report(data):
    """حفظ الخطوات في ملف تقرير خارجي"""
    with open("ctf_report.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.datetime.now()} ---\n")
        f.write(data + "\n")

def get_ai_guidance(user_input, target_info):
    """إرسال البيانات لـ Gemini والحصول على التوجيه"""
    prompt = f"""
    أنت خبير Pentesting مختص في تحديات CTF (مثل TryHackMe و HTB).
    بيانات الهدف الحالية: {target_info}
    
    المطلوب منك:
    1. تحليل مخرجات الأدوات التي سيزودك بها المستخدم.
    2. تحديد الثغرات المحتملة (Vulnerabilities).
    3. إعطاء أمر محدد (Command) لينفذه المستخدم في الخطوة التالية.
    4. اشرح "لماذا" اخترنا هذا الأمر باختصار شديد.
    
    قاعدة صارمة: ابدأ دائماً بـ '👉 اكتب هذا الأمر:' متبوعاً بالكود.
    
    المخرجات الحالية للتحليل:
    {user_input}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"خطأ في الاتصال بالذكاء الاصطناعي: {e}"

def main():
    os.system('clear')
    print(f"{Colors.HEADER}{Colors.BOLD}=== 🛡️ AI CTF MENTOR v1.0 ==={Colors.ENDC}")
    print(f"{Colors.OKBLUE}أداة تعليمية لحل التحديات باستخدام الذكاء الاصطناعي{Colors.ENDC}\n")

    target_ip = input(f"{Colors.BOLD}[?] أدخل IP الهدف: {Colors.ENDC}")
    platform = input(f"{Colors.BOLD}[?] المنصة (THM / HTB / Other): {Colors.ENDC}")
    
    target_info = f"IP: {target_ip}, Platform: {platform}"
    
    # البداية الافتراضية
    print(f"\n{Colors.OKGREEN}[*] الخطوة الأولى المقترحة:{Colors.ENDC}")
    first_cmd = f"nmap -sV -sC -Pn {target_ip}"
    print(f"👉 اكتب هذا الأمر: {Colors.BOLD}{first_cmd}{Colors.ENDC}")
    
    save_to_report(f"Target: {target_info}\nStarting with: {first_cmd}")

    while True:
        print(f"\n{Colors.WARNING}--------------------------------------------------{Colors.ENDC}")
        print(f"انسخ مخرجات الأمر (Output) هنا، أو اكتب 'exit' للإغلاق:")
        user_output = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break # اضغط Enter مرتين للإرسال
            user_output.append(line)
        
        full_output = "\n".join(user_output)
        
        if not full_output.strip():
            continue

        print(f"\n{Colors.OKBLUE}[*] جاري تحليل البيانات بواسطة Gemini AI...{Colors.ENDC}")
        
        guidance = get_ai_guidance(full_output, target_info)
        
        print(f"\n{Colors.OKGREEN}🤖 توجيهات المدرب الذكي:{Colors.ENDC}")
        print(guidance)
        
        # حفظ السجل
        save_to_report(f"User Output Analysis:\n{full_output}\n\nAI Guidance:\n{guidance}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] تم إغلاق الأداة.{Colors.ENDC}")
