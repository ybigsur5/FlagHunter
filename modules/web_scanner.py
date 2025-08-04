"""
Web scanning module for FlagHunter
"""

import requests
from urllib.parse import urljoin, urlparse
import re

class WebScanner:
    def __init__(self, session):
        self.session = session
        
    def scan_robots_txt(self, base_url):
        """Scan robots.txt for flags"""
        robots_url = urljoin(base_url, '/robots.txt')
        try:
            response = self.session.get(robots_url)
            return response.text
        except:
            return ""
    
    def scan_common_files(self, base_url):
        """Scan common files for flags"""
        common_files = [
            'robots.txt', 'sitemap.xml', '.htaccess', 'config.php',
            'readme.txt', 'changelog.txt', 'version.txt'
        ]
        
        results = {}
        for file in common_files:
            url = urljoin(base_url, file)
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    results[url] = response.text
            except:
                continue
                
        return results
    
    def extract_links(self, html, base_url):
        """Extract links from HTML"""
        link_pattern = r'href=[\'"]?([^\'" >]+)'
        links = re.findall(link_pattern, html, re.IGNORECASE)
        
        full_links = []
        for link in links:
            full_url = urljoin(base_url, link)
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                full_links.append(full_url)
                
        return full_links
