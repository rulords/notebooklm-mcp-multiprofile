# 🤖 NotebookLM MCP — Multi-Account Setup

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![notebooklm-mcp-cli](https://img.shields.io/badge/notebooklm--mcp--cli-0.2.7-green.svg)](https://pypi.org/project/notebooklm-mcp-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Configuración lista para usar de **NotebookLM como servidor MCP** con soporte para **múltiples cuentas de Google simultáneas**. Diseñada para integrarse con cualquier cliente AI compatible con MCP (Antigravity, Claude Desktop, Cline, Continue, etc.).

## ✨ ¿Qué incluye?

- **Multi-cuenta nativa**: cada perfil de Google corre como un servidor MCP independiente
- **~50 herramientas MCP**: gestión completa de notebooks, fuentes, notas, investigación profunda, generación de podcasts/videos/slides, exportación a Google Docs/Sheets
- **Autenticación robusta**: método manual con DevTools (más confiable que Selenium/CDP)
- **Scripts de utilidad**: inyección y verificación de cookies para cualquier perfil
- **Sin credenciales en el repo**: todo lo sensible queda en el sistema local del usuario

---

## 📋 Requisitos

- Python 3.10 o superior (recomendado: 3.11)
- Google Chrome instalado
- Una o más cuentas de Google con acceso a NotebookLM
- Un cliente AI compatible con MCP

> ⚠️ **Python 3.12+**: requiere `setuptools` adicional por la eliminación de `distutils`. El `requirements.txt` lo incluye.

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/notebooklm-mcp-multiprofile.git
cd notebooklm-mcp-multiprofile
```

### 2. Crear entorno virtual e instalar dependencias

```bash
# Crear venv
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (macOS/Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar autenticación

Para cada cuenta de Google que quieras usar:

```bash
# Cuenta personal
python inject_profile.py --profile personal --email tu@gmail.com

# Cuenta de trabajo
python inject_profile.py --profile work --email tu@empresa.com
```

Ver **[docs/AUTHENTICATION.md](docs/AUTHENTICATION.md)** para instrucciones detalladas sobre cómo obtener las cookies desde Chrome DevTools.

### 4. Configurar el cliente MCP

Copia `mcp_config.example.json` como referencia y adapta las rutas:

```json
{
  "mcpServers": {
    "notebooklm_personal": {
      "command": "C:/ruta/al/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": { "NLM_PROFILE": "personal" }
    },
    "notebooklm_work": {
      "command": "C:/ruta/al/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": { "NLM_PROFILE": "work" }
    }
  }
}
```

Ver **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)** para ubicaciones del archivo según tu cliente AI.

### 5. Verificar

```bash
python verify_profile.py
```

---

## 🛠️ Herramientas disponibles

Una vez configurado, tu cliente AI tendrá acceso a ~50 herramientas por perfil:

| Categoría | Herramientas |
|:---|:---|
| **Notebooks** | `notebook_list`, `notebook_create`, `notebook_get`, `notebook_describe`, `notebook_rename`, `notebook_delete`, `notebook_query` |
| **Fuentes** | `source_add` (URL/texto/Drive/archivo), `source_describe`, `source_get_content`, `source_delete`, `source_sync_drive` |
| **Notas** | `note` (create/list/update/delete) |
| **Investigación** | `research_start`, `research_status`, `research_import` |
| **Studio** | `studio_create` (audio/video/slides/infographic/report/flashcards/quiz/mind_map/data_table), `studio_status`, `studio_delete` |
| **Exportación** | `export_artifact` (Google Docs/Sheets), `download_artifact` |
| **Colaboración** | `notebook_share_public`, `notebook_share_invite` |
| **Auth** | `refresh_auth`, `save_auth_tokens` |

Las herramientas se acceden como `mcp_notebooklm_<perfil>_<herramienta>`. Por ejemplo:

```python
# Listar notebooks del perfil personal
mcp_notebooklm_personal_notebook_list(max_results=10)

# Crear notebook en cuenta de trabajo
mcp_notebooklm_work_notebook_create(title="Investigación Q1 2026")

# Generar podcast desde fuentes existentes
mcp_notebooklm_personal_studio_create(
    notebook_id="...",
    artifact_type="audio",
    confirm=True
)
```

---

## 🔄 Mantenimiento: cookies expiradas

Las cookies de Google expiran periódicamente. Cuando el MCP devuelva `RPC Error 16` o `Authentication expired`:

```bash
# 1. Obtener cookies frescas (ver docs/AUTHENTICATION.md)
# 2. Inyectar
python inject_profile.py --profile <nombre> --email <tu@email.com>

# 3. Recargar en el cliente AI
mcp_notebooklm_<nombre>_refresh_auth()
```

---

## 📁 Estructura del proyecto

```
notebooklm-mcp-multiprofile/
├── inject_profile.py          # Inyectar cookies para cualquier perfil
├── verify_profile.py          # Verificar estado de autenticación
├── requirements.txt           # Dependencias Python
├── mcp_config.example.json    # Plantilla de configuración MCP
├── .gitignore                 # Protege cookies y credenciales
├── docs/
│   ├── AUTHENTICATION.md      # Guía detallada de autenticación
│   ├── CONFIGURATION.md       # Configuración por cliente AI
│   └── internal/              # Documentación histórica del proyecto
└── .venv/                     # Entorno virtual (no se sube a GitHub)
```

---

## ⚠️ Seguridad

- **Nunca subas** archivos `*_cookies.txt` a GitHub (están en `.gitignore`)
- Los perfiles se guardan en `~/.notebooklm-mcp-cli/profiles/` (fuera del repo)
- El archivo `mcp_config.json` con tus rutas locales también está en `.gitignore`
- Usa siempre `mcp_config.example.json` como referencia pública

---

## 🐛 Solución de problemas

| Síntoma | Causa | Solución |
|:---|:---|:---|
| `RPC Error 16` | Cookies expiradas | Re-inyectar con `inject_profile.py` |
| `ModuleNotFoundError: distutils` | Python 3.12+ | `pip install setuptools` |
| `Redirected to login` | Cookies inválidas | Obtener cookies frescas |
| Servidor MCP no aparece | Ruta incorrecta en config | Verificar ruta al Python del `.venv` |

---

## 📚 Documentación

- [Guía de Autenticación](docs/AUTHENTICATION.md)
- [Configuración por cliente AI](docs/CONFIGURATION.md)
- [Documentación interna / histórica](docs/internal/)

---

## 🙏 Créditos

Basado en [notebooklm-mcp-cli](https://pypi.org/project/notebooklm-mcp-cli/) v0.2.7.

> **Nota sobre versiones**: La versión `0.2.7` es la que incluye el set completo de ~50 herramientas. Versiones posteriores como `notebooklm-mcp v2.0.x` son reescrituras incompletas con solo funciones básicas de chat.

---

## 📄 Licencia

MIT — ver [LICENSE](LICENSE)
