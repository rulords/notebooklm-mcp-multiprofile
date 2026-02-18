# 🤖 NotebookLM MCP — Multi-Account Setup

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![notebooklm-mcp-cli 0.2.7](https://img.shields.io/badge/notebooklm--mcp--cli-0.2.7-green.svg)](https://pypi.org/project/notebooklm-mcp-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Configuración lista para usar de **Google NotebookLM como servidor MCP**, con soporte para **múltiples cuentas de Google simultáneas**.

Compatible con cualquier cliente AI que soporte MCP: **Antigravity, Claude Desktop, Cline, Continue**, y otros.

---

## ¿Qué hace esto?

Convierte NotebookLM en un conjunto de ~50 herramientas que tu IA puede usar directamente:

- 📚 Gestionar notebooks (crear, listar, renombrar, eliminar, consultar)
- 🔗 Agregar fuentes (URLs, archivos locales, Google Drive, texto)
- 🎙️ Generar contenido (podcasts, videos, slides, informes, flashcards, quizzes)
- 🔍 Investigación profunda automática (busca y agrega docenas de fuentes web)
- 📝 Notas internas en notebooks (memoria persistente para el agente)
- 🔄 Multi-cuenta: cada cuenta de Google corre como servidor MCP independiente

---

## Instalación rápida

### 1. Clonar y crear entorno virtual

```bash
git clone https://github.com/tu-usuario/notebooklm-mcp-multiprofile.git
cd notebooklm-mcp-multiprofile

python -m venv .venv

# Windows
.venv\Scripts\pip install -r requirements.txt

# macOS / Linux
.venv/bin/pip install -r requirements.txt
```

### 2. Configurar autenticación

Para cada cuenta de Google que quieras usar:

```bash
# Primero obtener cookies desde Chrome (ver docs/AUTHENTICATION.md)
# Guardar en: personal_cookies.txt

python inject_profile.py --profile personal --email tu@gmail.com
python inject_profile.py --profile work --email tu@empresa.com
```

### 3. Registrar en tu cliente AI

Edita el archivo de configuración MCP de tu cliente (ver `mcp_config.example.json`):

```json
{
  "mcpServers": {
    "notebooklm_personal": {
      "command": "/ruta/al/proyecto/.venv/Scripts/python.exe",
      "args": ["-m", "notebooklm_tools.mcp.server"],
      "env": { "NLM_PROFILE": "personal" }
    }
  }
}
```

### 4. Verificar

```bash
python verify_profile.py
```

---

## Documentación

| Documento | Para quién |
|:---|:---|
| [docs/AUTHENTICATION.md](docs/AUTHENTICATION.md) | Cómo obtener e inyectar cookies desde Chrome |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | Configurar el MCP en cada cliente AI |
| [docs/AI_IMPLEMENTATION_GUIDE.md](docs/AI_IMPLEMENTATION_GUIDE.md) | **Para agentes AI**: guía completa de implementación paso a paso |

---

## Uso desde el cliente AI

```python
# Listar notebooks
mcp_notebooklm_personal_notebook_list(max_results=10)

# Crear notebook
mcp_notebooklm_work_notebook_create(title="Investigación Q1 2026")

# Agregar fuente URL
mcp_notebooklm_personal_source_add(
    notebook_id="...",
    source_type="url",
    url="https://ejemplo.com/articulo"
)

# Generar podcast
mcp_notebooklm_personal_studio_create(
    notebook_id="...",
    artifact_type="audio",
    confirm=True
)

# Investigación profunda
mcp_notebooklm_work_research_start(
    query="inteligencia artificial en salud 2025",
    mode="deep"
)
```

---

## Mantenimiento

Las cookies de Google expiran cada 1-4 semanas. Cuando el MCP devuelva `RPC Error 16`:

```bash
# Obtener cookies frescas (ver docs/AUTHENTICATION.md)
python inject_profile.py --profile [nombre] --email [email]

# Recargar en el cliente AI:
mcp_notebooklm_[nombre]_refresh_auth()
```

---

## Nota sobre versiones

> ⚠️ Este proyecto usa `notebooklm-mcp-cli==0.2.7` específicamente.  
> Las versiones `notebooklm-mcp 2.x` son reescrituras incompletas con solo funciones básicas de chat.  
> **No actualizar** sin verificar que el set completo de herramientas esté disponible.

---

## Seguridad

- Los archivos `*_cookies.txt` están en `.gitignore` — nunca se suben a GitHub
- Los perfiles se guardan en `~/.notebooklm-mcp-cli/` (fuera del repo)
- `mcp_config.json` con tus rutas locales también está ignorado — usar `mcp_config.example.json` como plantilla

---

## Licencia

MIT — ver [LICENSE](LICENSE)
