# Reparación de Autenticación NotebookLM MCP - Multi-Perfil

**Fecha:** 2026-02-10  
**Estado:** ✅ RESUELTO

## 🎯 Objetivo

Configurar y reparar la autenticación de NotebookLM MCP para soportar dos perfiles simultáneos:
- **Personal:** tu-cuenta@gmail.com
- **Work/Corporativo:** tu-cuenta@empresa.com

## ❌ Problemas Encontrados

### 1. Error de Módulo `distutils`
```
ModuleNotFoundError: No module named 'distutils'
```
**Causa:** Python 3.12+ eliminó el módulo `distutils` de la biblioteca estándar, pero `undetected-chromedriver` lo requería.

### 2. Autenticación Automática Fallida (Selenium)
- Chrome se abría pero mostraba selector de cuentas de Google
- No se podía seleccionar automáticamente la cuenta de Persat
- El script navegaba a NotebookLM antes de completar el login
- Timeout o cookies vacías

### 3. Cookies Manuales Inválidas
- Las cookies extraídas inicialmente redirigían a la página de login
- Faltaban tokens CSRF y Session ID

## ✅ Soluciones Implementadas

### 1. Parche de `distutils` en `undetected-chromedriver`

**Archivo modificado:** `.venv/Lib/site-packages/undetected_chromedriver/patcher.py`

```python
# Reemplazamos:
from distutils.version import LooseVersion

# Por un shim compatible:
class LooseVersion:
    def __init__(self, vstring):
        self.vstring = vstring
        self.version = [int(x) if x.isdigit() else x for x in vstring.replace('.', ' ').split()]
    def __str__(self):
        return self.vstring
```

**Resultado:** `undetected-chromedriver` funciona en Python 3.13

### 2. Método de Autenticación Manual

Dado que la autenticación automática con Selenium falló por el selector de cuentas de Google, implementamos un método manual más confiable:

#### Scripts Creados:

1. **`guia_auth_manual.py`**: Guía interactiva paso a paso
2. **`inject_persat_from_file.py`**: Procesa y valida cookies desde archivo

#### Proceso:

1. Usuario abre Chrome normalmente con cuenta de Persat
2. Navega a `https://notebooklm.google.com/`
3. Abre DevTools (F12) → Network
4. Copia cookies desde un request como cURL
5. Guarda cookies en `persat_cookies.txt`
6. Ejecuta `inject_persat_from_file.py` que:
   - Lee y parsea las cookies
   - Verifica validez conectándose a NotebookLM
   - Extrae CSRF token y Session ID
   - Guarda todo en el perfil

### 3. Configuración del MCP

**Archivo:** `~/.gemini/antigravity/mcp_config.json`

```json
{
  "mcpServers": {
    "notebooklm_work": {
      "command": "C:/ruta/al/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": {
        "NLM_PROFILE": "work"
      }
    },
    "notebooklm_personal": {
      "command": "C:/ruta/al/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": {
        "NLM_PROFILE": "personal"
      }
    }
  }
}
```

**Clave:** Usar el Python del venv que tiene el parche de `distutils`.

### 4. Recarga de Autenticación

Después de guardar las cookies, es necesario forzar la recarga:

```python
mcp_notebooklm_persat_refresh_auth()
```

## 📁 Estructura de Perfiles

```
~/.notebooklm-mcp-cli/
├── profiles/
│   ├── personal/
│   │   ├── cookies.json      # Cookies en formato lista de dicts
│   │   └── metadata.json     # CSRF token, Session ID, email
│   └── persat/
│       ├── cookies.json
│       └── metadata.json
└── chrome-profiles/          # Perfiles de Chrome (no usados en método manual)
    ├── personal/
    └── persat/
```

## 🔧 Comandos de Verificación

### Verificar cookies válidas:
```bash
python c:/01_Rodry/NotebookLM/test_cookies.py
```

### Listar notebooks:
```python
# Personal
mcp_notebooklm_personal_notebook_list(max_results=3)

# Persat
mcp_notebooklm_persat_notebook_list(max_results=3)
```

## ✅ Estado Final

- ✅ **MCP Personal:** 13 notebooks, funcionando
- ✅ **MCP Persat:** 50 notebooks (47 propios, 3 compartidos), funcionando
- ✅ Ambos perfiles operativos simultáneamente
- ✅ Método de autenticación manual confiable y documentado

## 📝 Lecciones Aprendidas

1. **Selenium no es confiable** para autenticación de Google cuando hay múltiples cuentas
2. **Método manual con DevTools** es más simple y confiable
3. **Python 3.12+** requiere parches para bibliotecas que usan `distutils`
4. **Refresh del MCP** es necesario después de actualizar credenciales
5. **Usar el Python del venv** en la configuración del MCP para tener los parches

## 🚀 Uso en Otros Proyectos

Los MCPs están configurados globalmente en Antigravity. Cualquier proyecto puede usar:

```python
# Listar notebooks de Persat
mcp_notebooklm_persat_notebook_list()

# Crear notebook en cuenta personal
mcp_notebooklm_personal_notebook_create(title="Mi Notebook")

# Agregar fuente a notebook de Persat
mcp_notebooklm_persat_source_add(
    notebook_id="...",
    source_type="url",
    url="https://example.com"
)
```

## 🔄 Mantenimiento

Si las cookies expiran:
1. Ejecutar `python c:/01_Rodry/NotebookLM/guia_auth_manual.py`
2. Seguir las instrucciones
3. Ejecutar `python c:/01_Rodry/NotebookLM/inject_persat_from_file.py`
4. Recargar: `mcp_notebooklm_persat_refresh_auth()`

---

**Autor:** Antigravity AI  
**Última actualización:** 2026-02-10
