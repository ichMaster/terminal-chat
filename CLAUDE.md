# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-user terminal chat over TCP sockets with async Python and Textual TUI. Educational project for learning sockets, async I/O, and terminal UI programming. Python 3.12+.

## Development Commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # textual>=1.0.0 (only external dep)

python src/server.py --port 9000 --log-level INFO
python src/client.py --host 127.0.0.1 --port 9000 --nick alice

pytest tests/                              # all tests
pytest tests/test_protocol.py              # unit tests only
pytest tests/test_server.py                # integration tests (real TCP)
```

## Architecture

Client-server over TCP using newline-delimited JSON (`\n`-framed, max 8 KB per message). All state is in-memory, no database.

- **`src/protocol.py`** — Wire format: `encode()`, `decode()`, `read_message()`, `write_message()`. Shared by server and client. Auto-adds ISO-8601 UTC timestamps.
- **`src/models.py`** — Dataclasses: `User`, `Room`, `ChatMessage`.
- **`src/server.py`** — `asyncio.start_server` loop. Manages `clients: dict[str, ConnectedClient]` (nick → client) and `rooms: dict[str, set[str]]` (room → nicks). Handles join/nick validation, room lifecycle, whisper routing, token-bucket rate limiting (5 tokens, 1/sec refill), and SIGINT/SIGTERM graceful shutdown.
- **`src/client.py`** — Entry point, connects and hands off to TUI.
- **`src/tui/app.py`** — Textual `App` subclass. Socket reader runs as a `self.run_worker()` background task, posts custom Textual messages (`ServerMessage`, `Disconnected`) to update widgets on the UI thread.
- **`src/tui/widgets.py`** — Custom widgets: ChatLog, UserList, RoomList.
- **`src/tui/styles.tcss`** — Textual CSS for layout and theming.

### Key Design Decisions

- Standard library only for networking (`asyncio` streams, not raw `socket`); `textual` is the sole external dependency.
- Nicknames: 2–16 chars, `[a-zA-Z0-9_-]`, case-insensitive uniqueness.
- Room `general` is permanent and auto-joined; other rooms auto-delete when empty. Max 10 rooms.
- The Textual app integrates the socket reader via `run_worker()` — UI updates must go through Textual's message system, not direct widget mutation from the reader coroutine.

## Specification Documents

- `specification/spec-terminal-chat-tui.md` — Full technical specification (wire protocol, server/client behavior, TUI layout, message types, error codes)
- `specification/plan-terminal-chat-phased-learning.md` — Phased learning plan with exercises and concepts per phase
- `specification/roadmap/roadmap-v1.md` — Phase overview (8 phases), feature list, dependencies
- `specification/roadmap/implementation/all-phases-tasks.md` — Detailed task tables per phase/subsection (issue cross-references)
- `specification/roadmap/implementation/phase-{1..8}-issues.md` — Issue definitions (TC-001 to TC-021) with descriptions, acceptance criteria, dependency trees — one file per phase

## Phased Implementation Plan

8 phases, 21 issues (TC-001 to TC-021). Each phase produces a runnable artifact. Implement in order.

1. **TCP Foundations** (TC-001, TC-002) — Blocking echo → async multi-client broadcast
2. **Wire Protocol** (TC-003, TC-004) — JSON framing, data models, protocol tests
3. **Server Core** (TC-005–TC-009) — Nicks, rooms, chat/whisper, rate limit, shutdown
4. **CLI Client** (TC-010) — Async stdin + socket, slash commands, full protocol validation
5. **TUI Layout** (TC-011, TC-012) — Textual shell with static data, TCSS styling
6. **TUI Integration** (TC-013–TC-015) — Socket worker, message handlers, slash commands
7. **Polish** (TC-016–TC-018) — Reconnection, nick prompt, scroll/history, input validation
8. **Testing** (TC-019–TC-021) — Unit tests, integration tests, README
