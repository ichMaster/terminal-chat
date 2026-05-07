# Phase 2 — Wire Protocol Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 3 | TC-003 | Wire protocol module and tests | M | 2 — Wire Protocol | TC-002 |
| 4 | TC-004 | Shared data models | S | 2 — Wire Protocol | TC-003 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-002 (async echo) [Phase 1]
    |
TC-003 (protocol)
    |
TC-004 (models)
```

---

### TC-003 — Wire protocol module and tests

**Description:**
Implement the shared protocol module that defines message framing (newline-delimited JSON), serialization, and validation. This module is imported by both server and client.

**What needs to be done:**
- Create `src/protocol.py` with `encode()`, `decode()`, `read_message()`, `write_message()`
- `MAX_MSG_SIZE = 8192` — reject messages exceeding this
- Auto-inject ISO-8601 UTC timestamps in `encode()`
- Handle `json.JSONDecodeError` in `decode()`
- Create `tests/test_protocol.py` with roundtrip tests for all 16+ message types, oversized rejection, malformed JSON, EOF handling

**Dependencies:** TC-002

**Expected result:**
A robust protocol module with full test coverage for all message types defined in the spec.

**Acceptance criteria:**
- [ ] Encode/decode roundtrip for all client-to-server message types (join, chat, join_room, leave_room, list_rooms, list_users, whisper, quit)
- [ ] Encode/decode roundtrip for all server-to-client message types (welcome, chat, whisper, system, room_list, user_list, error, user_joined, user_left)
- [ ] Messages > 8 KB raise `ValueError`
- [ ] Malformed JSON raises appropriate error
- [ ] `read_message()` returns `None` on EOF
- [ ] Timestamps auto-injected by `encode()`
- [ ] `pytest tests/test_protocol.py` passes

---

### TC-004 — Shared data models

**Description:**
Define the core dataclasses used by the server to track state: users, rooms, and chat messages.

**What needs to be done:**
- `src/models.py` with `User`, `Room`, `ChatMessage` dataclasses
- `User`: `nick: str`, `rooms: set[str]`
- `Room`: `name: str`, `members: set[str]`
- `ChatMessage`: `nick: str`, `room: str`, `body: str`, `ts: str`

**Dependencies:** TC-003

**Expected result:**
Clean dataclass definitions that the server and tests can import.

**Acceptance criteria:**
- [ ] `from src.models import User, Room, ChatMessage` works
- [ ] All dataclasses use type hints and `field(default_factory=set)` for mutable defaults
- [ ] Instantiation with valid data succeeds
