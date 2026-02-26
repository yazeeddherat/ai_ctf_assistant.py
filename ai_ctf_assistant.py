import os
import sys
import re
import time
import subprocess

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
#      {Colors.YELLOW}--- GHENA AI: THE ULTIMATE CTF AUTO-SOLVER ---{Colors.CYAN}         #
#            (No API Required - Platform Ready)                #
###############################################################{Colors.ENDC}
"""

# مخزن الأسئلة والحلول
QUESTIONS = []

def run_cmd(cmd):
    """تنفيذ أوامر النظام وعرض النتائج"""
    print(f"{Colors.YELLOW}[*] جاري تنفيذ: {cmd}{Colors.ENDC}")
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"{Colors.RED}[!] خطأ في التنفيذ: {e}{Colors.ENDC}")

def match_answer(data, category):
    """مطابقة البيانات مع أسئلة المنصة (THM, HTB, etc.)"""
    print(f"\n{Colors.HEADER}[🔍] جاري فحص المطابقة لـ ({category})...{Colors.ENDC}")
    found = False
    for i, q in enumerate(QUESTIONS):
        # منطق مطابقة بسيط بناءً على الكلمات المفتاحية
        if category.lower() in q.lower() or "answer" in q.lower() or "what" in q.lower():
            print(f"{Colors.GREEN}{Colors.BOLD}[🎯] احتمال حل للسؤال {i+1}:{Colors.ENDC}")
            print(f"{Colors.CYAN}السؤال: {q}{Colors.ENDC}")
            print(f"{Colors.GREEN}الحل المقترح: {data}{Colors.ENDC}")
            print("-" * 40)
            found = True
    if not found:
        print(f"{Colors.YELLOW}[i] تم استخراج ({data}) ولكن لم أجد سؤالاً مطابقاً له بعد.{Colors.ENDC}")

def analyze_engine(raw_text, target_ip):
    """المحرك الرئيسي لتحليل المخرجات"""
    
    # 1. كشف وكسر الهاشات تلقائياً (Hash Cracking)
    hash_list = {
        "MD5": r"\b[a-fA-F0-9]{32}\b",
        "SHA1": r"\b[a-fA-F0-9]{40}\b",
        "SHA256": r"\b[a-fA-F0-9]{64}\b"
    }
    
    for h_name, pattern in hash_list.items():
        match = re.search(pattern, raw_text)
        if match:
            h_val = match.group(0)
            print(f"\n{Colors.RED}[!] اكتشاف هاش {h_name}: {h_val}{Colors.ENDC}")
            match_answer(h_val, "Hash")
            
            if input(f"{Colors.YELLOW}[?] هل تريد كسر الهاش بـ John؟ (y/n): {Colors.ENDC}").lower() == 'y':
                with open("crack_me.txt", "w") as f: f.write(h_val)
                fmt = "--format=Raw-MD5" if h_name == "MD5" else ""
                run_cmd(f"john {fmt} --wordlist=/usr/share/wordlists/rockyou.txt crack_me.txt")
                res = subprocess.getoutput("john --show crack_me.txt")
                if ":" in res:
                    plain = res.split(":")[1].split()[0]
                    print(f"{Colors.GREEN}[+] تم الكسر! الباسورد هو: {plain}{Colors.ENDC}")
                    match_answer(plain, "Password")
            return

    # 2. تحليل المنافذ والخدمات (Nmap Analysis)
    ports = re.findall(r"(\d+)/tcp\s+open\s+([\w-]+)", raw_text)
    if ports:
        for p_num, s_name in ports:
            print(f"{Colors.CYAN}[+] منفذ مكتشف: {p_num} ({s_name}){Colors.ENDC}")
            match_answer(p_num, "Port")
            match_answer(s_name, "Service")
        
        # اقتراح هجوم تلقائي
        if "80" in [p[0] for p in ports]:
            if input(f"{Colors.YELLOW}[?] هل أشغل Gobuster للبحث عن مسارات مخفية؟ (y/n): {Colors.ENDC}").lower() == 'y':
                run_cmd(f"gobuster dir -u http://{target_ip} -w /usr/share/wordlists/dirb/common.txt -q")

    # 3. كشف الـ Flags (THM{...}, HTB{...}, etc.)
    flags = re.findall(r"([a-zA-Z0-9]+{[^}]+})", raw_text)
    if flags:
        for f in flags:
            print(f"{Colors.GREEN}[🚩] مبروك! تم العثور على Flag: {f}{Colors.ENDC}")
            match_answer(f, "Flag")

def main():
    os.system('clear')
    print(BANNER)

    # المرحلة 1: إدخال الأسئلة
    print(f"{Colors.BOLD}أولاً: أدخل أسئلة اللاب (سؤال لكل سطر، اضغط Enter مرتين للبدء):{Colors.ENDC}")
    while True:
        q_input = input(f"{Colors.CYAN}سؤال {len(QUESTIONS)+1}: {Colors.ENDC}")
        if q_input == "": break
        QUESTIONS.append(q_input)

    target_ip = input(f"\n{Colors.BOLD}ثانياً: أدخل IP الهدف: {Colors.ENDC}")
    print(f"\n{Colors.GREEN}[+] النظام جاهز. غنى تراقب مخرجاتك الآن...{Colors.ENDC}")

    # المرحلة 2: المراقبة والتحليل
    while True:
        print(f"\n{Colors.YELLOW}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}الصق مخرجات الأدوات (Nmap, Gobuster, إلخ) هنا:{Colors.ENDC}")
        
        buffer = []
        while True:
            try:
                line = input()
                if line.lower() == 'exit': sys.exit()
                if line == '': break
                buffer.append(line)
            except EOFError: break
        
        data = "\n".join(buffer)
        if data.strip():
            analyze_engine(data, target_ip)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] إيقاف النظام.{Colors.ENDC}")
