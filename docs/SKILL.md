---
name: notebooklm
description: >
  Orchestration skill for Google NotebookLM via MCP (notebooklm-mcp-cli v0.2.7).
  Supports multi-account management (any number of Google profiles), full notebook
  CRUD, source management, deep research, Studio content generation (audio/video/
  slides/reports/flashcards/quiz/mind_map), notes CRUD, and Workspace export.
  Auth uses manual cookie injection — never use nlm login for multi-account setups.
---

# NotebookLM MCP — Skill de Orquestación

## Reglas de Operación (leer siempre primero)

1. **Multi-perfil**: Las herramientas se llaman `mcp_notebooklm_[PERFIL]_[herramienta]`. Elegir el perfil correcto según el contexto del usuario. Si es ambiguo, preguntar.
2. **Async obligatorio**: `research_start` y `studio_create` son asíncronos. SIEMPRE hacer poll con `research_status` / `studio_status` hasta `status="completed"`. Nunca asumir completado inmediato.
3. **Confirmación**: Todas las herramientas `_create` destructivas y `_delete` requieren `confirm=True`. Si el usuario dio instrucción clara, proceder sin preguntar de nuevo.
4. **Auth expirada**: Si cualquier herramienta retorna `RPC Error 16` o `Authentication expired`, ejecutar `refresh_auth()` del perfil afectado. Si sigue fallando, informar al usuario que debe renovar cookies con `inject_profile.py`.
5. **Drive sync**: Antes de consultar notebooks con fuentes de Drive, ejecutar `source_list_drive` y si hay `needs_sync=True`, ejecutar `source_sync_drive(confirm=True)`.

---

## Referencia de Herramientas

### Notebooks
| Herramienta | Descripción |
|:---|:---|
| `notebook_list` | Lista todos los notebooks. Usar `max_results` para limitar. |
| `notebook_create` | Crea notebook vacío. Parámetro: `title`. |
| `notebook_get` | Detalles y lista de fuentes de un notebook. |
| `notebook_describe` | Resumen IA del contenido + temas sugeridos. |
| `notebook_rename` | Renombrar. Usar proactivamente si el título es genérico. |
| `notebook_delete` | Eliminar permanentemente. Requiere `confirm=True`. |
| `notebook_query` | Pregunta a la IA basada SOLO en las fuentes del notebook. Usar `conversation_id` para follow-up. |
| `chat_configure` | Configurar estilo de respuesta (`goal`, `response_length`). |

### Fuentes
| Herramienta | Descripción |
|:---|:---|
| `source_add` | Agregar fuente. `source_type`: `url`, `text`, `drive`, `file`. Usar `wait=True` para esperar procesamiento. |
| `source_describe` | Resumen IA de una fuente específica. |
| `source_get_content` | Texto crudo de la fuente (sin IA, más rápido). |
| `source_delete` | Eliminar fuente. Requiere `confirm=True`. |
| `source_list_drive` | Listar fuentes de Drive con estado de frescura. |
| `source_sync_drive` | Sincronizar fuentes desactualizadas. Requiere `confirm=True`. |

### Notas
| Herramienta | Descripción |
|:---|:---|
| `note` | CRUD unificado. `action`: `create`, `list`, `update`, `delete`. Usar para persistir razonamiento intermedio. |

### Investigación
| Herramienta | Descripción |
|:---|:---|
| `research_start` | Inicia búsqueda. `source`: `web` o `drive`. `mode`: `fast` (~30s, ~10 fuentes) o `deep` (~5min, ~40 fuentes). |
| `research_status` | Poll de progreso. Usar `max_wait=300`, `poll_interval=30`. Bloquea hasta completado. |
| `research_import` | Importa fuentes encontradas al notebook. |

### Studio (generación de contenido)
| Herramienta | Descripción |
|:---|:---|
| `studio_create` | Crear artefacto. `artifact_type`: `audio`, `video`, `infographic`, `slide_deck`, `report`, `flashcards`, `quiz`, `data_table`, `mind_map`. Requiere `confirm=True`. |
| `studio_status` | Verificar estado de generación y obtener URLs. |
| `studio_delete` | Eliminar artefacto. Requiere `confirm=True`. |
| `download_artifact` | Descargar artefacto a archivo local. |
| `export_artifact` | Exportar a Google Docs o Sheets. |

### Compartir
| Herramienta | Descripción |
|:---|:---|
| `notebook_share_public` | Habilitar/deshabilitar link público. |
| `notebook_share_invite` | Invitar colaborador por email. |
| `notebook_share_status` | Ver configuración de compartido actual. |

### Auth
| Herramienta | Descripción |
|:---|:---|
| `refresh_auth` | Recargar tokens desde disco. Llamar después de inyectar cookies nuevas. |
| `save_auth_tokens` | Guardar cookies manualmente (fallback). |

---

## Workflows Principales

### 🔍 Investigación Profunda
```
1. notebook_create(title="Research: {tema}")
2. research_start(query="{tema}", mode="deep", notebook_id=...)
3. research_status(notebook_id=..., max_wait=300)  ← esperar ~5min
4. research_import(notebook_id=..., task_id=...)
5. notebook_describe(notebook_id=...)  ← evaluar calidad
   → Si insuficiente: research_start con query refinada y repetir
6. studio_create(artifact_type="report", ...)
```

### 🎙️ Generador de Podcast/Video
```
1. Verificar fuentes en notebook (notebook_get)
2. studio_create(artifact_type="audio", confirm=True)
3. studio_status(notebook_id=...)  ← poll hasta "completed"
4. Retornar URL al usuario
```

### 📚 Pack de Estudio
```
1. source_add(source_type="file"/"drive", ..., wait=True)  ← por cada doc
2. studio_create(artifact_type="report", report_format="Study Guide", confirm=True)
3. studio_create(artifact_type="mind_map", confirm=True)
4. studio_create(artifact_type="flashcards", difficulty="medium", confirm=True)
5. studio_create(artifact_type="quiz", question_count=10, confirm=True)
6. studio_status(...)  ← verificar todos listos
```

### 🧠 Consulta Iterativa (Razonamiento Completo)
```
1. notebook_query(query="{pregunta}")
2. Evaluar si la respuesta es completa
   → Si parcial: notebook_query(query="{follow-up}", conversation_id=...)
   → Repetir hasta respuesta completa
3. Sintetizar todas las respuestas parciales en una respuesta final
4. Citar siempre las fuentes mencionadas
```

---

## Mantenimiento de Auth

Si cualquier herramienta retorna error de autenticación:

```python
# 1. Intentar refresh primero
mcp_notebooklm_[PERFIL]_refresh_auth()

# 2. Si sigue fallando, informar al usuario:
"Las cookies del perfil [PERFIL] expiraron. Para renovarlas:
 1. Abre Chrome con tu cuenta [EMAIL]
 2. Ve a https://notebooklm.google.com/
 3. F12 → Network → F5 → clic derecho en request → Copy as cURL
 4. Extrae el valor del header 'cookie:' y guárdalo en [PERFIL]_cookies.txt
 5. Ejecuta: python inject_profile.py --profile [PERFIL] --email [EMAIL]
 6. Luego llama: mcp_notebooklm_[PERFIL]_refresh_auth()"
```
