#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Editor Plus - Main Entry Point
Advanced Text Editor with Syntax Highlighting and Auto-Formatting
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.text_editor import TextEditor
from src.themes import ThemeManager


def main():
    """Main entry point"""
    # Enable High DPI scaling support
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Set High DPI scale factor rounding policy for better scaling
    if hasattr(QApplication, 'setHighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    
    # Set environment variable for better DPI handling on Windows
    if sys.platform == 'win32':
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    
    app = QApplication(sys.argv)
    app.setApplicationName("Text Editor Plus")
    
    editor = TextEditor()
    editor.show()
    
    # Apply title bar theme after window is shown
    ThemeManager.update_title_bar_theme(editor, editor.current_theme)
    
    # Check for command-line arguments (file paths from "Open with")
    if len(sys.argv) > 1:
        # Get the file path from command-line arguments
        filepath = sys.argv[1]
        # Open the file if it exists
        if os.path.exists(filepath) and os.path.isfile(filepath):
            editor.open_file_from_path(filepath)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

