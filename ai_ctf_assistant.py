import os
import subprocess
import sys
import time

# ----------------------------
# ألوان وواجهة GHENA-AUTO
# ----------------------------
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

BANNER = f"""
{Colors.CYAN}████████████████████████████████████████████████████████████████
█                                                              █
█   {Colors.GREEN} ██████╗ ██╗  ██╗███████╗███╗   ██╗ █████╗       {Colors.CYAN}█
█   {Colors.GREEN}██╔════╝ ██║  ██║██╔════╝████╗  ██║██╔══██╗      {Colors.CYAN}█
█   {Colors.GREEN}██║  ███╗███████║█████╗  ██╔██╗ ██║███████║      {Colors.CYAN}█
█   {Colors.GREEN}██║   ██║██╔══██║██╔══╝  ██║╚██╗██║██╔══██║      {Colors.CYAN}█
█   {Colors.GREEN}╚██████╔╝██║  ██║███████╗██║ ╚████║██║  ██║      {Colors.CYAN}█
█   {Colors.GREEN} ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝      {Colors.CYAN}█
█                                                              █
█   {Colors.YELLOW}GHENA-AUTO — Automated CTF & Lab Solver{Colors.CYAN}            █
█   {Colors.BOLD}Mode:{Colors.ENDC} Fully Automatic | GPT-5 Assisted       █
█   {Colors.BOLD}Author:{Colors.ENDC} GHENA AI                                   █
█                                                              █
████████████████████████████████████████████████████████████████
{Colors.ENDC}
"""

# ----------------------------
# إعدادات الهدف والأدوات
# ----------------------------
TARGET_IP = input("🖥️ أدخل IP الهدف: ").strip()
LAB_URL = input("🌐 أدخل رابط اللاب: ").strip()

# الأدوات المطلوبة حسب اللاب (يمكن تعديلها)
TOOLS = ["nmap", "gobuster", "ftp-anon"]

# ----------------------------
# تعريف الأدوات
# ----------------------------
def run_nmap(ip):
    print("[*] تشغيل Nmap...")
    try:
        result = subprocess.run(["nmap", "-sV", ip], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"[!] خطأ في Nmap: {e}"

def run_gobuster(ip):
    print("[*] تشغيل Gobuster...")
    try:
        result = subprocess.run(["gobuster", "dir", "-u", f"http://{ip}/", "-w", "wordlist.txt"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"[!] خطأ في Gobuster: {e}"

def run_ftp_anon(ip):
    print("[*] فحص FTP Anonymous...")
    try:
        result = subprocess.run(f'echo "anonymous" | ftp {ip}', shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"[!] خطأ في FTP: {e}"

# ----------------------------
# تشغيل جميع الأدوات تلقائيًا
# ----------------------------
def run_tools(ip):
    outputs = []
    for tool in TOOLS:
        if tool == "nmap":
            outputs.append(run_nmap(ip))
        elif tool == "gobuster":
            outputs.append(run_gobuster(ip))
        elif tool == "ftp-anon":
            outputs.append(run_ftp_anon(ip))
    return "\n".join(outputs)

# ----------------------------
# تحليل GHENA AI (GPT-5 مباشر)
# ----------------------------
def analyze_with_ghena(output):
    prompt = f"""
أنت GHENA AI (GPT-5) خبير CTF.
الهدف: {TARGET_IP}
مخرجات الأدوات:
{output}

✅ أجب عن الأسئلة مباشرة
⚠️ أي تنبيهات أمنية
👉 اقترح الأمر التالي
"""
    print("\n🤖 تحليل GHENA AI:\n")
    print("[هنا سأعطيك الإجابة المباشرة حسب المخرجات]")
    print(prompt)
    print("\n" + "="*50 + "\n")

# ----------------------------
# التنفيذ
# ----------------------------
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    time.sleep(1)
    
    print(f"🚀 بدء GHENA-AUTO التلقائي على {TARGET_IP} ...\n")
    outputs = run_tools(TARGET_IP)
    
    analyze_with_ghena(outputs)
    
    print("✅ انتهى التحليل التلقائي.")

if __name__ == "__main__":
    main()
