# 🔐 Guía de Autenticación: NotebookLM MCP Multi-Perfil

Esta guía explica cómo obtener e inyectar las cookies de autenticación para cada perfil de Google que quieras usar con el MCP.

## ¿Por qué este método?

NotebookLM usa autenticación de Google, que detecta y bloquea intentos de login automatizados (Selenium, Playwright, etc.). El método más confiable es extraer las cookies directamente desde un navegador donde ya estás logueado.

**Tiempo estimado:** ~2 minutos por perfil.

---

## Paso 1: Obtener las cookies desde Chrome

1. Abre **Chrome** con la cuenta de Google que quieres configurar
2. Ve a **https://notebooklm.google.com/** y espera que cargue completamente
3. Presiona **F12** para abrir DevTools
4. Ve a la pestaña **Network** (Red)
5. Recarga la página con **F5**
6. En la lista de requests, haz clic en cualquier request que vaya a `notebooklm.google.com`
7. Clic derecho → **Copy** → **Copy as cURL (bash)**

Esto copia un comando `curl` completo al portapapeles.

---

## Paso 2: Extraer solo las cookies

Del texto copiado, busca la línea que empieza con:
```
-H 'cookie: ...'
```

Copia **solo el contenido** después de `cookie: ` (sin las comillas simples).

**Ejemplo:**
```
# Del cURL copiado:
-H 'cookie: SID=abc123; HSID=xyz789; SSID=def456; ...'

# Extraes solo esto:
SID=abc123; HSID=xyz789; SSID=def456; ...
```

---

## Paso 3: Guardar las cookies en un archivo

Crea un archivo de texto con el nombre `<perfil>_cookies.txt` en el directorio del proyecto y pega las cookies dentro.

**Ejemplos de nombres:**
- `personal_cookies.txt` → para tu cuenta personal
- `work_cookies.txt` → para tu cuenta de trabajo

> ⚠️ **Importante:** Este archivo está en `.gitignore` y **nunca debe subirse a GitHub**.

---

## Paso 4: Ejecutar el script de inyección

```bash
# Para cuenta personal
python inject_profile.py --profile personal --email tu@gmail.com

# Para cuenta de trabajo
python inject_profile.py --profile work --email tu@empresa.com

# Especificando el archivo de cookies manualmente
python inject_profile.py --profile work --email tu@empresa.com --cookies-file mis_cookies.txt
```

El script:
1. Lee y parsea las cookies
2. Verifica que sean válidas conectándose a NotebookLM
3. Extrae el CSRF token y Session ID
4. Guarda todo en `~/.notebooklm-mcp-cli/profiles/<perfil>/`

---

## Paso 5: Recargar la autenticación en el MCP

Después de inyectar las cookies, recarga el MCP desde tu cliente AI:

```python
# En Antigravity / Claude / cualquier cliente MCP:
mcp_notebooklm_personal_refresh_auth()
mcp_notebooklm_work_refresh_auth()
```

---

## Verificar el estado de los perfiles

```bash
# Verificar todos los perfiles configurados
python verify_profile.py

# Verificar un perfil específico
python verify_profile.py --profile personal
```

---

## ¿Cuándo necesito repetir este proceso?

Las cookies de Google expiran periódicamente (generalmente cada 1-4 semanas). Sabrás que expiraron cuando el MCP devuelva:

```
RPC Error 16: Authentication expired
No authentication found
Redirected to login
```

Cuando eso ocurra, repite desde el **Paso 1**.

---

## Estructura de archivos generados

Los perfiles se guardan **fuera del repositorio**, en el directorio home del usuario:

```
~/.notebooklm-mcp-cli/
└── profiles/
    ├── personal/
    │   ├── cookies.json      # Cookies de sesión (NO subir a GitHub)
    │   └── metadata.json     # CSRF token, Session ID, email
    └── work/
        ├── cookies.json
        └── metadata.json
```

---

## Solución de problemas

| Síntoma | Causa | Solución |
|:---|:---|:---|
| `RPC Error 16` | Cookies expiradas | Repetir desde Paso 1 |
| `ModuleNotFoundError: distutils` | Python 3.12+ sin setuptools | `pip install setuptools` |
| `Redirected to login` en verify | Cookies viejas | Repetir desde Paso 1 |
| CSRF token no encontrado | Cookies parciales | Asegúrate de copiar el header `cookie:` completo |
| `httpx` no instalado | Dependencia faltante | `pip install -r requirements.txt` |

---

## ¿Por qué no usar `nlm login`?

El comando oficial `nlm login` abre Chrome con automatización (CDP), que Google detecta y bloquea especialmente en cuentas con 2FA o múltiples cuentas. El método manual con DevTools es más confiable porque usa un navegador real donde ya estás autenticado.
