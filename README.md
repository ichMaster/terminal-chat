# terminal-chat

Multi-user terminal chat over TCP sockets with async Python and Textual TUI. Educational project for learning sockets, async I/O, and terminal UI programming.

## Prerequisites

- Python 3.12+

## Phase 1 — TCP Foundations

Phase 1 includes two standalone scripts that demonstrate core TCP concepts.

### Echo Server (blocking, single-client)

Start the server:

```bash
python3 echo_server.py
```

Connect with the client:

```bash
python3 echo_client.py
```

Or connect with telnet/netcat:

```bash
nc 127.0.0.1 9000
```

Type lines and they'll be echoed back. Only one client is served at a time — a second connection will hang until the first disconnects. This demonstrates the limitation that async solves.

### Async Echo Server (multi-client, broadcast)

Start the async server:

```bash
python3 async_echo_server.py
```

Connect multiple clients (each in a separate terminal):

```bash
nc 127.0.0.1 9000
```

Messages from any client are broadcast to all other connected clients. Disconnecting one client does not affect others.

## Project Roadmap

This project is built in 8 phases, each producing a runnable artifact:

1. **TCP Foundations** — blocking echo, async broadcast (current)
2. **Wire Protocol** — JSON framing and data models
3. **Server Core** — nicknames, rooms, whisper, rate limiting
4. **CLI Client** — async stdin + socket, slash commands
5. **TUI Layout** — Textual shell with static data
6. **TUI Integration** — socket worker, message handlers
7. **Polish** — reconnection, nick prompt, scroll/history
8. **Testing** — unit tests, integration tests, documentation
