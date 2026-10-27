import re


class IntentRouter:
    """Routes user input to either system commands or LLM."""

    def __init__(self, system_control):
        self.sys = system_control
        print("[ROUTER] IntentRouter initialized.")

    def try_command(self, user_text):
        """
        Try to match a system command.
        Returns response string if matched, None otherwise (falls back to LLM).
        """
        text = user_text.lower().strip().strip(".!?,")

        # ---------- 1. Open App ----------
        m = re.match(r"^(?:open|launch|start)\s+(.+)$", text)
        if m:
            app = re.sub(r"^(the|a|an)\s+", "", m.group(1).strip())
            return self.sys.open_app(app)

        m = re.match(r"^(.+?)\s+(?:kholo|khol|khol\s+do|open\s+karo|open\s+kardo)$", text)
        if m:
            return self.sys.open_app(m.group(1).strip())

        # ---------- 2. Close App ----------
        m = re.match(r"^(?:close|quit)\s+(.+)$", text)
        if m:
            app = re.sub(r"^(the|a|an)\s+", "", m.group(1).strip())
            return self.sys.close_app(app)

        m = re.match(r"^(.+?)\s+(?:band\s+karo|band\s+kardo|close\s+karo)$", text)
        if m:
            return self.sys.close_app(m.group(1).strip())

        # ---------- 3. Volume ----------
        if any(kw in text for kw in ["volume up", "awaaz badhao", "louder", "sound badhao"]):
            return self.sys.volume_up()
        if any(kw in text for kw in ["volume down", "awaaz kam", "quieter", "sound kam"]):
            return self.sys.volume_down()
        if "mute" in text or "chup karo" in text:
            return self.sys.mute()

        # ---------- 4. Screenshot ----------
        if any(kw in text for kw in ["screenshot", "screen shot", "screen capture", "screen capture karo"]):
            return self.sys.take_screenshot()

        # ---------- 5. Time ----------
        time_kw = [
            "what time", "what's the time", "what is the time",
            "time kya", "kitna baja", "samay kya", "time batao", "time kya hua",
        ]
        if any(kw in text for kw in time_kw):
            return self.sys.get_time()

        # ---------- 6. Date ----------
        date_kw = [
            "what date", "what's the date", "what is the date",
            "today's date", "aaj kya din", "aaj ki tarikh",
            "aaj kaunsi date", "date batao", "aaj kya date hai",
        ]
        if any(kw in text for kw in date_kw):
            return self.sys.get_date()
        # ---------- 7. Battery ----------
        if "battery" in text or "charge kitni" in text:
            return self.sys.get_battery()

        # ---------- 8. CPU ----------
        if "cpu" in text and any(kw in text for kw in ["usage", "use", "percent", "kitna"]):
            return self.sys.get_cpu_usage()

        # ---------- 9. RAM ----------
        if "ram" in text and any(kw in text for kw in ["usage", "use", "percent", "kitna"]):
            return self.sys.get_ram_usage()

        # ---------- 10. IP ----------
        if any(kw in text for kw in ["ip address", "ip kya", "mera ip", "my ip"]):
            return self.sys.get_ip()

        # No command matched — let LLM handle it
        return None