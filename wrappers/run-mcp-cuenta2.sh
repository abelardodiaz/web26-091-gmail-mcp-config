#!/bin/bash
# Wrapper MCP Gmail - cuenta 2 (HOME alterno = credenciales separadas).
# EDITA ALT_HOME: carpeta dedicada a esta cuenta.
{ source "$HOME/.profile"; } >/dev/null 2>&1
ALT_HOME="$HOME/gmail-cuenta2-home"
mkdir -p "$ALT_HOME"
export HOME="$ALT_HOME"
exec npx -y @gongrzhe/server-gmail-autoauth-mcp
