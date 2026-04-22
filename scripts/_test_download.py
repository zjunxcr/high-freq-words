#!/usr/bin/env python3
"""Quick test: verify Friends MP3 download from tingclass"""
import urllib.request, ssl, os
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://online1.tingclass.net/lesson/shi0529/0000/28/1.mp3'
out_dir = Path(__file__).parent.parent / 'audio' / 'friends'
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / '_s01e01_test.mp3'

print(f'Downloading: {url}')
print(f'Saving to: {out_path}')

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ctx, timeout=30)
    data = resp.read()
    with open(out_path, 'wb') as f:
        f.write(data)
    size_kb = len(data) / 1024
    print(f'OK! Size: {size_kb:.1f} KB ({len(data)} bytes)')
except Exception as e:
    print(f'Error: {e}')
