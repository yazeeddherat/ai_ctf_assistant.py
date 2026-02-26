import google.generativeai as genai
import os
import sys

# --- [ الإعدادات ] ---
# ضع المفتاح الذي ظهر في الصورة هنا
API_KEY = "AIzaSyCf6jw6eM5kqTPwfRnHNZiR1i0dMcH_4gY"

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[96m[*] GHENA AI: جاري تشغيل المحرك وفحص الاتصال بالـ API...\033[0m")
    
    try:
        # تهيئة الإعدادات
        genai.configure(api_key=API_KEY)
        
        # استخدام الموديل flash بشكل مباشر لتجنب أخطاء الإصدارات (v1beta)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # تجربة إرسال طلب اختبار للسيرفر
        print("\033[93m[*] جاري التحقق من صلاحية المفتاح والوقت...\033[0m")
        response = model.generate_content("Ping")
        
        if response.text:
            print("\033[92m[+] نجاح! تم تفعيل GHENA AI بنجاح.\033[0m")
            print(f"\033[94m🤖 رد النظام: {response.text}\033[0m")
            print("\n\033[95m[!] يمكنك الآن البدء بحل اللاب واستخراج الباسوردات.\033[0m")

    except Exception as e:
        print(f"\033[91m[!] خطأ فني: {e}\033[0m")
        if "404" in str(e):
            print("\033[33m💡 تنبيه: الكود يحتاج لتحديث مكتبة جوجل. نفذ الخطوة رقم 1 أعلاه.\033[0m")
        elif "API_KEY_INVALID" in str(e):
            print("\033[33m💡 تنبيه: تأكد من نسخ المفتاح كاملاً من Google AI Studio.\033[0m")

if __name__ == "__main__":
    main()
