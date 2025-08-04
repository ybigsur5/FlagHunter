# FlagHunter 🏴‍☠️

A comprehensive CTF flag hunting tool designed to automatically discover flags in various formats and locations during Capture The Flag competitions.

## Features

- 🔍 **Multi-format Flag Detection**: Supports various flag formats (CTF{}, FLAG{}, custom patterns)
- 🌐 **Web Scanning**: Scans web pages, source code, and HTTP headers
- 📁 **File Analysis**: Recursively searches through files and directories
- 🔗 **Network Probing**: Basic network reconnaissance for flag discovery
- ⚡ **Fast & Efficient**: Multi-threaded scanning capabilities
- 🎯 **Customizable Patterns**: Easy to add custom flag formats
- 📊 **Detailed Reporting**: Comprehensive output with location details

## Installation

```bash
git clone https://github.com/yourusername/FlagHunter.git
cd FlagHunter
pip install -r requirements.txt
Quick Start
Bash

# Scan a website
python flaghunter.py -u https://example.com

# Scan local files
python flaghunter.py -d /path/to/directory

# Scan with custom pattern
python flaghunter.py -u https://example.com -p "CUSTOM{.*?}"

# Verbose output
python flaghunter.py -u https://example.com -v
Usage
Basic Commands
Bash

# Web scanning
python flaghunter.py -u <URL>                    # Single URL
python flaghunter.py -f urls.txt                 # Multiple URLs from file

# File scanning  
python flaghunter.py -d <directory>              # Scan directory
python flaghunter.py -file <filename>            # Scan single file

# Network scanning
python flaghunter.py -n <target>                 # Network reconnaissance
Advanced Options
Bash

-p, --pattern     Custom flag pattern (regex)
-t, --threads     Number of threads (default: 10)
-o, --output      Output file for results
-v, --verbose     Verbose output
-r, --recursive   Recursive directory scanning
--timeout         Request timeout (default: 10s)
--user-agent      Custom user agent
--headers         Custom headers (JSON format)
Examples
Bash

# Comprehensive web scan
python flaghunter.py -u https://ctf.example.com -v -t 20 -o results.txt

# Deep file system scan
python flaghunter.py -d /home/ctf/challenge -r -v

# Custom pattern search
python flaghunter.py -u https://example.com -p "FLAG\{[a-zA-Z0-9_]+\}"

# Multiple targets
python flaghunter.py -f target_urls.txt -t 15 --timeout 15
Configuration
Edit config.json to customize:

Default flag patterns
File extensions to scan
Request headers and user agents
Output formats
Flag Patterns Supported
CTF{...}
FLAG{...}
flag{...}
PICO{...}
HTB{...}
Custom regex patterns
Contributing
Fork the repository
Create a feature branch
Make your changes
Submit a pull request

## Disclaimer
This tool is for educational purposes and authorized CTF competitions only. Always ensure you have permission before scanning any systems.

## License
MIT License - see LICENSE file for details.

