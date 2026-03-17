# 🔐 Guía de Autenticación: NotebookLM MCP Multi-Perfil

Esta guía explica cómo obtener e inyectar las cookies de autenticación para cada perfil de Google que quieras usar con el MCP.

## ¿Por qué este método?

NotebookLM usa autenticación de Google, que detecta y bloquea intentos de login automatizados (Selenium, Playwright, etc.). El método más confiable es extraer las cookies directamente desde un navegador donde ya estás logueado.

**Tiempo estimado:** ~1 minuto por perfil.

---

## Paso 1: Obtener las cookies desde Chrome (Copy as cURL)

1. Abre **Chrome** con la cuenta de Google que quieres configurar.
2. Ve a **https://notebooklm.google.com/** y espera que cargue completamente.
3. Presiona **F12** para abrir DevTools.
4. Ve a la pestaña **Network** (Red).
5. Recarga la página con **F5**.
6. En la lista de requests, haz clic en cualquier request que vaya a `notebooklm.google.com`.
7. Clic derecho → **Copy** → **Copy as cURL (bash)**.

---

## Paso 2: Guardar el contenido en un archivo

Crea un archivo de texto con el nombre `<perfil>_cookies.txt` en el directorio del proyecto y pega **todo el texto copiado** (el comando cURL completo) dentro. No te preocupes por limpiar el texto, el script lo hará por ti.

**Ejemplos de nombres:**
- `personal_cookies.txt` → para tu cuenta personal
- `persat_cookies.txt` → para tu cuenta de trabajo (corporativa)

> ⚠️ **Importante:** Este archivo está en `.gitignore` y **nunca debe subirse a GitHub**.

---

## Paso 3: Ejecutar el script de inyección

# (Windows) Para cuenta personal
.venv\Scripts\python inject_profile.py --profile personal --email tu@gmail.com

# (Windows) Para cuenta de trabajo (persat)
.venv\Scripts\python inject_profile.py --profile persat --email tu@persat.com.ar

# (Linux / macOS) Para cuenta personal
.venv/bin/python inject_profile.py --profile personal --email tu@gmail.com

El script automáticamente:
1. Detecta si es un comando cURL y extrae las cookies.
2. Verifica que sean válidas conectándose a NotebookLM.
3. Extrae el CSRF token y Session ID.
4. Guarda todo en `~/.notebooklm-mcp-cli/profiles/<perfil>/`.

---

## Paso 4: Recargar la autenticación en el MCP

Después de inyectar las cookies, recarga el MCP desde tu cliente AI:

```python
# En Antigravity / Claude / cualquier cliente MCP:
mcp_notebooklm_personal_refresh_auth()
mcp_notebooklm_persat_refresh_auth()
```

---

## Verificar el estado de los perfiles

```bash
# Verificar todos los perfiles configurados (Windows)
.venv\Scripts\python verify_profile.py

# Verificar todos los perfiles configurados (Linux / macOS)
.venv/bin/python verify_profile.py
```

---

## ¿Cuándo necesito repetir este proceso?

Las cookies de Google expiran periódicamente (generalmente cada 1-4 semanas). Sabrás que expiraron cuando el MCP devuelva un error de `Authentication expired` o similar. Cuando eso ocurra, simplemente repite desde el **Paso 1**.

---

## Solución de problemas

| Síntoma | Causa | Solución |
|:---|:---|:---|
| `Authentication expired` | Cookies expiradas | Repetir desde Paso 1 |
| `ModuleNotFoundError: distutils` | Python 3.12+ sin setuptools | `pip install setuptools` |
| `Redirected to login` | Cookies viejas/inválidas | Repetir desde Paso 1 |
| CSRF token no encontrado | Error en el parseo | Asegúrate de haber copiado el cURL (bash) correctamente |
| `httpx` no instalado | Dependencia faltante | `.venv/bin/pip install -r requirements.txt` |
