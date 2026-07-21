#!/bin/bash
# Wrapper MCP Gmail - cuenta 1 (usa el HOME por defecto).
# El protocolo MCP usa stdout: se suprime el ruido del profile.
{ source "$HOME/.profile"; } >/dev/null 2>&1
exec npx -y @gongrzhe/server-gmail-autoauth-mcp
