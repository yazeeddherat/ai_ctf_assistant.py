import google.generativeai as genai
import os
import datetime
import sys
import time

# --- الإعدادات المتقدمة للمحرك الذكي ---
API_KEY = "ضـع_مفـتاحك_هنـا"

# إعدادات لضمان أعلى مستويات الدقة التقنية
generation_config = {
    "temperature": 0.1,  # تركيز عالٍ جداً على الدقة التقنية
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# تعطيل الفلاتر للسماح بتحليل الثغرات الأمنية (لأغراض تعليمية وقانونية فقط)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

try:
    genai.configure(api_key=API_KEY)
    # استخدام Gemini 1.5 Pro للتحليل العميق وربط المعلومات المعقدة
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    chat = model.start_chat(history=[])
except Exception as e:
    print(f"{Colors.FAIL}[!] فشل في تشغيل المحرك العصبي: {e}{Colors.ENDC}")
    sys.exit()

def get_strategic_advice(user_data, target_info):
    # نظام التعليمات للذكاء الاصطناعي (System Prompt)
    system_instruction = f"""
    [ROLE: Senior Red Team Lead & Exploit Developer]
    [TARGET: {target_info}]
    
    أنت لست مجرد مساعد، أنت المحلل الاستراتيجي للعملية.
    مهمتك:
    1. ربط المخرجات ببعضها (Correlation). إذا وجدنا مستخدماً في FTP، جربه في SSH.
    2. البحث عن CVEs المرتبطة بالإصدارات المكتشفة.
    3. تقديم "خطة اختراق" (Exploitation Path) واضحة.
    
    نموذج الرد:
    ---
    🎯 التحليل الاستراتيجي: (اشرح ماذا وجدت وماذا يعني تقنياً)
    🛡️ نقاط الضعف المكتشفة: (قائمة بالثغرات المحتملة)
    🚀 الأوامر المقترحة:
       👉 [الأمر الأول] # الهدف من الأمر
       👉 [الأمر الثاني] # الهدف من الأمر
    ⚠️ تنبيه أمني: (تحذير من حظر أو تعليق خدمة)
    ---
    """
    
    try:
        response = chat.send_message(f"{system_instruction}\n\nالمخرجات الجديدة من المختبر:\n{user_data}")
        return response.text
    except Exception as e:
        return f"حدث خطأ في معالجة البيانات: {e}"

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════════════════════════╗")
    print(f"║       🧠 AI NEURAL PENTESTER - STRATEGIC ENGINE v5.0       ║")
    print(f"╚════════════════════════════════════════════════════════════╝{Colors.ENDC}")

    ip = input(f"{Colors.CYAN}[?] IP الهدف: {Colors.ENDC}")
    platform = input(f"{Colors.CYAN}[?] المنصة (HTB/THM): {Colors.ENDC}")
    target_info = f"IP: {ip}, Platform: {platform}"

    print(f"\n{Colors.GREEN}[+] تم تفعيل المحرك الاستنتاجي لـ {ip}. بانتظار البيانات...{Colors.ENDC}")

    while True:
        print(f"\n{Colors.BLUE}📋 الصق مخرجات الأداة (أو اكتب 'exit' للخروج):{Colors.ENDC}")
        
        user_lines = []
        while True:
            line = sys.stdin.readline().rstrip()
            if line == '': break
            user_lines.append(line)
        
        full_output = "\n".join(user_lines)
        if full_output.lower() == 'exit': break
        if not full_output.strip(): continue

        print(f"\n{Colors.WARNING}[⚡] جاري تحليل البيانات وبحث الثغرات...{Colors.ENDC}")
        
        start_time = time.time()
        advice = get_strategic_advice(full_output, target_info)
        end_time = time.time()

        # عرض النتائج بتنسيق احترافي
        print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
        formatted_advice = advice.replace("👉", f"{Colors.GREEN}{Colors.BOLD}👉{Colors.ENDC}{Colors.BOLD}")
        print(formatted_advice)
        print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.CYAN}⏱️ وقت التحليل: {round(end_time - start_time, 2)} ثانية{Colors.ENDC}")

        # حفظ الجلسة للرجوع إليها لاحقاً
        with open(f"session_log_{ip.replace('.', '_')}.md", "a", encoding="utf-8") as f:
            f.write(f"\n### تحليل بتاريخ {datetime.datetime.now()}\n{advice}\n")

if __name__ == "__main__":
    main()
