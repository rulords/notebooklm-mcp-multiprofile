# 🤖 ÍNDICE MAESTRO - ESTADO Y MANTENIMIENTO NOTEBOOKLM MCP

## 🎯 OBJETIVO FINAL (CRÍTICO)

El propósito de esta configuración es **habilitar los motores MCP de NotebookLM** para que **Antigravity** pueda interactuar con los cuadernos del usuario en dos contextos específicos:

1.  **Perfil Personal (`notebooklm_personal`):**
    *   Acceso a cuadernos personales.
    *   Uso: `mcp_notebooklm_personal_*`

2.  **Perfil Work/Corporativo (`notebooklm_work`):**
    *   Acceso a cuadernos de trabajo.
    *   Uso: `mcp_notebooklm_work_*`

**ESTADO ACTUAL (2026-02-10):** ✅ OPERATIVO
- Ambos perfiles están configurados y validados.
- Listos para ser consumidos por cualquier agente de Antigravity.

---

**Estado Actual (2026-02-10):** ✅ OPERATIVO
- **Perfil Personal:** Funciona (Sesión persistente).
- **Perfil Persat:** Funciona (Cookies inyectadas manualmente).

---

## 🚨 PROTOCOLO DE RECUPERACIÓN (SI FALLA PERSAT)

Si el MCP de Persat dice: `RPC Error 16: Authentication expired` o `No authentication found`.

### ❌ QUÉ NO HACER
- **NO** intentar usar Selenium, `undetected-chromedriver` o scripts de auto-login.
- **NO** usar `setup_persat_profile.py` (La política de seguridad de Chrome bloquea la extracción automática).

### ✅ SOLUCIÓN DEFINITIVA (MÉTODO DE ARCHIVO)

**Tiempo estimado:** 2 minutos.

1.  **Obtener Cookies Frescas:**
    *   Abrir Chrome manualmente con el perfil de trabajo.
    *   Ir a `https://notebooklm.google.com/`.
    *   `F12` -> `Network` -> Recargar (F5).
    *   Clic derecho en request a `notebooklm.google.com` -> `Copy` -> `Copy as cURL`.
    *   Extraer el contenido del header `Cookie:` (todo el string largo).

2.  **Crear Archivo de Paso:**
    *   Crear archivo: `c:/01_Rodry/NotebookLM/persat_cookies.txt`
    *   Pegar las cookies dentro (texto plano).

3.  **Ejecutar Inyección:**
    ```bash
    python inject_profile.py --profile work --email tu@empresa.com
    ```
    *Este script valida, extrae tokens (CSRF/SessionID) y guarda el perfil.*

4.  **Refrescar MCP:**
    *   Desde la IA o terminal:
    ```python
    mcp_notebooklm_persat_refresh_auth()
    ```

---

## 🔧 DIAGNÓSTICO RÁPIDO

| Síntoma | Causa Probable | Solución |
| :--- | :--- | :--- |
| `RPC Error 16` | Cookies expiradas | Ejecutar **Solución Definitiva** (arriba). |
| `ModuleNotFoundError: distutils` | Entorno incorrecto | Usar Python del venv: `.venv/Scripts/python.exe`. |
| `Redirected to login` en tests | Cookies viejas | Repetir **Solución Definitiva** con cookies nuevas. |

---

## 📂 UBICACIÓN DE ARCHIVOS CLAVE

*   **Script de Inyección:** `inject_profile.py`
*   **Config MCP:** `~/.gemini/antigravity/mcp_config.json`
*   **Perfiles Guardados:** `~/.notebooklm-mcp-cli/profiles/`

---

## 🧪 COMANDOS DE VERIFICACIÓN

```python
# Verificar Personal (debe dar success)
mcp_notebooklm_personal_notebook_list(max_results=1)

# Verificar Persat (debe dar success - 50+ notebooks)
mcp_notebooklm_persat_notebook_list(max_results=1)
```
