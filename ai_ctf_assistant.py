import sys
import time
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import QThread, pyqtSignal


# =========================
# LAB STATE
# =========================
@dataclass
class LabState:
    services_known: bool = False
    web_detected: bool = False
    creds_found: bool = False
    user_access: bool = False
    priv_esc_path: bool = False
    root_access: bool = False


# =========================
# TOOL REGISTRY (ALL TOOLS)
# =========================
class ToolRegistry:
    """
    كل أدوات CTF المعروفة — لكن Simulation فقط
    """
    NETWORK = [
        "nmap", "masscan", "rustscan"
    ]

    WEB = [
        "gobuster", "ffuf", "dirsearch",
        "nikto", "whatweb", "wpscan"
    ]

    CREDS = [
        "hydra", "medusa", "john", "hashcat"
    ]

    ENUMERATION = [
        "linpeas", "linenum", "pspy",
        "enum4linux", "smbclient"
    ]

    PRIV_ESC = [
        "sudo abuse", "SUID abuse",
        "cron abuse", "capabilities abuse"
    ]

    @staticmethod
    def suggest_tools(phase: str):
        return {
            "Service Discovery": ToolRegistry.NETWORK,
            "Web Enumeration": ToolRegistry.WEB,
            "Credential Attack": ToolRegistry.CREDS,
            "Privilege Escalation": ToolRegistry.ENUMERATION + ToolRegistry.PRIV_ESC
        }.get(phase, [])


# =========================
# DECISION ENGINE
# =========================
class DecisionEngine:
    def decide(self, state: LabState):
        if not state.services_known:
            return "Service Discovery"

        if state.web_detected and not state.creds_found:
            return "Web Enumeration"

        if state.creds_found and not state.user_access:
            return "Credential Attack"

        if state.user_access and not state.priv_esc_path:
            return "Privilege Escalation"

        if state.priv_esc_path and not state.root_access:
            return "Root Validation"

        return "Completed"


# =========================
# SIMULATION WORKER
# =========================
class SimulationWorker(QThread):
    output = pyqtSignal(str)
    done = pyqtSignal()

    def __init__(self, phase, state: LabState):
        super().__init__()
        self.phase = phase
        self.state = state

    def run(self):
        time.sleep(1.2)

        if self.phase == "Service Discovery":
            self.output.emit("✔ Services identified (simulated)")
            self.state.services_known = True
            self.state.web_detected = True

        elif self.phase == "Web Enumeration":
            self.output.emit("✔ Information disclosure detected (simulated)")
            self.state.creds_found = True

        elif self.phase == "Credential Attack":
            self.output.emit("✔ User access obtained (simulated)")
            self.output.emit("✔ user.txt located (hidden)")
            self.state.user_access = True

        elif self.phase == "Privilege Escalation":
            self.output.emit("✔ Privilege escalation vector found (simulated)")
            self.state.priv_esc_path = True

        elif self.phase == "Root Validation":
            self.output.emit("✔ Root access confirmed (simulated)")
            self.output.emit("✔ root.txt detected (hidden)")
            self.state.root_access = True

        self.done.emit()


# =========================
# GUI
# =========================
class GHENA_AI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHENA AI – All‑Tools CTF Framework (Simulation)")
        self.setMinimumSize(950, 750)

        self.state = LabState()
        self.engine = DecisionEngine()

        self.init_ui()
        self.update_view()

    def init_ui(self):
        layout = QVBoxLayout()

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Target IP (CTF Lab)")
        layout.addWidget(QLabel("<b>Target</b>"))
        layout.addWidget(self.ip_input)

        self.phase_box = QTextEdit()
        self.phase_box.setReadOnly(True)
        self.phase_box.setStyleSheet("background:#111;color:#00ffcc;")
        layout.addWidget(QLabel("<b>AI Decision & Tools</b>"))
        layout.addWidget(self.phase_box)

        btns = QHBoxLayout()
        self.approve = QPushButton("✔ Execute (Simulation)")
        self.stop = QPushButton("⛔ Stop")
        btns.addWidget(self.approve)
        btns.addWidget(self.stop)
        layout.addLayout(btns)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background:#000;color:#39ff14;")
        layout.addWidget(QLabel("<b>Console</b>"))
        layout.addWidget(self.console)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.approve.clicked.connect(self.run_phase)
        self.stop.clicked.connect(self.close)

    def update_view(self):
        phase = self.engine.decide(self.state)
        tools = ToolRegistry.suggest_tools(phase)

        self.phase_box.clear()
        self.phase_box.append(
            f"🎯 Current Phase: {phase}\n\n"
            f"🧠 Suggested Tools:\n- " + "\n- ".join(tools)
        )

    def log(self, msg):
        self.console.append(msg)

    def run_phase(self):
        if not self.ip_input.text().strip():
            QMessageBox.warning(self, "Error", "Enter target IP first.")
            return

        phase = self.engine.decide(self.state)
        if phase == "Completed":
            self.log("✅ Lab fully completed (simulation).")
            return

        self.log(f"\n[SIM] Running phase: {phase}")
        self.worker = SimulationWorker(phase, self.state)
        self.worker.output.connect(self.log)
        self.worker.done.connect(self.update_view)
        self.worker.start()


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GHENA_AI()
    win.show()
    sys.exit(app.exec())
