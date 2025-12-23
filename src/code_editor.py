#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Editor Module
Provides enhanced code editor with line numbers
"""

from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QFontMetrics


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
        
        # Use scalable font size based on DPI
        font = QFont("Consolas")
        font.setPointSize(11)
        self.setFont(font)
        
        # Calculate tab stop width based on font metrics (scales with DPI)
        metrics = QFontMetrics(font)
        tab_width = metrics.width(' ') * 4  # 4 spaces per tab
        self.setTabStopWidth(tab_width)
        
        self.current_theme = 'dark'  # Default theme
    
    def set_theme(self, theme):
        """Set theme for line number area"""
        self.current_theme = theme
        self.line_number_area.update()
    
    def line_number_area_width(self):
        """Calculate line number area width that scales with DPI"""
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        
        # Use font metrics for proper scaling
        metrics = self.fontMetrics()
        char_width = metrics.width('9')
        # Add padding that scales with DPI (minimum 10 logical pixels)
        # Use devicePixelRatioF() if available, otherwise use 1.0
        try:
            dpi_ratio = self.devicePixelRatioF()
        except:
            dpi_ratio = 1.0
        padding = max(10, int(10 * dpi_ratio))
        space = padding + char_width * digits
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

