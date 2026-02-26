import os
import sys
import re
import subprocess
import time

# --- [ إعدادات الألوان والواجهة ] ---
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    HEADER = '\033[95m'
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
#         {Colors.YELLOW}--- GHENA AI: AUTOMATIC PASSWORD FINDER ---{Colors.CYAN}         #
#            (No API - Offline Intelligent Analysis)           #
###############################################################{Colors.ENDC}
"""

QUESTIONS = []

def run_cmd(cmd):
    """تنفيذ أوامر النظام"""
    print(f"{Colors.YELLOW}[*] جاري تنفيذ: {cmd}{Colors.ENDC}")
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"{Colors.RED}[!] خطأ في التنفيذ: {e}{Colors.ENDC}")

def extract_potential_answers(text):
    """محرك استخراج اليوزرات، الباسوردات، والهاشات من النصوص"""
    findings = {
        "Password/Key": [],
        "User/Login": [],
        "Hash": [],
        "Flag": []
    }
    
    # 1. البحث عن الهاشات (MD5, SHA1)
    hashes = re.findall(r"\b([a-fA-F0-9]{32}|[a-fA-F0-9]{40})\b", text)
    findings["Hash"].extend(hashes)
    
    # 2. البحث عن كلمات مرور في ملفات الإعدادات (config, database, logs)
    # يبحث عن pass=... أو password: ... أو 'db_password' => '...'
    pass_patterns = [
        r"(?:pass|password|pwd|key|secret)\s*[:=]\s*['\"]?([\w!@#$%^&*.-]+)['\"]?",
        r"(?:user|username|login)\s*[:=]\s*['\"]?([\w.-]+)['\"]?"
    ]
    for p in pass_patterns:
        matches = re.findall(p, text, re.IGNORECASE)
        if "user" in p: findings["User/Login"].extend(matches)
        else: findings["Password/Key"].extend(matches)
        
    # 3. البحث عن صيغة الـ Flags (THM{...}, HTB{...}, picoCTF{...})
    flags = re.findall(r"([a-zA-Z0-9_-]+{[^}]+})", text)
    findings["Flag"].extend(flags)
    
    return findings

def match_and_solve(extracted_data):
    """ربط البيانات المستخرجة بأسئلة اللاب"""
    print(f"\n{Colors.HEADER}[🔍] تحليل غنى للبيانات المستخرجة...{Colors.ENDC}")
    
    for category, values in extracted_data.items():
        for val in list(set(values)): # عرض القيم الفريدة فقط
            print(f"{Colors.GREEN}[+] تم العثور على {category}: {Colors.BOLD}{val}{Colors.ENDC}")
            
            # محاولة الربط بالأسئلة
            for i, q in enumerate(QUESTIONS):
                # إذا كان السؤال يطلب 'password' ووجدنا قيمة تشبهها
                if category.split("/")[0].lower() in q.lower() or "answer" in q.lower():
                    print(f"{Colors.CYAN}   🎯 حل محتمل للسؤال {i+1} ({q}): {Colors.GREEN}{val}{Colors.ENDC}")

def main():
    os.system('clear')
    print(BANNER)
    
    # المرحلة 1: تغذية الأسئلة
    print(f"{Colors.BOLD}1. أدخل أسئلة اللاب (سؤال لكل سطر، اضغط Enter مرتين للبدء):{Colors.ENDC}")
    while True:
        q_in = input(f"{Colors.CYAN}سؤال {len(QUESTIONS)+1}: {Colors.ENDC}")
        if q_in == "": break
        QUESTIONS.append(q_in)
    
    target_ip = input(f"\n{Colors.BOLD}2. أدخل IP الهدف (اختياري): {Colors.ENDC}")
    print(f"\n{Colors.GREEN}[+] تم حفظ {len(QUESTIONS)} مهمة. غنى جاهزة للصيد!{Colors.ENDC}")

    # المرحلة 2: التحليل المستمر
    while True:
        print(f"\n{Colors.YELLOW}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}الصق مخرجات الأدوات أو محتوى الملفات هنا للتحليل:{Colors.ENDC}")
        
        buffer = []
        while True:
            try:
                line = input()
                if line.lower() == 'exit': sys.exit()
                if line == '': break
                buffer.append(line)
            except EOFError: break
        
        raw_text = "\n".join(buffer)
        if not raw_text.strip(): continue

        # استخراج البيانات
        data_found = extract_potential_answers(raw_text)
        
        # ربط البيانات بالأسئلة
        match_and_solve(data_found)
        
        # ميزة الكسر التلقائي للهاشات إذا وجدت
        if data_found["Hash"]:
            if input(f"\n{Colors.RED}[?] وجدنا هاشات، هل تريد كسرها بـ John؟ (y/n): {Colors.ENDC}").lower() == 'y':
                with open("h.txt", "w") as f: f.write(data_found["Hash"][0])
                run_cmd(f"john --wordlist=/usr/share/wordlists/rockyou.txt h.txt")
                res = subprocess.getoutput("john --show h.txt")
                if ":" in res:
                    cracked = res.split(":")[1].split()[0]
                    print(f"{Colors.GREEN}[✅] الباسورد الصافي هو: {cracked}{Colors.ENDC}")
                    match_and_solve({"Cracked Password": [cracked]})

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] إغلاق البرنامج.{Colors.ENDC}")
