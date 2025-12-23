#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formatters Module
Provides code formatting functions for various file types
"""

import json
import xml.dom.minidom
import re


class Formatters:
    """Code formatters for various file types"""
    
    @staticmethod
    def format_xml(content):
        """Format XML content with professional standard formatting"""
        try:
            if not content.strip():
                return None, "No content to format"
            
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
            
            return formatted, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def format_json(content):
        """Format JSON content"""
        try:
            if not content.strip():
                return None, "No content to format"
            
            # Parse and format JSON
            data = json.loads(content)
            formatted = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False)
            
            return formatted, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def format_python(content):
        """Format Python content using basic formatting"""
        try:
            if not content.strip():
                return None, "No content to format"
            
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
            return formatted, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def format_css(content):
        """Format CSS content"""
        try:
            if not content.strip():
                return None, "No content to format"
            
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
            return formatted, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def format_javascript(content):
        """Format JavaScript content"""
        try:
            if not content.strip():
                return None, "No content to format"
            
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
            return formatted, None
        except Exception as e:
            return None, str(e)

