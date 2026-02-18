# Documentación de Instalación: NotebookLM MCP Server

Este documento detalla los pasos realizados para la instalación y configuración operativa del servidor MCP de NotebookLM en el sistema.

## 1. Diagnóstico del Entorno
- **Sistema Operativo:** Windows (PowerShell/pwsh)
- **Versión de Python:** 3.13.9
- **Entorno Virtual:** No (Instalación realizada en el ámbito de usuario).

## 2. Instalación del Servidor MCP
Se utilizó `pip` para instalar la última versión disponible del servidor:
- **Comando:** `python -m pip install -U notebooklm-mcp-server`
- **Versión Confirmada:** `0.1.15`

## 3. Registro del MCP en Antigravity
- **Archivo de Configuración:** `c:\Users\rsalv\.gemini\antigravity\mcp_config.json`
- **Copia de Seguridad:** Creada en `c:\Users\rsalv\.gemini\antigravity\mcp_config.json.bak`
- **Configuración Añadida:**
```json
"notebooklm": {
  "command": "python",
  "args": [
    "-m",
    "notebooklm_mcp.server"
  ]
}
```

## 4. Autenticación
### 4.1 Método Estándar (Deprecado/Frágil)
Se ejecutó el comando de autenticación automatizada:
- **Comando:** `notebooklm-mcp-auth` (o `nlm login`)
- **Resultado:** Inicio de sesión detectado en Chrome. Tokens y cookies extraídos y guardados en `C:\Users\rsalv\.notebooklm-mcp\auth.json`.
- **Nota:** Este método puede fallar en sesiones persistentes debido a la detección de automatización.

### 4.2 Método Robusto (Recomendado)
Se ha implementado un script personalizado que utiliza `undetected-chromedriver` para una autenticación resistente a detecciones.
- **Script:** `c:\01_Rodry\NotebookLM\auth_manager_selenium.py`
- **Uso:**
  ```powershell
  python auth_manager_selenium.py personal
  python auth_manager_selenium.py persat
  ```
- **Funcionamiento:** Lanza un navegador Chrome real (no headless por defecto para login inicial), permite el login manual si es necesario, y extrae los tokens en el formato exacto que el MCP requiere.

## 5. Validación de Herramientas
Se verificó el servidor para asegurar que expone todas las capacidades:
- **Total de herramientas detectadas:** 32
- **Herramienta para crear notebooks/cuadernos:** `notebook_create`

## 6. Prueba Funcional
Se realizó una llamada de prueba para listar los notebooks existentes en la cuenta:
- **Resultado:** Exitoso. Se detectaron **46 notebooks**.
- **Ejemplo de notebooks listados:**
  - Guía ChatGPT Pro: Dominando la IA de Forma Profesional
  - Botpress Avances
  - (Resto de notebooks omitidos por brevedad)

---
**Estado final:** ¡Instalación operativa!
