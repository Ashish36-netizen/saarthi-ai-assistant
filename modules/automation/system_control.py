import os
import subprocess
import platform
import socket
from datetime import datetime

import pyautogui
import psutil


class SystemControl:
    """Handles OS-level automation: apps, volume, screenshot, system info."""

    def __init__(self):
        self.os_type = platform.system()
        print(f"[SYS] SystemControl initialized on {self.os_type}")

    # ---------- App Management ----------
    def open_app(self, app_name):
        """Open an application by name."""
        app_name = app_name.lower().strip()

        aliases = {
            "chrome": "chrome",
            "google chrome": "chrome",
            "notepad": "notepad",
            "calculator": "calc",
            "calc": "calc",
            "paint": "mspaint",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "vlc": "vlc",
            "spotify": "spotify",
            "whatsapp": "whatsapp",
            "file explorer": "explorer",
            "explorer": "explorer",
            "settings": "ms-settings:",
        }

        actual_app = aliases.get(app_name, app_name)

        try:
            if self.os_type == "Windows":
                os.startfile(actual_app)
            elif self.os_type == "Darwin":
                subprocess.Popen(["open", "-a", actual_app])
            else:
                subprocess.Popen([actual_app])
            return f"{app_name.title()} khol diya"
        except Exception as e:
            return f"{app_name} nahi khol paya. Error: {e}"

    def close_app(self, app_name):
        """Close a running application."""
        app_name = app_name.lower().strip()
        killed = False
        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = (proc.info["name"] or "").lower()
                if app_name in proc_name:
                    proc.terminate()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if killed:
            return f"{app_name.title()} band kar diya"
        return f"{app_name} chal nahi raha ya mila nahi"

    # ---------- Volume ----------
    def volume_up(self, steps=5):
        for _ in range(steps):
            pyautogui.press("volumeup")
        return "Volume badha diya"

    def volume_down(self, steps=5):
        for _ in range(steps):
            pyautogui.press("volumedown")
        return "Volume kam kar diya"

    def mute(self):
        pyautogui.press("volumemute")
        return "Mute kar diya"

    # ---------- Screenshot ----------
    def take_screenshot(self):
        try:
            import mss
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            with mss.mss() as sct:
                sct.shot(output=filename)
            return f"Screenshot le liya: {filename}"
        except Exception as e:
            return f"Screenshot nahi le paya. Error: {e}"

    # ---------- Time / Date ----------
    def get_time(self):
        now = datetime.now()
        return f"Abhi {now.strftime('%I:%M %p').lstrip('0')} hai"

    def get_date(self):
        now = datetime.now()
        return f"Aaj {now.strftime('%A, %d %B %Y')} hai"

    # ---------- Battery ----------
    def get_battery(self):
        battery = psutil.sensors_battery()
        if battery is None:
            return "Battery info available nahi hai (desktop system lagta hai)"
        percent = int(battery.percent)
        status = "charging ho rahi hai" if battery.power_plugged else "charging nahi ho rahi"
        return f"Battery {percent}% hai, {status}"

    # ---------- CPU / RAM ----------
    def get_cpu_usage(self):
        cpu = psutil.cpu_percent(interval=0.5)
        return f"CPU usage {cpu:.0f}% hai"

    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return f"RAM {ram.percent:.0f}% use ho rahi hai"

    # ---------- IP ----------
    def get_ip(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return f"Aapka local IP {ip} hai"
        except Exception as e:
            return f"IP nahi mil paya. Error: {e}"