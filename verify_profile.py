"""
verify_profile.py - Verificar el estado de autenticación de un perfil NotebookLM MCP

Uso:
    python verify_profile.py [--profile <nombre_perfil>]

Ejemplos:
    python verify_profile.py                    # verifica todos los perfiles
    python verify_profile.py --profile personal # verifica solo 'personal'
    python verify_profile.py --profile work     # verifica solo 'work'
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import httpx
except ImportError:
    print("❌ Error: 'httpx' no está instalado.")
    print("   Ejecuta: pip install httpx")
    sys.exit(1)


def check_profile(profile_name: str) -> bool:
    """
    Verifica si las cookies de un perfil son válidas.
    Retorna True si la sesión está activa, False en caso contrario.
    """
    profile_dir = Path.home() / ".notebooklm-mcp-cli" / "profiles" / profile_name
    cookies_file = profile_dir / "cookies.json"
    metadata_file = profile_dir / "metadata.json"

    print(f"\n🔍 Perfil: '{profile_name}'")
    print(f"   Directorio: {profile_dir}")

    if not cookies_file.exists():
        print("   ❌ No se encontraron cookies (perfil no configurado)")
        return False

    # Leer metadata si existe
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
            email = metadata.get("email", "desconocido")
            last_validated = metadata.get("last_validated", "nunca")
            print(f"   📧 Email: {email}")
            print(f"   🕐 Última validación: {last_validated}")
        except Exception:
            pass

    # Leer cookies
    try:
        cookies_list = json.loads(cookies_file.read_text(encoding="utf-8"))
        cookies_dict = {c["name"]: c["value"] for c in cookies_list}
        print(f"   🍪 Cookies almacenadas: {len(cookies_list)}")
    except Exception as e:
        print(f"   ❌ Error leyendo cookies: {e}")
        return False

    # Verificar conectividad
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/147.0.0.0 Safari/537.36"
        )
    }

    try:
        with httpx.Client(
            cookies=cookies_dict, headers=headers, follow_redirects=True
        ) as client:
            r = client.get("https://notebooklm.google.com/", timeout=20.0)

        if "accounts.google.com" in str(r.url):
            print("   ❌ Estado: EXPIRADO (redirige a login)")
            print("   💡 Solución: ejecuta inject_profile.py con cookies frescas")
            return False

        has_csrf = "SNlM0e" in r.text
        print(f"   ✅ Estado: ACTIVO (CSRF token: {'encontrado' if has_csrf else 'no encontrado'})")
        return True

    except httpx.ConnectError:
        print("   ⚠️  No se pudo conectar (verifica tu conexión a internet)")
        return False
    except Exception as e:
        print(f"   ❌ Error de verificación: {e}")
        return False


def list_profiles() -> list[str]:
    """Lista todos los perfiles configurados."""
    profiles_dir = Path.home() / ".notebooklm-mcp-cli" / "profiles"
    if not profiles_dir.exists():
        return []
    return [p.name for p in profiles_dir.iterdir() if p.is_dir()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verifica el estado de autenticación de perfiles NotebookLM MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python verify_profile.py                    # verifica todos los perfiles
  python verify_profile.py --profile personal
  python verify_profile.py --profile work
        """,
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Nombre del perfil a verificar (por defecto: todos)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  NotebookLM MCP - Verificador de Autenticación")
    print("=" * 60)

    if args.profile:
        profiles = [args.profile]
    else:
        profiles = list_profiles()
        if not profiles:
            print("\n⚠️  No se encontraron perfiles configurados.")
            print(f"   Directorio esperado: {Path.home() / '.notebooklm-mcp-cli' / 'profiles'}")
            print("\n💡 Para configurar un perfil, ejecuta:")
            print("   python inject_profile.py --profile <nombre> --email <tu@email.com>")
            sys.exit(0)
        print(f"\n📋 Perfiles encontrados: {', '.join(profiles)}")

    results = {}
    for profile in profiles:
        results[profile] = check_profile(profile)

    print("\n" + "=" * 60)
    print("  Resumen")
    print("=" * 60)
    all_ok = True
    for profile, ok in results.items():
        status = "✅ ACTIVO" if ok else "❌ INACTIVO"
        print(f"  {profile:20s} → {status}")
        if not ok:
            all_ok = False

    if not all_ok:
        print()
        print("💡 Para reactivar un perfil:")
        print("   python inject_profile.py --profile <nombre> --email <tu@email.com>")
        print("   Ver docs/AUTHENTICATION.md para instrucciones completas.")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
