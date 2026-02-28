import sys, subprocess, os, time
import google.generativeai as genai
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex, Qt
from PyQt6.QtGui import QFont, QColor

# ---------------------------------------------------------
# 1. إعداد ذكاء Gemini (العقل المدبر)
# ---------------------------------------------------------
# ضع مفتاح الـ API الخاص بك هنا
GEMINI_API_KEY = "ضعه_هنا_API_KEY" 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ---------------------------------------------------------
# 2. محرك التحليل والتنفيذ (The Autonomous Brain)
# ---------------------------------------------------------
class AutonomousBrain(QThread):
    log_signal = pyqtSignal(str, str)
    ask_permission_signal = pyqtSignal(str, str)
    status_signal = pyqtSignal(str)
    finished_mission = pyqtSignal()

    def __init__(self, target_ip, goal):
        super().__init__()
        self.ip = target_ip
        self.goal = goal
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.approved = False
        self.stop_chain = False
        self.history = []

    def approve_command(self):
        self.approved = True
        self.condition.wakeAll()

    def run(self):
        # الخطوة الأولى دائماً: جمع المعلومات
        next_cmd = f"nmap -sV -T4 {self.ip}"
        last_reason = "بدء عملية فحص المنافذ والخدمات للتعرف على الهدف."

        for step in range(1, 11): # الحد الأقصى 10 خطوات تسلسلية
            if self.stop_chain: break

            # طلب إذن التنفيذ من المستخدم
            self.ask_permission_signal.emit(next_cmd, last_reason)
            
            self.mutex.lock()
            self.condition.wait(self.mutex)
            self.mutex.unlock()
            
            if not self.approved:
                self.log_signal.emit("🛑 تم إيقاف العملية من قبل المستخدم.", "#e74c3c")
                break

            # تنفيذ الأمر
            self.log_signal.emit(f"🛠 [خطوة {step}] جارِ تنفيذ: {next_cmd}", "#3498db")
            output = self.execute_linux_cmd(next_cmd)
            self.log_signal.emit(f"✅ اكتمل التنفيذ. حجم البيانات: {len(output)} حرف.", "#2ecc71")

            # تخزين النتائج في الذاكرة لـ Gemini
            self.history.append({"cmd": next_cmd, "output": output[:1500]}) # نرسل جزءاً من المخرجات لسرعة الاستجابة

            # استشارة Gemini للخطوة التالية
            self.status_signal.emit("🤔 Gemini يقوم بتحليل النتائج الآن...")
            analysis = self.ask_gemini()
            
            next_cmd = analysis.get("COMMAND", "")
            last_reason = analysis.get("REASON", "")

            if "DONE" in next_cmd.upper():
                self.log_signal.emit("🏁 اكتمل الهجوم: Gemini قرر أن الهدف قد تحقق.", "#f1c40f")
                break
            
            self.approved = False # إعادة التعيين للخطوة التالية

        self.finished_mission.emit()

    def execute_linux_cmd(self, cmd):
        try:
            # تنفيذ حقيقي في Kali Linux
            process = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            return process
        except Exception as e:
            return f"Error: {str(e)}"

    def ask_gemini(self):
        history_text = "\n".join([f"Command: {h['cmd']}\nResult: {h['output']}" for h in self.history])
        
        prompt = f"""
        أنت خبير اختراق (Red Team Specialist). الهدف الحالي هو: {self.ip}
        الغاية: {self.goal}
        
        سجل العمليات التي تمت حتى الآن:
        {history_text}
        
        بناءً على المخرجات أعلاه، ما هي الأداة التالية المناسبة في Kali Linux؟
        - إذا وجدت بورت 80، استخدم gobuster.
        - إذا وجدت ثغرة معروفة، استخدم searchsploit أو msfconsole.
        - إذا حصلت على Root، أجب بـ COMMAND: DONE.

        يجب أن يكون الرد بالتنسيق التالي بدقة:
        REASON: [شرح بالعربية للسبب]
        COMMAND: [الأمر البرمجي الذي سيتم وضعه في Terminal]
        """
        try:
            response = model.generate_content(prompt)
            text = response.text
            reason = text.split("REASON:")[1].split("COMMAND:")[0].strip()
            command = text.split("COMMAND:")[1].strip()
            return {"REASON": reason, "COMMAND": command}
        except:
            return {"REASON": "فشل الاتصال بـ Gemini", "COMMAND": "DONE"}

# ---------------------------------------------------------
# 3. الواجهة الرسومية الاحترافية (GUI)
# ---------------------------------------------------------
class GhenaAI_Final(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI v36.0 - Gemini Autonomous Engine")
        self.setMinimumSize(1000, 800)
        self.setStyleSheet("background-color: #121212; color: #ffffff;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # الجزء العلوي: الإعدادات
        top_box = QGroupBox("Target Settings")
        top_box.setStyleSheet("color: #00ccff; border: 1px solid #333;")
        top_layout = QHBoxLayout()
        self.ip_input = QLineEdit(); self.ip_input.setPlaceholderText("Target IP (e.g., 10.10.10.5)")
        self.ip_input.setStyleSheet("background: #1e1e1e; border: 1px solid #555; padding: 5px;")
        self.goal_input = QComboBox()
        self.goal_input.addItems(["Full Compromise (Root)", "Initial Access", "Privilege Escalation"])
        self.btn_start = QPushButton("🚀 LAUNCH MISSION")
        self.btn_start.setStyleSheet("background: #c0392b; font-weight: bold; padding: 10px;")
        self.btn_start.clicked.connect(self.run_mission)
        
        top_layout.addWidget(QLabel("IP:")); top_layout.addWidget(self.ip_input)
        top_layout.addWidget(QLabel("Goal:")); top_layout.addWidget(self.goal_input)
        top_layout.addWidget(self.btn_start)
        top_box.setLayout(top_layout)
        main_layout.addWidget(top_box)

        # الجزء الأوسط: مقترحات Gemini
        self.proposal_box = QGroupBox("Gemini Strategic Analysis")
        self.proposal_box.setStyleSheet("color: #f1c40f; border: 1px solid #f1c40f;")
        prop_layout = QVBoxLayout()
        self.lbl_reason = QLabel("Waiting for AI analysis..."); self.lbl_reason.setWordWrap(True)
        self.lbl_cmd = QLineEdit(); self.lbl_cmd.setReadOnly(True)
        self.lbl_cmd.setStyleSheet("background: #000; color: #e67e22; font-family: monospace; font-size: 14px;")
        self.btn_approve = QPushButton("✅ APPROVE & EXECUTE NEXT STEP")
        self.btn_approve.setEnabled(False)
        self.btn_approve.setStyleSheet("background: #27ae60; color: white; font-weight: bold; height: 40px;")
        self.btn_approve.clicked.connect(self.on_approve)

        prop_layout.addWidget(self.lbl_reason); prop_layout.addWidget(self.lbl_cmd); prop_layout.addWidget(self.btn_approve)
        self.proposal_box.setLayout(prop_layout)
        main_layout.addWidget(self.proposal_box)

        # الجزء السفلي: الكونسول والنتائج
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.setStyleSheet("background: #000; color: #2ecc71; font-family: 'Courier New'; border: 1px solid #333;")
        main_layout.addWidget(QLabel("Live Execution Log:"))
        main_layout.addWidget(self.console)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        container = QWidget(); container.setLayout(main_layout); self.setCentralWidget(container)

    def run_mission(self):
        target = self.ip_input.text()
        if not target: return
        self.console.clear()
        self.btn_start.setEnabled(False)
        self.brain = AutonomousBrain(target, self.goal_input.currentText())
        self.brain.log_signal.connect(self.log)
        self.brain.status_signal.connect(self.status_bar.showMessage)
        self.brain.ask_permission_signal.connect(self.show_ai_move)
        self.brain.finished_mission.connect(lambda: self.btn_start.setEnabled(True))
        self.brain.start()

    def show_ai_move(self, cmd, reason):
        self.lbl_reason.setText(f"💡 AI التحليل: {reason}")
        self.lbl_cmd.setText(cmd)
        self.btn_approve.setEnabled(True)
        self.btn_approve.setText("✅ APPROVE & EXECUTE")

    def on_approve(self):
        self.btn_approve.setEnabled(False)
        self.btn_approve.setText("⌛ Executing...")
        self.brain.approve_command()

    def log(self, text, color):
        self.console.append(f"<font color='{color}'>{text}</font>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GhenaAI_Final(); window.show()
    sys.exit(app.exec())import sys, subprocess, time
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
