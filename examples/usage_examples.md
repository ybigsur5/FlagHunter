# FlagHunter Usage Examples

## Basic Web Scanning

```bash
# Scan a single website
python flaghunter.py -u https://ctf.example.com

# Scan with verbose output
python flaghunter.py -u https://ctf.example.com -v

# Scan multiple URLs from file
python flaghunter.py -f urls.txt

# Save results to file
python flaghunter.py -u https://ctf.example.com -o results.txt
