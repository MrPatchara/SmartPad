# Text Editor Plus (SmartPad)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**A powerful, modern text editor with syntax highlighting and auto-formatting capabilities**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Development](#-development)

</div>

---

## 📋 Overview

Text Editor Plus (also known as SmartPad) is an advanced, cross-platform text editor built with Python and PyQt5. It provides a clean, modern interface with professional code editing features including syntax highlighting, auto-formatting, and theme support.

## ✨ Features

### Core Features
- **🎨 Syntax Highlighting** - Support for multiple programming languages:
  - XML/HTML
  - JSON
  - Python
  - CSS
  - JavaScript
  - And more...

- **🔧 Auto-Formatting** - Professional code formatting with one click
  - XML/HTML formatting with proper indentation
  - JSON pretty printing with 2-space indentation
  - Python code formatting
  - CSS rule organization
  - JavaScript brace formatting

- **🌓 Theme Support** - Beautiful themes inspired by VS Code
  - Dark Theme (default)
  - Light Theme
  - Smooth theme switching

- **📝 Advanced Editor Features**
  - Line numbers
  - Word wrap toggle
  - Find and replace with match counter
  - Undo/Redo support
  - Customizable font size (8-72pt)
  - Status bar with file information

- **🖥️ High DPI Support** - Perfect scaling on all screen sizes
  - Supports 100%, 125%, 150% DPI scaling
  - Responsive window sizing
  - Optimized for modern displays

- **📁 File Management**
  - Open any text file
  - Save and Save As functionality
  - Recent file support
  - File type detection

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Text-Editor-Plus.git
cd Text-Editor-Plus
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python main.py
```

## 💻 Usage

### Opening Files

- **Menu**: File → Open
- **Shortcut**: `Ctrl+O` (Windows/Linux) or `Cmd+O` (macOS)
- Supports all text file formats

### Saving Files

- **Save**: File → Save or `Ctrl+S`
- **Save As**: File → Save As... or `Ctrl+Shift+S`

### Auto-Formatting

- **Menu**: Edit → Auto-Formatting
- **Shortcut**: `Ctrl+Shift+F`
- Automatically detects file type and formats accordingly

### Find and Replace

- **Find**: Edit → Find... or `Ctrl+F`
- **Find Next**: `F3`
- Features:
  - Case-sensitive search option
  - Match counter
  - Highlight all matches

### Theme Switching

- **Menu**: Settings → Theme → Dark Theme / Light Theme
- Dark theme is the default

### Font Size Adjustment

- **Menu**: Settings → Font Size...
- Adjust editor font size from 8 to 72 points

### Word Wrap

- **Menu**: Edit → Word Wrap
- Toggle word wrapping on/off

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New File | `Ctrl+N` |
| Open File | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| Find | `Ctrl+F` |
| Find Next | `F3` |
| Auto-Format | `Ctrl+Shift+F` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` |
| Cut | `Ctrl+X` |
| Copy | `Ctrl+C` |
| Paste | `Ctrl+V` |
| Select All | `Ctrl+A` |
| Help | `F1` |
| Exit | `Ctrl+Q` |

## 📸 Screenshots

> **Note**: Add screenshots of your application here
> 
> Example:
> - Dark theme screenshot
> - Light theme screenshot
> - Syntax highlighting example
> - Auto-formatting before/after

## 🏗️ Project Structure

```
Text-Editor-Plus/
├── src/                      # Source code modules
│   ├── __init__.py          # Package initialization
│   ├── text_editor.py       # Main editor window
│   ├── code_editor.py       # Code editor with line numbers
│   ├── syntax_highlighter.py # Syntax highlighting module
│   ├── formatters.py        # Code formatters (XML, JSON, etc.)
│   ├── themes.py            # Theme management
│   ├── utils.py             # Utility functions
│   ├── logo.png             # Application icon
│   └── logo1.png            # Alternative icon
├── demo/                     # Demo files
│   └── *.xml, *.epx         # Sample files
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## 🔧 Development

### Adding New Language Support

To add syntax highlighting for a new language:

1. Edit `src/syntax_highlighter.py`
2. Add language detection patterns in `src/utils.py`
3. Define syntax rules and color schemes

### Adding New Formatters

To add auto-formatting for a new file type:

1. Edit `src/formatters.py`
2. Implement formatting logic
3. Add file type detection in `src/utils.py`

### Customizing Themes

To customize or add new themes:

1. Edit `src/themes.py`
2. Define color schemes
3. Update theme switching logic

### Building from Source

```bash
# Clone repository
git clone https://github.com/yourusername/Text-Editor-Plus.git
cd Text-Editor-Plus

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📦 Dependencies

- **PyQt5** (>=5.15.0) - GUI framework
  - Provides cross-platform windowing and widgets
  - High DPI support
  - Modern UI components

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Inspired by modern code editors like VS Code
- Syntax highlighting patterns based on common language specifications

## 📧 Contact

For questions, suggestions, or support, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ using Python and PyQt5**

⭐ Star this repo if you find it useful!

</div>
