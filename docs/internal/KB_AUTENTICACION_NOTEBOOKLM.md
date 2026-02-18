# 🔐 KB: Autenticación Persistente en NotebookLM (Windows Headless)

**Fecha:** 07/02/2026
**Contexto:** Migración a `notebooklm-mcp` (cualquier versión basada en Selenium).
**Problema:** Google detecta automatización y cierra sesión/impide login headless.

---

## ⚠️ El Problema Fundamental
Los motores de NotebookLM basados en Selenium fallan en modo `headless` puro porque:
1.  Falta `undetected-chromedriver` o sus dependencias (`setuptools/distutils`).
2.  Google invalida sesiones iniciadas por robots.
3.  El navegador se cierra antes de completar el handshake de autenticación.

## ✅ La Solución Definitiva (Hard-Testing)

### 1. Prerrequisitos Críticos
Asegurar que el entorno Python tenga estas librerías para evitar detección:
```powershell
pip install undetected-chromedriver setuptools
```
*(Nota: `setuptools` es necesario para que `undetected-chromedriver` funcione en Python 3.12+)*

### 2. Estrategia de Perfiles de Usuario
NO usar perfiles temporales. Usar rutas absolutas y específicas por cuenta:
- **Work:** `~/.notebooklm-mcp/profiles/work/chrome_profile_notebooklm`
- **Personal:** `~/.notebooklm-mcp/profiles/personal/chrome_profile_notebooklm`

### 3. El Método "Login Humano" (Bypassing Detection)
El método más fiable para generar cookies persistentes es iniciar Chrome manualmente con el flag de perfil, loguearse, y cerrar. El motor luego "hereda" esa sesión.

**Comando PowerShell para Login Manual:**
```powershell
Start-Process chrome -ArgumentList '--user-data-dir="~/.notebooklm-mcp/profiles/TU_PERFIL"', 'https://notebooklm.google.com'
```
1.  Ejecutar comando.
2.  Loguearse en Google.
3.  Cerrar ventana.
4.  Ejecutar motor en modo headless (funcionará porque las cookies ya están en disco).

### 4. Parche de Compatibilidad (Si falla driver)
Si el motor intenta descargar una versión de ChromeDriver (ej. 145) que no coincide con el Chrome instalado (ej. 144), el script fallará.
**Solución:** Forzar la versión en la inicialización de `undetected_chromedriver`:
```python
# En el código del cliente (client.py):
self.driver = uc.Chrome(options=options, version_main=144) # <--- Forzar versión mayor
```

### 5. Configuración de Tiempos (Headless Race Conditions)
En modo headless, la página carga más rápido de lo que los elementos son interactuables.
**Solución:** Aumentar esperas explícitas antes de buscar elementos de chat.
```python
# Añadir espera de carga
import time
time.sleep(5) 
# Aumentar timeout de búsqueda
WebDriverWait(self.driver, 10).until(...)
```

---

## 🔄 Workflow de Recuperación (Si falla en el futuro)
Si el motor vuelve a decir "Authentication required":
1.  Detener el proceso del servidor.
2.  Ejecutar el comando de "Login Humano" (Punto 3).
3.  Verificar acceso visualmente.
4.  Reiniciar servidor.

---
*Este documento debe ser consultado antes de reinstalar o actualizar cualquier herramienta de NotebookLM.*
