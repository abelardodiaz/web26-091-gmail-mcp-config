# gmail-mcp-config

Configuracion multi-cuenta del servidor MCP de Gmail
([@gongrzhe/server-gmail-autoauth-mcp](https://github.com/GongRzhe/Gmail-MCP-Server))
corriendo en WSL, para usarlo desde Claude Code (u otro cliente MCP) en Windows.

La idea clave: **una instancia por cuenta de Gmail, cada una con su propio HOME**.
El paquete guarda sus credenciales en `$HOME/.gmail-mcp/`, asi que cambiando el
HOME del proceso cada instancia lee y escribe credenciales separadas, sin
variables especiales ni forks del paquete. Multi-cuenta real sin intercambiar auth.

```
wrappers/run-mcp.sh          -> cuenta 1 (HOME por defecto)
wrappers/run-mcp-cuenta2.sh  -> cuenta 2 (HOME alterno, editable)
scripts/ejemplo-send-mcp-directo.py -> fallback JSON-RPC stdio sin cliente MCP
```

## Requisitos

- WSL con Node.js/npx en el PATH del profile
- Un proyecto de Google Cloud por cuenta (o uno compartido si ambas cuentas
  pueden usar el mismo client OAuth) con **Gmail API habilitada**
- Client OAuth tipo **Desktop (installed)**; si la app esta en modo Prueba,
  agrega cada cuenta como *test user*

## Instalacion

1. Copia los wrappers a `~/.gmail-mcp/` en WSL y dales `chmod +x`.
   En `run-mcp-cuenta2.sh` ajusta `ALT_HOME` si quieres otra carpeta.
2. Descarga el JSON del client OAuth de cada cuenta (Google Cloud Console ->
   Google Auth Platform -> Clientes -> descargar JSON) y colocalo como
   `gcp-oauth.keys.json` en la carpeta de credenciales de cada instancia:
   - cuenta 1: `~/.gmail-mcp/gcp-oauth.keys.json`
   - cuenta 2: `<ALT_HOME>/.gmail-mcp/gcp-oauth.keys.json`
3. Autentica cada cuenta (abre la URL que imprime; callback en `localhost:3000`):
   ```bash
   npx -y @gongrzhe/server-gmail-autoauth-mcp auth                     # cuenta 1
   HOME=<ALT_HOME> npx -y @gongrzhe/server-gmail-autoauth-mcp auth     # cuenta 2
   ```
   Esto genera el `credentials.json` (token) de cada instancia.
4. Registra los servidores en Claude Code (desde Windows):
   ```bash
   claude mcp add --scope user gmail-cuenta1 -- wsl /home/USUARIO/.gmail-mcp/run-mcp.sh
   claude mcp add --scope user gmail-cuenta2 -- wsl /home/USUARIO/.gmail-mcp/run-mcp-cuenta2.sh
   claude mcp list   # ambos deben aparecer Connected
   ```

## Notas de uso

- **Adjuntos**: el servidor corre en WSL; las rutas de Windows van como
  `/mnt/c/...`, no `C:\...`.
- Ambas instancias exponen las mismas herramientas (`send_email`,
  `search_emails`, `read_email`, `draft_email`, etc.); cambia solo el prefijo
  del servidor.
- Si registraste un servidor con la sesion del agente ya abierta y sus
  herramientas no aparecen, usa `scripts/ejemplo-send-mcp-directo.py` como
  puente JSON-RPC temporal (o reinicia la sesion).

## Seguridad

- **Nunca** subas a git `credentials.json`, `gcp-oauth.keys.json` ni
  `client_secret*.json` (el `.gitignore` de este repo los bloquea).
- Los tokens se regeneran con el paso 3; el client JSON se re-descarga de la
  consola de GCP. No hay nada irrecuperable fuera del repo.
