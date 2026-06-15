import sys
import threading
import ctypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox)
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
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

class EntityPlaysOptimizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.thread = None
        self.is_optimizing = False
        self.init_ui()
        self.check_admin()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("EntityPlays - PC Optimizer")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Logo/Title
        title_label = QLabel("EntityPlays")
        title_font = QFont("Arial", 32, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #00D4FF; text-shadow: 0px 0px 10px #00D4FF;")
        
        subtitle_label = QLabel("PC Optimizer")
        subtitle_font = QFont("Arial", 16)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #FFFFFF;")
        
        title_vbox = QVBoxLayout()
        title_vbox.addWidget(title_label)
        title_vbox.addWidget(subtitle_label)
        header_layout.addLayout(title_vbox)
        header_layout.addStretch()
        
        # Info label
        info_label = QLabel("by Vishnu Branding")
        info_font = QFont("Arial", 10)
        info_label.setFont(info_font)
        info_label.setStyleSheet("color: #888888;")
        header_layout.addWidget(info_label, alignment=Qt.AlignRight | Qt.AlignTop)
        
        main_layout.addLayout(header_layout)
        
        # Separator
        separator = QLabel("━" * 60)
        separator.setStyleSheet("color: #00D4FF;")
        main_layout.addWidget(separator)
        
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
        main_layout.addWidget(info_section)
        
        # Status/Log area
        log_label = QLabel("📋 Optimization Log:")
        log_label.setFont(QFont("Arial", 12, QFont.Bold))
        log_label.setStyleSheet("color: #00D4FF;")
        main_layout.addWidget(log_label)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet(
            "QTextEdit { background-color: #1a1a1a; color: #00FF00; font-family: 'Courier New'; "
            "font-size: 10px; border: 2px solid #00D4FF; border-radius: 5px; padding: 10px; }"
        )
        self.log_display.setFont(QFont("Courier New", 9))
        main_layout.addWidget(self.log_display)
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.optimize_btn = QPushButton("🚀 START OPTIMIZATION")
        self.optimize_btn.setFont(QFont("Arial", 13, QFont.Bold))
        self.optimize_btn.setCursor(Qt.PointingHandCursor)
        self.optimize_btn.setStyleSheet(self.get_button_stylesheet())
        self.optimize_btn.setMinimumHeight(50)
        self.optimize_btn.setMinimumWidth(250)
        self.optimize_btn.clicked.connect(self.start_optimization)
        
        clear_btn = QPushButton("🗑️  Clear Log")
        clear_btn.setFont(QFont("Arial", 11))
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet(self.get_secondary_button_stylesheet())
        clear_btn.setMinimumHeight(50)
        clear_btn.setMinimumWidth(150)
        clear_btn.clicked.connect(self.log_display.clear)
        
        button_layout.addWidget(self.optimize_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Footer
        footer = QLabel("⚠️  Administrator privileges required for full optimization | Restart your PC after optimization")
        footer.setFont(QFont("Arial", 9))
        footer.setStyleSheet("color: #FF6B6B;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
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
                transition: all 0.3s ease;
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
    
    def check_admin(self):
        """Check if running as admin"""
        is_admin = ctypes.windll.shell.IsUserAnAdmin()
        if not is_admin:
            self.add_log("⚠️  WARNING: Not running as Administrator!")
            self.add_log("Some optimizations may fail or be skipped.")
            self.add_log("Please restart the application as Administrator.")
            self.add_log("")
    
    def add_log(self, message):
        """Add message to log display"""
        current_text = self.log_display.toPlainText()
        if current_text:
            self.log_display.setText(current_text + "\n" + message)
        else:
            self.log_display.setText(message)
        
        # Auto-scroll to bottom
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def start_optimization(self):
        """Start the optimization process"""
        if self.is_optimizing:
            QMessageBox.warning(self, "Already Running", "Optimization is already in progress!")
            return
        
        # Confirm with user
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
        self.add_log("🎮 EntityPlays PC Optimizer started...\n")
        
        # Create worker thread
        self.thread = QThread()
        self.worker = OptimizeWorker()
        self.worker.moveToThread(self.thread)
        
        # Connect signals
        self.worker.status_update.connect(self.add_log)
        self.worker.finished.connect(self.optimization_finished)
        self.thread.started.connect(self.worker.run)
        
        # Start thread
        self.thread.start()
    
    def optimization_finished(self):
        """Called when optimization is finished"""
        self.is_optimizing = False
        self.optimize_btn.setEnabled(True)
        self.optimize_btn.setText("🚀 START OPTIMIZATION")
        self.thread.quit()
        self.thread.wait()
        
        QMessageBox.information(self, "Success! 🎉",
                               "All optimizations have been applied successfully!\n\n"
                               "💡 Please restart your PC for best results.")

def main():
    app = QApplication(sys.argv)
    window = EntityPlaysOptimizer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
