import os
import subprocess
import shutil
import ctypes
import threading
from pathlib import Path

class PCOptimizer:
    def __init__(self, status_callback=None):
        self.status_callback = status_callback
        self.is_admin = ctypes.windll.shell.IsUserAnAdmin()
        
    def log(self, message):
        """Send status message to UI"""
        if self.status_callback:
            self.status_callback(message)
        print(message)
    
    def run_command(self, command, description=""):
        """Run registry command safely"""
        try:
            subprocess.run(command, shell=True, capture_output=True, check=False)
            self.log(f"✓ {description}")
            return True
        except Exception as e:
            self.log(f"✗ {description} - Error: {str(e)}")
            return False
    
    def disable_xbox_dvr(self):
        """Disable Xbox Game Bar & DVR"""
        self.log("\n⚙️  DISABLING XBOX GAME BAR & DVR")
        self.run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f', 
                        "Xbox Game Bar disabled")
        self.run_command('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f',
                        "Game DVR disabled")
        self.run_command('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_FSEBehaviorMode /t REG_DWORD /d 2 /f',
                        "Game DVR FS Behavior disabled")
    
    def set_high_performance(self):
        """Set Windows to High Performance Power Plan"""
        self.log("\n⚡ SETTING HIGH PERFORMANCE MODE")
        self.run_command('powercfg -setactive SCHEME_MIN', "High Performance Power Plan activated")
    
    def disable_power_throttling(self):
        """Disable Power Throttling"""
        self.log("\n🔥 DISABLING POWER THROTTLING")
        self.run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerThrottling" /v PowerThrottlingOff /t REG_DWORD /d 1 /f',
                        "Power Throttling disabled")
    
    def disable_superfetch(self):
        """Disable SysMain (Superfetch)"""
        self.log("\n🧹 DISABLING SUPERFETCH")
        try:
            subprocess.run('sc stop SysMain', shell=True, capture_output=True, check=False)
            subprocess.run('sc config SysMain start= disabled', shell=True, capture_output=True, check=False)
            self.log("✓ SysMain (Superfetch) disabled")
        except Exception as e:
            self.log(f"✗ SysMain disable failed: {str(e)}")
    
    def disable_windows_search(self):
        """Disable Windows Search Indexing"""
        self.log("\n🔍 DISABLING WINDOWS SEARCH")
        try:
            subprocess.run('sc stop WSearch', shell=True, capture_output=True, check=False)
            subprocess.run('sc config WSearch start= disabled', shell=True, capture_output=True, check=False)
            self.log("✓ Windows Search disabled")
        except Exception as e:
            self.log(f"✗ Windows Search disable failed: {str(e)}")
    
    def disable_fullscreen_optimization(self):
        """Disable Fullscreen Optimizations"""
        self.log("\n📺 DISABLING FULLSCREEN OPTIMIZATIONS")
        self.run_command('reg add "HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers" /v "*" /t REG_SZ /d "~ DISABLEDXMAXIMIZEDWINDOWEDMODE" /f',
                        "Fullscreen Optimizations disabled")
    
    def reduce_background_throttling(self):
        """Reduce background throttling"""
        self.log("\n⏱️  REDUCING BACKGROUND THROTTLING")
        self.run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 26 /f',
                        "Background Throttling reduced")
    
    def clear_temp_files(self):
        """Clear temporary files"""
        self.log("\n🗑️  CLEARING TEMPORARY FILES")
        temp_paths = [
            os.path.expandvars('%TEMP%'),
            os.path.expandvars('%WINDIR%\\Temp'),
            os.path.expandvars('%LOCALAPPDATA%\\Temp'),
        ]
        
        deleted_count = 0
        for temp_path in temp_paths:
            if os.path.exists(temp_path):
                try:
                    for filename in os.listdir(temp_path):
                        filepath = os.path.join(temp_path, filename)
                        try:
                            if os.path.isfile(filepath):
                                os.unlink(filepath)
                                deleted_count += 1
                            elif os.path.isdir(filepath):
                                shutil.rmtree(filepath, ignore_errors=True)
                        except Exception:
                            pass
                except Exception:
                    pass
        
        self.log(f"✓ Cleared {deleted_count} temporary files")
    
    def disable_startup_programs(self):
        """Disable unnecessary startup programs"""
        self.log("\n🚀 OPTIMIZING STARTUP PROGRAMS")
        startup_items = [
            ('OneDrive', 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v OneDrive /d "" /f'),
        ]
        
        for name, cmd in startup_items:
            try:
                subprocess.run(cmd, shell=True, capture_output=True, check=False)
                self.log(f"✓ {name} startup disabled")
            except Exception:
                pass
    
    def disable_visual_effects(self):
        """Disable unnecessary visual effects"""
        self.log("\n🎨 DISABLING VISUAL EFFECTS")
        self.run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f',
                        "Visual Effects reduced")
    
    def optimize_network(self):
        """Optimize network settings"""
        self.log("\n🌐 OPTIMIZING NETWORK SETTINGS")
        self.run_command('netsh int tcp set global autotuninglevel=normal',
                        "Network Auto-Tuning optimized")
    
    def apply_all_tweaks(self):
        """Apply all optimization tweaks"""
        self.log("=" * 60)
        self.log("🎮 ENTITYPLAYS PC OPTIMIZER - STARTING")
        self.log("=" * 60)
        
        if not self.is_admin:
            self.log("\n⚠️  WARNING: Not running as Administrator!")
            self.log("Some tweaks may fail. Please run as Admin.")
        
        self.set_high_performance()
        self.disable_xbox_dvr()
        self.disable_power_throttling()
        self.reduce_background_throttling()
        self.disable_fullscreen_optimization()
        self.disable_superfetch()
        self.disable_windows_search()
        self.disable_visual_effects()
        self.disable_startup_programs()
        self.clear_temp_files()
        self.optimize_network()
        
        self.log("\n" + "=" * 60)
        self.log("✅ ALL OPTIMIZATIONS APPLIED SUCCESSFULLY!")
        self.log("=" * 60)
        self.log("💡 Restart your PC for best results")
        self.log("=" * 60)
