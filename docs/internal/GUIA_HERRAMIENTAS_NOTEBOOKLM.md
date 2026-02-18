# Guía de Herramientas: NotebookLM MCP Server

Este documento describe las herramientas disponibles en el servidor MCP de NotebookLM.
**Actualización 05/02/2026:** El sistema ha migrado al motor unificado `notebooklm-mcp` (v0.2.7), añadiendo capacidades de gestión de notas, subida directa y multi-cuenta.

## 📋 Gestión de Notebooks (Cuadernos)

| Herramienta | Descripción |
| :--- | :--- |
| `notebook_list` | Lista todos los notebooks disponibles en tu cuenta. |
| `notebook_create` | Crea un nuevo notebook vacío (puedes especificar un título). |
| `notebook_get` | Obtiene los detalles técnicos de un notebook y su lista de fuentes. |
| `notebook_describe` | Genera un resumen por IA del contenido del notebook y sugiere temas. |
| `notebook_rename` | Cambia el título de un notebook existente. |
| `notebook_delete` | Elimina un notebook de forma permanente (requiere confirmación). |
| `notebook_query` | Realiza preguntas a la IA basadas **solo** en las fuentes del notebook. |
| `chat_configure` | Configura el comportamiento del chat (estilo de respuesta, longitud, etc.). |

## 📂 Gestión de Fuentes (Sources)

| Herramienta | Descripción |
| :--- | :--- |
| `notebook_add_url` | Añade una URL web o un vídeo de YouTube como fuente. |
| `notebook_add_text` | Añade texto pegado directamente como una nueva fuente. |
| `notebook_add_drive` | Añade documentos de Google Drive (Doc, Slides, Sheets, PDF). |
| `source_describe` | Genera un resumen por IA de una fuente específica y extrae palabras clave. |
| `source_get_content` | Recupera el texto crudo extraído de una fuente (sin procesar por IA). |
| `source_list_drive` | Lista fuentes de Drive y comprueba si están desactualizadas. |
| `source_sync_drive` | Sincroniza las fuentes de Drive con su versión más reciente. |
| `source_delete` | Elimina una fuente específica de un notebook. |
| `source_add_file` (**NUEVO**) | Sube archivos locales (PDF, TXT, MD, MP3) directamente sin usar Drive/URL. |

## 📝 Gestión de Notas (NUEVO v0.2)

| Herramienta | Descripción |
| :--- | :--- |
| `notes_create` | Crea una nota dentro del cuaderno (ideal para apuntes del agente). |
| `notes_list` | Lista todas las notas guardadas en el notebook. |
| `notes_get` | Lee el contenido de una nota específica. |
| `notes_update` | Edita una nota existente. |
| `notes_delete` | Borra una nota de forma permanente. |

## 🔍 Investigación (Research)

| Herramienta | Descripción |
| :--- | :--- |
| `research_start` | Inicia una búsqueda profunda (Web) o rápida (Drive) para encontrar nuevas fuentes. |
| `research_status` | Consulta el progreso de una tarea de investigación en curso. |
| `research_import` | Importa los hallazgos de una investigación al notebook como fuentes. |

## 🎨 Generación de Contenido (Studio)

| Herramienta | Descripción |
| :--- | :--- |
| `audio_overview_create`| Genera el popular "Audio Overview" (charla tipo podcast). |
| `video_overview_create`| Genera una versión en vídeo explicativo del contenido. |
| `slide_deck_create` | Crea una presentación de diapositivas basada en las fuentes. |
| `infographic_create` | Genera una infografía visual con los puntos clave. |
| `report_create` | Genera documentos como Briefing Docs, Guías de Estudio o Blog Posts. |
| `mind_map_create` | Genera y guarda un mapa mental estructurado. |
| `data_table_create` | Genera una tabla de datos comparativa o estructurada. |
| `flashcards_create` | Genera tarjetas de estudio para memorización. |
| `quiz_create` | Crea un cuestionario interactivo para evaluar conocimientos. |
| `studio_status` | Comprueba el estado de generación y obtiene las URLs de descarga/vista. |
| `studio_delete` | Elimina un artefacto de contenido generado (audio, video, etc.). |

## 🌐 Compartir y Workspace (NUEVO v0.2)

| Herramienta | Descripción |
| :--- | :--- |
| `sharing_create_link` | Genera un enlace público para compartir el cuaderno. |
| `sharing_invite` | Envía invitaciones por email para colaborar en el notebook. |
| `export_to_sheets` | Exporta tablas de datos generadas directamente a Google Sheets. |
| `export_to_docs` | Envía reportes (Blog posts/briefings) directamente a Google Docs. |

## 🔑 Autenticación y Perfiles

| Herramienta | Descripción |
| :--- | :--- |
| `refresh_auth` | Recarga los tokens de acceso desde el disco o intenta re-autenticación. |
| `save_auth_tokens` | Método de respaldo manual para guardar cookies de sesión. |

---
*Nota: Todas las herramientas de creación (`create`) requieren el parámetro `confirm=True` para ejecutarse después de que el usuario apruebe la configuración inicial.*
