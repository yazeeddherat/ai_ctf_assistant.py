import sys, subprocess, time
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal

# ---------------------------------------------------------
# محرك التنفيذ الحقيقي (Real Execution Engine)
# ---------------------------------------------------------
class ExecutionWorker(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        # تنفيذ الأداة الحقيقية في كالي
        process = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            self.output_signal.emit(line.strip())
        process.wait()
        self.finished_signal.emit()

# ---------------------------------------------------------
# الواجهة الذكية (The Strategic Hub)
# ---------------------------------------------------------
class GhenaStrategist(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI - Strategic Auto-Chain v33.0")
        self.setMinimumSize(1000, 850)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # إدخال الهدف والـ IP
        config_group = QGroupBox("Target Configuration")
        config_layout = QHBoxLayout()
        self.ip_input = QLineEdit(); self.ip_input.setPlaceholderText("Target IP (e.g. 10.113.174.41)")
        self.goal_selector = QComboBox()
        self.goal_selector.addItems(["Initial Access (user.txt)", "Privilege Escalation (root.txt)"])
        config_layout.addWidget(QLabel("IP:")); config_layout.addWidget(self.ip_input)
        config_layout.addWidget(QLabel("Target Goal:")); config_layout.addWidget(self.goal_selector)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # زر البدء الذكي
        self.btn_launch = QPushButton("🚀 LAUNCH TARGETED ATTACK")
        self.btn_launch.setFixedHeight(55)
        self.btn_launch.setStyleSheet("background: #c0392b; color: white; font-weight: bold; font-size: 15px;")
        layout.addWidget(self.btn_launch)

        # صندوق التحليل والسبب (Reasoning)
        self.reason_box = QTextEdit(); self.reason_box.setReadOnly(True); self.reason_box.setMaximumHeight(100)
        self.reason_box.setStyleSheet("background: #1a1a1a; color: #00ccff; border: 1px solid #00ccff; font-size: 13px;")
        layout.addWidget(QLabel("<b>AI Reasoning & Strategy:</b>")); layout.addWidget(self.reason_box)

        # كونسول التنفيذ المباشر
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.setStyleSheet("background: #000; color: #39ff14; font-family: 'Monospace'; font-size: 12px;")
        layout.addWidget(QLabel("<b>Live Execution Console:</b>")); layout.addWidget(self.console)

        container = QWidget(); container.setLayout(layout); self.setCentralWidget(container)
        self.btn_launch.clicked.connect(self.start_phase_1)

    def log(self, text, color="#ffffff"):
        self.console.append(f"<font color='{color}'><b>{text}</b></font>")

    # --- الخطوة 1: الفحص لتحديد المسار ---
    def start_phase_1(self):
        ip = self.ip_input.text().strip()
        if not ip: return
        self.console.clear()
        self.reason_box.setText("💡 جاري فحص الخدمات المفتوحة لتحديد الأداة الأكثر فائدة للوصول للهدف...")
        
        # فحص الخدمات (مثل اللي سويته في صورتك)
        cmd = f"nmap -sV -Pn {ip}"
        self.log(f"\n[!] Phase 1: Service Discovery", "#3498db")
        self.log(f"[EXECUTING]: {cmd}", "#e67e22")
        
        self.worker = ExecutionWorker(cmd)
        self.worker.output_signal.connect(self.console.append)
        # الانتقال التلقائي فور انتهاء Nmap
        self.worker.finished_signal.connect(lambda: self.decide_and_run_phase_2(ip))
        self.worker.start()

    # --- الخطوة 2: الانتقال التلقائي للأداة المطلوبة فقط ---
    def decide_and_run_phase_2(self, ip):
        output = self.console.toPlainText()
        goal = self.goal_selector.currentText()
        
        self.log("\n[🧠] تحليل مخرجات Nmap لاختيار الأداة المطلوبة...", "#f1c40f")

        # حالة الوصول الأولي (Initial Access)
        if "Initial Access" in goal:
            # التحقق من بورت 80 (الويب) - المسار الأسرع في Chill Hack
            if "80/tcp open" in output or "http" in output:
                reason = "اكتشفت منفذ ويب مفتوح (80). في هذا اللاب، الطريق الأقصر للوصول للمستخدم هو عبر فحص المجلدات المخفية. سأشغل Gobuster الآن."
                self.reason_box.setText(f"🎯 {reason}")
                next_cmd = f"gobuster dir -u http://{ip}/ -w /usr/share/wordlists/dirb/common.txt -q"
                self.execute_next_tool("Web Discovery", next_cmd)
            
            # التحقق من بورت 21 (FTP) - مسار بديل إذا كان الويب غير مفيد
            elif "21/tcp open" in output:
                reason = "وجدنا بورت FTP مفتوح. سأفحص إذا كان يسمح بالدخول المجهول للحصول على بيانات المستخدم."
                self.reason_box.setText(f"🎯 {reason}")
                next_cmd = f"nmap --script ftp-anon -p 21 {ip}"
                self.execute_next_tool("FTP Scan", next_cmd)

        # حالة تصعيد الصلاحيات (Privilege Escalation)
        elif "Privilege Escalation" in goal:
            reason = "الهدف هو الروت. سأبحث عن ملفات SUID أو صلاحيات sudo المفتوحة فوراً."
            self.reason_box.setText(f"🎯 {reason}")
            self.execute_next_tool("PrivEsc Check", "find / -perm -4000 2>/dev/null")

    def execute_next_tool(self, name, cmd):
        self.log(f"\n[!] Phase 2: {name} (Auto-Triggered)", "#3498db")
        self.log(f"[EXECUTING]: {cmd}", "#e67e22")
        self.worker = ExecutionWorker(cmd)
        self.worker.output_signal.connect(self.console.append)
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GhenaStrategist(); window.show()
    sys.exit(app.exec())
