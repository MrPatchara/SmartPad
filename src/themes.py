#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Themes Module
Provides theme management for the application
"""

import sys
from PyQt5.QtGui import QColor, QPalette


class ThemeManager:
    """Manages application themes"""
    
    @staticmethod
    def get_dark_theme_style():
        """Get dark theme stylesheet"""
        return """
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
        QToolBar QToolButton {
            padding: 3px 6px;
            font-size: 8.5pt;
            min-width: 45px;
            min-height: 26px;
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
    
    @staticmethod
    def get_light_theme_style():
        """Get light theme stylesheet"""
        return """
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
        QToolBar QToolButton {
            padding: 3px 6px;
            font-size: 8.5pt;
            min-width: 45px;
            min-height: 26px;
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
    
    @staticmethod
    def apply_theme(widget, theme):
        """Apply theme to widget"""
        if theme == 'dark':
            widget.setStyleSheet(ThemeManager.get_dark_theme_style())
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor("#1e1e1e"))
            palette.setColor(QPalette.WindowText, QColor("#d4d4d4"))
            widget.setPalette(palette)
        else:
            widget.setStyleSheet(ThemeManager.get_light_theme_style())
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor("#ffffff"))
            palette.setColor(QPalette.WindowText, QColor("#333333"))
            widget.setPalette(palette)
    
    @staticmethod
    def update_title_bar_theme(window, theme):
        """Update title bar theme using Windows API"""
        try:
            if sys.platform == 'win32':
                import ctypes
                from ctypes import wintypes
                # Enable/disable dark mode for title bar (Windows 10/11)
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                hwnd = int(window.winId())
                dark_mode = 1 if theme == 'dark' else 0
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    wintypes.HWND(hwnd),
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(ctypes.c_int(dark_mode)),
                    ctypes.sizeof(ctypes.c_int)
                )
        except Exception:
            pass  # Ignore if not Windows or API not available

