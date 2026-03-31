cat > main.py << 'EOF'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import subprocess
import os
from datetime import datetime

class SecurityScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        title = Label(text='🔒 SecurityGuard', font_size=30, size_hint_y=None, height=60)
        self.add_widget(title)
        
        scan_btn = Button(text='🛡️ Full System Scan', size_hint_y=None, height=60, font_size=20)
        scan_btn.bind(on_press=self.full_scan)
        self.add_widget(scan_btn)
        
        root_btn = Button(text='👑 Root Detection', size_hint_y=None, height=50)
        root_btn.bind(on_press=self.check_root)
        self.add_widget(root_btn)
        
        forward_btn = Button(text='📱 Forwarding Check', size_hint_y=None, height=50)
        forward_btn.bind(on_press=self.check_forwarding)
        self.add_widget(forward_btn)
        
        self.status = Label(text='Ready to scan...', font_size=16)
        self.add_widget(self.status)
        
        self.report = Label(text='', font_size=14, halign='left', valign='top', text_size=(None, None))
        self.add_widget(self.report)
    
    def log_report(self, title, details):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_path = '/sdcard/SecurityGuard/'
        os.makedirs(report_path, exist_ok=True)
        
        with open(f'{report_path}{title}_{timestamp}.txt', 'w') as f:
            f.write(f'SecurityGuard Report - {timestamp}\n')
            f.write(f'Title: {title}\n\n')
            f.write(details)
        
        self.status.text = f'✅ Report saved: {report_path}'
    
    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            return result.stdout + result.stderr
        except:
            return "Command failed"
    
    def full_scan(self, instance):
        self.status.text = '🔍 Scanning...'
        
        # Root check
        root = self.check_root()
        
        # Suspicious packages
        packages = self.run_command("pm list packages | grep -E '(root|su|magisk|kingroot)'")
        
        # Forwarding services
        forwarding = self.run_command("dumpsys telephony.registry | grep -i forward")
        
        report = f"ROOT: {root}\nPACKAGES: {packages}\nFORWARDING: {forwarding}"
        self.report.text = report[:500] + "..."
        self.log_report("full_scan", report)
    
    def check_root(self, instance=None):
        tests = [
            self.run_command("which su"),
            self.run_command("ls /system/xbin/su"),
            self.run_command("id | grep uid=0"),
        ]
        root_detected = any("No such file" not in t and len(t.strip()) > 0 for t in tests)
        status = "🚨 ROOT DETECTED!" if root_detected else "✅ No root found"
        self.status.text = status
        self.log_report("root_check", f"Root status: {'Detected' if root_detected else 'Clean'}")
        return status
    
    def check_forwarding(self, instance):
        self.status.text = '📞 Checking call forwarding...'
        result = self.run_command("dumpsys telephony.registry | grep -i 'call forwarding\|forward'")
        self.report.text = result[:800]
        self.log_report("forwarding_check", result)

class SecurityApp(App):
    def build(self):
        return SecurityScreen()

if __name__ == '__main__':
    SecurityApp().run()
EOF
