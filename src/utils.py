#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utils Module
Provides utility functions for the application
"""

import json
import re
from pathlib import Path


def detect_language(filename):
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


def detect_file_type_from_content(content):
    """Detect file type from content - more robust detection"""
    if not content or not content.strip():
        return None
    
    content_stripped = content.strip()
    
    # Check for XML - more comprehensive
    # Look for XML declaration or XML-like tags
    if content_stripped.startswith('<?xml'):
        return 'xml'
    
    # Check for XML-like structure (tags with < >)
    if re.search(r'<[^>]+>', content):
        # Count XML-like patterns
        tag_count = len(re.findall(r'<[^>]+>', content))
        # If there are multiple tags, likely XML
        if tag_count >= 2:
            # Check for common XML patterns
            if re.search(r'</\w+>', content) or re.search(r'<\w+[^>]*/>', content):
                return 'xml'
            # Check for XML-like structure even without closing tags
            if tag_count >= 3:
                return 'xml'
    
    # Check for JSON - more robust
    if content_stripped.startswith('{') or content_stripped.startswith('['):
        try:
            json.loads(content)
            return 'json'
        except:
            # Try to detect JSON-like structure even if invalid
            if (content_stripped.startswith('{') and '}' in content) or \
               (content_stripped.startswith('[') and ']' in content):
                # Check for JSON-like patterns
                if re.search(r'"[^"]+"\s*:', content) and re.search(r':\s*"[^"]+"', content):
                    return 'json'
    
    return None

