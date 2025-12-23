#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Editor Module
Main text editor application window
"""

import sys
import os
import re
import json
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QMenuBar, QMenu, QFileDialog, 
                             QMessageBox, QStatusBar, QToolBar, QAction, 
                             QVBoxLayout, QWidget, QPlainTextEdit, QDialog, 
                             QDialogButtonBox, QFormLayout, QSpinBox, QLineEdit,
                             QCheckBox, QLabel, QHBoxLayout, QPushButton, QFrame,
                             QTextEdit, QTextBrowser, QScrollArea, QApplication)
from PyQt5.QtCore import Qt, QSize, QPoint, QFile, QTextStream
from PyQt5.QtGui import QKeySequence, QTextCursor, QTextDocument, QFont, QIcon

from .code_editor import CodeEditor
from .syntax_highlighter import SyntaxHighlighter
from .formatters import Formatters
from .themes import ThemeManager
from .utils import detect_language, detect_file_type_from_content


class TextEditor(QMainWindow):
    """Main text editor window"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.highlighter = None
        self.current_theme = 'dark'  # Default theme
        self.find_bar = None  # Find bar widget
        self.init_ui()
        ThemeManager.apply_theme(self, 'dark')
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("SmartPad")
        
        # Set window icon
        icon_path = Path(__file__).parent / "logo.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Get screen geometry for responsive sizing
        screen = self.screen().availableGeometry()
        # Use 80% of screen size, but with minimum and maximum constraints
        width = max(800, min(1600, int(screen.width() * 0.8)))
        height = max(600, min(1200, int(screen.height() * 0.8)))
        
        # Center window on screen
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        
        self.setGeometry(x, y, width, height)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create text editor with line numbers
        self.text_edit = CodeEditor()
        layout.addWidget(self.text_edit)
        
        # Create find bar (initially hidden)
        self.find_bar = FindBar(self)
        self.find_bar.hide()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Connect text change signal
        self.text_edit.textChanged.connect(self.on_text_changed)
    
    def create_menu_bar(self):
        """Create menu bar with actions"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New', self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save As...', self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        find_action = QAction('Find...', self)
        find_action.setShortcut(QKeySequence.Find)
        find_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(find_action)
        
        find_next_action = QAction('Find Next', self)
        find_next_action.setShortcut(QKeySequence("F3"))
        find_next_action.triggered.connect(self.find_next)
        edit_menu.addAction(find_next_action)
        
        edit_menu.addSeparator()
        
        format_action = QAction('Auto-Formatting', self)
        format_action.setShortcut(QKeySequence("Ctrl+Shift+F"))
        format_action.triggered.connect(self.auto_format)
        edit_menu.addAction(format_action)
        
        edit_menu.addSeparator()
        
        undo_action = QAction('Undo', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('Redo', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction('Cut', self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction('Copy', self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('Paste', self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)
        
        select_all_action = QAction('Select All', self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        word_wrap_action = QAction('Word Wrap', self)
        word_wrap_action.setCheckable(True)
        word_wrap_action.setChecked(False)
        word_wrap_action.triggered.connect(self.toggle_word_wrap)
        edit_menu.addAction(word_wrap_action)
        
        # Settings menu
        settings_menu = menubar.addMenu('Settings')
        
        theme_menu = settings_menu.addMenu('Theme')
        
        dark_theme_action = QAction('Dark Theme', self)
        dark_theme_action.setCheckable(True)
        dark_theme_action.setChecked(True)
        dark_theme_action.triggered.connect(lambda: self.change_theme('dark'))
        theme_menu.addAction(dark_theme_action)
        
        light_theme_action = QAction('Light Theme', self)
        light_theme_action.setCheckable(True)
        light_theme_action.triggered.connect(lambda: self.change_theme('light'))
        theme_menu.addAction(light_theme_action)
        
        # Create theme action group
        self.theme_actions = [dark_theme_action, light_theme_action]
        
        settings_menu.addSeparator()
        
        font_size_action = QAction('Font Size...', self)
        font_size_action.triggered.connect(self.change_font_size)
        settings_menu.addAction(font_size_action)
        
        # Help menu
        help_action = QAction('About', self)
        help_action.setShortcut(QKeySequence("F1"))
        help_action.triggered.connect(self.show_help)
        menubar.addAction(help_action)
    
    def create_toolbar(self):
        """Create toolbar with common actions"""
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # Show text beside icon
        
        # Icon size scales with DPI - smaller size
        try:
            dpi_scale = self.devicePixelRatioF()
        except:
            dpi_scale = 1.0
        # Base icon size: 18 (reduced from 20)
        base_icon_size = 18
        icon_size = int(base_icon_size * max(1.0, dpi_scale))
        toolbar.setIconSize(QSize(icon_size, icon_size))
        
        # Set toolbar button size - smaller height
        toolbar.setMinimumHeight(int(30 * max(1.0, dpi_scale)))
        
        self.addToolBar(toolbar)
        
        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        format_action = QAction('Auto-Formatting', self)
        format_action.setShortcut(QKeySequence("Ctrl+Shift+F"))
        format_action.triggered.connect(self.auto_format)
        toolbar.addAction(format_action)
    
    def change_theme(self, theme):
        """Change application theme"""
        self.current_theme = theme
        ThemeManager.apply_theme(self, theme)
        # Update code editor theme
        if hasattr(self, 'text_edit'):
            self.text_edit.set_theme(theme)
        # Update syntax highlighter colors if needed
        if self.highlighter:
            self.highlighter.set_theme(theme)
        # Update find bar theme
        if hasattr(self, 'find_bar') and self.find_bar:
            self.find_bar.apply_theme()
        # Update title bar
        ThemeManager.update_title_bar_theme(self, theme)
        # Update theme action check states
        if hasattr(self, 'theme_actions'):
            self.theme_actions[0].setChecked(theme == 'dark')
            self.theme_actions[1].setChecked(theme == 'light')
    
    def toggle_word_wrap(self, checked):
        """Toggle word wrap"""
        if checked:
            self.text_edit.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)
    
    def change_font_size(self):
        """Open dialog to change font size"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Font Size")
        # Make dialog responsive to DPI
        dialog.setMinimumSize(300, 100)
        layout = QFormLayout(dialog)
        
        spin_box = QSpinBox()
        spin_box.setRange(8, 72)
        current_size = self.text_edit.font().pointSize()
        spin_box.setValue(current_size)
        layout.addRow("Font Size:", spin_box)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            font = self.text_edit.font()
            font.setPointSize(spin_box.value())
            self.text_edit.setFont(font)
            # Update tab stop width when font changes
            metrics = self.text_edit.fontMetrics()
            tab_width = metrics.width(' ') * 4
            self.text_edit.setTabStopWidth(tab_width)
    
    def update_syntax_highlighting(self, language):
        """Update syntax highlighting based on language or content"""
        # If language is generic, try to detect from content
        if language == 'generic':
            content = self.text_edit.toPlainText()
            detected = detect_file_type_from_content(content)
            if detected:
                language = detected
        
        if self.highlighter:
            self.highlighter.setDocument(None)
        
        self.highlighter = SyntaxHighlighter(
            self.text_edit.document(), 
            language, 
            self.current_theme
        )
        self.status_bar.showMessage(f"Language: {language.upper()}")
    
    def new_file(self):
        """Create a new file"""
        if self.maybe_save():
            self.text_edit.clear()
            self.text_edit.document().setModified(False)  # Mark as unmodified
            self.current_file = None
            self.setWindowTitle("SmartPad - Untitled")
            if self.highlighter:
                self.highlighter.setDocument(None)
                self.highlighter = None
            self.status_bar.showMessage("New file created")
    
    def open_file(self):
        """Open a file"""
        if self.maybe_save():
            filename, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", "All Files (*.*)"
            )
            if filename:
                self.open_file_from_path(filename)
    
    def open_file_from_path(self, filepath):
        """Open a file from a given file path (used for command-line arguments and 'Open with')"""
        if not filepath:
            return False
        
        # Check if file exists
        if not os.path.exists(filepath):
            QMessageBox.critical(self, "Error", f"File not found:\n{filepath}")
            return False
        
        # Check if it's a file (not a directory)
        if not os.path.isfile(filepath):
            QMessageBox.critical(self, "Error", f"Path is not a file:\n{filepath}")
            return False
        
        # Check if we need to save current file
        if not self.maybe_save():
            return False
        
        try:
            # Get file size to determine loading strategy
            file_size = os.path.getsize(filepath)
            file_size_mb = file_size / (1024 * 1024)  # Size in MB
            is_large_file = file_size > 500 * 1024  # 500 KB (approximately 500k characters)
            
            # Show loading message for large files
            if is_large_file:
                self.status_bar.showMessage(f"Loading large file ({file_size_mb:.2f} MB)... Please wait")
                QApplication.processEvents()  # Allow UI to update
            
            # Read file content - use QTextStream for better performance with large files
            qt_file = QFile(filepath)
            if not qt_file.open(QFile.ReadOnly | QFile.Text):
                raise IOError(f"Could not open file: {filepath}")
            
            stream = QTextStream(qt_file)
            stream.setCodec('UTF-8')
            content = stream.readAll()
            qt_file.close()
            
            # Allow UI to update after reading
            QApplication.processEvents()
            
            self.current_file = filepath
            self.setWindowTitle(f"SmartPad - {Path(filepath).name}")
            
            # For very large files, disable syntax highlighting to prevent freezing
            # Threshold: 500k characters (approximately)
            char_count = len(content)
            should_highlight = char_count < 500000  # Disable highlighting for files > 500k chars
            
            if is_large_file:
                self.status_bar.showMessage(f"Setting content ({char_count:,} characters)...")
                QApplication.processEvents()
            
            # Set content
            self.text_edit.setPlainText(content)
            self.text_edit.document().setModified(False)  # Mark as unmodified
            
            # Allow UI to update after setting text
            QApplication.processEvents()
            
            # Detect language from extension first, then from content (only sample for large files)
            language = detect_language(filepath)
            
            # Only apply syntax highlighting for smaller files to prevent freezing
            if should_highlight:
                # If generic, try to detect from content (use sample for large files)
                if language == 'generic':
                    # For large files, only check first 10000 characters for detection
                    sample = content[:10000] if len(content) > 10000 else content
                    detected = detect_file_type_from_content(sample)
                    if detected:
                        language = detected
                
                self.update_syntax_highlighting(language)
                self.status_bar.showMessage(f"Opened: {filepath} ({language.upper()}, {char_count:,} chars)")
            else:
                # Disable syntax highlighting for very large files
                if self.highlighter:
                    self.highlighter.setDocument(None)
                    self.highlighter = None
                
                # Still detect language for display, but don't highlight
                if language == 'generic':
                    sample = content[:10000] if len(content) > 10000 else content
                    detected = detect_file_type_from_content(sample)
                    if detected:
                        language = detected
                
                self.status_bar.showMessage(
                    f"Opened: {filepath} ({language.upper()}, {char_count:,} chars) - "
                    f"Syntax highlighting disabled for large file"
                )
            
            return True
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{str(e)}")
            return False
    
    def save_file(self):
        """Save current file - overwrites existing file if it exists"""
        if self.current_file:
            # File already exists, save directly (overwrite)
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.text_edit.document().setModified(False)
                self.status_bar.showMessage(f"Saved: {self.current_file}")
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
                return False
        else:
            # No file yet, use Save As dialog
            return self.save_as_file()
    
    def save_as_file(self):
        """Save file with new name - shows dialog to choose location"""
        # Suggest current filename if exists
        suggested_name = ""
        if self.current_file:
            suggested_name = str(self.current_file)
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File As", suggested_name, "All Files (*.*)"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.current_file = filename
                self.text_edit.document().setModified(False)
                self.setWindowTitle(f"SmartPad - {Path(filename).name}")
                
                # Update syntax highlighting
                language = detect_language(filename)
                self.update_syntax_highlighting(language)
                
                self.status_bar.showMessage(f"Saved: {filename}")
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
                return False
        return False
    
    def maybe_save(self):
        """Check if file needs saving before closing"""
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "The document has been modified.\nDo you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                return self.save_file()
            elif reply == QMessageBox.Cancel:
                return False
        return True
    
    def auto_format(self):
        """Auto-detect file type and format accordingly"""
        content = self.text_edit.toPlainText()
        if not content.strip():
            QMessageBox.warning(self, "Warning", "No content to format")
            return
        
        # Try to detect from file extension first
        language = None
        if self.current_file:
            language = detect_language(self.current_file)
        
        # Try to detect from content if no file
        if not language:
            detected = detect_file_type_from_content(content)
            if detected:
                language = detected
        
        # Format based on language
        formatted = None
        error = None
        
        if language == 'xml' or language == 'html':
            formatted, error = Formatters.format_xml(content)
        elif language == 'json':
            formatted, error = Formatters.format_json(content)
        elif language == 'python':
            formatted, error = Formatters.format_python(content)
        elif language == 'css':
            formatted, error = Formatters.format_css(content)
        elif language == 'javascript':
            formatted, error = Formatters.format_javascript(content)
        else:
            # Try XML first (most common), then JSON
            if '<' in content and '>' in content:
                formatted, error = Formatters.format_xml(content)
                if formatted:
                    self.text_edit.setPlainText(formatted)
                    self.status_bar.showMessage("XML formatted successfully")
                    return
            
            # Try JSON
            if '{' in content or '[' in content:
                formatted, error = Formatters.format_json(content)
                if formatted:
                    self.text_edit.setPlainText(formatted)
                    self.status_bar.showMessage("JSON formatted successfully")
                    return
            
            QMessageBox.information(
                self, "Info",
                "Could not auto-detect file format.\n\n"
                "Supported formats:\n"
                "- XML/HTML (starts with <?xml or <tag)\n"
                "- JSON (starts with { or [)\n"
                "- Python (.py files)\n"
                "- CSS (.css files)\n"
                "- JavaScript (.js files)\n\n"
                "Please ensure your file has the correct format or extension."
            )
            return
        
        # Apply formatting
        if formatted:
            self.text_edit.setPlainText(formatted)
            self.status_bar.showMessage(f"{language.upper()} formatted successfully")
        elif error:
            QMessageBox.critical(
                self, "Error", 
                f"Could not format {language.upper()}:\n{error}\n\n"
                "Make sure the content is valid."
            )
    
    def on_text_changed(self):
        """Handle text change events"""
        self.text_edit.document().setModified(True)
        # Update status bar with line/column info
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        total_lines = self.text_edit.blockCount()
        total_chars = len(self.text_edit.toPlainText())
        self.status_bar.showMessage(
            f"Line {line}/{total_lines}, Column {col} | Characters: {total_chars}"
        )
    
    def show_find_dialog(self):
        """Show/hide find bar"""
        if self.find_bar.isVisible():
            self.find_bar.hide()
            # Return focus to text editor
            self.text_edit.setFocus()
        else:
            # Show first to get proper size
            self.find_bar.show()
            # Position at top right after showing
            self.position_find_bar()
            # Activate
            self.find_bar.raise_()
            self.find_bar.activateWindow()
            # Clear text
            self.find_bar.find_edit.clear()
            # Set focus immediately and ensure it works
            self.find_bar.find_edit.setFocus()
            # Use QTimer as backup to ensure focus is set
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(50, lambda: (
                self.find_bar.find_edit.setFocus(),
                self.find_bar.find_edit.setCursorPosition(0)
            ))
    
    def position_find_bar(self):
        """Position find bar at top right of window"""
        if self.find_bar.isVisible():
            # Get window geometry
            window_rect = self.geometry()
            find_bar_width = self.find_bar.width()
            find_bar_height = self.find_bar.height()
            
            # Calculate position (top right, with some margin)
            # Get global position of window top-left corner
            window_top_left = self.mapToGlobal(QPoint(0, 0))
            # Calculate x position (right side with margin)
            x = window_top_left.x() + window_rect.width() - find_bar_width - 20
            # Calculate y position (below menu bar and toolbar, about 60px from top)
            y = window_top_left.y() + 60
            
            self.find_bar.move(x, y)
    
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        if self.find_bar.isVisible():
            self.position_find_bar()
    
    def find_next(self):
        """Find next occurrence"""
        if self.find_bar.isVisible():
            self.find_bar.find_next()
        else:
            self.show_find_dialog()
    
    def show_help(self):
        """Show help documentation"""
        help_dialog = HelpDialog(self)
        help_dialog.show()
        # Update title bar theme after showing
        from .themes import ThemeManager
        ThemeManager.update_title_bar_theme(help_dialog, 'dark')
        help_dialog.exec_()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()


class FindBar(QFrame):
    """Find bar widget embedded in main window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_editor = parent
        # Set as tool window so it stays on top of parent
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedHeight(40)
        self.setMinimumWidth(350)
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize find bar UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        
        # Find label and input
        self.find_label = QLabel("Find:")
        self.find_label.setFixedWidth(60)
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("Enter text to find and press Enter...")
        self.find_edit.setMinimumWidth(300)
        self.find_edit.setFocusPolicy(Qt.StrongFocus)
        self.find_edit.returnPressed.connect(self.find_next)
        self.find_edit.textChanged.connect(self.on_text_changed)
        
        # Add widgets to layout
        layout.addWidget(self.find_label)
        layout.addWidget(self.find_edit)
        
        # Store search state
        self.current_match_index = 0
        self.total_matches = 0
        self.search_text = ""
        self.match_positions = []
    
    def apply_theme(self):
        """Apply theme to find bar"""
        if hasattr(self.parent_editor, 'current_theme'):
            theme = self.parent_editor.current_theme
            if theme == 'dark':
                self.setStyleSheet("""
                    QFrame {
                        background-color: #2d2d30;
                        border: 1px solid #3e3e42;
                        border-radius: 4px;
                    }
                    QLabel {
                        color: #cccccc;
                    }
                    QLineEdit {
                        background-color: #3c3c3c;
                        color: #cccccc;
                        border: 1px solid #3e3e42;
                        padding: 4px;
                        border-radius: 2px;
                    }
                    QLineEdit:focus {
                        border: 1px solid #0e639c;
                    }
                """)
            else:
                self.setStyleSheet("""
                    QFrame {
                        background-color: #f3f3f3;
                        border: 1px solid #d0d0d0;
                        border-radius: 4px;
                    }
                    QLabel {
                        color: #333333;
                    }
                    QLineEdit {
                        background-color: #ffffff;
                        color: #333333;
                        border: 1px solid #d0d0d0;
                        padding: 4px;
                        border-radius: 2px;
                    }
                    QLineEdit:focus {
                        border: 1px solid #0078d4;
                    }
                """)
    
    def hide_find_bar(self):
        """Hide find bar and return focus to editor"""
        self.hide()
        if self.parent_editor:
            self.parent_editor.text_edit.setFocus()
    
    def on_text_changed(self):
        """Handle text change in find box"""
        # Reset search state when text changes
        new_search_text = self.find_edit.text()
        
        # Only reset if text actually changed
        if new_search_text != self.search_text:
            self.current_match_index = 0
            self.total_matches = 0
            self.match_positions = []
            self.search_text = new_search_text
            
            # Count total matches
            if self.search_text:
                self.count_matches()
            else:
                self.find_label.setText("Find:")
    
    def count_matches(self):
        """Count total matches in document"""
        try:
            text_edit = self.parent_editor.text_edit
            if not text_edit:
                return
            
            content = text_edit.toPlainText()
            if not content or not self.search_text:
                self.total_matches = 0
                self.match_positions = []
                self.find_label.setText("Find:")
                return
            
            # Count all matches (case-insensitive by default)
            import re
            pattern = re.escape(self.search_text)
            
            self.match_positions = []
            for match in re.finditer(pattern, content, re.IGNORECASE):
                self.match_positions.append(match.start())
            
            self.total_matches = len(self.match_positions)
            
            # Update label
            if self.total_matches > 0:
                self.current_match_index = 1
                self.find_label.setText(f"{self.current_match_index}/{self.total_matches}")
            else:
                self.find_label.setText("Find: (0)")
        except Exception:
            self.find_label.setText("Find:")
    
    def showEvent(self, event):
        """Handle show event - set focus when shown"""
        super().showEvent(event)
        # Set focus to input field when shown - use QTimer to ensure it works
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(0, lambda: (
            self.find_edit.setFocus(),
            self.find_edit.setCursorPosition(0)
        ))
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            self.hide_find_bar()
        else:
            super().keyPressEvent(event)
    
    def find_next(self):
        """Find next occurrence"""
        try:
            search_text = self.find_edit.text()
            if not search_text:
                self.find_label.setText("Find:")
                return
            
            # Update search text if changed - this will trigger count_matches via on_text_changed
            if search_text != self.search_text:
                # Reset to first match when search text changes
                self.current_match_index = 0
            
            # Ensure matches are counted
            if not self.match_positions and search_text:
                self.search_text = search_text
                self.count_matches()
            
            if self.total_matches == 0:
                self.find_label.setText("Find: (0)")
                self.parent_editor.status_bar.showMessage("Text not found")
                return
            
            text_edit = self.parent_editor.text_edit
            if not text_edit:
                return
            
            cursor = text_edit.textCursor()
            if not cursor:
                return
            
            # Get current position - use selection start if exists, otherwise cursor position
            if cursor.hasSelection():
                current_pos = cursor.selectionStart()
            else:
                current_pos = cursor.position()
            
            # Find next match position - always move to next
            next_index = None
            for i, pos in enumerate(self.match_positions):
                if pos > current_pos:
                    next_index = i
                    break
            
            # If no match found after current position, wrap to first
            if next_index is None:
                next_index = 0
                self.current_match_index = 1
            else:
                self.current_match_index = next_index + 1
            
            # Move cursor to match position
            match_pos = self.match_positions[next_index]
            cursor.setPosition(match_pos)
            cursor.setPosition(match_pos + len(search_text), QTextCursor.KeepAnchor)
            text_edit.setTextCursor(cursor)
            text_edit.ensureCursorVisible()
            
            # Update label
            self.find_label.setText(f"{self.current_match_index}/{self.total_matches}")
            self.parent_editor.status_bar.showMessage(f"Found {self.current_match_index} of {self.total_matches}")
            
        except Exception as e:
            self.parent_editor.status_bar.showMessage(f"Search error: {str(e)}")
            self.find_label.setText("Find:")


class HelpDialog(QDialog):
    """Help Documentation Dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_editor = parent
        self.setWindowTitle("About - SmartPad")
        
        # Set window icon
        icon_path = Path(__file__).parent / "logo.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Calculate DPI-aware sizes
        try:
            dpi_ratio = self.devicePixelRatioF() if hasattr(self, 'devicePixelRatioF') else 1.0
        except:
            dpi_ratio = 1.0
        
        # Scale minimum size with DPI - optimized for no scrolling
        base_width = 450
        base_height = 380
        self.setMinimumSize(int(base_width * dpi_ratio), int(base_height * dpi_ratio))
        
        # Set initial size proportional to parent window if available
        if parent:
            parent_size = parent.size()
            # Use 50% of parent width and 55% of parent height, but with limits
            initial_width = min(int(parent_size.width() * 0.5), int(480 * dpi_ratio))
            initial_height = min(int(parent_size.height() * 0.55), int(400 * dpi_ratio))
            self.resize(initial_width, initial_height)
        
        self.init_ui()
        self.apply_theme()
        
        # Update title bar theme to dark
        from .themes import ThemeManager
        ThemeManager.update_title_bar_theme(self, 'dark')
    
    def get_scaled_size(self, base_size):
        """Get DPI-scaled size"""
        try:
            dpi_ratio = self.devicePixelRatioF() if hasattr(self, 'devicePixelRatioF') else 1.0
        except:
            dpi_ratio = 1.0
        return int(base_size * max(1.0, dpi_ratio))
    
    def init_ui(self):
        """Initialize help dialog UI"""
        # Calculate scaled spacing and margins - optimized layout
        spacing = self.get_scaled_size(10)
        margin = self.get_scaled_size(15)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(spacing)
        layout.setContentsMargins(margin, margin, margin, margin)
        
        # Content area - no scroll, fixed height
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(self.get_scaled_size(10))
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # About section - Beautiful design
        about_label = QLabel("About")
        about_font = QFont()
        about_font.setPointSize(self.get_scaled_size(10))
        about_font.setBold(True)
        about_label.setFont(about_font)
        content_layout.addWidget(about_label)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setMaximumHeight(self.get_scaled_size(180))
        # Set font size for content
        content_font = QFont()
        content_font.setPointSize(self.get_scaled_size(8))
        about_text.setFont(content_font)
        about_content = """
<div style="font-size: 8pt; line-height: 1.7;">
<div style="text-align: center; margin-bottom: 8px;">
<strong style="font-size: 11pt; color: #4fc3f7;">SmartPad v1.0.0
</strong>
</div>
<div style="text-align: center; margin-bottom: 12px; color: #a0a0a0;">
A smart text editor inspired by Notepad
</div>

<div style="background-color: rgba(79, 195, 247, 0.1); padding: 8px; border-radius: 4px; margin: 8px 0;">
<strong style="font-size: 9pt; color: #4fc3f7;">✨ Key Features</strong>
</div>
<div style="padding-left: 8px;">
• <b>Universal File Support</b> - Open and edit any file type<br>
• <b>Smart Syntax Highlighting</b> - Beautiful colors for XML, JSON, Python, CSS, JavaScript<br>
• <b>Auto-Formatting</b> - Professional code formatting with one click<br>
• <b>Dark/Light Themes</b> - Beautiful UI with theme switching<br>
• <b>Advanced Search</b> - Find and replace with match counter<br>
• <b>Line Numbers</b> - Professional code editor features<br>
• <b>DPI Scaling</b> - Perfect on all screen sizes (100%, 125%, 150%)<br>
</div>

<div style="margin-top: 8px; padding: 6px; background-color: rgba(79, 195, 247, 0.05); border-radius: 4px;">
<strong style="font-size: 9pt;">🔧 Technologies:</strong> Python 3 • PyQt5 • Modern UI/UX
</div>
</div>
"""
        about_text.setHtml(about_content)
        content_layout.addWidget(about_text)
        
        content_layout.addSpacing(self.get_scaled_size(6))
        
        # Developer section - Compact design
        dev_label = QLabel("👨‍💻 Developer")
        dev_font = QFont()
        dev_font.setPointSize(self.get_scaled_size(8))
        dev_font.setBold(True)
        dev_label.setFont(dev_font)
        content_layout.addWidget(dev_label)
        
        dev_text = QTextBrowser()
        dev_text.setReadOnly(True)
        dev_text.setOpenExternalLinks(True)
        dev_text.setMaximumHeight(self.get_scaled_size(85))
        # Set smaller font size for developer section
        dev_font_small = QFont()
        dev_font_small.setPointSize(self.get_scaled_size(7))
        dev_text.setFont(dev_font_small)
        dev_content = """
<div style="font-size: 7pt; line-height: 1.5;">
<strong>Developer:</strong> Mr. Patchara Al-umaree<br>
<strong>📧 Email:</strong> <a href="mailto:Patcharaalumaree@gmail.com" style="color: #4fc3f7; text-decoration: none;">Patcharaalumaree@gmail.com</a><br>
<strong>🔗 GitHub:</strong> <a href="https://github.com/MrPatchara" style="color: #4fc3f7; text-decoration: none;">https://github.com/MrPatchara</a><br>
<strong>📍 Location:</strong> Bangkok, Thailand • <strong>🎓 Education:</strong> Computer Engineering Student
</div>
"""
        dev_text.setHtml(dev_content)
        content_layout.addWidget(dev_text)
        
        # Add content widget directly to layout (no scroll)
        layout.addWidget(content_widget)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setMinimumWidth(self.get_scaled_size(70))
        close_btn.setMinimumHeight(self.get_scaled_size(22))
        close_btn_font = QFont()
        close_btn_font.setPointSize(self.get_scaled_size(7))
        close_btn.setFont(close_btn_font)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
    
    def apply_theme(self):
        """Apply theme to help dialog - matches main window theme with DPI scaling"""
        if hasattr(self.parent_editor, 'current_theme'):
            theme = self.parent_editor.current_theme
            padding = self.get_scaled_size(10)
            border_radius = self.get_scaled_size(4)
            
            if theme == 'dark':
                self.setStyleSheet(f"""
                    QDialog {{
                        background-color: #1e1e1e;
                        color: #d4d4d4;
                    }}
                    QLabel {{
                        color: #d4d4d4;
                    }}
                    QTextEdit {{
                        background-color: #252526;
                        color: #d4d4d4;
                        border: 1px solid #3e3e42;
                        border-radius: {border_radius}px;
                        padding: {padding}px;
                        font-size: 8pt;
                    }}
                    QTextBrowser {{
                        background-color: #252526;
                        color: #d4d4d4;
                        border: 1px solid #3e3e42;
                        border-radius: {border_radius}px;
                        padding: {padding}px;
                        font-size: 8pt;
                    }}
                    QTextBrowser a {{
                        color: #4fc3f7;
                        text-decoration: none;
                    }}
                    QTextBrowser a:hover {{
                        color: #81d4fa;
                        text-decoration: underline;
                    }}
                    QScrollArea {{
                        border: 1px solid #3e3e42;
                        border-radius: {border_radius}px;
                        background-color: #1e1e1e;
                    }}
                    QScrollBar:vertical {{
                        background-color: #252526;
                        width: {self.get_scaled_size(10)}px;
                        border: none;
                    }}
                    QScrollBar::handle:vertical {{
                        background-color: #424242;
                        border-radius: {self.get_scaled_size(5)}px;
                        min-height: {self.get_scaled_size(25)}px;
                    }}
                    QScrollBar::handle:vertical:hover {{
                        background-color: #4e4e4e;
                    }}
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                        height: 0px;
                    }}
                    QPushButton {{
                        background-color: #0e639c;
                        color: #ffffff;
                        padding: {self.get_scaled_size(6)}px {self.get_scaled_size(20)}px;
                        border: none;
                        border-radius: {border_radius}px;
                        font-weight: bold;
                        font-size: 7pt;
                    }}
                    QPushButton:hover {{
                        background-color: #1177bb;
                    }}
                    QPushButton:pressed {{
                        background-color: #0a4d75;
                    }}
                """)
            else:
                self.setStyleSheet(f"""
                    QDialog {{
                        background-color: #ffffff;
                        color: #333333;
                    }}
                    QLabel {{
                        color: #333333;
                    }}
                    QTextEdit {{
                        background-color: #f8f8f8;
                        color: #333333;
                        border: 1px solid #d0d0d0;
                        border-radius: {border_radius}px;
                        padding: {padding}px;
                        font-size: 8pt;
                    }}
                    QTextBrowser {{
                        background-color: #f8f8f8;
                        color: #333333;
                        border: 1px solid #d0d0d0;
                        border-radius: {border_radius}px;
                        padding: {padding}px;
                        font-size: 8pt;
                    }}
                    QTextBrowser a {{
                        color: #0078d4;
                        text-decoration: none;
                    }}
                    QTextBrowser a:hover {{
                        color: #005a9e;
                        text-decoration: underline;
                    }}
                    QScrollArea {{
                        border: 1px solid #d0d0d0;
                        border-radius: {border_radius}px;
                        background-color: #ffffff;
                    }}
                    QScrollBar:vertical {{
                        background-color: #f0f0f0;
                        width: {self.get_scaled_size(10)}px;
                        border: none;
                    }}
                    QScrollBar::handle:vertical {{
                        background-color: #c0c0c0;
                        border-radius: {self.get_scaled_size(5)}px;
                        min-height: {self.get_scaled_size(25)}px;
                    }}
                    QScrollBar::handle:vertical:hover {{
                        background-color: #a0a0a0;
                    }}
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                        height: 0px;
                    }}
                    QPushButton {{
                        background-color: #0078d4;
                        color: #ffffff;
                        padding: {self.get_scaled_size(6)}px {self.get_scaled_size(20)}px;
                        border: none;
                        border-radius: {border_radius}px;
                        font-weight: bold;
                        font-size: 7pt;
                    }}
                    QPushButton:hover {{
                        background-color: #005a9e;
                    }}
                    QPushButton:pressed {{
                        background-color: #004578;
                    }}
                """)

