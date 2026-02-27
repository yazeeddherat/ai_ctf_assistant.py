from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess, sys, time, os

# 

# ---------------------------------------------------------
# محرك الأوامر الشامل لجميع المنصات (TryHackMe, HTB, VulnHub)
# ---------------------------------------------------------
class UniversalPlugins:
    @staticmethod
    def quick_scan(target):
        # فحص سريع جداً للمنافذ المفتوحة
        return f"nmap -F --open {target}"

    @staticmethod
    def deep_scan(target):
        # فحص عميق للخدمات، الإصدارات، والسكربتات الافتراضية
        return f"nmap -sV -sC -A -p- {target}"

    @staticmethod
    def web_discovery(target):
        # فحص المسارات والمجلدات المخفية في مواقع الويب
        return f"gobuster dir -u http://{target}/ -w /usr/share/wordlists/dirb/common.txt -q -x php,txt,html"

    @staticmethod
    def smb_enum(target):
        # فحص بروتوكول SMB للملفات المشتركة بدون كلمة سر
        return f"smbclient -L //{target} -N"

    @staticmethod
    def john_crack(hash_file):
        # كسر الهاشات باستخدام قائمة rockyou الشهيرة
        return f"john --wordlist=/usr/share/wordlists/rockyou.txt {hash_file}"

# ---------------------------------------------------------
# خيط التنفيذ (لضمان استقرار الواجهة أثناء الفحص)
# ---------------------------------------------------------
class CmdWorker(QThread):
    output_signal = pyqtSignal(str)
    
    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        
    def run(self):
        # تنفيذ الأمر وجلب المخرجات سطراً بسطر
        process = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            self.output_signal.emit(line.strip())

# ---------------------------------------------------------
# الواجهة الرسومية الرئيسية
# ---------------------------------------------------------
class GHENA_ULTIMATE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI – Universal Lab Solver v20.0")
        self.setMinimumSize(1000, 750)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- قسم إدخال البيانات ---
        input_group = QGroupBox("Target Information")
        input_layout = QGridLayout()
        
        self.target_ip = QLineEdit(); self.target_ip.setPlaceholderText("أدخل IP الهدف هنا (مثلاً: 10.10.x.x)")
        input_layout.addWidget(QLabel("Target IP:"), 0, 0)
        input_layout.addWidget(self.target_ip, 0, 1)

        self.lab_type = QComboBox()
        self.lab_type.addItems(["Linux Machine", "Windows Machine", "Web Application"])
        input_layout.addWidget(QLabel("Machine Type:"), 1, 0)
        input_layout.addWidget(self.lab_type, 1, 1)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # --- قسم أزرار التحكم ---
        btn_layout = QHBoxLayout()
        
        self.qscan_btn = QPushButton("🔍 Quick Scan")
        self.qscan_btn.clicked.connect(self.run_quick_scan)
        
        self.full_btn = QPushButton("🔥 Full Exploit Path")
        self.full_btn.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold;")
        self.full_btn.clicked.connect(self.run_full_attack)
        
        self.clear_btn = QPushButton("🗑 Clear Console")
        self.clear_btn.clicked.connect(lambda: self.console.clear())

        btn_layout.addWidget(self.qscan_btn)
        btn_layout.addWidget(self.full_btn)
        btn_layout.addWidget(self.clear_btn)
        main_layout.addLayout(btn_layout)

        # --- قسم مخرجات التيرمينال ---
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            background-color: #000000; 
            color: #00FF00; 
            font-family: 'Courier New'; 
            font-size: 13px;
            border: 2px solid #333;
        """)
        main_layout.addWidget(QLabel("<b>Execution Console:</b>"))
        main_layout.addWidget(self.console)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # --- وظائف التنفيذ ---
    def log(self, text):
        self.console.append(f"<b>[*] {text}</b>")

    def execute_command(self, cmd):
        self.worker = CmdWorker(cmd)
        self.worker.output_signal.connect(self.console.append)
        self.worker.start()
        # انتظار انتهاء العملية مع إبقاء الواجهة حية
        while self.worker.isRunning():
            QApplication.processEvents()
            time.sleep(0.05)

    def run_quick_scan(self):
        ip = self.target_ip.text().strip()
        if not ip: return
        self.log(f"Starting Quick Scan on {ip}...")
        self.execute_command(UniversalPlugins.quick_scan(ip))

    def run_full_attack(self):
        ip = self.target_ip.text().strip()
        if not ip:
            QMessageBox.critical(self, "Error", "يجب إدخال IP الهدف أولاً!")
            return
        
        confirm = QMessageBox.question(self, "تأكيد", "هل تريد بدء هجوم شامل؟ قد يستغرق هذا وقتاً طويلاً.")
        if confirm != QMessageBox.StandardButton.Yes: return

        self.log("--- STARTING FULL EXPLOITATION PATH ---")
        
        # المرحلة 1: الفحص العميق
        self.log("Phase 1: Deep Port Scanning...")
        self.execute_command(UniversalPlugins.deep_scan(ip))
        
        # المرحلة 2: فحص الويب (بشكل تلقائي)
        self.log("Phase 2: Web Directories Discovery...")
        self.execute_command(UniversalPlugins.web_discovery(ip))
        
        # المرحلة 3: فحص الـ SMB (مفيد جداً في لابات الويندوز)
        self.log("Phase 3: Enumerating SMB Shares...")
        self.execute_command(UniversalPlugins.smb_enum(ip))
        
        self.log("--- FULL PATH COMPLETED ---")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GHENA_ULTIMATE()
    window.show()
    sys.exit(app.exec())
