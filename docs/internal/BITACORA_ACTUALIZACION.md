# 📔 Bitácora de Actualización: NotebookLM MCP

**Fecha:** 06 de Febrero de 2026

## 🚀 Actualización del Motor
Se ha migrado el sistema de la versión antigua (`notebooklm-mcp-server` v0.1.15) al nuevo motor unificado:
*   **Nuevo Motor:** `notebooklm-mcp` (v2.0.11)
*   **Tecnología:** Basado en FastMCP v2 con soporte moderno para procesos asíncronos y multi-perfil.

### ✨ Mejoras Incorporadas
1.  **Manejo Multi-Cuenta Nativo:** Ahora el sistema utiliza perfiles de Chrome aislados (`persat` y `personal`) para permitir el acceso simultáneo a dos cuentas sin conflictos de sesión.
2.  **Gestión de Notas (CRUD):** El agente ahora puede crear, leer, editar y borrar notas internas directamente en los cuadernos.
3.  **Subida Directa de Archivos:** Se incorporó la herramienta `source_add_file` que permite cargar archivos locales (PDF, TXT, MD, MP3) sin depender de Google Drive o URLs.
4.  **Exportación a Workspace:** Capacidad de exportar tablas de datos a Google Sheets y reportes a Google Docs.
5.  **Descargas:** El motor ahora soporta la obtención directa de archivos generados (WAV, MP4, PNG).
6.  **Colaboración:** Nuevas herramientas para invitar colaboradores y crear links compartidos.

---

## 🛠️ Desafíos y Soluciones (Post-Mortem)

### ❌ Error 1: Sesiones Pisadas y Sobrescritas (Rutas Relativas)
*   **Problema:** Al usar `./chrome_profile_notebooklm`, el motor creaba la sesión en la carpeta donde se ejecutaba el comando. Al configurar la segunda cuenta, esta sobrescribía los archivos de la primera, invalidando el login previo.
*   **Solución:** Se forzó el uso de **Rutas Absolutas** en los archivos de configuración. Esto garantiza que cada cuenta tenga su propia "caja de seguridad" para las cookies, totalmente aislada.

### ❌ Error 2: Desincronización del Handshake (Invalid Session ID)
*   **Problema:** El navegador se cerraba antes de que el script de automatización pudiera "asegurar" la sesión después del login manual.
*   **Solución:** Se aumentó el `timeout` a 120 segundos y se utilizó el comando `quick-setup` que permite una validación más robusta del estado del navegador.

### ❌ Error 3: Desactivación de Undetected Chromedriver
*   **Problema:** El entorno de Python por defecto a veces no detectaba el driver anti-detección, cayendo en el driver de Selenium estándar que es más propenso a ser bloqueado por Google.
*   **Solución:** Se forzó la instalación de `undetected-chromedriver` y se configuró el modo `headless: true` en producción para mayor estabilidad.

---

## 📋 Estado Final del Sistema
*   **Skill Global:** Actualizada con descripciones detalladas de todas las herramientas (v2.0).
*   **Servidores Activos:**
    *   `notebooklm_persat`: Cuenta Corporativa.
    *   `notebooklm_personal`: Cuenta Personal.
*   **Estructura de Configuración:** Centralizada en `c:\01_Rodry\NotebookLM\configs\`.

---

## ⚠️ Limitación Crítica: Persistencia de Sesión

### Problema Identificado
### Problema Identificado
El motor `notebooklm-mcp-cli` (actualmente v0.2.17) utiliza `httpx` para las operaciones y un sistema basado en **CDP (Chrome DevTools Protocol)** puro para la autenticación.
*   **No utiliza Selenium** nativamente, sino que lanza un proceso de Chrome con `subprocess` y se conecta por WebSocket.
*   **Falla de Persistencia:** Este método es frágil y detectable por Google, lo que causa que las sesiones se invaliden rápidamente o que el login no persista entre reinicios.
*   **Limitación:** Al no usar `undetected-chromedriver`, pierde las capacidades anti-detección modernas.

### Solución Implementada: `auth_manager_selenium.py`
Se ha desarrollado un **Gestor de Autenticación Híbrido** que reemplaza el mecanismo nativo `nlm login`.
1.  **Motor:** Utiliza `undetected-chromedriver` (Selenium) para lanzar navegadores robustos.
2.  **Perfiles:** Gestiona `user-data-dir` persistentes en `~/.notebooklm-mcp-cli/chrome-profiles/<perfil>`.
3.  **Inyección:** Extrae los tokens (cookies, CSRF, SessionID) y los inyecta quirúrgicamente en el formato `auth.json` que el MCP espera.

Esta solución permite mantener el motor MCP actual (con todas sus herramientas) pero con una capa de autenticación "blindada" por Selenium.

### Recomendaciones
1. **Instalar dependencia faltante:**
   ```powershell
   pip install undetected-chromedriver
   ```
2. **Usar integración MCP con Antigravity** (en lugar del CLI directo)
3. **Reportar issue** al repositorio oficial del paquete

---

## 🏁 Conclusión y Estado Final (07/02/2026)

**El Proyecto ha concluido EXITOSAMENTE tras resolver un problema crítico de versiones.**

### 🛑 El Problema Crítico Detectado
Inicialmente instalamos la versión `notebooklm-mcp v2.0.11` (la más reciente en PyPI), pero descubrimos que esta versión era una **reescritura incompleta** que eliminó el 80% de las funcionalidades prometidas (solo dejaba chat básico).

### ✅ La Solución Definitiva
Realizamos un "downgrade" estratégico a la versión **`notebooklm-mcp-cli v0.2.7`**, recuperando así el **set completo de ~50 herramientas**:
*   ✅ **Gestión Completa:** Crear, borrar, renombrar notebooks.
*   ✅ **Contenido:** Subida de archivos locales, notas CRUD, investigación profunda.
*   ✅ **Studio:** Generación de Podcasts, Videos, Briefings.
*   ✅ **Multi-Perfil:** Soporte nativo para perfiles `persat` y `personal`.

### ⚙️ Configuración Actual Implementada

1.  **Motor Instalado:**
    *   Paquete: `notebooklm-mcp-cli`
    *   Versión: `0.2.7`
    *   Ubicación: `.../Scripts/nlm.exe`

2.  **Perfiles y Autenticación:**
    *   **Work:** `~/.notebooklm-mcp-cli/chrome-profiles/work` (Autenticado ✅)
    *   **Personal:** `~/.notebooklm-mcp-cli/chrome-profiles/personal` (Autenticado ✅)
    *   *Nota:* Las cookies fueron migradas exitosamente de la estructura anterior.

3.  **Integración MCP (Antigravity):**
    *   Archivo configurado: `cline_mcp_settings.json`
    *   Servidores activos:
        *   `notebooklm_persat`: Usa perfil Persat.
        *   `notebooklm_personal`: Usa perfil Personal.

### 🚀 Cómo Usar (Instrucciones para Agente/Usuario)

Una vez reiniciado el entorno (VS Code/Antigravity), el agente tendrá acceso a estas nuevas herramientas:

**Comandos de Ejemplo:**
*   *"Lista mis notebooks del perfil Persat"* -> `notebook_list`
*   *"Crea un cuaderno llamado 'Inversiones 2026' en mi cuenta personal"* -> `notebook_create`
*   *"Sube este PDF a mi cuaderno de finanzas"* -> `source_add_file`
*   *"Genera un podcast sobre este tema"* -> `audio_overview_create`

---
*Fin de la bitácora - Misión Cumplida*
