from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess, sys, time, os

# ---------------------------------------------------------
# محرك الأوامر الشامل (Plugins)
# ---------------------------------------------------------
class UniversalPlugins:
    @staticmethod
    def quick_scan(target):
        return f"nmap -F --open {target}"

    @staticmethod
    def deep_scan(target):
        # تم إضافة -Pn لتجنب الحظر وفحص كل المنافذ
        return f"nmap -sV -sC -Pn -p- {target}"

    @staticmethod
    def web_discovery(target):
        return f"gobuster dir -u http://{target}/ -w /usr/share/wordlists/dirb/common.txt -q -x php,txt,html"

    @staticmethod
    def smb_enum(target):
        return f"smbclient -L //{target} -N"

# ---------------------------------------------------------
# خيط التنفيذ (الذي يضمن تسلسل الأوامر)
# ---------------------------------------------------------
class CmdWorker(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        
    def run(self):
        process = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            self.output_signal.emit(line.strip())
        process.wait()
        self.finished_signal.emit()

# ---------------------------------------------------------
# الواجهة الرسومية المحسنة
# ---------------------------------------------------------
class GHENA_CHAIN(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI – Sequential Engine v21.0")
        self.setMinimumSize(1000, 750)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # قسم إدخال الـ IP
        input_group = QGroupBox("Target Configuration")
        input_layout = QHBoxLayout()
        self.target_ip = QLineEdit(); self.target_ip.setPlaceholderText("أدخل IP الهدف هنا...")
        input_layout.addWidget(QLabel("Target IP:"))
        input_layout.addWidget(self.target_ip)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # أزرار التحكم
        btn_layout = QHBoxLayout()
        self.qscan_btn = QPushButton("🔍 Quick Scan")
        self.full_btn = QPushButton("🔥 START FULL ATTACK CHAIN")
        self.full_btn.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; height: 40px;")
        
        btn_layout.addWidget(self.qscan_btn)
        btn_layout.addWidget(self.full_btn)
        main_layout.addLayout(btn_layout)

        # الكونسول
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #000; color: #0f0; font-family: 'Courier New';")
        main_layout.addWidget(QLabel("<b>Execution Logs:</b>"))
        main_layout.addWidget(self.console)

        container = QWidget(); container.setLayout(main_layout); self.setCentralWidget(container)

        # الربط
        self.qscan_btn.clicked.connect(self.run_quick)
        self.full_btn.clicked.connect(self.run_chain)

    def log(self, text):
        self.console.append(f"<font color='white'><b>[*] {text}</b></font>")

    def execute_and_wait(self, name, cmd):
        """وظيفة لتنفيذ الأمر والانتظار حتى ينتهي تماماً"""
        self.log(f"Starting Phase: {name}")
        self.log(f"Command: {cmd}")
        
        # إنشاء Worker جديد لكل أمر
        worker = CmdWorker(cmd)
        worker.output_signal.connect(self.console.append)
        
        # استخدام loop محلي لانتظار انتهاء الخيط (Thread)
        is_running = True
        def on_finished(): nonlocal is_running; is_running = False
        
        worker.finished_signal.connect(on_finished)
        worker.start()

        # الحفاظ على الواجهة مستجيبة أثناء الانتظار
        while is_running:
            QApplication.processEvents()
            time.sleep(0.1)
        
        self.log(f"Finished Phase: {name}\n" + "-"*30)

    def run_quick(self):
        ip = self.target_ip.text().strip()
        if not ip: return
        self.execute_and_wait("Quick Scan", UniversalPlugins.quick_scan(ip))

    def run_chain(self):
        ip = self.target_ip.text().strip()
        if not ip:
            QMessageBox.warning(self, "Error", "الرجاء إدخال الـ IP")
            return

        self.log("🚀 INITIATING AUTOMATIC ATTACK CHAIN...")
        
        # تمرير الـ IP لكل الأوامر بالتسلسل
        # 1. فحص عميق
        self.execute_and_wait("Deep Enumeration", UniversalPlugins.deep_scan(ip))
        
        # 2. فحص ويب (تلقائياً بعد الأول)
        self.execute_and_wait("Web Directory Discovery", UniversalPlugins.web_discovery(ip))
        
        # 3. فحص SMB
        self.execute_and_wait("SMB Share Analysis", UniversalPlugins.smb_enum(ip))
        
        self.log("✅ ALL PHASES COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GHENA_CHAIN()
    window.show()
    sys.exit(app.exec())
