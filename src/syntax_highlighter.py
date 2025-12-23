#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Syntax Highlighter Module
Provides syntax highlighting for multiple programming languages
"""

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import (QTextCharFormat, QFont, QColor, QSyntaxHighlighter)


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
        """XML syntax highlighting - Beautiful balanced colors for comfortable coding"""
        if self.theme == 'light':
            # Light theme colors - Balanced and readable
            tag_color = "#7C4DFF"  # Rich Lavender - tags (darker, more visible)
            closing_tag_color = "#9C27B0"  # Deep Purple - closing tags
            attr_color = "#E91E63"  # Pink - attributes (clearer)
            attr_value_color = "#2196F3"  # Blue - attribute values
            comment_color = "#4CAF50"  # Green - comments
            cdata_color = "#FF9800"  # Orange - CDATA
            text_color = "#424242"  # Dark Gray - text content
            declaration_color = "#1976D2"  # Deep Blue - XML declaration
            namespace_color = "#9C27B0"  # Purple - namespace prefixes
        else:
            # Dark theme colors - Balanced, readable, not too bright
            tag_color = "#82B1FF"  # Medium Blue - opening tags (clearer)
            closing_tag_color = "#80CBC4"  # Teal - closing tags
            attr_color = "#F48FB1"  # Medium Pink - attributes
            attr_value_color = "#FFCC80"  # Amber - attribute values
            comment_color = "#A5D6A7"  # Light Green - comments
            cdata_color = "#FFE082"  # Light Yellow - CDATA
            text_color = "#E0E0E0"  # Light Gray - text content
            declaration_color = "#90CAF9"  # Light Blue - XML declaration
            namespace_color = "#CE93D8"  # Light Purple - namespace prefixes
        
        # XML Declaration - <?xml ... ?>
        declaration_format = QTextCharFormat()
        declaration_format.setForeground(QColor(declaration_color))
        declaration_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'<\?xml[^?>]*\?>'), declaration_format))
        
        # Opening Tags - <tag> or <tag ...>
        opening_tag_format = QTextCharFormat()
        opening_tag_format.setForeground(QColor(tag_color))
        opening_tag_format.setFontWeight(QFont.Bold)
        # Match opening tags (not closing, not self-closing)
        self.highlighting_rules.append((QRegExp(r'<(?!/)[\w:]+(?:\s+[^>]*)?(?<!/)>'), opening_tag_format))
        
        # Closing Tags - </tag>
        closing_tag_format = QTextCharFormat()
        closing_tag_format.setForeground(QColor(closing_tag_color))
        closing_tag_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'</[\w:]+>'), closing_tag_format))
        
        # Self-closing Tags - <tag/>
        self_closing_format = QTextCharFormat()
        self_closing_format.setForeground(QColor(tag_color))
        self_closing_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'<[\w:]+\s+[^>]*/>'), self_closing_format))
        
        # Namespace prefixes - xmlns, xsi, etc.
        namespace_format = QTextCharFormat()
        namespace_format.setForeground(QColor(namespace_color))
        namespace_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\bxmlns(?::\w+)?\b'), namespace_format))
        self.highlighting_rules.append((QRegExp(r'\bxsi(?::\w+)?\b'), namespace_format))
        
        # XML Attributes - match attribute names (improved)
        attr_format = QTextCharFormat()
        attr_format.setForeground(QColor(attr_color))
        attr_format.setFontWeight(QFont.Bold)
        # Match attribute names before = (including namespace prefixes)
        self.highlighting_rules.append((QRegExp(r'\s+[\w:-]+\s*='), attr_format))
        
        # Attribute Values - match quoted values (improved)
        attr_value_format = QTextCharFormat()
        attr_value_format.setForeground(QColor(attr_value_color))
        # Match attribute values in single or double quotes
        self.highlighting_rules.append((QRegExp(r'=\s*"[^"]*"'), attr_value_format))
        self.highlighting_rules.append((QRegExp(r"=\s*'[^']*'"), attr_value_format))
        
        # Comments - multi-line support (improved)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        # Match comments (including multi-line) - more robust
        self.highlighting_rules.append((QRegExp(r'<!--[^-]*(?:-(?!->)[^-]*)*-->'), comment_format))
        
        # CDATA sections (improved)
        cdata_format = QTextCharFormat()
        cdata_format.setForeground(QColor(cdata_color))
        cdata_format.setFontWeight(QFont.Bold)
        # Match CDATA with better regex
        self.highlighting_rules.append((QRegExp(r'<!\[CDATA\[.*?\]\]>'), cdata_format))
        
        # Processing Instructions - <?pi ... ?>
        pi_format = QTextCharFormat()
        pi_format.setForeground(QColor(declaration_color))
        pi_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'<\?[\w-]+\s+[^?>]*\?>'), pi_format))
    
    def setup_json_highlighting(self):
        """JSON syntax highlighting - VS Code Dark+ theme"""
        if self.theme == 'light':
            # Light theme colors (VS Code Light+)
            key_color = "#0451A5"  # Blue
            string_color = "#A31515"  # Dark Red
            number_color = "#098658"  # Green
            keyword_color = "#0000FF"  # Blue
            punctuation_color = "#000000"  # Black
        else:
            # Dark theme colors (VS Code Dark+)
            key_color = "#9CDCFE"  # Light Blue - keys
            string_color = "#CE9178"  # Orange - strings
            number_color = "#B5CEA8"  # Light Green - numbers
            keyword_color = "#569CD6"  # Cyan Blue - keywords (true, false, null)
            punctuation_color = "#D4D4D4"  # Light Gray - brackets, commas
        
        # Keys - JSON property names
        key_format = QTextCharFormat()
        key_format.setForeground(QColor(key_color))
        # Match key: pattern (key name before colon)
        self.highlighting_rules.append((QRegExp(r'"([^"]+)"\s*:'), key_format))
        
        # Strings - JSON string values
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string_color))
        # Match string values (not keys)
        self.highlighting_rules.append((QRegExp(r':\s*"[^"]*"'), string_format))
        # Also match standalone strings in arrays
        self.highlighting_rules.append((QRegExp(r'(?:^|,|\s)\s*"[^"]*"(?=\s*[,}\]])'), string_format))
        
        # Numbers - integers and floats
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(number_color))
        # Match numbers (integers and decimals)
        self.highlighting_rules.append((QRegExp(r'\b\d+\.?\d*\b'), number_format))
        
        # Keywords (true, false, null)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(keyword_color))
        keyword_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\b(true|false|null)\b'), keyword_format))
    
    def setup_python_highlighting(self):
        """Python syntax highlighting - VS Code Dark+ theme"""
        if self.theme == 'light':
            # Light theme colors (VS Code Light+)
            keyword_color = "#0000FF"  # Blue
            string_color = "#A31515"  # Dark Red
            comment_color = "#008000"  # Green
            number_color = "#098658"  # Green
            function_color = "#795E26"  # Brown
            class_color = "#267F99"  # Teal
        else:
            # Dark theme colors (VS Code Dark+)
            keyword_color = "#569CD6"  # Cyan Blue - keywords
            string_color = "#CE9178"  # Orange - strings
            comment_color = "#6A9955"  # Green - comments
            number_color = "#B5CEA8"  # Light Green - numbers
            function_color = "#DCDCAA"  # Beige - functions
            class_color = "#4EC9B0"  # Cyan - classes
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(keyword_color))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ['def', 'class', 'import', 'from', 'if', 'else', 'elif', 
                   'for', 'while', 'try', 'except', 'finally', 'return', 
                   'yield', 'with', 'as', 'pass', 'break', 'continue', 
                   'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False',
                   'lambda', 'raise', 'assert', 'del', 'global', 'nonlocal']
        for keyword in keywords:
            self.highlighting_rules.append((QRegExp(r'\b' + keyword + r'\b'), keyword_format))
        
        # Functions - def function_name
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(function_color))
        self.highlighting_rules.append((QRegExp(r'\bdef\s+(\w+)'), function_format))
        
        # Classes - class ClassName
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(class_color))
        class_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\bclass\s+(\w+)'), class_format))
        
        # Strings - single and double quotes, triple quotes
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string_color))
        # Single line strings
        self.highlighting_rules.append((QRegExp(r'"[^"]*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'[^']*'"), string_format))
        # Triple quoted strings (multi-line)
        self.highlighting_rules.append((QRegExp(r'"""[^"]*"""'), string_format))
        self.highlighting_rules.append((QRegExp(r"'''[^']*'''"), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))
        
        # Numbers - integers, floats, hex, binary
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(number_color))
        # Match numbers (integers, floats, hex, binary)
        self.highlighting_rules.append((QRegExp(r'\b\d+\.?\d*\b'), number_format))
        self.highlighting_rules.append((QRegExp(r'\b0[xX][0-9a-fA-F]+\b'), number_format))
        self.highlighting_rules.append((QRegExp(r'\b0[bB][01]+\b'), number_format))
    
    def setup_html_highlighting(self):
        """HTML syntax highlighting (similar to XML)"""
        self.setup_xml_highlighting()
    
    def setup_css_highlighting(self):
        """CSS syntax highlighting - VS Code Dark+ theme"""
        if self.theme == 'light':
            selector_color = "#800000"  # Maroon
            property_color = "#FF0000"  # Red
            value_color = "#0451A5"  # Blue
            comment_color = "#008000"  # Green
            unit_color = "#098658"  # Green
        else:
            # Dark theme colors (VS Code Dark+)
            selector_color = "#D7BA7D"  # Yellow/Beige - selectors
            property_color = "#9CDCFE"  # Light Blue - properties
            value_color = "#CE9178"  # Orange - values
            comment_color = "#6A9955"  # Green - comments
            unit_color = "#B5CEA8"  # Light Green - units (px, em, etc.)
        
        # Selectors - before {
        selector_format = QTextCharFormat()
        selector_format.setForeground(QColor(selector_color))
        self.highlighting_rules.append((QRegExp(r'[^{]+\{'), selector_format))
        
        # Properties - property name before :
        property_format = QTextCharFormat()
        property_format.setForeground(QColor(property_color))
        self.highlighting_rules.append((QRegExp(r'\s+[\w-]+\s*:'), property_format))
        
        # Values - after : before ;
        value_format = QTextCharFormat()
        value_format.setForeground(QColor(value_color))
        self.highlighting_rules.append((QRegExp(r':\s*[^;]+;'), value_format))
        
        # Units in values (px, em, rem, %, etc.)
        unit_format = QTextCharFormat()
        unit_format.setForeground(QColor(unit_color))
        self.highlighting_rules.append((QRegExp(r'\b\d+(?:px|em|rem|%|pt|cm|mm|in|ex|ch|vw|vh|vmin|vmax)\b'), unit_format))
        
        # Comments - multi-line support
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        # Match CSS comments (including multi-line)
        self.highlighting_rules.append((QRegExp(r'/\*[^*]*(?:\*(?!/)[^*]*)*\*/'), comment_format))
    
    def setup_javascript_highlighting(self):
        """JavaScript syntax highlighting - VS Code Dark+ theme"""
        if self.theme == 'light':
            keyword_color = "#0000FF"  # Blue
            string_color = "#A31515"  # Dark Red
            comment_color = "#008000"  # Green
            number_color = "#098658"  # Green
            function_color = "#795E26"  # Brown
            class_color = "#267F99"  # Teal
        else:
            # Dark theme colors (VS Code Dark+)
            keyword_color = "#569CD6"  # Cyan Blue - keywords
            string_color = "#CE9178"  # Orange - strings
            comment_color = "#6A9955"  # Green - comments
            number_color = "#B5CEA8"  # Light Green - numbers
            function_color = "#DCDCAA"  # Beige - functions
            class_color = "#4EC9B0"  # Cyan - classes
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(keyword_color))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ['function', 'var', 'let', 'const', 'if', 'else', 'for', 
                   'while', 'return', 'true', 'false', 'null', 'undefined', 
                   'this', 'new', 'class', 'extends', 'import', 'export',
                   'async', 'await', 'try', 'catch', 'finally', 'throw',
                   'switch', 'case', 'default', 'break', 'continue', 'do']
        for keyword in keywords:
            self.highlighting_rules.append((QRegExp(r'\b' + keyword + r'\b'), keyword_format))
        
        # Functions - function functionName
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(function_color))
        self.highlighting_rules.append((QRegExp(r'\bfunction\s+(\w+)'), function_format))
        # Arrow functions
        self.highlighting_rules.append((QRegExp(r'\b(\w+)\s*=>'), function_format))
        
        # Classes - class ClassName
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(class_color))
        class_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\bclass\s+(\w+)'), class_format))
        
        # Strings - single and double quotes, template literals
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string_color))
        self.highlighting_rules.append((QRegExp(r'"[^"]*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'[^']*'"), string_format))
        # Template literals
        self.highlighting_rules.append((QRegExp(r'`[^`]*`'), string_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(number_color))
        self.highlighting_rules.append((QRegExp(r'\b\d+\.?\d*\b'), number_format))
        self.highlighting_rules.append((QRegExp(r'\b0[xX][0-9a-fA-F]+\b'), number_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        # Single line comments
        self.highlighting_rules.append((QRegExp(r'//.*'), comment_format))
        # Multi-line comments
        self.highlighting_rules.append((QRegExp(r'/\*[^*]*(?:\*(?!/)[^*]*)*\*/'), comment_format))
    
    def setup_generic_highlighting(self):
        """Generic highlighting for unknown file types - Beautiful and colorful"""
        if self.theme == 'light':
            # Light theme colors - Beautiful and readable
            string_color = "#A31515"  # Rich Red - strings
            comment_color = "#008000"  # Forest Green - comments
            number_color = "#098658"  # Emerald Green - numbers
            keyword_color = "#0000FF"  # Pure Blue - keywords
            url_color = "#0066CC"  # Bright Blue - URLs
            email_color = "#0066CC"  # Bright Blue - emails
            path_color = "#8B4513"  # Chocolate Brown - file paths
            date_color = "#007ACC"  # Azure Blue - dates/times
            ip_color = "#9B26B6"  # Vibrant Purple - IP addresses
            hex_color = "#0E7C0E"  # Forest Green - hex colors
            version_color = "#005A9E"  # Deep Blue - version numbers
            boolean_color = "#0000FF"  # Pure Blue - true/false
            operator_color = "#333333"  # Charcoal Gray - operators
            bracket_color = "#666666"  # Medium Gray - brackets
            error_color = "#E51400"  # Bright Red - error keywords
            success_color = "#0E7C0E"  # Forest Green - success keywords
        else:
            # Dark theme colors - VS Code Dark+ Enhanced (Beautiful & Readable)
            string_color = "#CE9178"  # Warm Peach - strings (very readable)
            comment_color = "#6A9955"  # Soft Mint - comments
            number_color = "#B5CEA8"  # Pale Green - numbers
            keyword_color = "#569CD6"  # Sky Blue - keywords
            url_color = "#4EC9B0"  # Aqua Cyan - URLs
            email_color = "#4EC9B0"  # Aqua Cyan - emails
            path_color = "#DCDCAA"  # Light Khaki - file paths
            date_color = "#4EC9B0"  # Aqua Cyan - dates/times
            ip_color = "#C586C0"  # Soft Lavender - IP addresses
            hex_color = "#B5CEA8"  # Pale Green - hex colors
            version_color = "#9CDCFE"  # Light Cyan - version numbers
            boolean_color = "#569CD6"  # Sky Blue - true/false
            operator_color = "#D4D4D4"  # Light Silver - operators
            bracket_color = "#808080"  # Medium Gray - brackets
            error_color = "#F48771"  # Coral Pink - error keywords
            success_color = "#89D185"  # Light Lime - success keywords
        
        # Strings - single and double quotes
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(string_color))
        self.highlighting_rules.append((QRegExp(r'"[^"]*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'[^']*'"), string_format))
        
        # Numbers - integers and floats
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(number_color))
        self.highlighting_rules.append((QRegExp(r'\b\d+\.?\d*\b'), number_format))
        
        # Version numbers - v1.2.3, 1.2.3.4, etc.
        version_format = QTextCharFormat()
        version_format.setForeground(QColor(version_color))
        version_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\bv?\d+\.\d+(?:\.\d+)*(?:-[a-zA-Z0-9]+)?\b'), version_format))
        
        # IP addresses - IPv4 and IPv6
        ip_format = QTextCharFormat()
        ip_format.setForeground(QColor(ip_color))
        ip_format.setFontWeight(QFont.Bold)
        # IPv4: 192.168.1.1
        self.highlighting_rules.append((QRegExp(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'), ip_format))
        # IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
        self.highlighting_rules.append((QRegExp(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'), ip_format))
        
        # Hex colors - #FF0000, #fff, etc.
        hex_color_format = QTextCharFormat()
        hex_color_format.setForeground(QColor(hex_color))
        hex_color_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'#[0-9a-fA-F]{3,6}\b'), hex_color_format))
        
        # Dates and times - various formats
        date_format = QTextCharFormat()
        date_format.setForeground(QColor(date_color))
        # Dates: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY
        self.highlighting_rules.append((QRegExp(r'\b\d{4}-\d{2}-\d{2}\b'), date_format))
        self.highlighting_rules.append((QRegExp(r'\b\d{1,2}/\d{1,2}/\d{4}\b'), date_format))
        # Times: HH:MM:SS, HH:MM
        self.highlighting_rules.append((QRegExp(r'\b\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?\b'), date_format))
        # ISO datetime: 2024-01-01T12:00:00
        self.highlighting_rules.append((QRegExp(r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?\b'), date_format))
        
        # URLs - http, https, ftp, file://
        url_format = QTextCharFormat()
        url_format.setForeground(QColor(url_color))
        url_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        self.highlighting_rules.append((QRegExp(r'https?://[^\s<>"\'{}|\\^`\[\]]+'), url_format))
        self.highlighting_rules.append((QRegExp(r'ftp://[^\s<>"\'{}|\\^`\[\]]+'), url_format))
        self.highlighting_rules.append((QRegExp(r'file://[^\s<>"\'{}|\\^`\[\]]+'), url_format))
        
        # Email addresses
        email_format = QTextCharFormat()
        email_format.setForeground(QColor(email_color))
        email_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        self.highlighting_rules.append((QRegExp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), email_format))
        
        # File paths - Windows and Unix style
        path_format = QTextCharFormat()
        path_format.setForeground(QColor(path_color))
        # Windows paths: C:\path\to\file or \\server\share
        self.highlighting_rules.append((QRegExp(r'[A-Za-z]:\\[^\s<>"\'{}|\\^`\[\]]+'), path_format))
        self.highlighting_rules.append((QRegExp(r'\\\\[^\s<>"\'{}|\\^`\[\]]+'), path_format))
        # Unix paths: /path/to/file or ~/path/to/file
        self.highlighting_rules.append((QRegExp(r'/[^\s<>"\'{}|\\^`\[\]]+'), path_format))
        self.highlighting_rules.append((QRegExp(r'~/[^\s<>"\'{}|\\^`\[\]]+'), path_format))
        
        # Boolean values
        boolean_format = QTextCharFormat()
        boolean_format.setForeground(QColor(boolean_color))
        boolean_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\b(true|false|yes|no|on|off|enabled|disabled|active|inactive)\b'), boolean_format))
        
        # Operators and special characters
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(operator_color))
        # Math operators: +, -, *, /, =, !=, <, >, <=, >=
        self.highlighting_rules.append((QRegExp(r'[+\-*/=<>!]+'), operator_format))
        
        # Brackets and parentheses
        bracket_format = QTextCharFormat()
        bracket_format.setForeground(QColor(bracket_color))
        bracket_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'[{}[\]()]'), bracket_format))
        
        # Comments - various styles
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(comment_color))
        comment_format.setFontItalic(True)
        # Hash comments (#)
        self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))
        # Double slash comments (//)
        self.highlighting_rules.append((QRegExp(r'//.*'), comment_format))
        # Semicolon comments (;)
        self.highlighting_rules.append((QRegExp(r';.*'), comment_format))
        
        # Common keywords (if they appear in plain text)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(keyword_color))
        keyword_format.setFontWeight(QFont.Bold)
        common_keywords = ['null', 'none', 'warning', 'info', 'debug',
                          'ok', 'okay', 'done', 'start', 'stop', 'begin', 
                          'end', 'init', 'exit', 'load', 'save', 'open', 
                          'close', 'read', 'write', 'create', 'delete', 
                          'update', 'insert', 'select']
        for keyword in common_keywords:
            self.highlighting_rules.append((QRegExp(r'\b' + keyword + r'\b'), keyword_format))
        
        # Error keywords - special color
        error_format = QTextCharFormat()
        error_format.setForeground(QColor(error_color))
        error_format.setFontWeight(QFont.Bold)
        error_keywords = ['error', 'fail', 'failed', 'failure', 'exception', 
                         'crash', 'abort', 'invalid', 'wrong', 'bad']
        for keyword in error_keywords:
            self.highlighting_rules.append((QRegExp(r'\b' + keyword + r'\b'), error_format))
        
        # Success keywords - special color
        success_format = QTextCharFormat()
        success_format.setForeground(QColor(success_color))
        success_format.setFontWeight(QFont.Bold)
        success_keywords = ['success', 'pass', 'passed', 'complete', 'completed',
                           'valid', 'good', 'ok', 'okay', 'done', 'finished']
        for keyword in success_keywords:
            self.highlighting_rules.append((QRegExp(r'\b' + keyword + r'\b'), success_format))
    
    def highlightBlock(self, text):
        """Apply highlighting to a block of text"""
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

