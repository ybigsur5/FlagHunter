# FlagHunter 🏴‍☠️
FlagHunter is a powerful, multi-threaded CTF (Capture The Flag) reconnaissance tool designed to automatically discover flags across various formats and locations during cybersecurity competitions. Built for efficiency and versatility, FlagHunter streamlines the flag hunting process through comprehensive scanning capabilities that cover web applications, file systems, and network services.

## Features

- 🔍 **Multi-format Flag Detection**: Supports various flag formats (CTF{}, FLAG{}, custom patterns)
- 🌐 **Web Scanning**: Scans web pages, source code, and HTTP headers
- 📁 **File Analysis**: Recursively searches through files and directories
- 🔗 **Network Probing**: Basic network reconnaissance for flag discovery
- ⚡ **Fast & Efficient**: Multi-threaded scanning capabilities
- 🎯 **Customizable Patterns**: Easy to add custom flag formats
- 📊 **Detailed Reporting**: Comprehensive output with location details

## Installation

    git clone https://github.com/yourusername/FlagHunter.git
    cd FlagHunter
    pip install -r requirements.txt

## Quick Start

    # Scan a website
    python flaghunter.py -u https://example.com

    # Scan local files
    python flaghunter.py -d /path/to/directory

    # Scan with custom pattern
    python flaghunter.py -u https://example.com -p "CUSTOM{.*?}"

    # Verbose output
    python flaghunter.py -u https://example.com -v

## Usage

### Basic Commands

    # Web scanning
    python flaghunter.py -u <URL>                    # Single URL
    python flaghunter.py -f urls.txt                 # Multiple URLs from file

    # File scanning  
    python flaghunter.py -d <directory>              # Scan directory
    python flaghunter.py --single-file <filename>    # Scan single file

    # Network scanning
    python flaghunter.py -n <target>                 # Network reconnaissance

### Advanced Options

    -p, --pattern     Custom flag pattern (regex)
    -t, --threads     Number of threads (default: 10)
    -o, --output      Output file for results
    -v, --verbose     Verbose output
    -r, --recursive   Recursive directory scanning
    --timeout         Request timeout (default: 10s)
    --user-agent      Custom user agent
    --headers         Custom headers (JSON format)

### Examples

    # Comprehensive web scan
    python flaghunter.py -u https://ctf.example.com -v -t 20 -o results.txt

    # Deep file system scan
    python flaghunter.py -d /home/ctf/challenge -r -v

    # Custom pattern search
    python flaghunter.py -u https://example.com -p "FLAG\{[a-zA-Z0-9_]+\}"

    # Multiple targets
    python flaghunter.py -f target_urls.txt -t 15 --timeout 15

    # Real CTF scenarios
    python flaghunter.py -u https://web.ctf.com -v -t 15 -o web_flags.txt
    python flaghunter.py -d ./extracted_files -r -v
    python flaghunter.py -u http://10.10.10.100:8080 -v

## Configuration

Edit `config.json` to customize:

    {
        "flag_patterns": [
            "CTF\\{[^}]+\\}",
            "FLAG\\{[^}]+\\}",
            "flag\\{[^}]+\\}",
            "PICO\\{[^}]+\\}",
            "HTB\\{[^}]+\\}"
        ],
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ],
        "file_extensions": [".txt", ".html", ".js", ".php", ".py", ".log"],
        "timeout": 10,
        "max_threads": 10
    }

## Flag Patterns Supported

- `CTF{...}` - Standard CTF format
- `FLAG{...}` - Generic flag format
- `flag{...}` - Lowercase variant
- `PICO{...}` - PicoCTF format
- `HTB{...}` - HackTheBox format
- `CYBER{...}` - CyberDefenders format
- Custom regex patterns

## File Structure

    FlagHunter/
    ├── README.md
    ├── flaghunter.py           # Main script
    ├── requirements.txt        # Python dependencies
    ├── config.json            # Configuration file
    ├── wordlists/
    │   ├── flag_patterns.txt   # Flag pattern wordlist
    │   └── common_flags.txt    # Common flag examples
    ├── modules/
    │   ├── __init__.py
    │   ├── web_scanner.py      # Web scanning module
    │   ├── file_scanner.py     # File scanning module
    │   └── network_scanner.py  # Network scanning module
    └── examples/
        └── usage_examples.md   # Detailed usage examples

## Output Format

    FlagHunter Results
    ==================

    Flag: CTF{example_flag_here}
    Source: URL: https://example.com (body)
    Timestamp: 2024-01-15 14:30:25
    --------------------------------------------------

    Flag: FLAG{another_flag}
    Source: File: /path/to/file.txt
    Timestamp: 2024-01-15 14:30:26
    --------------------------------------------------

## Common Use Cases

### Web Challenges
- Source code analysis
- HTTP header inspection
- Cookie examination
- JavaScript file scanning
- robots.txt and sitemap.xml checking

### File Analysis
- Log file examination
- Configuration file scanning
- Source code review
- Binary string extraction
- Archive content analysis

### Network Reconnaissance
- Service banner grabbing
- Port scanning with flag detection
- Network service enumeration

## Tips for CTF Usage

1. **Start with verbose mode** (`-v`) to see what's being scanned
2. **Use custom patterns** (`-p`) for competition-specific formats
3. **Increase threads** (`-t 20`) for faster scanning of multiple targets
4. **Save results** (`-o results.txt`) for later analysis
5. **Recursive scanning** (`-r`) for deep directory analysis

## Troubleshooting

### Common Issues

**Permission Denied**: Run with appropriate permissions for file scanning

    sudo python flaghunter.py -d /protected/directory -r

**Timeout Errors**: Increase timeout for slow targets

    python flaghunter.py -u https://slow-site.com --timeout 30

**Too Many Requests**: Reduce thread count

    python flaghunter.py -f urls.txt -t 5

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-scanner`)
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Adding New Flag Patterns

Edit `config.json` and add your pattern:

    "flag_patterns": [
        "YOURNEW\\{[^}]+\\}",
        "CUSTOM_FORMAT_[A-Za-z0-9]+"
    ]

### Adding New Modules

Create a new module in the `modules/` directory following the existing pattern.

## Security Notice

⚠️ **Important**: This tool is designed for:
- Authorized CTF competitions
- Educational purposes
- Security research with proper authorization

**Do NOT use this tool on systems you don't own or don't have explicit permission to test.**

## License

MIT License

Copyright (c) 2025 FlagHunter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Check the examples directory for usage patterns
- Review the configuration file for customization options

---

**Happy Flag Hunting! 🚩**
