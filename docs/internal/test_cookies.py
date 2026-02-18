import httpx
import json
from pathlib import Path

p = Path.home() / '.notebooklm-mcp-cli/profiles/persat/cookies.json'
cookies = {c['name']: c['value'] for c in json.loads(p.read_text())}
r = httpx.get('https://notebooklm.google.com/', cookies=cookies, headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
print(f'URL: {r.url}')
print(f'Status: {r.status_code}')
print(f'Has SNlM0e: {"SNlM0e" in r.text}')
print(f'Redirected to login: {"accounts.google.com" in str(r.url)}')
