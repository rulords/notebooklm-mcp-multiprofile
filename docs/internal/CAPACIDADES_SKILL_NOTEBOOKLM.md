# 🧠 Capacidades de la Skill: NotebookLM Pro

Esta skill transforma al agente en un **Usuario Experto de NotebookLM**, otorgándole flujos de trabajo orquestados para investigar, crear contenido educativo/multimedia y gestionar conocimiento de forma autónoma. Aprovecha la totalidad de las 32 herramientas del MCP.

## 🚀 ¿Qué "superpoderes" añade esta skill?

A diferencia de usar las herramientas sueltas, esta skill le enseña al agente **estrategias completas** (Best Practices) para cuatro perfiles de uso principales.

### 1. 🕵️‍♂️ Agente de Investigación Profunda (Deep Research Agent)
El agente sabe cómo conducir una investigación exhaustiva sin supervisión constante.
*   **Capacidad:** Crea una libreta, lanza una investigación "Deep" (que busca en docenas de fuentes web), espera pacientemente los 3-5 minutos requeridos y procesa los resultados automáticamente.
*   **Herramientas clave:** `research_start`, `research_status`, `research_import`.
*   **Cómo activarlo:** *"Investiga a fondo sobre [Tema]"* o *"Haz un reporte completo sobre las novedades de [Tema]"*.

### 2. 🎙️ Fábrica de Contenidos (Content Studio Factory)
Automatiza la producción de formatos complejos como podcasts, vídeos o presentaciones.
*   **Capacidad:** Entiende que para crear un Audio Overview o Video primero debe verificar fuentes, solicitar la generación y monitorear hasta que la URL esté lista.
*   **Herramientas clave:** `audio_overview_create`, `video_overview_create`, `slide_deck_create`, `infographic_create`.
*   **Cómo activarlo:** *"Genera un podcast sobre estas notas"* o *"Crea una presentación (slides) basada en mi investigación"*.

### 3. 🎓 Compañero de Estudio Definitivo (The Ultimate Study Buddy)
Un nuevo perfil diseñado para estudiantes y profesionales que necesitan dominar un tema.
*   **Capacidad:** Ingiere documentos y genera automáticamente un ecosistema de estudio completo: Guías, Flashcards, Quizzes y Tablas Comparativas.
*   **Herramientas clave:** `flashcards_create`, `quiz_create`, `data_table_create`, `report_create`, `mind_map_create`.
*   **Cómo activarlo:** *"Prepara un plan de estudio para mi examen"* o *"Hazme un quiz y flashcards sobre estos PDFs"*.

### 4. 🧠 Gestor de Conocimiento (Knowledge Manager)
Mantiene la higiene y actualización de tu base de conocimientos.
*   **Capacidad:** Sabe que antes de responder preguntas sobre documentos de Drive, debe verificar si están desactualizados (`needs_sync`) y sincronizarlos automáticamente. Mantiene el orden renombrando y eliminando items obsoletos.
*   **Herramientas clave:** `source_sync_drive`, `notebook_list`, `notebook_query`, `studio_delete`.
*   **Cómo activarlo:** *"Sincroniza mis documentos y resume los cambios"* o *"Responde a esta pregunta basándote estrictamente en mis documentos"*.

---

## 📋 Flujos de Trabajo (Workflows) Definidos

Estos son los "guiones" que el agente sigue paso a paso gracias a la skill:

### Workflow 1: Investigación desde Cero
1.  **Crear:** Genera un cuaderno específico para el tema.
2.  **Investigar:** Lanza `research_start` en modo `deep`.
3.  **Espera Inteligente:** Monitorea `research_status` (sabe que tarda minutos).
4.  **Importar:** Trae las fuentes descubiertas al cuaderno.
5.  **Sintetizar:** Genera el producto final solicitado.

### Workflow 2: Generador Multimedia (Podcast/Video)
1.  **Validar:** Asegura que haya fuentes en el cuaderno.
2.  **Generar:** Ejecuta `audio_overview_create` o `video_overview_create`.
3.  **Monitorear:** Consulta `studio_status` hasta obtener el éxito.
4.  **Entregar:** Te presenta la URL final para consumir el contenido.

### Workflow 3: El Pack de Estudio (Study Buddy)
1.  **Ingesta:** Carga tus PDFs o Docs de Drive.
2.  **Resumen:** Genera una Guía de Estudio (`report_create`).
3.  **Práctica:** Crea Flashcards y un Quiz de evaluación.
4.  **Estructura:** (Opcional) Crea un Mapa Mental (`mind_map_create`).
5.  **Entrega:** Verifica que todo esté listo en `studio_status`.

---

## 🛠️ Instrucciones Técnicas para el Agente

La skill también impone reglas de seguridad y eficiencia:
*   **Confirmación:** Obliga al agente a pedirte confirmación (`confirm=True`) antes de crear artefactos o borrar datos, protegiendo tus créditos y datos.
*   **Asincronía:** Le enseña que procesos como la investigación profunda y la generación de video no son inmediatos y debe "esperar" (poll) por ti.
*   **Totalidad:** El agente ahora tiene conciencia de las 32 herramientas disponibles, incluyendo las operaciones de mantenimiento (`refresh_auth`, `save_auth_tokens`) y gestión granular de fuentes (`source_get_content`, `source_describe`).
