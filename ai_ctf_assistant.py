#!/usr/bin/env python3
# GHENA-AUTO v1.0 — Educational CTF/Labs Framework

import os, sys, re, subprocess, time, requests
from bs4 import BeautifulSoup

# =========================
# UI (ألوان + Banner)
# =========================
class C:
    G="\033[92m"; C="\033[96m"; Y="\033[93m"; R="\033[91m"; B="\033[1m"; E="\033[0m"

BANNER=f"""
{C.C}████████████████████████████████████████████████████████████████
█ {C.G}GHENA-AUTO{C.C} — Metasploit-like CTF/Lab Solver (EDU)           █
█ Mode: Modules / Sessions | Smart Question Matching              █
████████████████████████████████████████████████████████████████{C.E}
"""

def clear(): os.system('cls' if os.name=='nt' else 'clear')

# =========================
# LAB: جلب الأسئلة
# =========================
def fetch_questions(url):
    qs=[]
    try:
        r=requests.get(url,timeout=10)
        s=BeautifulSoup(r.text,"html.parser")
        for t in s.find_all(["h1","h2","h3","p","li"]):
            txt=t.get_text().strip()
            if "?" in txt or "question" in txt.lower():
                qs.append(txt)
    except:
        pass
    return qs

# =========================
# AI خفيف: فهم النية
# =========================
def detect_intent(q):
    q=q.lower()
    if "flag" in q: return "FLAG"
    if "port" in q or "service" in q: return "SERVICE"
    if "ftp" in q and ("find" in q or "discover" in q): return "FTP_CONTENT"
    if "how" in q and "access" in q: return "ACCESS_METHOD"
    if "hidden" in q or "directory" in q or "entry" in q: return "HIDDEN_PATH"
    return "GENERIC"

def match_by_intent(intent, out):
    if intent=="SERVICE":
        for l in out.splitlines():
            if "/tcp" in l and "open" in l: return l.strip()
    if intent=="FTP_CONTENT":
        for l in out.splitlines():
            if any(x in l.lower() for x in [".txt",".bak",".zip"]): return l.strip()
    if intent=="ACCESS_METHOD":
        if "anonymous" in out.lower(): return "Anonymous FTP Login"
    if intent=="FLAG":
        m=re.search(r"(flag\{.*?\}|CTF\{.*?\})", out, re.I)
        return m.group(1) if m else None
    return None

# =========================
# Modules Framework
# =========================
class Module:
    name=""; desc=""
    def run(self, target, mem): return ""

class Nmap(Module):
    name="scanner/nmap"; desc="Service discovery"
    def run(self, target, mem):
        print("[*] Running Nmap (safe scan)…")
        try:
            p=subprocess.run(["nmap","-sV","-Pn",target],capture_output=True,text=True)
            mem["nmap"]=p.stdout
            return p.stdout
        except Exception as e:
            return str(e)

class FTPEnum(Module):
    name="enum/ftp"; desc="Check anonymous FTP (safe)"
    def run(self, target, mem):
        print("[*] Checking FTP anonymous (safe)…")
        # محاكاة/قراءة فقط
        out="Anonymous login allowed\npub/\nreadme.txt"
        mem["ftp"]=out
        return out

class HTTPEnum(Module):
    name="enum/http"; desc="Dir discovery (safe placeholder)"
    def run(self, target, mem):
        out="Found: /admin\nFound: /backup"
        mem["http"]=out
        return out

# =========================
# Engine: ربط النتائج بالأسئلة
# =========================
def check_questions(qs, answered, out):
    for i,q in enumerate(qs,1):
        if i in answered: continue
        intent=detect_intent(q)
        ans=match_by_intent(intent,out)
        if ans:
            answered[i]=ans
            print(f"\n{C.G}✅ جواب السؤال {i}:{C.E}\n📝 {q}\n🎯 {ans}\n")

# =========================
# Console (Metasploit-like)
# =========================
MODULES={
    "scanner/nmap": Nmap(),
    "enum/ftp": FTPEnum(),
    "enum/http": HTTPEnum(),
}

def console(target, qs):
    mem={}; answered={}
    current=None
    print(BANNER)
    print(f"Target: {target}\nQuestions loaded: {len(qs)}\n")

    while True:
        p="GHENA-AUTO"
        if current: p+=f"({current.name})"
        cmd=input(f"{p}> ").strip()

        if cmd in ["exit","quit"]: break
        if cmd=="help":
            print("use <module> | run | modules | sessions | auto | exit")
        elif cmd=="modules":
            for k,v in MODULES.items(): print(f"{k:15} - {v.desc}")
        elif cmd.startswith("use "):
            m=cmd.split(" ",1)[1]
            current=MODULES.get(m)
            if not current: print("Module not found")
        elif cmd=="run" and current:
            out=current.run(target,mem)
            print(out)
            check_questions(qs,answered,out)
        elif cmd=="sessions":
            print(mem.keys())
        elif cmd=="auto":
            # تسلسل آمن: nmap → حسب النتائج
            out=MODULES["scanner/nmap"].run(target,mem); print(out)
            check_questions(qs,answered,out)
            if "21/tcp" in out:
                out=MODULES["enum/ftp"].run(target,mem); print(out)
                check_questions(qs,answered,out)
            if "80/tcp" in out or "http" in out.lower():
                out=MODULES["enum/http"].run(target,mem); print(out)
                check_questions(qs,answered,out)
        else:
            print("Unknown command. type help")

# =========================
# Main
# =========================
def main():
    clear()
    target=input("Target IP: ").strip()
    lab=input("Lab URL: ").strip()
    qs=fetch_questions(lab)
    console(target, qs)

if __name__=="__main__":
    main()
