# 🚀 NotebookLM Elite Auth (Modo Agente)

Este documento describe el procedimiento de autenticación "Elite" optimizado para que agentes de IA (como Antigravity, Claude o GPT-4) puedan gestionar el acceso a NotebookLM de forma rápida y sin errores de parseo manual de cookies.

## Concepto
A diferencia del método manual (copiar cURL), el modo **Elite** utiliza el binario nativo `nlm` para abrir un navegador real y capturar la sesión de forma íntegra. Esto evita bloqueos de User-Agent y problemas con redirecciones de seguridad de Google.

---

## 🤖 Guía para el Agente IA

Si detectas que las herramientas de NotebookLM devuelven `Authentication expired` o el servidor no inicia, sigue estos pasos:

### 1. Identificar Entorno
El proyecto reside en: `/mnt/d/proyectos/personal/NotebookLM` (o tu ruta local equivalente).

### 2. Ejecutar el Login Automático
Lanza el siguiente comando para el perfil afectado (`persat` o `personal`):

```bash
# Formato: .venv/bin/nlm login --profile <perfil>
/mnt/d/proyectos/personal/NotebookLM/.venv/bin/nlm login --profile persat
```

### 3. Instrucción al Usuario
Informa inmediatamente al usuario:
> "He abierto una ventana de Chrome para la autenticación de NotebookLM. Por favor, completa el login manualmente. Avisame cuando termines o espera a que la terminal confirme el éxito."

### 4. Verificación
Espera a que el comando devuelva `✓ Successfully authenticated!`. Luego, confirma el estado con:

```bash
/mnt/d/proyectos/personal/NotebookLM/.venv/bin/python verify_profile.py --profile <perfil>
```

### 5. Refrescar MCP
Una vez validado, llama a la herramienta de refresco para que el servidor cargue las nuevas credenciales:
`mcp_notebooklm_<perfil>_refresh_auth()`

---

## 🛠️ Detalle Técnico (Under the Hood)

- **Binario**: `.venv/bin/nlm`
- **Mecanismo**: Utiliza Playwright/CDP para orquestar una instancia de Chrome con el perfil de usuario.
- **Persistencia**: Los tokens se guardan en `~/.notebooklm-mcp-cli/profiles/<perfil>/`.
- **Compatibilidad**: Probado en WSL2 (Ubuntu) con Google Chrome instalado en el entorno Linux.

---

> [!IMPORTANT]
> No intentes inyectar cookies manualmente si tienes acceso al binario `nlm`. Es 10x más confiable y maneja automáticamente el CSRF token y el Session ID.
