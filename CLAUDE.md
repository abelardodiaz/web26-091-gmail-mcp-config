# CLAUDE.md - Gmail MCP Config (web26-091)

## PROJECT.yaml - IMPORTANTE

Este proyecto tiene un archivo `PROJECT.yaml` en la raiz. Es leido por el Project Manager (99999) para monitorear el estado.

**Cuando actualizar:**
- Cambio de version -> actualiza `project.version`
- Siempre actualiza `updated_at` y `updated_by: claude-091`

**NO modificar sin razon:**
- `project.code` - identificador unico
- `server.base_path` - ruta del proyecto (relativa a proposito, repo publico)

---

## Que es este proyecto

Mini repo de configuracion: multi-cuenta del servidor MCP de Gmail
([@gongrzhe/server-gmail-autoauth-mcp](https://github.com/GongRzhe/Gmail-MCP-Server))
corriendo en WSL, consumido desde Claude Code en Windows.

Idea clave: **una instancia por cuenta de Gmail, cada una con su propio HOME**.
El paquete guarda credenciales en `$HOME/.gmail-mcp/`; cambiando el HOME del
proceso, cada instancia lee credenciales separadas sin forks del paquete.

## Estructura

```
wrappers/run-mcp.sh                  -> cuenta 1 (HOME por defecto)
wrappers/run-mcp-cuenta2.sh          -> cuenta 2 (HOME alterno, editable)
scripts/ejemplo-send-mcp-directo.py  -> fallback JSON-RPC stdio sin cliente MCP
PRIVATE-NOTES.md                     -> mapeo real de esta maquina (GITIGNORED)
```

## Naturaleza dual: publico + produccion privada

- El **repo es publico** (GitHub `origin` + GitLab `gitlab`): solo wrappers
  genericos y guia. Nombres de cuenta reales, rutas reales y proyectos GCP
  viven en `PRIVATE-NOTES.md`, que esta gitignored y NUNCA se commitea.
- La **instalacion real** en esta maquina esta en produccion: los wrappers
  copiados a sus HOME definitivos y registrados en Claude Code (scope user).
  Ver `PRIVATE-NOTES.md` para el mapeo local.

## Politica de seguridad (CRITICA)

- NUNCA commitear `credentials.json`, `gcp-oauth.keys.json`, `client_secret*.json`
  ni `PRIVATE-NOTES.md`. El `.gitignore` los bloquea; no lo debilites.
- Antes de cualquier push, revisar `git status` por archivos de credenciales.
- Los tokens son regenerables (re-auth) y el client JSON se re-descarga de GCP;
  nada irrecuperable debe vivir en el repo.

## Convenciones

- Sin emojis en scripts (se corren tambien desde PowerShell).
- Cambios notables van al `CHANGELOG.md` (Keep a Changelog + SemVer).
- Ejemplos en README usan placeholders (`USUARIO`, `ALT_HOME`), nunca datos reales.
