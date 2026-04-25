# ⚙️ Guía de Configuración: MCP en tu cliente AI

Esta guía explica cómo registrar los servidores MCP de NotebookLM en tu cliente de IA (Antigravity, Claude Desktop, Cline, etc.).

---

## Prerrequisitos

1. Haber completado la [instalación](../README.md#instalación)
2. Haber configurado al menos un perfil (ver [AUTHENTICATION.md](AUTHENTICATION.md))

---

## Estructura de la configuración

Cada perfil de Google se registra como un **servidor MCP independiente**. Esto permite que tu IA acceda a múltiples cuentas simultáneamente con herramientas separadas.

```
notebooklm_personal → herramientas: mcp_notebooklm_personal_*
notebooklm_work     → herramientas: mcp_notebooklm_work_*
```

---

## Archivo de configuración

Copia `mcp_config.example.json` como referencia y adapta las rutas a tu sistema.

### Windows

```json
{
  "mcpServers": {
    "notebooklm_personal": {
      "command": "C:/ruta/al/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": {
        "NLM_PROFILE": "personal"
      }
    },
    "notebooklm_work": {
      "command": "C:/ruta/al/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": {
        "NLM_PROFILE": "work"
      }
    }
  }
}
```

### macOS / Linux

```json
{
  "mcpServers": {
    "notebooklm_personal": {
      "command": "/ruta/al/proyecto/.venv/bin/python",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": {
        "NLM_PROFILE": "personal"
      }
    }
  }
}
```

---

## Ubicación del archivo de configuración

| Cliente | Ubicación |
|:---|:---|
| **Antigravity** | `~/.gemini/antigravity/mcp_config.json` |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) |
| **Cline (VS Code)** | `.vscode/cline_mcp_settings.json` en el workspace |
| **Continue** | `~/.continue/config.json` |

---

## ¿Por qué usar el Python del `.venv`?

El entorno virtual incluye el parche de compatibilidad para `distutils` (eliminado en Python 3.12+). Si usas el Python del sistema, puede fallar con:

```
ModuleNotFoundError: No module named 'distutils'
```

Siempre apunta al Python dentro de `.venv/`.

---

## Verificar que los servidores están activos

Después de reiniciar tu cliente AI, prueba:

```python
# Debe retornar lista de notebooks de tu cuenta personal
mcp_notebooklm_personal_notebook_list(max_results=3)

# Debe retornar lista de notebooks de tu cuenta de trabajo
mcp_notebooklm_work_notebook_list(max_results=3)
```

Si alguno falla con error de autenticación, ver [AUTHENTICATION.md](AUTHENTICATION.md).

---

## Agregar más perfiles

Puedes agregar tantos perfiles como cuentas de Google tengas. Por cada perfil:

1. Configura la autenticación: `python inject_profile.py --profile <nombre> --email <email>`
2. Agrega una entrada en `mcp_config.json` con `"NLM_PROFILE": "<nombre>"`
3. Reinicia tu cliente AI

Las herramientas estarán disponibles como `mcp_notebooklm_<nombre>_*`.
