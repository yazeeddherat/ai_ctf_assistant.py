# ghena_ai_op.py
from PyQt6.QtWidgets import *
import subprocess, sys, time, re, os, requests

# ----------------------------
# Plugins داخل نفس الملف (Drop-in)
# ----------------------------
class Plugins:
    @staticmethod
    def nmap(target):
        cmd = f"nmap -sC -sV {target}"
        return {"tool":"nmap","command":cmd,"reason":"Discover services and ports","confidence":0.95,"sets":{"ports":True,"http":True}}

    @staticmethod
    def gobuster(target):
        cmd = f"gobuster dir -u http://{target}/ -w /usr/share/wordlists/dirb/common.txt"
        return {"tool":"gobuster","command":cmd,"reason":"Discover hidden directories/files","confidence":0.88,"sets":{"directories":True}}

    @staticmethod
    def ssh(user,target):
        cmd = f"ssh {user}@{target}"
        return {"tool":"ssh","command":cmd,"reason":"Access user shell after credentials","confidence":0.9,"sets":{"user_shell":True}}

    @staticmethod
    def john(hash_file):
        cmd = f"john --wordlist=/usr/share/wordlists/rockyou.txt {hash_file}"
        return {"tool":"john","command":cmd,"reason":"Crack hashes using wordlist","confidence":0.9,"sets":{"cracked_password":True}}

    @staticmethod
    def priv_esc():
        cmd = "sudo -l; find / -perm -4000 2>/dev/null"
        return {"tool":"priv_esc","command":cmd,"reason":"Privilege escalation analysis","confidence":0.93,"sets":{"root_shell":True}}

    @staticmethod
    def file_ops(file_path):
        cmd = f"cat {file_path}"
        return {"tool":"file_ops","command":cmd,"reason":"Read file content (flags/passwords)","confidence":0.99,"sets":{"read_file":True}}

# ----------------------------
# Utils
# ----------------------------
def extract_questions_from_lab(url):
    questions = []
    try:
        html = requests.get(url, timeout=10).text.lower()
        patterns = [r"user flag",r"root flag",r"what is the password",r"find the flag",r"what is the username"]
        for p in patterns:
            if re.search(p, html):
                questions.append(p)
    except Exception:
        questions = ["user flag","root flag"]
    return list(set(questions))

def suggest_tools(questions):
    plan = []
    if "user flag" in questions:
        plan.append(("nmap","scan ports"))
        plan.append(("gobuster","find directories"))
        plan.append(("ssh","user access"))
    if "root flag" in questions:
        plan.append(("priv_esc","privilege escalation"))
    return plan

# ----------------------------
# GUI + Engine
# ----------------------------
class GHENA(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI – OP Edition (Single File)")
        self.resize(1000,700)
        layout = QVBoxLayout()

        self.lab_url = QLineEdit(); self.lab_url.setPlaceholderText("Lab URL"); layout.addWidget(self.lab_url)
        self.mode = QComboBox(); self.mode.addItems(["Manual","Auto"]); layout.addWidget(self.mode)
        self.start = QPushButton("Analyze Lab"); layout.addWidget(self.start)
        self.output = QTextEdit(); self.output.setReadOnly(True); layout.addWidget(self.output)
        container = QWidget(); container.setLayout(layout); self.setCentralWidget(container)
        self.start.clicked.connect(self.run)

    def run_command(self,cmd):
        self.output.append(f"[EXEC] {cmd}")
        process=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        for line in process.stdout:
            self.output.append(line.strip())

    def run(self):
        url = self.lab_url.text()
        mode = self.mode.currentText().lower()
        self.output.append(f"🔍 Analyzing lab: {url}")
        questions = extract_questions_from_lab(url)
        self.output.append("📋 Detected Questions:")
        for q in questions: self.output.append(f" - {q}")

        plan = suggest_tools(questions)
        for tool_name, reason in plan:
            if tool_name=="ssh": cmd=Plugins.ssh("user","<IP>")["command"]
            elif tool_name=="file_ops": cmd=Plugins.file_ops("/tmp/password.txt")["command"]
            elif tool_name=="priv_esc": cmd=Plugins.priv_esc()["command"]
            elif tool_name=="nmap": cmd=Plugins.nmap("<IP>")["command"]
            elif tool_name=="gobuster": cmd=Plugins.gobuster("<IP>")["command"]
            else: cmd=f"echo unknown {tool_name}"

            self.output.append(f"\n🤖 Suggestion: {tool_name}\nReason: {reason}\nCommand: {cmd}")

            if mode=="manual":
                reply=QMessageBox.question(self,"Execute?",f"Execute {tool_name}?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
                if reply!=QMessageBox.StandardButton.Yes: continue
            else: time.sleep(2)

            self.run_command(cmd)

# ----------------------------
# Run
# ----------------------------
if __name__=="__main__":
    app=QApplication(sys.argv)
    w=GHENA()
    w.show()
    sys.exit(app.exec())
