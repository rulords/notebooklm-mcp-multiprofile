# Roadmap de Migración: Nuevo Motor NotebookLM MCP

Este documento detalla el procedimiento paso a paso para actualizar el sistema al nuevo motor `notebooklm-mcp` (v0.2.7+), permitiendo el manejo multi-cuenta de forma eficiente.

## Fase 1: Limpieza y Preparación
1.  **Eliminar Motor Antiguo:**
    `pip uninstall notebooklm-mcp-server`
2.  **Limpiar Caché de Autenticación (Opcional pero recomendado):**
    Eliminar la carpeta `C:\Users\rsalv\.notebooklm-mcp` para evitar conflictos de cookies entre la versión vieja y la nueva.

## Fase 2: Instalación del Nuevo Motor
1.  **Instalar Paquete Unificado:**
    `pip install -U notebooklm-mcp`
2.  **Verificar Instalación:**
    `nlm --version` (Debería devolver v0.2.7 o superior).

## Fase 3: Configuración Multi-Perfil
Para cada cuenta, realizaremos un proceso de login independiente que creará perfiles aislados.

1.  **Configurar Cuenta PERSAT:**
    *   Comando: `nlm auth --profile persat`
    *   Acción: Se abrirá Chrome, loguearse con la cuenta corporativa.
2.  **Configurar Cuenta PERSONAL:**
    *   Comando: `nlm auth --profile personal`
    *   Acción: Se abrirá Chrome, loguearse con la cuenta personal.

## Fase 4: Registro en Antigravity
Modificaremos el archivo `mcp_config.json` para registrar **dos servidores distintos** que apunten a sus respectivos perfiles.

```json
{
  "mcpServers": {
    "notebooklm_persat": {
      "command": "python",
      "args": ["-m", "notebooklm_mcp.server", "--profile", "persat"]
    },
    "notebooklm_personal": {
      "command": "python",
      "args": ["-m", "notebooklm_mcp.server", "--profile", "personal"]
    }
  }
}
```

## Fase 5: Validación
1.  Reiniciar el entorno del agente.
2.  Ejecutar `notebooklm_persat.notebook_list` y verificar que solo muestra cuadernos de trabajo.
3.  Ejecutar `notebooklm_personal.notebook_list` y verificar que solo muestra cuadernos personales.

---
**Resultado Esperado:** Un entorno robusto, sin conflictos de sesión y con capacidades extendidas de gestión de notas y exportación.
