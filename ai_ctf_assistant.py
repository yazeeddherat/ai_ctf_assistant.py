from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess, sys

# ============================
# Plugins / Tools Engine
# ============================
class AllInOnePlugins:
    @staticmethod
    def nmap_deep(target):
        return f"nmap -sV -sC -Pn {target}"

    @staticmethod
    def gobuster(target):
        return (
            f"gobuster dir -u http://{target}/ "
            f"-w /usr/share/wordlists/dirb/common.txt "
            f"-q -x php,txt,html"
        )

    @staticmethod
    def smb_check(target):
        return f"smbclient -L //{target} -N"

    @staticmethod
    def priv_esc_check():
        return "sudo -l || find / -perm -4000 2>/dev/null"


# ============================
# Lab / Goal Inference Engine
# ============================
class LabInferenceEngine:
    @staticmethod
    def infer(target):
        """
        استنتاج أهداف اللاب بدون قراءة أسئلة مباشرة
        (Boot2Root pattern)
        """
        goals = [
            "Service Enumeration",
            "Initial Access",
            "User Flag",
            "Privilege Escalation",
            "Root Flag"
        ]

        execution_plan = [
            ("Port Discovery (Nmap)", AllInOnePlugins.nmap_deep(target)),
            ("Web Enumeration (Gobuster)", AllInOnePlugins.gobuster(target)),
            ("SMB Enumeration", AllInOnePlugins.smb_check(target)),
            ("Privilege Escalation Check", AllInOnePlugins.priv_esc_check()),
        ]

        return goals, execution_plan


# ============================
# Command Worker Thread
# ============================
class CmdWorker(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        process = subprocess.Popen(
            self.cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in process.stdout:
            self.output_signal.emit(line.rstrip())
        process.wait()
        self.finished_signal.emit()


# ============================
# GUI Application
# ============================
class GHENA_OCTOPUS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI – OCTOPUS Framework v1.0")
        self.setMinimumSize(1000, 800)
        self.queue = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.target_ip = QLineEdit()
        self.target_ip.setPlaceholderText("Enter Target IP (e.g. 10.10.10.10)")
        self.target_ip.setStyleSheet(
            "padding:12px;font-size:15px;border-radius:6px;"
        )

        layout.addWidget(QLabel("<b>Target IP</b>"))
        layout.addWidget(self.target_ip)

        self.btn = QPushButton("🐙 ANALYZE & EXECUTE")
        self.btn.setFixedHeight(55)
        self.btn.setStyleSheet("""
            background:#e74c3c;
            color:white;
            font-size:16px;
            font-weight:bold;
            border-radius:10px;
        """)
        layout.addWidget(self.btn)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            background:#111;
            color:#39FF14;
            font-family:monospace;
            font-size:13px;
            padding:10px;
        """)
        layout.addWidget(QLabel("<b>Execution Console</b>"))
        layout.addWidget(self.console)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.btn.clicked.connect(self.start_attack)

    def log(self, msg, color="#ffffff"):
        self.console.append(f"<font color='{color}'><b>{msg}</b></font>")

    # ============================
    # Main Logic
    # ============================
    def start_attack(self):
        ip = self.target_ip.text().strip()
        if not ip:
            QMessageBox.warning(self, "Error", "Target IP is required.")
            return

        self.console.clear()
        self.log("🧠 Analyzing lab objectives...", "#9b59b6")

        goals, plan = LabInferenceEngine.infer(ip)

        for g in goals:
            self.log(f"🎯 Objective detected: {g}", "#1abc9c")

        self.queue = plan
        self.log("\n🚀 Execution plan ready.", "#3498db")
        self.run_next_phase()

    def run_next_phase(self):
        if not self.queue:
            self.log("\n✅ All phases completed.", "#2ecc71")
            return

        name, cmd = self.queue.pop(0)

        reply = QMessageBox.question(
            self,
            "Confirm Execution",
            f"Execute this phase?\n\n{name}\n\n{cmd}",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            self.log(f"⏭ Skipped: {name}", "#e67e22")
            self.run_next_phase()
            return

        self.log(f"\n[🚀] Phase: {name}", "#f1c40f")
        self.log(f"[>] Command: {cmd}", "#95a5a6")

        self.worker = CmdWorker(cmd)
        self.worker.output_signal.connect(self.console.append)
        self.worker.finished_signal.connect(self.run_next_phase)
        self.worker.start()


# ============================
# App Entry
# ============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GHENA_OCTOPUS()
    window.show()
    sys.exit(app.exec())
