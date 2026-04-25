# 🔐 Guía de Autenticación: NotebookLM MCP Multi-Perfil

Esta guía explica cómo obtener e inyectar las cookies de autenticación para cada perfil de Google que quieras usar con el MCP.

## ¿Por qué este método?

NotebookLM usa autenticación de Google, que detecta y bloquea intentos de login automatizados (Selenium, Playwright, etc.). El método más confiable es extraer las cookies directamente desde un navegador donde ya estás logueado.

**Tiempo estimado:** ~30 segundos por perfil.

---

## 🚀 Método Recomendado: Modo Elite (Automático)

Este es el método más rápido y confiable, especialmente para que agentes de IA autogestionen su acceso. Utiliza el binario nativo `nlm` para abrir un navegador real y capturar la sesión.

1. Identifica el directorio del proyecto.
2. Ejecuta:
   ```bash
   .venv/bin/nlm login --profile [nombre_perfil]
   ```
3. Se abrirá una ventana de Chrome. Completa el login manualmente.
4. Una vez que la terminal confirme el éxito, el perfil estará listo.

Ver [docs/ELITE_AUTH.md](ELITE_AUTH.md) para más detalles sobre este modo.

---

## 🛠️ Método Alternativo: Inyección Manual (Legacy)

Si el modo Elite no está disponible, puedes extraer las cookies manualmente:

### Paso 1: Obtener las cookies desde Chrome (Copy as cURL)

1. Abre **Chrome** con la cuenta de Google que quieres configurar.
2. Ve a **https://notebooklm.google.com/** y espera que cargue completamente.
3. Presiona **F12** para abrir DevTools.
4. Ve a la pestaña **Network** (Red).
5. Recarga la página con **F5**.
6. En la lista de requests, haz clic en cualquier request que vaya a `notebooklm.google.com`.
7. Clic derecho → **Copy** → **Copy as cURL (bash)**.

---

## Paso 2: Guardar el contenido en un archivo

Crea un archivo de texto con el nombre `<perfil>_cookies.txt` en el directorio del proyecto y pega **todo el texto copiado** (el comando cURL completo) dentro. No te preocupes por limpiar el texto, el script lo hará por ti.

**Ejemplos de nombres:**
- `personal_cookies.txt` → para tu cuenta personal
- `persat_cookies.txt` → para tu cuenta de trabajo (corporativa)

> ⚠️ **Importante:** Este archivo está en `.gitignore` y **nunca debe subirse a GitHub**.

---

## Paso 3: Ejecutar el script de inyección

# (Windows) Para cuenta personal
.venv\Scripts\python inject_profile.py --profile personal --email tu@gmail.com

# (Windows) Para cuenta de trabajo (persat)
.venv\Scripts\python inject_profile.py --profile persat --email tu@persat.com.ar

# (Linux / macOS) Para cuenta personal
.venv/bin/python inject_profile.py --profile personal --email tu@gmail.com

El script automáticamente:
1. Detecta si es un comando cURL y extrae las cookies.
2. Verifica que sean válidas conectándose a NotebookLM.
3. Extrae el CSRF token y Session ID.
4. Guarda todo en `~/.notebooklm-mcp-cli/profiles/<perfil>/`.

---

## Paso 4: Recargar la autenticación en el MCP

Después de inyectar las cookies, recarga el MCP desde tu cliente AI:

```python
# En Antigravity / Claude / cualquier cliente MCP:
mcp_notebooklm_personal_refresh_auth()
mcp_notebooklm_persat_refresh_auth()
```

---

## Verificar el estado de los perfiles

```bash
# Verificar todos los perfiles configurados (Windows)
.venv\Scripts\python verify_profile.py

# Verificar todos los perfiles configurados (Linux / macOS)
.venv/bin/python verify_profile.py
```

---

## ¿Cuándo necesito repetir este proceso?

Las cookies de Google expiran periódicamente (generalmente cada 1-4 semanas). Sabrás que expiraron cuando el MCP devuelva un error de `Authentication expired` o similar. Cuando eso ocurra, simplemente repite desde el **Paso 1**.

---

## Solución de problemas

| Síntoma | Causa | Solución |
|:---|:---|:---|
| `Authentication expired` | Cookies expiradas | Repetir desde Paso 1 |
| `ModuleNotFoundError: distutils` | Python 3.12+ sin setuptools | `pip install setuptools` |
| `Redirected to login` | Cookies viejas/inválidas | Repetir desde Paso 1 |
| CSRF token no encontrado | Error en el parseo | Asegúrate de haber copiado el cURL (bash) correctamente |
| `httpx` no instalado | Dependencia faltante | `.venv/bin/pip install -r requirements.txt` |
| Server aparece en `mcp_config.json` pero Antigravity dice "server not found" | Cookies expiradas → `MCP_SERVER_INIT_ERROR` al iniciar | Correr `verify_profile.py` → si muestra EXPIRADO, repetir desde Paso 1 y hacer Refresh en panel MCP |

---

## Diagnóstico rápido: MCP_SERVER_INIT_ERROR en Antigravity

Si Antigravity no reconoce el servidor (`server name notebooklm_X not found` en sus logs), el primer paso **siempre** es:

```bash
.venv/bin/python verify_profile.py
```

Si algún perfil muestra `❌ EXPIRADO`, ese es el problema. El MCP server no puede inicializarse con cookies inválidas, por lo que Antigravity lo descarta al arrancar.

Los logs de Antigravity donde aparece el error:
```
~/.config/Antigravity/logs/<fecha>/window1/exthost/google.antigravity/Antigravity.log
```
Buscar: `MCP_SERVER_INIT_ERROR` (aparece ~2 min después del startup).
