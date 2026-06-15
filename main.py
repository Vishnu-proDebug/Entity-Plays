import sys
import threading
import subprocess
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox,
                             QTabWidget, QScrollArea)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from optimizer import PCOptimizer

class OptimizeWorker(QObject):
    """Worker thread for optimization"""
    finished = pyqtSignal()
    status_update = pyqtSignal(str)
    
    def run(self):
        optimizer = PCOptimizer(status_callback=self.status_update.emit)
        optimizer.apply_all_tweaks()
        self.finished.emit()

class MouseOptimizeWorker(QObject):
    """Worker thread for mouse optimization"""
    finished = pyqtSignal()
    status_update = pyqtSignal(str)
    
    def run(self):
        try:
            self.status_update.emit("🖱️  APPLYING MOUSE AIM OPTIMIZATION")
            self.status_update.emit("Loading Ultimate Mouse Linear Settings...")
            
            # Apply mouse optimization registry settings
            commands = [
                'reg add "HKCU\\Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 0 /f',
                'reg add "HKCU\\Control Panel\\Mouse" /v MouseThreshold1 /t REG_SZ /d 0 /f',
                'reg add "HKCU\\Control Panel\\Mouse" /v MouseThreshold2 /t REG_SZ /d 0 /f',
                'reg add "HKCU\\Control Panel\\Mouse" /v MouseSensitivity /t REG_SZ /d 6 /f',
                'reg add "HKCU\\Control Panel\\Mouse" /v MouseTrails /t REG_SZ /d 0 /f',
                'reg add "HKCU\\Control Panel\\Mouse" /v EnhancePointerPrecision /t REG_SZ /d 0 /f',
                'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouclass\\Parameters" /v SmoothMouse /t REG_DWORD /d 0 /f',
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True, capture_output=True, check=False)
            
            self.status_update.emit("✓ Mouse acceleration disabled")
            self.status_update.emit("✓ Mouse threshold optimized")
            self.status_update.emit("✓ Linear mouse response enabled")
            self.status_update.emit("✓ Smooth mouse curves applied")
            self.status_update.emit("✓ Enhanced pointer precision disabled")
            self.status_update.emit("\n✅ MOUSE AIM OPTIMIZATION COMPLETE!")
            self.status_update.emit("💡 Restart your game for best results\n")
            
        except Exception as e:
            self.status_update.emit(f"✗ Error: {str(e)}")
        
        self.finished.emit()

class EntityPlaysOptimizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.thread = None
        self.is_optimizing = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("VishnuXtamim Sensi - PC Optimizer")
        self.setGeometry(50, 50, 1100, 800)
        self.setStyleSheet(self.get_stylesheet())
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Logo
        try:
            logo_label = QLabel()
            logo_pixmap = QPixmap("logo.png")
            if not logo_pixmap.isNull():
                logo_pixmap = logo_pixmap.scaledToHeight(80, Qt.SmoothTransformation)
                logo_label.setPixmap(logo_pixmap)
            header_layout.addWidget(logo_label)
        except:
            pass
        
        # Title
        title_label = QLabel("VishnuXtamim_Sensi")
        title_font = QFont("Arial", 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #00D4FF; text-shadow: 0px 0px 10px #00D4FF;")
        
        subtitle_label = QLabel("Gaming Performance Optimizer")
        subtitle_font = QFont("Arial", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #FFFFFF;")
        
        title_vbox = QVBoxLayout()
        title_vbox.addWidget(title_label)
        title_vbox.addWidget(subtitle_label)
        header_layout.addLayout(title_vbox)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Separator
        separator = QLabel("━" * 80)
        separator.setStyleSheet("color: #00D4FF;")
        main_layout.addWidget(separator)
        
        # Create Tab Widget
        tabs = QTabWidget()
        tabs.setStyleSheet(self.get_tab_stylesheet())
        
        # Tab 1: Optimization
        opt_widget = self.create_optimization_tab()
        tabs.addTab(opt_widget, "🎮 System Optimization")
        
        # Tab 2: Mouse Aim
        mouse_widget = self.create_mouse_optimization_tab()
        tabs.addTab(mouse_widget, "🖱️  Mouse Aim Optimizer")
        
        # Tab 3: Personal Settings
        settings_widget = self.create_personal_settings_tab()
        tabs.addTab(settings_widget, "⚙️  My Personal Settings")
        
        main_layout.addWidget(tabs)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def create_optimization_tab(self):
        """Create PC optimization tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Info section
        info_section = QLabel("⚡ Boost your gaming performance with one click!\n\n"
                             "This optimizer will:\n"
                             "✓ Disable unnecessary background services\n"
                             "✓ Enable High Performance mode\n"
                             "✓ Clear temporary files\n"
                             "✓ Optimize system settings\n"
                             "✓ Maximize FPS & reduce latency")
        info_section.setFont(QFont("Arial", 11))
        info_section.setStyleSheet("color: #CCCCCC; background: rgba(0, 212, 255, 0.1); padding: 15px; border-radius: 5px; border-left: 4px solid #00D4FF;")
        layout.addWidget(info_section)
        
        # Status/Log area
        log_label = QLabel("📋 Optimization Log:")
        log_label.setFont(QFont("Arial", 12, QFont.Bold))
        log_label.setStyleSheet("color: #00D4FF;")
        layout.addWidget(log_label)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet(
            "QTextEdit { background-color: #1a1a1a; color: #00FF00; font-family: 'Courier New'; "
            "font-size: 10px; border: 2px solid #00D4FF; border-radius: 5px; padding: 10px; }"
        )
        self.log_display.setFont(QFont("Courier New", 9))
        layout.addWidget(self.log_display)
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.optimize_btn = QPushButton("🚀 START SYSTEM OPTIMIZATION")
        self.optimize_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.optimize_btn.setCursor(Qt.PointingHandCursor)
        self.optimize_btn.setStyleSheet(self.get_button_stylesheet())
        self.optimize_btn.setMinimumHeight(45)
        self.optimize_btn.setMinimumWidth(250)
        self.optimize_btn.clicked.connect(self.start_optimization)
        
        clear_btn = QPushButton("🗑️  Clear Log")
        clear_btn.setFont(QFont("Arial", 11))
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet(self.get_secondary_button_stylesheet())
        clear_btn.setMinimumHeight(45)
        clear_btn.setMinimumWidth(150)
        clear_btn.clicked.connect(self.log_display.clear)
        
        button_layout.addWidget(self.optimize_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_mouse_optimization_tab(self):
        """Create mouse optimization tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Info section
        info_section = QLabel("🖱️  ULTIMATE MOUSE LINEAR OPTIMIZATION\n\n"
                             "Optimized for: Free Fire Gaming\n"
                             "Ant Esports GM320 @ 800 DPI\n\n"
                             "This will:\n"
                             "✓ Disable mouse acceleration\n"
                             "✓ Disable enhanced pointer precision\n"
                             "✓ Enable linear mouse response\n"
                             "✓ Optimize mouse sensitivity\n"
                             "✓ Remove mouse smoothing")
        info_section.setFont(QFont("Arial", 11))
        info_section.setStyleSheet("color: #CCCCCC; background: rgba(255, 100, 50, 0.1); padding: 15px; border-radius: 5px; border-left: 4px solid #FF6432;")
        layout.addWidget(info_section)
        
        # Log area
        log_label = QLabel("📋 Mouse Optimization Log:")
        log_label.setFont(QFont("Arial", 12, QFont.Bold))
        log_label.setStyleSheet("color: #FF6432;")
        layout.addWidget(log_label)
        
        self.mouse_log_display = QTextEdit()
        self.mouse_log_display.setReadOnly(True)
        self.mouse_log_display.setStyleSheet(
            "QTextEdit { background-color: #1a1a1a; color: #FF9900; font-family: 'Courier New'; "
            "font-size: 10px; border: 2px solid #FF6432; border-radius: 5px; padding: 10px; }"
        )
        self.mouse_log_display.setFont(QFont("Courier New", 9))
        layout.addWidget(self.mouse_log_display)
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        mouse_btn = QPushButton("🖱️  APPLY MOUSE AIM OPTIMIZATION")
        mouse_btn.setFont(QFont("Arial", 12, QFont.Bold))
        mouse_btn.setCursor(Qt.PointingHandCursor)
        mouse_btn.setStyleSheet(self.get_mouse_button_stylesheet())
        mouse_btn.setMinimumHeight(45)
        mouse_btn.setMinimumWidth(250)
        mouse_btn.clicked.connect(self.start_mouse_optimization)
        
        clear_mouse_btn = QPushButton("🗑️  Clear Log")
        clear_mouse_btn.setFont(QFont("Arial", 11))
        clear_mouse_btn.setCursor(Qt.PointingHandCursor)
        clear_mouse_btn.setStyleSheet(self.get_secondary_button_stylesheet())
        clear_mouse_btn.setMinimumHeight(45)
        clear_mouse_btn.setMinimumWidth(150)
        clear_mouse_btn.clicked.connect(self.mouse_log_display.clear)
        
        button_layout.addWidget(mouse_btn)
        button_layout.addWidget(clear_mouse_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_personal_settings_tab(self):
        """Create personal settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: 2px solid #00D4FF; border-radius: 5px; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        # Title
        title = QLabel("⚙️  MY PERSONAL BEST SENSITIVITY & SETTINGS")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #00D4FF;")
        content_layout.addWidget(title)
        
        # Settings content
        settings_text = QLabel(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📋 EMULATOR & RESOLUTION SETTINGS:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  EMULATOR DPI: 600\n\n"
            "2️⃣  RESOLUTION OPTIONS:\n"
            "    • 1920 x 1080 (If no dedicated Graphics Card)\n"
            "    • 3840 x 2160 (Only when you have dedicated GPU)\n\n"
            "3️⃣  EMULATOR X & Y SETTINGS:\n"
            "    • X-Axis: 3.65\n"
            "    • Y-Axis: 1.65\n\n"
            "4️⃣  MOUSE DPI: 1600\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🎮 IN-GAME SETTINGS:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Display: ULTRA\n"
            "FPS: HIGH\n"
            "Sensitivity: GENERAL - 11\n"
            "Rest All Settings: 0\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        settings_text.setFont(QFont("Courier New", 10))
        settings_text.setStyleSheet("color: #00FF00; background: rgba(0, 212, 255, 0.05); padding: 15px; border-radius: 5px;")
        settings_text.setWordWrap(True)
        content_layout.addWidget(settings_text)
        
        # Separator
        sep = QLabel("━" * 60)
        sep.setStyleSheet("color: #FF6432;")
        content_layout.addWidget(sep)
        
        # Paid Settings Info
        paid_info = QLabel(
            "💰 PERSONALIZED PAID SETTINGS & OPTIMIZATION\n\n"
            "For Custom Paid Settings, Contact:\n\n"
            "📧 EMAIL: vishnutam2011@gmail.com\n\n"
            "📱 INSTAGRAM:\n"
            "   • @Vishnu_tam.0023m\n"
            "   • @_tamim_official_459\n\n"
            "📞 WHATSAPP: 7460063550\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💵 PRICING:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "• Paid Settings Only: ₹100\n"
            "• Paid Settings + Full Optimization: ₹150\n"
            "• No Recoil + 99% Headshot Settings: ₹99\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        paid_info.setFont(QFont("Arial", 10))
        paid_info.setStyleSheet("color: #FFD700; background: rgba(255, 100, 50, 0.1); padding: 15px; border-radius: 5px; border-left: 4px solid #FFD700;")
        paid_info.setWordWrap(True)
        content_layout.addWidget(paid_info)
        
        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def get_stylesheet(self):
        """Get main stylesheet"""
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #0a0e27, stop:1 #1a1a3e);
            }
            QLabel {
                color: #FFFFFF;
            }
            QTabWidget::pane {
                border: 2px solid #00D4FF;
                border-radius: 5px;
            }
        """
    
    def get_tab_stylesheet(self):
        """Get tab widget stylesheet"""
        return """
            QTabBar::tab {
                background: #1a1a3e;
                color: #CCCCCC;
                padding: 8px 20px;
                border: 1px solid #00D4FF;
                border-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #00D4FF;
                color: #000000;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #0099CC;
                color: #FFFFFF;
            }
        """
    
    def get_button_stylesheet(self):
        """Get optimize button stylesheet"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #00D4FF, stop:1 #0099CC);
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #00E5FF, stop:1 #00AADD);
                box-shadow: 0 0 20px #00D4FF;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #0088BB, stop:1 #005588);
            }
            QPushButton:disabled {
                background: #444444;
                color: #888888;
            }
        """
    
    def get_mouse_button_stylesheet(self):
        """Get mouse button stylesheet"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #FF6432, stop:1 #CC5025);
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #FF7A4D, stop:1 #DD6535);
                box-shadow: 0 0 20px #FF6432;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #DD5220, stop:1 #BB4118);
            }
            QPushButton:disabled {
                background: #444444;
                color: #888888;
            }
        """
    
    def get_secondary_button_stylesheet(self):
        """Get secondary button stylesheet"""
        return """
            QPushButton {
                background: #333333;
                color: #FFFFFF;
                border: 2px solid #00D4FF;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #444444;
                box-shadow: 0 0 10px #00D4FF;
            }
            QPushButton:pressed {
                background: #222222;
            }
        """
    
    def add_log(self, message):
        """Add message to log display"""
        current_text = self.log_display.toPlainText()
        if current_text:
            self.log_display.setText(current_text + "\n" + message)
        else:
            self.log_display.setText(message)
        
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def add_mouse_log(self, message):
        """Add message to mouse log display"""
        current_text = self.mouse_log_display.toPlainText()
        if current_text:
            self.mouse_log_display.setText(current_text + "\n" + message)
        else:
            self.mouse_log_display.setText(message)
        
        scrollbar = self.mouse_log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def start_optimization(self):
        """Start the optimization process"""
        if self.is_optimizing:
            QMessageBox.warning(self, "Already Running", "Optimization is already in progress!")
            return
        
        reply = QMessageBox.question(self, "Confirm Optimization",
                                    "This will apply system optimizations.\n\n"
                                    "Make sure to:\n"
                                    "• Close all important applications\n"
                                    "• Run as Administrator\n\n"
                                    "Continue?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.No:
            return
        
        self.is_optimizing = True
        self.optimize_btn.setEnabled(False)
        self.optimize_btn.setText("⏳ OPTIMIZING...")
        self.log_display.clear()
        self.add_log("🎮 VishnuXtamim Optimizer started...\n")
        
        self.thread = QThread()
        self.worker = OptimizeWorker()
        self.worker.moveToThread(self.thread)
        
        self.worker.status_update.connect(self.add_log)
        self.worker.finished.connect(self.optimization_finished)
        self.thread.started.connect(self.worker.run)
        
        self.thread.start()
    
    def optimization_finished(self):
        """Called when optimization is finished"""
        self.is_optimizing = False
        self.optimize_btn.setEnabled(True)
        self.optimize_btn.setText("🚀 START SYSTEM OPTIMIZATION")
        self.thread.quit()
        self.thread.wait()
        
        QMessageBox.information(self, "Success! 🎉",
                               "All optimizations have been applied successfully!\n\n"
                               "💡 Please restart your PC for best results.")
    
    def start_mouse_optimization(self):
        """Start mouse optimization"""
        reply = QMessageBox.question(self, "Confirm Mouse Optimization",
                                    "This will apply Ultimate Mouse Linear settings.\n\n"
                                    "Optimized for:\n"
                                    "• Free Fire Gaming\n"
                                    "• Ant Esports GM320 @ 800 DPI\n\n"
                                    "Continue?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.No:
            return
        
        self.mouse_log_display.clear()
        
        self.thread = QThread()
        self.worker = MouseOptimizeWorker()
        self.worker.moveToThread(self.thread)
        
        self.worker.status_update.connect(self.add_mouse_log)
        self.worker.finished.connect(self.mouse_optimization_finished)
        self.thread.started.connect(self.worker.run)
        
        self.thread.start()
    
    def mouse_optimization_finished(self):
        """Called when mouse optimization is finished"""
        self.thread.quit()
        self.thread.wait()
        
        QMessageBox.information(self, "Success! 🎉",
                               "Mouse AIM Optimization applied successfully!\n\n"
                               "💡 Restart your game for best results!")

def main():
    app = QApplication(sys.argv)
    window = EntityPlaysOptimizer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
