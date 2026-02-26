import google.generativeai as genai
import os
import sys

# --- [ الإعدادات ] ---
# ضع مفتاحك الجديد هنا (الذي ينتهي بـ 4gY)
API_KEY = "AIzaSyDmm3sH2JC4PJDLJwUP47DQbX3zqCrcNDA"

def main():
    # تنظيف الشاشة لواجهة احترافية
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("\033[96m" + "="*50)
    print("   GHENA AI | THE ERROR-FREE TERMINAL EDITION")
    print("="*50 + "\033[0m")

    try:
        # الربط مع جوجل
        genai.configure(api_key=API_KEY)
        
        # اختيار الموديل الأكثر استقراراً (Flash 1.5)
        # استخدمنا الإعداد الافتراضي لتجنب خطأ 404 اللي ظهر بصورك
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("\033[93m[*] جاري فحص استجابة الـ API...\033[0m")
        
        # طلب تجريبي بسيط
        response = model.generate_content("Are you ready for CTF?")
        
        print("\033[92m[+] تم الاتصال بنجاح! المحرك يعمل 100%.\033[0m")
        print(f"\033[94m🤖 رد غنى: {response.text}\033[0m")
        print("\n\033[95m[!] ابدأ الآن بلصق مخرجات اللاب (Nmap, Hydra...).\033[0m")

        # حلقة التحليل اللانهائية
        while True:
            print("\n" + "-"*30)
            user_input = input("\033[93mالصق المخرج هنا (أو اكتب exit للخروج): \033[0m")
            if user_input.lower() == 'exit': break
            
            # تحليل ذكي سريع
            analysis = model.generate_content(f"تحلل هذا المخرج واستخرج أي باسوورد أو جواب للاب: {user_input}")
            print(f"\n\033[92m🎯 التحليل:\n{analysis.text}\033[0m")

    except Exception as e:
        print(f"\033[91m[!] حدث خطأ: {e}\033[0m")
        print("\033[93m💡 حل سريع: تأكد من تشغيل 'pip install -U google-generativeai'\033[0m")

if __name__ == "__main__":
    main()
