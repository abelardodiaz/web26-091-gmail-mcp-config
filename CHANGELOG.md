# Changelog

Todos los cambios notables de este proyecto seran documentados en este archivo.

El formato esta basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

---

## [0.1.0] - 2026-07-20

### Agregado

- Wrappers multi-cuenta: `wrappers/run-mcp.sh` (cuenta 1, HOME por defecto) y
  `wrappers/run-mcp-cuenta2.sh` (cuenta 2, HOME alterno editable). Una instancia
  del servidor MCP por cuenta de Gmail, cada una con sus credenciales aisladas
  en su propio `$HOME/.gmail-mcp/`.
- `scripts/ejemplo-send-mcp-directo.py` — fallback JSON-RPC stdio para enviar
  correo sin cliente MCP (util cuando la sesion del agente no recargo tools).
- `README.md` con guia completa: requisitos, OAuth por cuenta en Google Cloud,
  autenticacion, registro en Claude Code desde Windows y notas de uso.
- `.gitignore` que bloquea credenciales (`*credentials*.json`, `*gcp-oauth*.json`,
  `*client_secret*.json`, `*.token`) y notas privadas locales (`PRIVATE-NOTES.md`).
- Regularizacion por 996: `PROJECT.yaml`, `CHANGELOG.md` y `CLAUDE.md`.
