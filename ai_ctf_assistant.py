import google.generativeai as genai
import os
import sys
import datetime

# --- الإعدادات ---
API_KEY = "ضع_مفتاحك_هنا"

# إعداد الألوان
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- تهيئة الموديل (تعديل الإصدار هنا) ---
try:
    genai.configure(api_key=API_KEY)
    # قمت بتغييره من pro إلى flash ليعمل عندك فوراً
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

def main():
    os.system('clear')
    print(f"{Colors.HEADER}=== GHENA AI | STABLE VERSION ==={Colors.ENDC}\n")

    target_ip = input("[?] Target IP: ")
    
    while True:
        print(f"\n{Colors.WARNING}الصق المخرجات هنا (Enter مرتين للتحليل):{Colors.ENDC}")
        user_input = []
        while True:
            line = input()
            if line.lower() == 'exit': sys.exit()
            if line == '': break 
            user_input.append(line)
        
        raw_data = "\n".join(user_input)
        if not raw_data.strip(): continue

        print(f"\n{Colors.OKBLUE}[*] جاري التحليل...{Colors.ENDC}")
        response = model.generate_content(f"Target: {target_ip}\nAnalyze this:\n{raw_data}")
        print(f"\n{Colors.OKGREEN}🤖 التوجيهات:{Colors.ENDC}\n{response.text}")

if __name__ == "__main__":
    main()
