# Phase 6 — TUI Network Integration Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 13 | TC-013 | Socket reader worker and connection setup | M | 6 — TUI Integration | TC-012 |
| 14 | TC-014 | Server message handlers and room switching | M | 6 — TUI Integration | TC-013 |
| 15 | TC-015 | Slash command integration | M | 6 — TUI Integration | TC-013 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-012 (TCSS) [Phase 5]
    |
TC-013 (socket worker)
    |
    +--------+
    v        v
TC-014   TC-015
(handlers) (commands)
```

**Parallelization hints:**

- TC-014 and TC-015 can run in parallel after TC-013

---

### TC-013 — Socket reader worker and connection setup

**Description:**
Connect the TUI to the real server. The socket reader runs as a Textual `Worker` background task, posting custom messages for UI-thread-safe widget updates.

**What needs to be done:**
- Define `ServerMessage(Message)` and `Disconnected(Message)` custom Textual messages
- Implement `socket_reader()` — loop reading from server, posting custom messages
- Launch via `self.run_worker(self.socket_reader(), exclusive=True)` in `on_mount()`
- Connection setup: `asyncio.open_connection`, send `join`, handle `welcome` or `error`
- Store `reader`, `writer`, `nick`, `current_room` as app state

**Dependencies:** TC-012

**Expected result:**
TUI connects to server, receives welcome, and displays incoming messages in real time.

**Acceptance criteria:**
- [ ] TUI connects to server on mount
- [ ] Welcome message displayed in chat log
- [ ] Incoming server messages appear in real time
- [ ] Connection failure shows error message
- [ ] No UI freezing — socket reader runs in background

---

### TC-014 — Server message handlers and room switching

**Description:**
Route incoming server messages to appropriate widget updates. Implement room switching via sidebar click.

**What needs to be done:**
- `on_server_message()` dispatcher routing by `msg["type"]`
- Handle all server message types: chat, whisper, system, error, user_joined, user_left, room_list, user_list
- Room switching: click room in sidebar → update `current_room`, header, user list
- Messages sent go to the active room

**Dependencies:** TC-013

**Expected result:**
All server messages render correctly in the TUI. Room switching works via sidebar.

**Acceptance criteria:**
- [ ] Chat messages render with timestamp and nick
- [ ] Whisper messages render with italic styling
- [ ] System messages render dimmed
- [ ] Error messages render red
- [ ] User list updates on join/leave events
- [ ] Clicking room in sidebar switches active room
- [ ] Header updates to show active room name

---

### TC-015 — Slash command integration

**Description:**
Parse slash commands from the input bar and route to appropriate protocol messages.

**What needs to be done:**
- Parse `/` prefix in `on_input_submitted()`
- Implement all slash commands: `/join`, `/leave`, `/rooms`, `/users`, `/whisper`, `/nick`, `/clear`, `/help`, `/quit`
- Local commands (`/nick`, `/clear`, `/help`) don't send to server
- Non-slash input sends `chat` to current room

**Dependencies:** TC-013

**Expected result:**
All slash commands from the spec work in the TUI.

**Acceptance criteria:**
- [ ] `/join dev` sends `join_room` and updates sidebar on response
- [ ] `/leave dev` sends `leave_room` and updates sidebar
- [ ] `/whisper bob hello` sends whisper and shows outgoing in chat log
- [ ] `/rooms` and `/users` trigger list requests and display results
- [ ] `/help` renders command reference locally
- [ ] `/clear` clears chat log
- [ ] `/quit` sends quit and exits app
- [ ] Plain text sends chat to current room
