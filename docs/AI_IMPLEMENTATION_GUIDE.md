# AI Implementation Guide — NotebookLM MCP Multi-Account

> **Para agentes AI (Antigravity, Claude, etc.):** Esta guía contiene todo lo necesario para implementar el sistema completo. Léela de arriba a abajo una sola vez y ejecuta en orden.

---

## 1. CONTEXTO DEL SISTEMA

**Qué hace:** Expone Google NotebookLM como servidor MCP con ~50 herramientas. Soporta múltiples cuentas de Google simultáneas, cada una como servidor MCP independiente.

**Motor:** `notebooklm-mcp-cli==0.2.7` (PyPI). Esta versión específica tiene el set completo. Versiones `2.x` son reescrituras incompletas — NO usar.

**Autenticación:** Cookies manuales extraídas desde Chrome DevTools. No usar `nlm login` (Google bloquea automatización CDP con múltiples cuentas).

**Datos que necesitas recolectar del usuario (uno por perfil):**
- Nombre del perfil (ej: `personal`, `work`, `empresa`)
- Email de Google asociado
- String de cookies (extraído por el usuario desde Chrome DevTools)

---

## 2. PREREQUISITOS — VERIFICAR ANTES DE EMPEZAR

```python
# Verificar Python >= 3.10
run_command("python --version")

# Verificar Chrome instalado (necesario para que el usuario extraiga cookies)
run_command("where chrome")  # Windows
run_command("which google-chrome")  # Linux/macOS
```

Si Python < 3.10 → pedir al usuario que actualice. No continuar.

---

## 3. INSTALACIÓN (ejecutar en orden)

```bash
# 3.1 Crear entorno virtual en el directorio del proyecto
python -m venv .venv

# 3.2 Instalar dependencias (incluye setuptools para Python 3.12+)
.venv/Scripts/pip install -r requirements.txt        # Windows
.venv/bin/pip install -r requirements.txt            # macOS/Linux

# 3.3 Verificar instalación
.venv/Scripts/python -c "import notebooklm_tools; print('OK')"  # Windows
.venv/bin/python -c "import notebooklm_tools; print('OK')"      # macOS/Linux
```

**Si falla con `ModuleNotFoundError: distutils`:**
```bash
.venv/Scripts/pip install setuptools  # Windows
.venv/bin/pip install setuptools      # macOS/Linux
```

---

## 4. RECOLECTAR DATOS DEL USUARIO

Para cada cuenta de Google, pedir al usuario que ejecute este proceso:

### Instrucciones para el usuario (copiar y pegar):

```
1. Abre Chrome con tu cuenta de Google: [EMAIL_DEL_PERFIL]
2. Ve a: https://notebooklm.google.com/
3. Espera que cargue completamente (deben verse tus notebooks)
4. Presiona F12 → pestaña "Network" → recarga con F5
5. Haz clic en cualquier request a "notebooklm.google.com"
6. Clic derecho → Copy → "Copy as cURL (bash)"
7. Pega el texto en un editor y busca la línea: -H 'cookie: ...'
8. Copia SOLO el contenido después de 'cookie: ' (sin comillas)
9. Guarda ese texto en el archivo: [PERFIL]_cookies.txt
   (en el directorio del proyecto)
```

---

## 5. CONFIGURAR CADA PERFIL

```bash
# Por cada perfil (reemplazar valores):
python inject_profile.py --profile [NOMBRE] --email [EMAIL]

# Ejemplos:
python inject_profile.py --profile personal --email usuario@gmail.com
python inject_profile.py --profile work --email usuario@empresa.com
```

**Salida esperada (éxito):**
```
✅ Cookies guardadas (N cookies)
✅ Metadata guardada
🎉 ¡Perfil 'X' configurado exitosamente!
```

**Si falla con "CSRF token no encontrado":** Las cookies son inválidas. Pedir al usuario que repita el paso 4.

**Archivos generados** (fuera del repo, en home del usuario):
```
~/.notebooklm-mcp-cli/profiles/[PERFIL]/cookies.json
~/.notebooklm-mcp-cli/profiles/[PERFIL]/metadata.json
```

---

## 6. CONFIGURAR EL CLIENTE MCP

### 6.1 Obtener la ruta absoluta al Python del venv

```bash
# Windows:
(Get-Item .venv/Scripts/python.exe).FullName

# macOS/Linux:
realpath .venv/bin/python
```

### 6.2 Crear/editar mcp_config.json

Ubicaciones según cliente:
- **Antigravity:** `~/.gemini/antigravity/mcp_config.json`
- **Claude Desktop (macOS):** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Cline (VS Code):** `.vscode/cline_mcp_settings.json`

Estructura (agregar dentro de `mcpServers`, un bloque por perfil):

```json
"notebooklm_[PERFIL]": {
  "command": "[RUTA_ABSOLUTA_AL_PYTHON_DEL_VENV]",
  "args": ["-m", "notebooklm_tools.mcp.server"],
  "env": {
    "NLM_PROFILE": "[PERFIL]"
  }
}
```

**Ejemplo completo para Antigravity con 2 perfiles:**
```json
{
  "mcpServers": {
    "notebooklm_personal": {
      "command": "C:/Users/USUARIO/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": { "NLM_PROFILE": "personal" }
    },
    "notebooklm_work": {
      "command": "C:/Users/USUARIO/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": { "NLM_PROFILE": "work" }
    }
  }
}
```

### 6.3 Reiniciar el cliente AI

Después de editar `mcp_config.json`, el cliente AI debe reiniciarse para cargar los nuevos servidores.

---

## 7. VERIFICAR FUNCIONAMIENTO

```bash
# Verificar perfiles configurados localmente:
python verify_profile.py
```

Desde el cliente AI (después de reiniciar):
```python
# Debe retornar lista de notebooks:
mcp_notebooklm_personal_notebook_list(max_results=3)
mcp_notebooklm_work_notebook_list(max_results=3)
```

**Si retorna error de autenticación:** ejecutar `mcp_notebooklm_[PERFIL]_refresh_auth()` y reintentar.

---

## 8. MANTENIMIENTO — COOKIES EXPIRADAS

Las cookies expiran cada 1-4 semanas. Síntomas:
- `RPC Error 16: Authentication expired`
- `No authentication found`
- `Redirected to login`
- **En Antigravity:** `server name notebooklm_X not found` → `MCP_SERVER_INIT_ERROR` en logs

**Diagnóstico rápido — siempre empezar aquí:**
```bash
.venv/bin/python verify_profile.py
```
Si muestra `❌ EXPIRADO`, las cookies son la causa. No hace falta revisar otros logs.

**Procedimiento de renovación:**
1. Usuario extrae cookies frescas (repetir paso 4)
2. Guardar en `[PERFIL]_cookies.txt`
3. `python inject_profile.py --profile [PERFIL] --email [EMAIL]`
4. Hacer Refresh en el panel MCP del cliente AI (Antigravity: botón Refresh en MCP panel)
5. Opcional: `mcp_notebooklm_[PERFIL]_refresh_auth()` si el server ya está corriendo

**Nota WSL/Linux:** Si `verify_profile.py` muestra todos los perfiles ACTIVOS pero Antigravity sigue sin reconocer el servidor, verificar que el cliente AI haya reiniciado correctamente después del Refresh. Los `MCP_SERVER_INIT_ERROR` se registran solo al arrancar Antigravity.

---

## 9. REFERENCIA RÁPIDA DE HERRAMIENTAS MCP

Las herramientas se llaman como `mcp_notebooklm_[PERFIL]_[herramienta]`.

| Categoría | Herramientas clave |
|:---|:---|
| Notebooks | `notebook_list`, `notebook_create`, `notebook_get`, `notebook_describe`, `notebook_rename`, `notebook_delete`, `notebook_query` |
| Fuentes | `source_add` (url/text/drive/file), `source_describe`, `source_get_content`, `source_delete` |
| Notas | `note` (action: create/list/update/delete) |
| Investigación | `research_start` → `research_status` → `research_import` |
| Studio | `studio_create` (audio/video/slides/infographic/report/flashcards/quiz/mind_map/data_table) |
| Estado | `studio_status` (poll hasta completado) |
| Exportar | `download_artifact`, `export_artifact` |
| Auth | `refresh_auth`, `save_auth_tokens` |

**Patrones importantes:**
- `research_start` y `studio_create` son **asíncronos** → siempre hacer poll con `research_status` / `studio_status`
- Operaciones destructivas requieren `confirm=True`
- Para multi-cuenta: elegir el perfil correcto según contexto del usuario

---

## 10. CHECKLIST DE IMPLEMENTACIÓN

```
[ ] Python >= 3.10 instalado
[ ] .venv creado e instalado (requirements.txt)
[ ] Perfil 1 configurado: python inject_profile.py --profile X --email Y
[ ] Perfil 2 configurado (si aplica)
[ ] verify_profile.py retorna ✅ ACTIVO para todos los perfiles
[ ] mcp_config.json actualizado con rutas correctas
[ ] Cliente AI reiniciado
[ ] notebook_list retorna notebooks correctamente para cada perfil
```
