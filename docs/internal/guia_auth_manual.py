"""
Guía paso a paso para autenticar manualmente el perfil Persat
"""

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  AUTENTICACIÓN MANUAL - PERFIL PERSAT                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PASO 1: Abrir Chrome con tu cuenta de Persat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Abre Chrome NORMALMENTE (no con este script)
2. Asegúrate de estar logueado con: rsalvucci@persat.com.ar
3. Ve a: https://notebooklm.google.com/
4. Espera a que cargue completamente la aplicación

PASO 2: Abrir DevTools
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Presiona F12 para abrir las herramientas de desarrollador
2. Ve a la pestaña "Network" (Red)
3. Recarga la página (F5 o Ctrl+R)

PASO 3: Extraer cookies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. En la lista de requests, busca uno que vaya a "notebooklm.google.com"
2. Haz clic derecho sobre ese request
3. Selecciona: Copy > Copy as cURL (bash)
4. Pega el contenido en un archivo de texto temporal

PASO 4: Extraer solo las cookies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Del texto que copiaste, busca la línea que empieza con:
  -H 'cookie: ...'

Copia SOLO el contenido después de 'cookie: ' (sin las comillas)

EJEMPLO:
Si ves esto:
  -H 'cookie: SID=abc123; HSID=xyz789; ...'

Copia esto:
  SID=abc123; HSID=xyz789; ...

PASO 5: Ejecutar el script de inyección
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Guarda las cookies en un archivo: c:/01_Rodry/NotebookLM/persat_cookies.txt
2. Ejecuta: python c:/01_Rodry/NotebookLM/inject_persat_from_file.py

╔══════════════════════════════════════════════════════════════════════════════╗
║  ¿Listo? Presiona Enter cuando hayas completado los pasos 1-4...            ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

input()

print("\n✅ Perfecto! Ahora ejecuta el script de inyección:")
print("   python c:/01_Rodry/NotebookLM/inject_persat_from_file.py")
