# Phase 3 — Server Core Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 5 | TC-005 | Server foundation — startup, nickname registration, CLI args | M | 3 — Server Core | TC-004 |
| 6 | TC-006 | Room management | M | 3 — Server Core | TC-005 |
| 7 | TC-007 | Chat and whisper routing | M | 3 — Server Core | TC-006 |
| 8 | TC-008 | Rate limiting | S | 3 — Server Core | TC-005 |
| 9 | TC-009 | Graceful shutdown | S | 3 — Server Core | TC-005 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-004 (models) [Phase 2]
    |
TC-005 (server foundation)
    |
    +--------+--------+
    v        v        v
TC-006   TC-008   TC-009
(rooms)  (rate)   (shutdown)
    |
TC-007 (chat/whisper)
```

**Parallelization hints:**

- TC-006, TC-008, and TC-009 can run in parallel after TC-005

---

### TC-005 — Server foundation — startup, nickname registration, CLI args

**Description:**
Build the server entry point with TCP listener, connection lifecycle, nickname validation, and CLI argument parsing.

**What needs to be done:**
- `src/server.py` — `asyncio.start_server` on `0.0.0.0:<port>`
- `ConnectedClient` dataclass with nick, writer, rooms, rate limit state
- Connection handler: await `join` message (10s timeout via `asyncio.wait_for`), validate nick, send `welcome` or `error`
- Nick validation: 2–16 chars, `[a-zA-Z0-9_-]`, case-insensitive uniqueness
- CLI: `argparse` with `--port` (default 9000), `--log-level` (default INFO)
- Structured logging via `logging` module

**Dependencies:** TC-004

**Expected result:**
Server starts, accepts connections, validates nicknames, sends welcome/error responses.

**Acceptance criteria:**
- [ ] Server listens on configurable port (default 9000)
- [ ] Valid nickname → `welcome` response with room list
- [ ] Duplicate nickname → `error: nick_taken`
- [ ] Invalid nickname → `error: nick_invalid`
- [ ] Connection without `join` within 10s → timeout and close
- [ ] `--port` and `--log-level` CLI flags work
- [ ] Structured log output on connections

---

### TC-006 — Room management

**Description:**
Implement multi-room support: create, join, leave, list rooms, and list users. Rooms auto-delete when empty (except `general`).

**What needs to be done:**
- `join_room` handler — create room if not exists, add user, broadcast `user_joined`
- `leave_room` handler — remove user, broadcast `user_left`, auto-delete if empty
- `list_rooms` handler — respond with room names and user counts
- `list_users` handler — respond with user list for requested room
- Room name validation: 1–24 chars, `[a-zA-Z0-9_-]`
- Max 10 rooms active simultaneously
- `general` room cannot be deleted

**Dependencies:** TC-005

**Expected result:**
Users can create, join, leave, and query rooms. Empty rooms auto-delete.

**Acceptance criteria:**
- [ ] New user auto-joins `general` on connect
- [ ] `/join dev` creates room and adds user
- [ ] `/leave dev` removes user and deletes room if empty
- [ ] `general` cannot be deleted even when empty
- [ ] `list_rooms` returns all rooms with user counts
- [ ] `list_users` returns users in specified room
- [ ] 11th room creation returns error
- [ ] Room names validated (reject invalid chars, too long)

---

### TC-007 — Chat and whisper routing

**Description:**
Implement message routing: broadcast chat to room members, and private whisper delivery to specific users.

**What needs to be done:**
- `chat` handler — validate sender is in the room, broadcast `chat` to all room members
- `whisper` handler — find target by nick, send `whisper` message, return `error: user_not_found` if offline
- Message body validation: max 2000 characters → `error: msg_too_long`
- `user_joined` / `user_left` broadcast on connect/disconnect to all affected rooms

**Dependencies:** TC-006

**Expected result:**
Messages route correctly — chat to room, whisper to individual. Join/leave notifications broadcast.

**Acceptance criteria:**
- [ ] Chat message from Alice in `general` received by all `general` members
- [ ] Chat message NOT received by users not in the room
- [ ] Whisper from Alice to Bob received only by Bob
- [ ] Whisper to offline user returns `error: user_not_found`
- [ ] Message > 2000 chars returns `error: msg_too_long`
- [ ] `user_joined` notification sent to room members on join
- [ ] `user_left` notification sent to room members on disconnect

---

### TC-008 — Rate limiting

**Description:**
Implement per-client token bucket rate limiting to prevent message flooding.

**What needs to be done:**
- Token bucket: 5 tokens, refill 1 per second
- Check and deduct token before processing each chat/whisper message
- On violation: send `error: rate_limited`, drop the message
- Refill based on elapsed time since last refill

**Dependencies:** TC-005

**Expected result:**
Rapid message sending triggers rate limiting after 5 messages. Normal-paced conversation is unaffected.

**Acceptance criteria:**
- [ ] 5 messages in < 1 second all succeed
- [ ] 6th message in < 1 second returns `error: rate_limited`
- [ ] After 1 second wait, sending succeeds again (token refilled)
- [ ] Rate limiting is per-client (one client's rate limit doesn't affect others)

---

### TC-009 — Graceful shutdown

**Description:**
Handle SIGINT/SIGTERM to shut down the server cleanly — notify clients and close connections.

**What needs to be done:**
- Register signal handlers for `SIGINT` and `SIGTERM` using `loop.add_signal_handler`
- On signal: broadcast `system` message ("Server shutting down") to all connected clients
- Close all client `StreamWriter`s, stop the server, exit cleanly

**Dependencies:** TC-005

**Expected result:**
Ctrl+C on the server sends a shutdown notification to all clients before closing.

**Acceptance criteria:**
- [ ] SIGINT triggers graceful shutdown
- [ ] All connected clients receive `system: "Server shutting down"` message
- [ ] All connections closed after notification
- [ ] Server exits with code 0
