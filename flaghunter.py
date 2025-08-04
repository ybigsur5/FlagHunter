#!/usr/bin/env python3
"""
FlagHunter - CTF Flag Discovery Tool
Author: Aviraaa
Description: Automated flag hunting tool for CTF competitions
"""

import re
import requests
import argparse
import threading
import json
import os
import sys
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class FlagHunter:
    def __init__(self, config_file='config.json'):
        self.session = requests.Session()
        self.found_flags = []
        self.scanned_urls = set()
        self.load_config(config_file)
        self.setup_session()
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = self.default_config()
            
        self.flag_patterns = [re.compile(pattern, re.IGNORECASE) 
                             for pattern in self.config['flag_patterns']]
    
    def default_config(self):
        """Default configuration if config file not found"""
        return {
            "flag_patterns": [
                r"CTF\{[^}]+\}",
                r"FLAG\{[^}]+\}",
                r"flag\{[^}]+\}",
                r"PICO\{[^}]+\}",
                r"HTB\{[^}]+\}",
                r"[A-Za-z0-9_]+\{[A-Za-z0-9_!@#$%^&*()+=\-\[\]{}|;:,.<>?/~`]+\}"
            ],
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            ],
            "file_extensions": [".txt", ".html", ".js", ".php", ".py", ".java", ".c", ".cpp", ".log"],
            "timeout": 10,
            "max_threads": 10
        }
    
    def setup_session(self):
        """Setup requests session with headers"""
        self.session.headers.update({
            'User-Agent': self.config['user_agents'][0],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.session.timeout = self.config['timeout']
    
    def print_banner(self):
        """Print tool banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════╗
║              FlagHunter               ║
║        CTF Flag Discovery Tool        ║
║              Version 1.0              ║
╚═══════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    def search_flags(self, text, source=""):
        """Search for flags in given text"""
        flags = []
        for pattern in self.flag_patterns:
            matches = pattern.findall(text)
            for match in matches:
                if match not in [f['flag'] for f in self.found_flags]:
                    flag_info = {
                        'flag': match,
                        'source': source,
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    flags.append(flag_info)
                    self.found_flags.append(flag_info)
        return flags
    
    def scan_url(self, url, verbose=False):
        """Scan a single URL for flags"""
        if url in self.scanned_urls:
            return []
            
        self.scanned_urls.add(url)
        flags = []
        
        try:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.END} Scanning: {url}")
                
            response = self.session.get(url)
            
            # Search in response text
            text_flags = self.search_flags(response.text, f"URL: {url} (body)")
            flags.extend(text_flags)
            
            # Search in headers
            headers_text = str(response.headers)
            header_flags = self.search_flags(headers_text, f"URL: {url} (headers)")
            flags.extend(header_flags)
            
            # Search in cookies
            cookies_text = str(response.cookies)
            cookie_flags = self.search_flags(cookies_text, f"URL: {url} (cookies)")
            flags.extend(cookie_flags)
            
            if flags and verbose:
                for flag in flags:
                    print(f"{Colors.GREEN}[FOUND]{Colors.END} {flag['flag']} in {flag['source']}")
                    
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"{Colors.RED}[ERROR]{Colors.END} Failed to scan {url}: {str(e)}")
                
        return flags
    
    def scan_file(self, filepath, verbose=False):
        """Scan a single file for flags"""
        flags = []
        try:
            if verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.END} Scanning file: {filepath}")
                
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                file_flags = self.search_flags(content, f"File: {filepath}")
                flags.extend(file_flags)
                
                if file_flags and verbose:
                    for flag in file_flags:
                        print(f"{Colors.GREEN}[FOUND]{Colors.END} {flag['flag']} in {flag['source']}")
                        
        except Exception as e:
            if verbose:
                print(f"{Colors.RED}[ERROR]{Colors.END} Failed to scan {filepath}: {str(e)}")
                
        return flags
    
    def scan_directory(self, directory, recursive=False, verbose=False):
        """Scan directory for flags"""
        flags = []
        path = Path(directory)
        
        if not path.exists():
            print(f"{Colors.RED}[ERROR]{Colors.END} Directory not found: {directory}")
            return flags
            
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file():
                if any(str(file_path).endswith(ext) for ext in self.config['file_extensions']):
                    file_flags = self.scan_file(file_path, verbose)
                    flags.extend(file_flags)
                    
        return flags
    
    def scan_urls_from_file(self, filename, threads=10, verbose=False):
        """Scan multiple URLs from file"""
        flags = []
        
        try:
            with open(filename, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
                
            with ThreadPoolExecutor(max_workers=threads) as executor:
                future_to_url = {executor.submit(self.scan_url, url, verbose): url 
                               for url in urls}
                
                for future in as_completed(future_to_url):
                    url_flags = future.result()
                    flags.extend(url_flags)
                    
        except FileNotFoundError:
            print(f"{Colors.RED}[ERROR]{Colors.END} File not found: {filename}")
            
        return flags
    
    def add_custom_pattern(self, pattern):
        """Add custom flag pattern"""
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            self.flag_patterns.append(compiled_pattern)
            print(f"{Colors.GREEN}[INFO]{Colors.END} Added custom pattern: {pattern}")
        except re.error as e:
            print(f"{Colors.RED}[ERROR]{Colors.END} Invalid regex pattern: {e}")
    
    def save_results(self, output_file):
        """Save results to file"""
        try:
            with open(output_file, 'w') as f:
                f.write("FlagHunter Results\n")
                f.write("==================\n\n")
                
                for flag_info in self.found_flags:
                    f.write(f"Flag: {flag_info['flag']}\n")
                    f.write(f"Source: {flag_info['source']}\n")
                    f.write(f"Timestamp: {flag_info['timestamp']}\n")
                    f.write("-" * 50 + "\n")
                    
            print(f"{Colors.GREEN}[INFO]{Colors.END} Results saved to: {output_file}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.END} Failed to save results: {e}")
    
    def print_summary(self):
        """Print scan summary"""
        print(f"\n{Colors.BOLD}Scan Summary:{Colors.END}")
        print(f"Total flags found: {Colors.GREEN}{len(self.found_flags)}{Colors.END}")
        
        if self.found_flags:
            print(f"\n{Colors.BOLD}Found Flags:{Colors.END}")
            for i, flag_info in enumerate(self.found_flags, 1):
                print(f"{Colors.YELLOW}{i}.{Colors.END} {Colors.GREEN}{flag_info['flag']}{Colors.END}")
                print(f"   Source: {flag_info['source']}")
                print(f"   Time: {flag_info['timestamp']}\n")

def main():
    parser = argparse.ArgumentParser(description="FlagHunter - CTF Flag Discovery Tool")
    
    # Target options
    parser.add_argument('-u', '--url', help='Single URL to scan')
    parser.add_argument('-f', '--file', help='File containing URLs to scan')
    parser.add_argument('-d', '--directory', help='Directory to scan')
    parser.add_argument('--single-file', help='Single file to scan')
    
    # Scanning options
    parser.add_argument('-p', '--pattern', help='Custom flag pattern (regex)')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursive directory scan')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output file for results')
    
    # Network options
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout')
    parser.add_argument('--user-agent', help='Custom user agent')
    
    args = parser.parse_args()
    
    if not any([args.url, args.file, args.directory, args.single_file]):
        parser.print_help()
        sys.exit(1)
    
    # Initialize FlagHunter
    hunter = FlagHunter()
    hunter.print_banner()
    
    # Add custom pattern if provided
    if args.pattern:
        hunter.add_custom_pattern(args.pattern)
    
    # Update timeout if provided
    if args.timeout:
        hunter.config['timeout'] = args.timeout
        hunter.setup_session()
    
    # Update user agent if provided
    if args.user_agent:
        hunter.session.headers['User-Agent'] = args.user_agent
    
    # Start scanning based on input type
    if args.url:
        hunter.scan_url(args.url, args.verbose)
    elif args.file:
        hunter.scan_urls_from_file(args.file, args.threads, args.verbose)
    elif args.directory:
        hunter.scan_directory(args.directory, args.recursive, args.verbose)
    elif args.single_file:
        hunter.scan_file(args.single_file, args.verbose)
    
    # Print results
    hunter.print_summary()
    
    # Save results if output file specified
    if args.output:
        hunter.save_results(args.output)

if __name__ == "__main__":
    main()
