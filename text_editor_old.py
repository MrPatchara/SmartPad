#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Editor Plus - Advanced Text Editor with Syntax Highlighting and Auto-Formatting
"""

import sys
import os
import json
import xml.dom.minidom
import re
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QMenuBar, 
                             QMenu, QFileDialog, QMessageBox, QStatusBar, 
                             QToolBar, QAction, QVBoxLayout, QWidget, QLabel,
                             QPlainTextEdit, QScrollArea, QSpinBox, QCheckBox,
                             QDialog, QDialogButtonBox, QFormLayout, QComboBox)
from PyQt5.QtCore import Qt, QRegExp, QSize, QRect, QRectF
from PyQt5.QtGui import (QTextCharFormat, QFont, QColor, QSyntaxHighlighter, 
                        QKeySequence, QIcon, QTextCursor, QTextDocument,
                        QPainter, QTextBlock, QPalette)

class SyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for multiple languages"""
    
    def __init__(self, parent=None, language='xml', theme='dark'):
        super().__init__(parent)
        self.language = language
        self.theme = theme
        self.highlighting_rules = []
        self.setup_highlighting()
    
    def setup_highlighting(self):
        """Setup highlighting rules based on language"""
        if self.language == 'xml':
            self.setup_xml_highlighting()
        elif self.language == 'json':
            self.setup_json_highlighting()
        elif self.language == 'python':
            self.setup_python_highlighting()
        elif self.language == 'html':
            self.setup_html_highlighting()
        elif self.language == 'css':
            self.setup_css_highlighting()
        elif self.language == 'javascript':
            self.setup_javascript_highlighting()
        else:
            self.setup_generic_highlighting()
    
    def set_theme(self, theme):
        """Update theme and reapply highlighting"""
        self.theme = theme
        self.highlighting_rules = []
        self.setup_highlighting()
        self.rehighlight()
    
    def setup_xml_highlighting(self):
        """XML syntax highlighting"""
        if self.theme == 'light':
            # Light theme colors
            tag_color = "#0000FF"  # Blue
            attr_color = "#0070C1"  # Dark Blue
            attr_value_color = "#A31515"  # Dark Red
            comment_color = "#008000"  # Green
            cdata_color = "#795E26"  # Brown
        else:
            # Dark theme colors (VS Code style)
            tag_color = "#569CD6"  # Blue
            attr_color = "#92C5F7"  # Light Blue
            attr_value_color = "#CE9178"  # Orange
            comment_color = "#6A9955"  # Green
            cdata_color = "#DCDCAA"  # Yellow
        
        # XML Tags
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor(tag_color))
        tag_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'<[^>]+>'), tag_format))
        
        # XML Attributes
        attr_format = QTextCharFormat()
        attr_format.setForeground(QColor(attr_color))
        self.highlighting_rules.append((QRegExp(r'\s+\w+\s*='), attr_format))
        
        # Attribute Values
        attr_value_format = QTextCharFormat()
        attr_value_format.setForeground(QColor(attr_value_color))
        self.highlighting_rules.append((QRegExp(r'="[^"]*"'), attr_value_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'<!--.*-->'), comment_format))
        
        # CDATA
        cdata_format = QTextCharFormat()
        cdata_format.setForeground(QColor(cdata_color))
        self.highlighting_rules.append((QRegExp(r'<!\[CDATA\[.*\]\]>'), cdata_format))
    
    def setup_json_highlighting(self):
        """JSON syntax highlighting"""
        if self.theme == 'light':
            key_color = "#0000FF"  # Blue
            string_color = "#A31515"  # Dark Red
            number_color = "#098658"  # Green
            keyword_color = "#0000FF"  # Blue
        else:
            key_color = "#9CDCFE"  # Light Blue
            string_color = "#CE9178"  # Orange
            number_color = "#B5CEA8"  # Light Green
            keyword_color = "#569CD6"  # Blue
        
        # Keys
        key_format = QTextCharFormat()
        key_format.setForeground(QColor(key_color))
        self.highlighting_rules.append((QRegExp(r'"([^"]+)":'), key_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string_color))
        self.highlighting_rules.append((QRegExp(r'"[^"]*"'), string_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(number_color))
        self.highlighting_rules.append((QRegExp(r'\b\d+\.?\d*\b'), number_format))
        
        # Keywords (true, false, null)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(keyword_color))
        keyword_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\b(true|false|null)\b'), keyword_format))
    
    def setup_python_highlighting(self):
        """Python syntax highlighting"""
        if self.theme == 'light':
            keyword_color = "#0000FF"  # Blue
            string_color = "#A31515"  # Dark Red
            comment_color = "#008000"  # Green
            number_color = "#098658"  # Green
        else:
            keyword_color = "#569CD6"  # Blue
            string_color = "#CE9178"  # Orange
            comment_color = "#6A9955"  # Green
            number_color = "#B5CEA8"  # Light Green
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(keyword_color))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ['def', 'class', 'import', 'from', 'if', 'else', 'elif', 
                   'for', 'while', 'try', 'except', 'finally', 'return', 
                   'yield', 'with', 'as', 'pass', 'break', 'continue', 
                   'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False']
        for keyword in keywords:
            self.highlighting_rules.append((QRegExp(r'\b' + keyword + r'\b'), keyword_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string_color))
        self.highlighting_rules.append((QRegExp(r'"[^"]*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'[^']*'"), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(number_color))
        self.highlighting_rules.append((QRegExp(r'\b\d+\.?\d*\b'), number_format))
    
    def setup_html_highlighting(self):
        """HTML syntax highlighting (similar to XML)"""
        self.setup_xml_highlighting()
    
    def setup_css_highlighting(self):
        """CSS syntax highlighting"""
        # Selectors
        selector_format = QTextCharFormat()
        selector_format.setForeground(QColor("#D7BA7D"))  # Yellow
        self.highlighting_rules.append((QRegExp(r'[^{]+\{'), selector_format))
        
        # Properties
        property_format = QTextCharFormat()
        property_format.setForeground(QColor("#9CDCFE"))  # Light Blue
        self.highlighting_rules.append((QRegExp(r'\s+\w+:'), property_format))
        
        # Values
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#CE9178"))  # Orange
        self.highlighting_rules.append((QRegExp(r':\s*[^;]+;'), value_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Green
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'/\*.*\*/'), comment_format))
    
    def setup_javascript_highlighting(self):
        """JavaScript syntax highlighting"""
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))  # Blue
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ['function', 'var', 'let', 'const', 'if', 'else', 'for', 
                   'while', 'return', 'true', 'false', 'null', 'undefined', 
                   'this', 'new', 'class', 'extends', 'import', 'export']
        for keyword in keywords:
            self.highlighting_rules.append((QRegExp(r'\b' + keyword + r'\b'), keyword_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Orange
        self.highlighting_rules.append((QRegExp(r'"[^"]*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'[^']*'"), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Green
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'//.*'), comment_format))
        self.highlighting_rules.append((QRegExp(r'/\*.*\*/'), comment_format))
    
    def setup_generic_highlighting(self):
        """Generic highlighting for unknown file types"""
        if self.theme == 'light':
            string_color = "#A31515"  # Dark Red
            comment_color = "#008000"  # Green
        else:
            string_color = "#CE9178"  # Orange
            comment_color = "#6A9955"  # Green
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string_color))
        self.highlighting_rules.append((QRegExp(r'"[^"]*"'), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))
    
    def highlightBlock(self, text):
        """Apply highlighting to a block of text"""
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class LineNumberArea(QWidget):
    """Line number area widget"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """Enhanced code editor with line numbers"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)
        self.setFont(QFont("Consolas", 11))
        self.setTabStopWidth(40)
        self.current_theme = 'dark'  # Default theme
    
    def set_theme(self, theme):
        """Set theme for line number area"""
        self.current_theme = theme
        self.line_number_area.update()
    
    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        space = 10 + self.fontMetrics().width('9') * digits
        return space
    
    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                        self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )
    
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        # Use theme from CodeEditor
        if self.current_theme == 'light':
            painter.fillRect(event.rect(), QColor("#f8f8f8"))
            text_color = QColor("#858585")
        else:
            painter.fillRect(event.rect(), QColor("#252526"))
            text_color = QColor("#858585")
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(text_color)
                rect = QRect(
                    0, int(top), 
                    self.line_number_area.width(), 
                    self.fontMetrics().height()
                )
                painter.drawText(rect, Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1


class TextEditor(QMainWindow):
    """Main text editor window"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.highlighter = None
        self.current_theme = 'dark'  # Default theme
        self.init_ui()
        self.apply_dark_theme()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Text Editor Plus")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create text editor with line numbers
        self.text_edit = CodeEditor()
        layout.addWidget(self.text_edit)
        
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
    
    def create_toolbar(self):
        """Create toolbar with common actions"""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
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
    
    def apply_dark_theme(self):
        """Apply beautiful dark theme"""
        # Set window background for title bar area (Windows)
        self.setStyleSheet("")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1e1e1e"))
        palette.setColor(QPalette.WindowText, QColor("#d4d4d4"))
        self.setPalette(palette)
        
        dark_style = """
        QMainWindow {
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        QWidget {
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        QPlainTextEdit {
            background-color: #1e1e1e;
            color: #d4d4d4;
            border: none;
            selection-background-color: #264f78;
            selection-color: #ffffff;
        }
        QMenuBar {
            background-color: #2d2d30;
            color: #cccccc;
            border-bottom: 1px solid #3e3e42;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        QMenuBar::item:selected {
            background-color: #3e3e42;
        }
        QMenu {
            background-color: #252526;
            color: #cccccc;
            border: 1px solid #3e3e42;
            padding: 4px;
        }
        QMenu::item {
            padding: 4px 20px 4px 20px;
        }
        QMenu::item:selected {
            background-color: #094771;
        }
        QMenu::separator {
            height: 1px;
            background: #3e3e42;
            margin: 4px 0px;
        }
        QToolBar {
            background-color: #2d2d30;
            border: none;
            spacing: 3px;
            padding: 4px;
        }
        QToolBar::separator {
            background-color: #3e3e42;
            width: 1px;
            margin: 4px;
        }
        QStatusBar {
            background-color: #007acc;
            color: #ffffff;
            border-top: 1px solid #005a9e;
        }
        QAction {
            color: #cccccc;
            padding: 4px;
        }
        QAction:hover {
            background-color: #3e3e42;
        }
        QAction:checked {
            background-color: #094771;
        }
        """
        self.setStyleSheet(dark_style)
        self.current_theme = 'dark'
        # Update theme action check states
        if hasattr(self, 'theme_actions'):
            self.theme_actions[0].setChecked(True)
            self.theme_actions[1].setChecked(False)
        
    
    def apply_light_theme(self):
        """Apply beautiful light theme"""
        # Set window background for title bar area (Windows)
        self.setStyleSheet("")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#ffffff"))
        palette.setColor(QPalette.WindowText, QColor("#333333"))
        self.setPalette(palette)
        
        light_style = """
        QMainWindow {
            background-color: #ffffff;
            color: #333333;
        }
        QWidget {
            background-color: #ffffff;
            color: #333333;
        }
        QPlainTextEdit {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #d0d0d0;
            selection-background-color: #add6ff;
            selection-color: #000000;
        }
        QMenuBar {
            background-color: #f0f0f0;
            color: #333333;
            border-bottom: 1px solid #d0d0d0;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }
        QMenu {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #d0d0d0;
            padding: 4px;
        }
        QMenu::item {
            padding: 4px 20px 4px 20px;
        }
        QMenu::item:selected {
            background-color: #add6ff;
        }
        QMenu::separator {
            height: 1px;
            background: #d0d0d0;
            margin: 4px 0px;
        }
        QToolBar {
            background-color: #f0f0f0;
            border: none;
            spacing: 3px;
            padding: 4px;
        }
        QToolBar::separator {
            background-color: #d0d0d0;
            width: 1px;
            margin: 4px;
        }
        QStatusBar {
            background-color: #0078d4;
            color: #ffffff;
            border-top: 1px solid #005a9e;
        }
        QAction {
            color: #333333;
            padding: 4px;
        }
        QAction:hover {
            background-color: #e0e0e0;
        }
        QAction:checked {
            background-color: #add6ff;
        }
        """
        self.setStyleSheet(light_style)
        self.current_theme = 'light'
        # Update theme action check states
        if hasattr(self, 'theme_actions'):
            self.theme_actions[0].setChecked(False)
            self.theme_actions[1].setChecked(True)
        # Update line number area color for light theme
        # This will be handled in the CodeEditor paint event
        
    
    def update_title_bar_theme(self):
        """Update title bar theme using Windows API"""
        try:
            if sys.platform == 'win32':
                import ctypes
                from ctypes import wintypes
                # Enable/disable dark mode for title bar (Windows 10/11)
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                hwnd = int(self.winId())
                dark_mode = 1 if self.current_theme == 'dark' else 0
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    wintypes.HWND(hwnd),
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(ctypes.c_int(dark_mode)),
                    ctypes.sizeof(ctypes.c_int)
                )
        except Exception as e:
            pass  # Ignore if not Windows or API not available
    
    def change_theme(self, theme):
        """Change application theme"""
        if theme == 'dark':
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
        # Update code editor theme
        if hasattr(self, 'text_edit'):
            self.text_edit.set_theme(theme)
        # Update syntax highlighter colors if needed
        if self.highlighter:
            self.highlighter.set_theme(theme)
        # Update title bar
        self.update_title_bar_theme()
    
    
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
        layout = QFormLayout(dialog)
        
        spin_box = QSpinBox()
        spin_box.setRange(8, 72)
        spin_box.setValue(self.text_edit.font().pointSize())
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
    
    def detect_language(self, filename):
        """Detect programming language from file extension"""
        if not filename:
            return 'generic'
        
        ext = Path(filename).suffix.lower()
        language_map = {
            '.xml': 'xml',
            '.html': 'html',
            '.htm': 'html',
            '.json': 'json',
            '.py': 'python',
            '.css': 'css',
            '.js': 'javascript',
            '.jsx': 'javascript',
        }
        return language_map.get(ext, 'generic')
    
    def update_syntax_highlighting(self, language):
        """Update syntax highlighting based on language"""
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
            self.current_file = None
            self.setWindowTitle("Text Editor Plus - Untitled")
            if self.highlighter:
                self.highlighter.setDocument(None)
                self.highlighter = None
            self.status_bar.showMessage("New file created")
    
    def open_file(self):
        """Open a file with auto-formatting"""
        if self.maybe_save():
            filename, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", "All Files (*.*)"
            )
            if filename:
                try:
                    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    self.current_file = filename
                    self.setWindowTitle(f"Text Editor Plus - {Path(filename).name}")
                    
                    # Set content
                    self.text_edit.setPlainText(content)
                    self.status_bar.showMessage(f"Opened: {filename}")
                    
                    # Detect language and update syntax highlighting
                    language = self.detect_language(filename)
                    self.update_syntax_highlighting(language)
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not open file:\n{str(e)}")
    
    def save_file(self):
        """Save current file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.status_bar.showMessage(f"Saved: {self.current_file}")
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
                return False
        else:
            return self.save_as_file()
    
    def save_as_file(self):
        """Save file with new name"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "All Files (*.*)"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.current_file = filename
                self.setWindowTitle(f"Text Editor Plus - {Path(filename).name}")
                
                # Update syntax highlighting
                language = self.detect_language(filename)
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
        
        content_stripped = content.strip()
        
        # Try to detect format from content first
        is_xml = False
        is_json = False
        
        # Check for XML: starts with <?xml or <tag, contains XML tags
        if content_stripped.startswith('<?xml') or content_stripped.startswith('<'):
            # Verify it's XML by checking for XML tags
            if re.search(r'<[^>]+>', content):
                is_xml = True
        
        # Check for JSON: starts with { or [
        if not is_xml and (content_stripped.startswith('{') or content_stripped.startswith('[')):
            try:
                json.loads(content)  # Try to parse as JSON
                is_json = True
            except:
                pass
        
        # If we have a file, also check extension
        if self.current_file:
            language = self.detect_language(self.current_file)
            if language == 'xml' or language == 'html':
                is_xml = True
            elif language == 'json':
                is_json = True
            elif language == 'python':
                self.format_python()
                return
            elif language == 'css':
                self.format_css()
                return
            elif language == 'javascript':
                self.format_javascript()
                return
        
        # Format based on detection
        if is_xml:
            self.format_xml()
        elif is_json:
            self.format_json()
        else:
            # Try XML first (most common), then JSON
            # XML formatter will show error if not valid XML
            if '<' in content and '>' in content:
                # Looks like it might be XML, try formatting
                if self.format_xml(silent=True):
                    return
            
            # Try JSON
            if '{' in content or '[' in content:
                if self.format_json(silent=True):
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
    
    def format_xml(self, silent=False):
        """Format XML content with professional standard formatting"""
        try:
            content = self.text_edit.toPlainText()
            if not content.strip():
                if not silent:
                    QMessageBox.warning(self, "Warning", "No content to format")
                return False
            
            # Parse and format XML using minidom
            dom = xml.dom.minidom.parseString(content)
            # Use 2 spaces for indentation (standard)
            formatted = dom.toprettyxml(indent="  ")
            
            # Clean up and improve formatting
            lines = formatted.split('\n')
            cleaned_lines = []
            
            # Remove empty lines from minidom output and clean up
            for line in lines:
                stripped = line.rstrip()
                if stripped:  # Keep non-empty lines
                    cleaned_lines.append(stripped)
            
            # Professional formatting: organize with proper spacing
            result_lines = []
            prev_line = None
            prev_indent = -1
            
            for i, line in enumerate(cleaned_lines):
                # Skip XML declaration line (keep it as is)
                if line.startswith('<?xml'):
                    result_lines.append(line)
                    if i < len(cleaned_lines) - 1:
                        result_lines.append('')  # Add blank line after declaration
                    continue
                
                # Calculate current indent level
                indent = len(line) - len(line.lstrip())
                stripped = line.strip()
                
                # Detect line type
                is_closing = stripped.startswith('</')
                is_opening = stripped.startswith('<') and not is_closing and not stripped.startswith('<!--')
                is_comment = stripped.startswith('<!--')
                is_self_closing = stripped.endswith('/>')
                
                # Add blank line before major elements at root or same level
                if prev_line and not is_comment:
                    # Add blank line when:
                    # 1. Previous was closing tag and current is opening at same/higher level
                    # 2. Both are opening tags at same level (sibling elements)
                    if is_opening:
                        if prev_line.strip().startswith('</'):
                            # Previous was closing, add blank line before new element
                            if indent <= prev_indent:
                                result_lines.append('')
                        elif prev_line.strip().startswith('<') and not prev_line.strip().startswith('<!--'):
                            # Previous was opening tag, add blank line if at same level
                            if indent == prev_indent and indent > 0:
                                result_lines.append('')
                
                result_lines.append(line)
                prev_line = line
                prev_indent = indent
            
            formatted = '\n'.join(result_lines)
            
            # Preserve original XML declaration encoding
            if content.strip().startswith('<?xml'):
                original_decl = content.strip().split('\n')[0]
                if formatted.startswith('<?xml'):
                    # Replace declaration with original to preserve encoding
                    formatted_lines = formatted.split('\n')
                    formatted_lines[0] = original_decl
                    formatted = '\n'.join(formatted_lines)
            
            self.text_edit.setPlainText(formatted)
            if not silent:
                self.status_bar.showMessage("XML formatted successfully with standard indentation")
            return True
        except Exception as e:
            if not silent:
                QMessageBox.critical(self, "Error", f"Could not format XML:\n{str(e)}\n\nMake sure the XML is well-formed.")
            return False
    
    def format_json(self, silent=False):
        """Format JSON content"""
        try:
            content = self.text_edit.toPlainText()
            if not content.strip():
                if not silent:
                    QMessageBox.warning(self, "Warning", "No content to format")
                return False
            
            # Parse and format JSON
            data = json.loads(content)
            formatted = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False)
            
            self.text_edit.setPlainText(formatted)
            if not silent:
                self.status_bar.showMessage("JSON formatted successfully")
            return True
        except Exception as e:
            if not silent:
                QMessageBox.critical(self, "Error", f"Could not format JSON:\n{str(e)}")
            return False
    
    def format_python(self, silent=False):
        """Format Python content using basic formatting"""
        try:
            content = self.text_edit.toPlainText()
            if not content.strip():
                if not silent:
                    QMessageBox.warning(self, "Warning", "No content to format")
                return False
            
            # Basic Python formatting: fix indentation and spacing
            lines = content.split('\n')
            formatted_lines = []
            indent_level = 0
            indent_size = 4
            
            for line in lines:
                stripped = line.lstrip()
                if not stripped:
                    formatted_lines.append('')
                    continue
                
                # Decrease indent for certain keywords
                if stripped.startswith(('elif ', 'else:', 'except', 'finally:', 'except ')):
                    indent_level = max(0, indent_level - 1)
                
                # Add proper indentation
                formatted_line = ' ' * (indent_level * indent_size) + stripped
                formatted_lines.append(formatted_line)
                
                # Increase indent for certain patterns
                if stripped.endswith(':'):
                    indent_level += 1
                elif stripped.startswith(('return ', 'break', 'continue', 'pass', 'raise ')):
                    indent_level = max(0, indent_level - 1)
            
            formatted = '\n'.join(formatted_lines)
            self.text_edit.setPlainText(formatted)
            if not silent:
                self.status_bar.showMessage("Python formatted successfully")
            return True
        except Exception as e:
            if not silent:
                QMessageBox.critical(self, "Error", f"Could not format Python:\n{str(e)}")
            return False
    
    def format_css(self, silent=False):
        """Format CSS content"""
        try:
            content = self.text_edit.toPlainText()
            if not content.strip():
                if not silent:
                    QMessageBox.warning(self, "Warning", "No content to format")
                return False
            
            # Basic CSS formatting
            formatted = ""
            indent_level = 0
            in_rule = False
            
            for char in content:
                if char == '{':
                    formatted += ' {\n'
                    indent_level += 1
                    in_rule = True
                    formatted += ' ' * (indent_level * 2)
                elif char == '}':
                    indent_level = max(0, indent_level - 1)
                    formatted += '\n' + ' ' * (indent_level * 2) + '}'
                    in_rule = False
                elif char == ';':
                    formatted += ';\n'
                    if in_rule:
                        formatted += ' ' * (indent_level * 2)
                elif char == '\n':
                    # Skip extra newlines
                    if formatted and formatted[-1] != '\n':
                        formatted += ' '
                else:
                    formatted += char
            
            # Clean up extra spaces
            lines = formatted.split('\n')
            cleaned_lines = []
            for line in lines:
                cleaned = line.rstrip()
                if cleaned or (cleaned_lines and cleaned_lines[-1].strip()):
                    cleaned_lines.append(cleaned)
            
            formatted = '\n'.join(cleaned_lines)
            self.text_edit.setPlainText(formatted)
            if not silent:
                self.status_bar.showMessage("CSS formatted successfully")
            return True
        except Exception as e:
            if not silent:
                QMessageBox.critical(self, "Error", f"Could not format CSS:\n{str(e)}")
            return False
    
    def format_javascript(self, silent=False):
        """Format JavaScript content"""
        try:
            content = self.text_edit.toPlainText()
            if not content.strip():
                if not silent:
                    QMessageBox.warning(self, "Warning", "No content to format")
                return False
            
            # Basic JavaScript formatting (similar to Python)
            lines = content.split('\n')
            formatted_lines = []
            indent_level = 0
            indent_size = 2
            
            for line in lines:
                stripped = line.lstrip()
                if not stripped:
                    formatted_lines.append('')
                    continue
                
                # Decrease indent for closing braces/brackets
                if stripped.startswith(('}', ']')):
                    indent_level = max(0, indent_level - 1)
                
                # Add proper indentation
                formatted_line = ' ' * (indent_level * indent_size) + stripped
                formatted_lines.append(formatted_line)
                
                # Increase indent for opening braces
                if stripped.endswith(('{', '[')):
                    indent_level += 1
                elif stripped.endswith(';') and not stripped.startswith(('if', 'for', 'while', 'switch')):
                    # End of statement
                    pass
            
            formatted = '\n'.join(formatted_lines)
            self.text_edit.setPlainText(formatted)
            if not silent:
                self.status_bar.showMessage("JavaScript formatted successfully")
            return True
        except Exception as e:
            if not silent:
                QMessageBox.critical(self, "Error", f"Could not format JavaScript:\n{str(e)}")
            return False
    
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
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Text Editor Plus")
    
    editor = TextEditor()
    editor.show()
    
    # Apply title bar theme after window is shown
    editor.update_title_bar_theme()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

