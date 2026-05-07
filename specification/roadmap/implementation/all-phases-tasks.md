# Terminal Chat — All Phases Tasks

## Phase 1 — TCP Foundations

### 1.1 Synchronous echo server (`echo_server.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Create `echo_server.py` using `socket` module — `AF_INET`, `SOCK_STREAM`, bind to `127.0.0.1:9000` | TC-001 |
| 2 | Implement `listen(1)` → `accept()` → `recv(1024)` → `sendall()` loop for single client | TC-001 |
| 3 | Handle `ConnectionResetError` on abrupt client disconnect | TC-001 |
| 4 | Print client `addr` (IP + ephemeral port) on connect/disconnect | TC-001 |

### 1.2 Synchronous echo client (`echo_client.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Create `echo_client.py` — connect to `127.0.0.1:9000`, send a line, print echo, disconnect | TC-001 |
| 2 | Add input loop — read from stdin, send, print response, repeat until EOF | TC-001 |

### 1.3 Async multi-client echo server (`async_echo_server.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Create `async_echo_server.py` using `asyncio.start_server` with `handle_client(reader, writer)` coroutine | TC-002 |
| 2 | Read lines with `reader.readline()`, echo back with `writer.write()` + `writer.drain()` | TC-002 |
| 3 | Track connected clients in `clients: list[asyncio.StreamWriter]` | TC-002 |
| 4 | Implement broadcast — when one client sends, relay to all other connected clients | TC-002 |
| 5 | Handle `ConnectionResetError` and clean up client list on disconnect | TC-002 |
| 6 | Log connect/disconnect events with `peername` | TC-002 |

---

## Phase 2 — Wire Protocol

### 2.1 Protocol module (`src/protocol.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Create project structure: `src/` package with `__init__.py` | TC-003 |
| 2 | Implement `MAX_MSG_SIZE = 8192` constant | TC-003 |
| 3 | Implement `encode(msg: dict) -> bytes` — auto-add ISO-8601 UTC timestamp, serialize to JSON, append `\n`, encode UTF-8 | TC-003 |
| 4 | Implement `decode(line: bytes) -> dict` — decode UTF-8, strip, parse JSON | TC-003 |
| 5 | Implement `async read_message(reader: asyncio.StreamReader) -> dict | None` — read one line, return `None` on EOF, raise `ValueError` if exceeds `MAX_MSG_SIZE` | TC-003 |
| 6 | Implement `async write_message(writer: asyncio.StreamWriter, msg: dict) -> None` — encode and send with drain | TC-003 |
| 7 | Handle `json.JSONDecodeError` gracefully in `decode()` | TC-003 |

### 2.2 Data models (`src/models.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Define `User` dataclass — `nick: str`, `rooms: set[str]` | TC-004 |
| 2 | Define `Room` dataclass — `name: str`, `members: set[str]` | TC-004 |
| 3 | Define `ChatMessage` dataclass — `nick: str`, `room: str`, `body: str`, `ts: str` | TC-004 |

### 2.3 Protocol tests (`tests/test_protocol.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Create `tests/` directory with `__init__.py` and `conftest.py` | TC-003 |
| 2 | Test encode/decode roundtrip for all 8 client-to-server message types (`join`, `chat`, `join_room`, `leave_room`, `list_rooms`, `list_users`, `whisper`, `quit`) | TC-003 |
| 3 | Test encode/decode roundtrip for all 8 server-to-client message types (`welcome`, `chat`, `whisper`, `system`, `room_list`, `user_list`, `error`, `user_joined`, `user_left`) | TC-003 |
| 4 | Test oversized message rejection (> 8 KB) | TC-003 |
| 5 | Test malformed JSON handling | TC-003 |
| 6 | Test `read_message` returns `None` on EOF | TC-003 |
| 7 | Test auto-timestamp injection in `encode()` | TC-003 |

---

## Phase 3 — Chat Server Core

### 3.1 Server state model (`src/server.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Define `ConnectedClient` dataclass — `nick: str`, `writer: asyncio.StreamWriter`, `rooms: set[str]`, `bucket_tokens: float`, `last_refill: float` | TC-005 |
| 2 | Initialize server state: `clients: dict[str, ConnectedClient]` (nick → client), `rooms: dict[str, set[str]]` (room → nicks) | TC-005 |
| 3 | Create default `general` room on startup | TC-005 |

### 3.2 Connection lifecycle and nickname registration

| # | Task | Issue |
|---|------|-------|
| 1 | Implement `asyncio.start_server` on `0.0.0.0:<port>` (default `9000`, configurable via `--port`) | TC-005 |
| 2 | On new connection, await `join` message with `asyncio.wait_for()` (10-second timeout) | TC-005 |
| 3 | Validate nickname: length 2–16, regex `[a-zA-Z0-9_-]`, case-insensitive uniqueness | TC-005 |
| 4 | On valid nick: add to `clients`, auto-join `general`, send `welcome` message with room list | TC-005 |
| 5 | On invalid nick: send `error` (`nick_taken` or `nick_invalid`), close connection | TC-005 |
| 6 | Enter message loop after successful join | TC-005 |

### 3.3 Room management

| # | Task | Issue |
|---|------|-------|
| 1 | Implement `join_room` handler — create room if not exists (max 10 rooms), add user, broadcast `user_joined` | TC-006 |
| 2 | Implement `leave_room` handler — remove user, broadcast `user_left`, auto-delete room if empty (except `general`) | TC-006 |
| 3 | Implement `list_rooms` handler — respond with `room_list` (name + user count for each room) | TC-006 |
| 4 | Implement `list_users` handler — respond with `user_list` for requested room | TC-006 |
| 5 | Validate room names: 1–24 chars, `[a-zA-Z0-9_-]` | TC-006 |

### 3.4 Chat and whisper routing

| # | Task | Issue |
|---|------|-------|
| 1 | Implement `chat` handler — validate sender is in room, broadcast to all members | TC-007 |
| 2 | Implement `whisper` handler — find target nick, send `whisper` directly, return `error: user_not_found` if offline | TC-007 |
| 3 | Validate message body length (max 2000 chars), return `error: msg_too_long` | TC-007 |
| 4 | Broadcast `user_joined` / `user_left` notifications on connect/disconnect to all affected rooms | TC-007 |

### 3.5 Rate limiting

| # | Task | Issue |
|---|------|-------|
| 1 | Implement token bucket: bucket size 5, refill rate 1/sec | TC-008 |
| 2 | Check tokens before processing each message | TC-008 |
| 3 | On violation: send `error: rate_limited`, drop the message (do not broadcast) | TC-008 |
| 4 | Refill tokens based on elapsed time since `last_refill` | TC-008 |

### 3.6 Graceful shutdown

| # | Task | Issue |
|---|------|-------|
| 1 | Register handlers for `SIGINT` and `SIGTERM` | TC-009 |
| 2 | On signal: broadcast `system` message ("Server shutting down") to all connected clients | TC-009 |
| 3 | Close all client writers, stop the server, exit cleanly | TC-009 |

### 3.7 CLI arguments

| # | Task | Issue |
|---|------|-------|
| 1 | Add `argparse` with `--port` (default `9000`) and `--log-level` (default `INFO`) | TC-005 |
| 2 | Configure `logging` module with structured format | TC-005 |

---

## Phase 4 — CLI Client

### 4.1 Simple async client (`simple_client.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Create `simple_client.py` with `argparse`: `--host` (default `127.0.0.1`), `--port` (default `9000`), `--nick` (required) | TC-010 |
| 2 | Connect via `asyncio.open_connection`, send `join` message, await `welcome` or `error` | TC-010 |
| 3 | Implement `receive_loop(reader)` — read server messages, format and print to stdout | TC-010 |
| 4 | Implement `send_loop(writer)` — read stdin via `run_in_executor`, parse slash commands or send chat | TC-010 |
| 5 | Run both loops concurrently with `asyncio.gather` | TC-010 |
| 6 | Implement slash command parsing: `/join`, `/leave`, `/rooms`, `/users`, `/whisper`, `/nick`, `/help`, `/quit` | TC-010 |
| 7 | Handle server disconnect — print message, exit | TC-010 |
| 8 | Format output: timestamps `[HH:MM]`, system messages with `--`, errors with `[!]` | TC-010 |

---

## Phase 5 — TUI Layout

### 5.1 Textual app shell (`src/tui/app.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | Create `src/tui/` package with `__init__.py` | TC-011 |
| 2 | Implement `ChatApp(App)` with `CSS_PATH = "styles.tcss"` | TC-011 |
| 3 | Implement `compose()`: `Header` → `Horizontal` container with `RichLog` (id=`chat-log`) + `Vertical` sidebar (id=`sidebar`) → `Input` → `Footer` | TC-011 |
| 4 | Sidebar contains: `Static("Users")` + `ListView` (id=`user-list`) + `Static("Rooms")` + `ListView` (id=`room-list`) | TC-011 |
| 5 | Set `Input` placeholder: `"Type a message... (/help for commands)"` | TC-011 |
| 6 | Add keybindings: F1 Help, F2 Rooms, F3 Users, F4 Whisper, Ctrl+C Quit | TC-011 |
| 7 | Implement `on_mount()` — populate chat log with hardcoded sample messages | TC-011 |
| 8 | Implement `on_input_submitted()` — clear input on Enter | TC-011 |

### 5.2 Textual CSS (`src/tui/styles.tcss`)

| # | Task | Issue |
|---|------|-------|
| 1 | Layout: chat-log takes remaining width, sidebar fixed 25 chars wide, docked right | TC-012 |
| 2 | Header: app title + current room indicator `[room: #general]` | TC-012 |
| 3 | Message styles: own message (highlighted nick), system (dimmed, `--` prefix), error (red, `[!]` prefix), whisper (italic) | TC-012 |
| 4 | Timestamp style: dimmed `[HH:MM]` | TC-012 |
| 5 | Footer: keybinding hints | TC-012 |
| 6 | Verify responsive behavior on terminal resize | TC-012 |

### 5.3 Custom widgets (`src/tui/widgets.py`)

| # | Task | Issue |
|---|------|-------|
| 1 | `ChatLog` — wrapper around `RichLog` with methods for each message type (chat, system, error, whisper) | TC-011 |
| 2 | `UserList` — `ListView` that updates from a list of nick strings | TC-011 |
| 3 | `RoomList` — `ListView` with click-to-switch behavior, highlight active room | TC-011 |

---

## Phase 6 — TUI Network Integration

### 6.1 Custom Textual messages

| # | Task | Issue |
|---|------|-------|
| 1 | Define `ServerMessage(Message)` — wraps a decoded server message dict | TC-013 |
| 2 | Define `Disconnected(Message)` — signals connection loss | TC-013 |

### 6.2 Socket reader worker

| # | Task | Issue |
|---|------|-------|
| 1 | Implement `socket_reader()` async method — loop calling `read_message(self.reader)`, post `ServerMessage` or `Disconnected` | TC-013 |
| 2 | Launch as `self.run_worker(self.socket_reader(), exclusive=True)` in `on_mount()` | TC-013 |
| 3 | Handle `ConnectionResetError` and EOF in the worker | TC-013 |

### 6.3 Connection setup

| # | Task | Issue |
|---|------|-------|
| 1 | In `on_mount()`: `asyncio.open_connection(host, port)`, send `join`, await `welcome` | TC-013 |
| 2 | On `error` response: show error in chat log, prompt for different nick | TC-013 |
| 3 | Store `self.reader`, `self.writer`, `self.nick`, `self.current_room` | TC-013 |

### 6.4 Server message handlers

| # | Task | Issue |
|---|------|-------|
| 1 | `on_server_message()` dispatcher — route by `msg["type"]` | TC-014 |
| 2 | Handle `chat` — render in chat log with timestamp, nick, styling for own vs other | TC-014 |
| 3 | Handle `whisper` — render italic with `[whisper from/to <nick>]` prefix | TC-014 |
| 4 | Handle `system` — render dimmed, centered with `--` prefix | TC-014 |
| 5 | Handle `error` — render red with `[!]` prefix | TC-014 |
| 6 | Handle `user_joined` / `user_left` — update user list widget, show notification in chat log | TC-014 |
| 7 | Handle `room_list` — update room list widget | TC-014 |
| 8 | Handle `user_list` — update user list widget | TC-014 |

### 6.5 Slash command integration

| # | Task | Issue |
|---|------|-------|
| 1 | Parse input for `/` prefix in `on_input_submitted()` | TC-015 |
| 2 | `/join <room>` — send `join_room` message, update sidebar | TC-015 |
| 3 | `/leave <room>` — send `leave_room` message, switch room if leaving active room | TC-015 |
| 4 | `/rooms` — send `list_rooms` request | TC-015 |
| 5 | `/users` — send `list_users` for current room | TC-015 |
| 6 | `/whisper <nick> <message>` — send `whisper` message, show outgoing whisper in chat log | TC-015 |
| 7 | `/nick` — display current nickname in chat log (local only) | TC-015 |
| 8 | `/clear` — clear chat log (local only) | TC-015 |
| 9 | `/help` — render command reference in chat log (local only) | TC-015 |
| 10 | `/quit` — send `quit` message, close connection, exit app | TC-015 |
| 11 | Non-slash input — send `chat` message to current room | TC-015 |

### 6.6 Room switching

| # | Task | Issue |
|---|------|-------|
| 1 | Click room in sidebar → set `self.current_room`, update header indicator | TC-014 |
| 2 | Messages typed go to `self.current_room` | TC-014 |
| 3 | Update user list to show members of active room | TC-014 |

---

## Phase 7 — Polish and Edge Cases

### 7.1 Reconnection logic

| # | Task | Issue |
|---|------|-------|
| 1 | On `Disconnected` event: show overlay with "Connection lost" message | TC-016 |
| 2 | Implement retry with exponential backoff (1s, 2s, 4s, 8s, max 30s) | TC-016 |
| 3 | On reconnect: re-send `join`, re-join previously joined rooms | TC-016 |
| 4 | Show reconnection progress in overlay | TC-016 |

### 7.2 Nickname prompt screen

| # | Task | Issue |
|---|------|-------|
| 1 | If `--nick` not passed via CLI, show Textual `Input` screen on startup | TC-017 |
| 2 | Validate nick format client-side before sending `join` | TC-017 |
| 3 | On `nick_taken` error, return to prompt with error message | TC-017 |

### 7.3 UX polish

| # | Task | Issue |
|---|------|-------|
| 1 | Auto-scroll to bottom on new messages; pause auto-scroll when user scrolls up | TC-018 |
| 2 | Per-room message buffer — store last 200 messages per room client-side, restore on room switch | TC-018 |
| 3 | Input validation — prevent sending empty messages, show inline error | TC-018 |
| 4 | Timestamp formatting — convert to local timezone, dimmed `[HH:MM]` style | TC-018 |
| 5 | Ctrl+C handling — send `quit` to server before exiting | TC-018 |

---

## Phase 8 — Testing and Documentation

### 8.1 Test fixtures

| # | Task | Issue |
|---|------|-------|
| 1 | Create `tests/conftest.py` with shared fixtures (event loop, server factory, client factory) | TC-019 |
| 2 | Create helper: `async_client()` — connect, send join, return (reader, writer) pair | TC-019 |

### 8.2 Unit tests

| # | Task | Issue |
|---|------|-------|
| 1 | `test_protocol.py` — encode/decode roundtrip for every message type, oversized rejection, malformed JSON, EOF handling | TC-019 |
| 2 | `test_models.py` — dataclass instantiation and field defaults | TC-019 |
| 3 | `test_nick_validation.py` — too short, too long, invalid chars, duplicates, case insensitivity | TC-019 |
| 4 | `test_rate_limiter.py` — token bucket math, refill timing, burst rejection | TC-019 |
| 5 | `test_room_logic.py` — create, join, leave, auto-delete, max 10 rooms, `general` permanence | TC-019 |

### 8.3 Integration tests

| # | Task | Issue |
|---|------|-------|
| 1 | `test_server_chat.py` — two async clients register, chat, verify message delivery | TC-020 |
| 2 | `test_server_rooms.py` — join/leave rooms, room auto-delete, room list query | TC-020 |
| 3 | `test_server_whisper.py` — whisper delivery, user_not_found error | TC-020 |
| 4 | `test_server_rate_limit.py` — send burst, verify rate_limited error after 5th message | TC-020 |
| 5 | `test_server_disconnect.py` — client disconnect triggers user_left in all rooms, cleanup | TC-020 |
| 6 | `test_server_shutdown.py` — SIGINT sends system message, clients receive it, server exits | TC-020 |
| 7 | `test_server_edge_cases.py` — oversized message rejection, duplicate nick, join timeout | TC-020 |

### 8.4 Documentation

| # | Task | Issue |
|---|------|-------|
| 1 | Expand `README.md` — project overview, screenshot, setup instructions (venv, install, run) | TC-021 |
| 2 | Add architecture diagram (ASCII) to README | TC-021 |
| 3 | Add slash command reference table to README | TC-021 |
| 4 | Add `requirements.txt` with `textual>=1.0.0`, `pytest>=7.0`, `pytest-asyncio>=0.21.0` | TC-021 |
