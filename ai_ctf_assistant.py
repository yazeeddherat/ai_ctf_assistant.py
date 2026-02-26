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
    findings
