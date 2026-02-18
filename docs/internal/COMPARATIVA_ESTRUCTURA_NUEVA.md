# Comparativa: Antiguo Motor vs. Nuevo Motor (NotebookLM MCP)

Este documento analiza las diferencias entre el servidor MCP original (`notebooklm-mcp-server`) y la nueva arquitectura unificada (`notebooklm-mcp` v0.2.7+).

## 📊 Resumen de Capacidades

| Característica | Motor Antiguo (v0.1.x) | Nuevo Motor (v0.2.x) | Estado |
| :--- | :--- | :--- | :--- |
| **Arquitectura** | Servidor MCP aislado | **Unificado** (CLI + MCP + API) | 🚀 Mejor |
| **Autenticación** | Perfil único global | **Multi-perfil** (Soporte `--profile`) | 🚀 Mejor |
| **Carga de Archivos** | Limitada/Browser dependiente | **Carga Directa** (PDF, TXT, MD, Audio) | 🚀 Mejor |
| **Gestión de Notas** | No disponible | **CRUD Completo** (Crear, leer, editar, borrar) | 🌟 Nuevo |
| **Exportación** | Solo lectura/vista | **Exportar a Google Sheets/Docs** | 🌟 Nuevo |
| **Descargas** | Enlaces temporales | **Descarga Directa** (WAV, MP4, PNG) | 🚀 Mejor |
| **Colaboración** | No disponible | **Sharing API** (Links públicos e invitaciones) | 🌟 Nuevo |

---

## 🛠️ Nuevas Herramientas (Tool Surface)

El nuevo motor expande la superficie de herramientas de 32 a aproximadamente 45+, agrupadas en dominios lógicos:

### 1. Dominio de Notas (`notes_`) - **¡NUEVO!**
Ahora el agente puede interactuar con las notas internas del cuaderno, no solo con las fuentes:
*   `notes_create`: Permite al agente tomar apuntes propios.
*   `notes_list` / `notes_get`: Recupera pensamientos previos.
*   `notes_update` / `notes_delete`: Mantiene la higiene de las notas.

### 2. Dominio de Carga Directa (`source_add_file`)
*   Ya no dependemos 100% de que el documento esté en Drive o en una URL. El agente puede subir archivos locales directamente al cuaderno por HTTP.

### 3. Dominio de Exportación y Compartido
*   `sharing_create_link`: Genera un link público del cuaderno.
*   `sharing_invite`: Añade a alguien por email.
*   `export_to_sheets` / `export_to_docs`: Mueve los reportes generados a tu espacio de trabajo real.

---

## 💎 Ventajas Estratégicas para "Rodry"

1.  **Orden Total:** Con el sistema de **Perfiles (`--profile`)**, podemos tener `nlm_persat` y `nlm_personal` conviviendo sin que las cookies se mezclen ni se cierren sesión entre sí.
2.  **Agente más Inteligente:** Al poder escribir notas, el agente puede usar NotebookLM como su "memoria a largo plazo" para proyectos, guardando resúmenes intermedios que él mismo escribió.
3.  **Higiene de Datos:** El soporte para **Bulk Delete** permite limpiar investigaciones fallidas en segundos en lugar de ir fuente por fuente.

---
*Documento generado para la evaluación de migración del sistema NotebookLM MCP.*
