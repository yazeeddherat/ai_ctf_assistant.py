import sys, subprocess, time, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal

# ---------------------------------------------------------
# محرك الأوامر الحقيقية (Real Tools Engine)
# ---------------------------------------------------------
class RealToolKit:
    @staticmethod
    def nmap_scan(ip):
        # فحص بورتات، خدمات، وإصدارات (Deep Scan)
        return f"nmap -sV -sC -Pn {ip}"

    @staticmethod
    def gobuster_scan(ip):
        # البحث عن المجلدات المخفية في الويب
        return f"gobuster dir -u http://{ip}/ -w /usr/share/wordlists/dirb/common.txt -q -x php,txt,html"

    @staticmethod
    def smb_enum(ip):
        # فحص مشاركات الملفات (SMB)
        return f"smbclient -L //{ip} -N"

    @staticmethod
    def priv_esc_check():
        # فحص صلاحيات الرفع (SUID/Sudo)
        return "sudo -l || find / -perm -4000 2>/dev/null"

# ---------------------------------------------------------
# خيط التنفيذ (الذي يمنع تجمد البرنامج)
# ---------------------------------------------------------
class ExecutionWorker(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        # تنفيذ الأمر الحقيقي وجلب المخرجات فوراً
        process = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            self.output_signal.emit(line.strip())
        process.wait()
        self.finished_signal.emit()

# ---------------------------------------------------------
# الواجهة الرسومية الشاملة
# ---------------------------------------------------------
class GhenaOctopus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI - The Full Chain v25.0")
        self.setMinimumSize(1000, 800)
        self.queue = [] # طابور المهام التلقائي
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # إدخال الـ IP
        ip_group = QGroupBox("Target Machine Configuration")
        ip_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("أدخل IP الهدف (مثلاً: 10.10.x.x)")
        self.ip_input.setStyleSheet("padding: 10px; font-size: 14px;")
        ip_layout.addWidget(QLabel("Target IP:"))
        ip_layout.addWidget(self.ip_input)
        ip_group.setLayout(ip_layout)
        main_layout.addWidget(ip_group)

        # زر البدء التلقائي
        self.btn_launch = QPushButton("🚀 LAUNCH AUTOMATIC EXPLOIT CHAIN")
        self.btn_launch.setFixedHeight(55)
        self.btn_launch.setStyleSheet("""
            background-color: #c0392b; color: white; 
            font-weight: bold; font-size: 16px; border-radius: 8px;
        """)
        main_layout.addWidget(self.btn_launch)

        # كونسول المخرجات
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            background-color: #000000; color: #39FF14; 
            font-family: 'Monospace'; font-size: 13px; padding: 10px;
        """)
        main_layout.addWidget(QLabel("<b>Live Execution Console:</b>"))
        main_layout.addWidget(self.console)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # الربط
        self.btn_launch.clicked.connect(self.start_full_attack)

    def log(self, text, color="#ffffff"):
        self.console.append(f"<font color='{color}'><b>{text}</b></font>")

    def start_full_attack(self):
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.critical(self, "Error", "يجب إدخال IP الهدف أولاً!")
            return

        # تجهيز السلسلة (تلقائياً)
        self.queue = [
            ("1. Port & Service Discovery (Nmap)", RealToolKit.nmap_scan(ip)),
            ("2. Web Path Brute-forcing (Gobuster)", RealToolKit.gobuster_scan(ip)),
            ("3. SMB Share Enumeration", RealToolKit.smb_enum(ip)),
            ("4. Privilege Escalation Audit", RealToolKit.priv_esc_check())
        ]

        self.console.clear()
        self.log("--- [!!!] INITIATING AUTOMATED ATTACK CHAIN [!!!] ---", "#e67e22")
        self.run_next_phase()

    def run_next_phase(self):
        if not self.queue:
            self.log("\n[✅] ALL PHASES COMPLETED. ANALYZE RESULTS ABOVE.", "#2ecc71")
            return

        name, cmd = self.queue.pop(0)
        self.log(f"\n[🚀] Phase: {name}", "#f1c40f")
        self.log(f"[>] Command: {cmd}", "#95a5a6")

        self.worker = ExecutionWorker(cmd)
        self.worker.output_signal.connect(self.console.append)
        # هذا السطر هو الذي يمرر البرنامج للمرحلة التالية تلقائياً عند انتهاء الحالية
        self.worker.finished_signal.connect(self.run_next_phase) 
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GhenaOctopus()
    window.show()
    sys.exit(app.exec())
