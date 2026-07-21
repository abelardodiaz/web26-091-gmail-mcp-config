---
name: enviar-correos
description: Enviar correos (con o sin adjuntos) desde dos cuentas Gmail via los servidores MCP multi-cuenta de este repo (gmail-cuenta1 / gmail-cuenta2). Usar cuando el usuario pida "envia un correo", "mandale el archivo a X", "responde el correo" o cualquier envio de email saliente. Cubre eleccion de cuenta, adjuntos con ruta WSL, confirmacion previa obligatoria y fallback por protocolo MCP directo si las herramientas no estan cargadas en la sesion.
---

# Enviar correos (multi-cuenta Gmail MCP)

Skill para Claude Code (o cualquier agente que soporte skills) sobre la
configuracion multi-cuenta de este repo. Ajusta nombres de servidor, cuentas y
rutas a tu instalacion.

## Cuentas disponibles

| Servidor MCP | Cuenta | Uso tipico |
|---|---|---|
| `gmail-cuenta1` | cuenta1@ejemplo.com | (describe aqui el uso de tu cuenta 1) |
| `gmail-cuenta2` | cuenta2@ejemplo.com | (describe aqui el uso de tu cuenta 2) |

Ambos corren en WSL con el paquete `@gongrzhe/server-gmail-autoauth-mcp` y
tienen las MISMAS herramientas (`send_email`, `search_emails`, `read_email`,
`draft_email`, etc.); solo cambia el prefijo: `mcp__gmail-cuenta1__*` o
`mcp__gmail-cuenta2__*`.

## Reglas de oro

1. **Confirmar antes de enviar, SIEMPRE.** Mostrar al usuario: De (cuenta),
   Para, Asunto, cuerpo completo y adjuntos, y esperar su OK explicito.
   Frases como "y si le enviamos...?" son pregunta, no orden.
   - **El cuerpo se muestra COMPLETO y LITERAL en cada confirmacion**, palabra
     por palabra tal como saldra. Prohibido referenciar versiones anteriores
     ("el mismo de arriba", "sin cambios"): cada confirmacion repite el correo
     entero, incluso tras un ajuste minimo.
   - **Redaccion con esfuerzo real**: el cuerpo debe ser un correo bien escrito
     para el contexto (destinatario, relacion, objetivo), no un placeholder.
2. **Que cuenta usar:** si el usuario no la dice, preguntar o deducir por
   contexto. Nunca asumir en silencio: un envio desde la cuenta equivocada
   molesta y no se puede deshacer.
3. **Adjuntos = ruta WSL.** Los servidores corren en WSL: convertir
   `C:\ruta\archivo` a `/mnt/c/ruta/archivo`. Rutas con espacios van tal cual
   en el JSON (sin escapar).
4. **Destinatarios:** verificar la direccion en correos enviados previos
   (`search_emails` con `in:sent`) antes de enviar a alguien nuevo. No adivinar
   dominios.
5. **Borrar correos/borradores:** solo papelera, nunca borrado definitivo.
6. Cuerpos en texto plano sin emojis; los acentos son validos pero asunto y
   cuerpo deben sobrevivir UTF-8.

## Envio normal (herramientas cargadas)

Si el cliente difiere herramientas, cargarlas primero (en Claude Code:
ToolSearch con `select:mcp__gmail-cuenta1__send_email`).

Llamada tipica:

```json
{
  "to": ["destinatario@ejemplo.com"],
  "subject": "Asunto",
  "body": "Cuerpo en texto plano",
  "attachments": ["/mnt/c/Users/USUARIO/ruta/archivo.pdf"]
}
```

La respuesta exitosa regresa `Email sent successfully with ID: <id>`.
Reportar ese ID al usuario como comprobante.

## Fallback: servidor no cargado en la sesion

Si el servidor MCP se registro con la sesion del agente ya abierta, sus
herramientas pueden no estar disponibles. En vez de reiniciar, hablarle al
servidor por JSON-RPC stdio directamente:

- Comando cuenta 1: `wsl /home/USUARIO/.gmail-mcp/run-mcp.sh`
- Comando cuenta 2: `wsl /home/USUARIO/.gmail-mcp/run-mcp-cuenta2.sh`

Secuencia MCP: (1) `initialize` con `protocolVersion: 2024-11-05`,
(2) notificacion `notifications/initialized`, (3) `tools/call` con
`name: "send_email"` y los argumentos de arriba. Leer stdout linea por linea
hasta la respuesta con `id: 2` (timeout 120s: npx tarda en arrancar la primera
vez). Ejemplo funcional: `scripts/ejemplo-send-mcp-directo.py`.

## Instalacion de esta skill

Copiala a tu carpeta de skills globales y edita cuentas/rutas:

```bash
mkdir -p ~/.claude/skills/enviar-correos
cp skills/enviar-correos/SKILL.md ~/.claude/skills/enviar-correos/
```

En Windows la carpeta es `C:\Users\USUARIO\.claude\skills\`.
