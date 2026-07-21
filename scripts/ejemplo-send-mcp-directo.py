"""Ejemplo: enviar un correo hablando al servidor MCP Gmail por JSON-RPC stdio.

Util cuando el servidor MCP se registro despues de iniciar la sesion del
agente y sus herramientas aun no estan cargadas. Ajusta WRAPPER, destinatario
y adjuntos. Los adjuntos van con ruta WSL (/mnt/c/...).
"""
import json
import subprocess
import threading
import sys

WRAPPER = ["wsl", "/home/USUARIO/.gmail-mcp/run-mcp.sh"]  # o run-mcp-cuenta2.sh

ARGUMENTS = {
    "to": ["destinatario@ejemplo.com"],
    "subject": "Asunto de ejemplo",
    "body": "Cuerpo del mensaje en texto plano.",
    # "attachments": ["/mnt/c/Users/USUARIO/ruta/archivo.pdf"],
}

proc = subprocess.Popen(
    WRAPPER, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
)

def send(msg):
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()

send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                 "clientInfo": {"name": "send-script", "version": "1.0"}}})

result = {"done": False}

def reader():
    for line in proc.stdout:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("id") == 1:
            send({"jsonrpc": "2.0", "method": "notifications/initialized"})
            send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                  "params": {"name": "send_email", "arguments": ARGUMENTS}})
        elif msg.get("id") == 2:
            print("RESPUESTA:", json.dumps(msg, ensure_ascii=False)[:500])
            result["done"] = True
            break

t = threading.Thread(target=reader, daemon=True)
t.start()
t.join(timeout=120)  # npx puede tardar en arrancar
proc.terminate()
if not result["done"]:
    print("TIMEOUT: sin respuesta en 120s")
    sys.exit(1)
