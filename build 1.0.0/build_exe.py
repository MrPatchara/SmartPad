#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for Text Editor Plus using NUITKA
This script creates a standalone .exe file in current folder
"""

import os
import sys
import subprocess
from pathlib import Path

def check_nuitka():
    """Check if NUITKA is installed"""
    try:
        import nuitka
        return True
    except ImportError:
        print("NUITKA is not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "nuitka"])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install NUITKA. Please install manually: pip install nuitka")
            return False

def build_exe():
    """Build the executable using NUITKA"""
    print("=" * 50)
    print("Building Text Editor Plus with NUITKA")
    print("=" * 50)
    print()
    
    # Change to project root directory (parent of build 1.0.0)
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Check NUITKA
    if not check_nuitka():
        return False
    
    # Build directory (current script location)
    build_dir = script_dir
    
    # Check if icon exists
    icon_path = project_root / "src" / "icon.ico"
    if not icon_path.exists():
        print(f"Warning: Icon file not found at {icon_path}")
        icon_option = ""
    else:
        icon_option = f"--windows-icon-from-ico={icon_path}"
    
    print("Starting NUITKA build...")
    print()
    
    # Build command
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        f"--output-dir={build_dir}",
        "--output-filename=TextEditorPlus.exe",
        "--include-package-data=src",
        "--include-data-dir=src=src",
        "--include-data-files=src/logo.png=src/logo.png",
        "--include-data-files=src/icon.ico=src/icon.ico",
        "--enable-plugin=pyqt5",
        "--windows-console-mode=disable",
        "--assume-yes-for-downloads",
        "--show-progress",
        "--show-memory",
        "--remove-output",
        "main.py"
    ]
    
    if icon_option:
        # Insert icon option after --onefile
        cmd.insert(3, icon_option)
    
    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 50)
        print("Build completed successfully!")
        print(f"Output: {build_dir / 'TextEditorPlus.exe'}")
        print("=" * 50)
        return True
    except subprocess.CalledProcessError as e:
        print()
        print("Build failed!")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)

