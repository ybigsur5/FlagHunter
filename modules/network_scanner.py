"""
Network scanning module for FlagHunter
"""

import socket
import subprocess
import platform

class NetworkScanner:
    def __init__(self):
        self.os_type = platform.system().lower()
        
    def ping_host(self, host):
        """Ping a host to check if it's alive"""
        param = '-n' if self.os_type == 'windows' else '-c'
        command = ['ping', param, '1', host]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def scan_port(self, host, port, timeout=3):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def banner_grab(self, host, port):
        """Grab banner from service"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            return banner
        except:
            return ""v
