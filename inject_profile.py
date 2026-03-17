"""
inject_profile.py - Inyectar cookies de autenticación para un perfil NotebookLM MCP

Uso:
    python inject_profile.py --profile <nombre_perfil> --email <tu@email.com>

Ejemplo:
    python inject_profile.py --profile personal --email tu@gmail.com
    python inject_profile.py --profile work --email tu@empresa.com

El archivo de cookies debe estar en: <nombre_perfil>_cookies.txt
(en el mismo directorio que este script, o especificado con --cookies-file)

Ver AUTHENTICATION.md para instrucciones detalladas de cómo obtener las cookies.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import httpx
except ImportError:
    print("❌ Error: 'httpx' no está instalado.")
    print("   Ejecuta: pip install httpx")
    sys.exit(1)


def parse_cookie_header(cookie_string: str) -> list[dict]:
    """Convierte el header de cookies en formato lista de diccionarios."""
    cookies = []
    for item in cookie_string.split("; "):
        if "=" in item:
            name, value = item.split("=", 1)
            name = name.strip()
            cookie = {
                "name": name,
                "value": value,
                "domain": ".google.com",
                "path": "/",
                "secure": name.startswith("__Secure-") or name.startswith("__Host-"),
                "httpOnly": False,
            }
            cookies.append(cookie)
    return cookies


def get_tokens_from_cookies(cookies_list: list[dict]) -> tuple[str, str]:
    """
    Verifica las cookies conectándose a NotebookLM y extrae CSRF token y Session ID.
    Retorna (csrf_token, session_id). Ambos pueden ser string vacío si no se encuentran.
    """
    cookies_dict = {c["name"]: c["value"] for c in cookies_list}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    print("🔍 Verificando cookies y obteniendo tokens...")
    try:
        with httpx.Client(
            cookies=cookies_dict, headers=headers, follow_redirects=True
        ) as client:
            r = client.get("https://notebooklm.google.com/", timeout=30.0)

            print(f"   Status: {r.status_code}")
            print(f"   URL final: {r.url}")

            if "accounts.google.com" in str(r.url):
                print("   ❌ Redirigido a login — las cookies son inválidas o expiraron")
                return "", ""

            page_source = r.text

            # Extraer CSRF token
            csrf_token = ""
            match = re.search(r'"SNlM0e":"([^"]+)"', page_source)
            if match:
                csrf_token = match.group(1)
                print(f"   ✅ CSRF token encontrado: {csrf_token[:20]}...")
            else:
                print("   ⚠️  CSRF token NO encontrado en la página")

            # Extraer Session ID
            session_id = ""
            patterns = [
                r'"FdrFJe":"(\d+)"',
                r'f\.sid[\s:=]+[\'"]?(\d+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, page_source)
                if match:
                    session_id = match.group(1)
                    print(f"   ✅ Session ID encontrado: {session_id}")
                    break

            if not session_id:
                print("   ⚠️  Session ID NO encontrado (puede funcionar sin él)")

            return csrf_token, session_id

    except httpx.ConnectError:
        print("   ❌ Error de conexión — verifica tu conexión a internet")
        return "", ""
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return "", ""


def save_profile(
    profile_name: str,
    email: str,
    cookies_list: list[dict],
    csrf_token: str,
    session_id: str,
) -> None:
    """Guarda las cookies y tokens en el directorio del perfil MCP."""
    profile_dir = (
        Path.home() / ".notebooklm-mcp-cli" / "profiles" / profile_name
    )
    profile_dir.mkdir(parents=True, exist_ok=True)

    # Guardar cookies
    cookies_file = profile_dir / "cookies.json"
    with open(cookies_file, "w") as f:
        json.dump(cookies_list, f, indent=2)
    print(f"\n✅ Cookies guardadas ({len(cookies_list)} cookies)")
    print(f"   → {cookies_file}")

    # Guardar metadata
    metadata = {
        "csrf_token": csrf_token or "",
        "session_id": session_id or "",
        "email": email,
        "last_validated": datetime.now().isoformat(),
    }
    metadata_file = profile_dir / "metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ Metadata guardada")
    print(f"   → {metadata_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inyecta cookies de autenticación en un perfil NotebookLM MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python inject_profile.py --profile personal --email tu@gmail.com
  python inject_profile.py --profile work --email tu@empresa.com
  python inject_profile.py --profile work --email tu@empresa.com --cookies-file mis_cookies.txt

Ver docs/AUTHENTICATION.md para instrucciones completas.
        """,
    )
    parser.add_argument(
        "--profile",
        required=True,
        help="Nombre del perfil (ej: personal, work, empresa)",
    )
    parser.add_argument(
        "--email",
        required=True,
        help="Email de la cuenta de Google asociada al perfil",
    )
    parser.add_argument(
        "--cookies-file",
        default=None,
        help="Ruta al archivo de cookies (por defecto: <profile>_cookies.txt en el directorio actual)",
    )
    args = parser.parse_args()

    # Determinar archivo de cookies
    if args.cookies_file:
        cookies_file = Path(args.cookies_file)
    else:
        cookies_file = Path(f"{args.profile}_cookies.txt")

    print(f"\n🔧 Configurando perfil: '{args.profile}' ({args.email})")
    print(f"📂 Leyendo cookies desde: {cookies_file.resolve()}\n")

    if not cookies_file.exists():
        print(f"❌ Error: No se encontró el archivo '{cookies_file}'")
        print()
        print("📝 Pasos para obtener las cookies:")
        print(f"   1. Abre Chrome con tu cuenta de Google ({args.email})")
        print("   2. Ve a https://notebooklm.google.com/")
        print("   3. Abre DevTools (F12) → pestaña Network → recarga (F5)")
        print("   4. Clic derecho en cualquier request a notebooklm.google.com")
        print("   5. Selecciona: Copy → Copy as cURL (bash)")
        print("   6. Del texto copiado, extrae el valor del header 'cookie:'")
        print(f"   7. Guarda ese texto en: {cookies_file}")
        print()
        print("Ver docs/AUTHENTICATION.md para instrucciones con capturas.")
        sys.exit(1)

    raw_cookies = cookies_file.read_text(encoding="utf-8").strip()

    if not raw_cookies:
        print(f"❌ Error: El archivo '{cookies_file}' está vacío")
        sys.exit(1)

    # Autodetectar y extraer cookies si es un comando cURL
    if "curl " in raw_cookies.lower() and ("-H " in raw_cookies or "-b " in raw_cookies):
        # Intentar extraer de headers -H 'cookie: ...'
        cookie_match = re.search(r"-H\s+['\"]cookie:\s*([^'\"]+)['\"]", raw_cookies, re.IGNORECASE)
        if not cookie_match:
            # Reintentar con -b '...' (formato abreviado de cookies en curl)
            cookie_match = re.search(r"-b\s+['\"]([^'\"]+)['\"]", raw_cookies, re.IGNORECASE)
        
        if cookie_match:
            raw_cookies = cookie_match.group(1)
            print("   ✨ Detectado comando cURL — Extrayendo string de cookies automáticamente")

    print(f"   Longitud del string: {len(raw_cookies)} caracteres")

    # Parsear cookies
    cookies_list = parse_cookie_header(raw_cookies)
    print(f"   Cookies parseadas: {len(cookies_list)}")

    # Verificar y obtener tokens
    csrf_token, session_id = get_tokens_from_cookies(cookies_list)

    if not csrf_token:
        print()
        print("❌ CRÍTICO: No se pudo obtener el CSRF token.")
        print("   Las cookies pueden ser inválidas o haber expirado.")
        print("   Obtén cookies frescas y vuelve a intentar.")
        sys.exit(1)

    # Guardar perfil
    save_profile(args.profile, args.email, cookies_list, csrf_token, session_id)

    print(f"\n🎉 ¡Perfil '{args.profile}' configurado exitosamente!")
    print()
    print("📋 Próximos pasos:")
    print("   1. Recarga la autenticación en tu cliente MCP:")
    print(f"      mcp_notebooklm_{args.profile}_refresh_auth()")
    print("   2. Verifica el acceso:")
    print(f"      mcp_notebooklm_{args.profile}_notebook_list(max_results=3)")


if __name__ == "__main__":
    main()
