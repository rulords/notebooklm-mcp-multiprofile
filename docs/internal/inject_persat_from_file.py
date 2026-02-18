"""
Script para inyectar cookies de Persat desde un archivo
Lee las cookies desde persat_cookies.txt y las guarda en el perfil
"""
import json
import re
from pathlib import Path
from datetime import datetime
import httpx

def parse_cookie_header(cookie_string):
    """Convierte el header de cookies en formato lista de diccionarios"""
    cookies = []
    for item in cookie_string.split('; '):
        if '=' in item:
            name, value = item.split('=', 1)
            cookie = {
                "name": name,
                "value": value,
                "domain": ".google.com",
                "path": "/",
                "secure": name.startswith("__Secure-") or name.startswith("__Host-"),
                "httpOnly": False
            }
            cookies.append(cookie)
    return cookies

def get_tokens_from_cookies(cookies_list):
    """Obtiene CSRF y Session ID usando las cookies"""
    cookies_dict = {c['name']: c['value'] for c in cookies_list}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    print("🔍 Verificando cookies y obteniendo tokens...")
    try:
        with httpx.Client(cookies=cookies_dict, headers=headers, follow_redirects=True) as client:
            r = client.get('https://notebooklm.google.com/', timeout=30.0)
            
            print(f"   Status: {r.status_code}")
            print(f"   Final URL: {r.url}")
            
            if "accounts.google.com" in str(r.url):
                print("   ❌ Redirigido a login - Las cookies son inválidas o expiraron")
                return None, None
            
            page_source = r.text
            
            # Extraer CSRF
            csrf_token = ""
            match = re.search(r'"SNlM0e":"([^"]+)"', page_source)
            if match:
                csrf_token = match.group(1)
                print(f"   ✅ CSRF token: {csrf_token[:20]}...")
            else:
                print(f"   ❌ CSRF token NO encontrado")
            
            # Extraer Session ID
            session_id = ""
            patterns = [
                r'"FdrFJe":"(\d+)"',
                r'f\.sid[\s:=]+[\'\"]?(\d+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, page_source)
                if match:
                    session_id = match.group(1)
                    print(f"   ✅ Session ID: {session_id}")
                    break
            
            if not session_id:
                print(f"   ⚠️ Session ID NO encontrado (puede funcionar sin él)")
            
            return csrf_token, session_id
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None, None

def save_persat_profile(cookies_list, csrf_token, session_id):
    """Guarda las cookies y tokens en el perfil persat"""
    profile_dir = Path.home() / ".notebooklm-mcp-cli" / "profiles" / "persat"
    profile_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar cookies
    cookies_file = profile_dir / "cookies.json"
    with open(cookies_file, 'w') as f:
        json.dump(cookies_list, f, indent=2)
    
    print(f"\n✅ Cookies guardadas: {len(cookies_list)} cookies")
    print(f"   Archivo: {cookies_file}")
    
    # Guardar metadata
    metadata = {
        "csrf_token": csrf_token or "",
        "session_id": session_id or "",
        "email": "rsalvucci@persat.com.ar",
        "last_validated": datetime.now().isoformat()
    }
    
    metadata_file = profile_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Metadata guardada")
    print(f"   Archivo: {metadata_file}")

def main():
    cookies_file = Path("c:/01_Rodry/NotebookLM/persat_cookies.txt")
    
    if not cookies_file.exists():
        print(f"❌ Error: No se encontró el archivo {cookies_file}")
        print(f"\n📝 Instrucciones:")
        print(f"   1. Copia las cookies desde Chrome DevTools")
        print(f"   2. Guárdalas en: {cookies_file}")
        print(f"   3. Ejecuta este script nuevamente")
        return
    
    print(f"📂 Leyendo cookies desde: {cookies_file}")
    raw_cookies = cookies_file.read_text().strip()
    
    if not raw_cookies:
        print(f"❌ Error: El archivo está vacío")
        return
    
    print(f"   Longitud: {len(raw_cookies)} caracteres")
    
    # Parsear cookies
    cookies_list = parse_cookie_header(raw_cookies)
    print(f"   Cookies parseadas: {len(cookies_list)}")
    
    # Verificar y obtener tokens
    csrf_token, session_id = get_tokens_from_cookies(cookies_list)
    
    if not csrf_token:
        print(f"\n❌ CRÍTICO: No se pudo obtener el CSRF token")
        print(f"   Las cookies pueden ser inválidas o haber expirado")
        print(f"   Por favor, extrae cookies frescas y vuelve a intentar")
        return
    
    # Guardar perfil
    save_persat_profile(cookies_list, csrf_token, session_id)
    
    print(f"\n🎉 ¡Perfil 'persat' configurado exitosamente!")
    print(f"\n📋 Próximos pasos:")
    print(f"   1. Reinicia el entorno de Antigravity (reload window)")
    print(f"   2. Prueba el MCP con: mcp_notebooklm_persat_notebook_list")

if __name__ == "__main__":
    main()
