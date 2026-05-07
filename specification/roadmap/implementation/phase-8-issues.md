# Phase 8 — Testing & Documentation Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 19 | TC-019 | Unit tests | M | 8 — Testing | TC-018 |
| 20 | TC-020 | Integration tests | L | 8 — Testing | TC-019 |
| 21 | TC-021 | README and documentation | S | 8 — Testing | TC-020 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-018 (UX) [Phase 7]
    |
TC-019 (unit tests)
    |
TC-020 (integration tests)
    |
TC-021 (docs)
```

---

### TC-019 — Unit tests

**Description:**
Write unit tests covering the protocol, models, nickname validation, rate limiter, and room logic.

**What needs to be done:**
- `tests/conftest.py` with shared fixtures (event loop, server factory, client factory)
- `test_protocol.py` — all message type roundtrips, edge cases
- `test_models.py` — dataclass instantiation
- `test_nick_validation.py` — boundary cases for nick rules
- `test_rate_limiter.py` — token bucket math and timing
- `test_room_logic.py` — create, join, leave, auto-delete, max rooms

**Dependencies:** TC-018

**Expected result:**
All unit tests pass, covering protocol correctness, validation logic, and rate limiting.

**Acceptance criteria:**
- [ ] `pytest tests/test_protocol.py` passes — all message types
- [ ] Nick validation catches all edge cases (too short, too long, invalid chars, case-insensitive dupes)
- [ ] Rate limiter math verified (refill timing, burst rejection)
- [ ] Room logic verified (auto-delete, max rooms, general permanence)
- [ ] `pytest` runs clean with no warnings

---

### TC-020 — Integration tests

**Description:**
Write integration tests using real TCP connections to the server, validating end-to-end message flows.

**What needs to be done:**
- `test_server_chat.py` — two clients register, chat, verify delivery
- `test_server_rooms.py` — join/leave rooms, auto-delete, list queries
- `test_server_whisper.py` — whisper delivery, user_not_found error
- `test_server_rate_limit.py` — burst → rate_limited error
- `test_server_disconnect.py` — client disconnect triggers cleanup and notifications
- `test_server_shutdown.py` — SIGINT sends system message
- `test_server_edge_cases.py` — oversized messages, duplicate nick, join timeout

**Dependencies:** TC-019

**Expected result:**
Full integration test suite validating all server behaviors with real TCP connections.

**Acceptance criteria:**
- [ ] All integration tests pass with real TCP connections
- [ ] Two-client chat roundtrip verified
- [ ] Whisper delivery verified
- [ ] Rate limiting triggers correctly
- [ ] Server shutdown notifies clients
- [ ] Edge cases covered (oversized, duplicate nick, timeout)
- [ ] `pytest --cov` shows coverage for all `src/` modules

---

### TC-021 — README and documentation

**Description:**
Write comprehensive README with setup instructions, architecture diagram, and command reference.

**What needs to be done:**
- Expand `README.md`: overview, screenshot, setup (venv, pip install, run server + client)
- ASCII architecture diagram
- Slash command reference table
- `requirements.txt` with `textual>=1.0.0`, `pytest>=7.0`, `pytest-asyncio>=0.21.0`

**Dependencies:** TC-020

**Expected result:**
A developer can clone the repo, follow the README, and have the chat app running in under 5 minutes.

**Acceptance criteria:**
- [ ] README covers setup from clone to running chat session
- [ ] Architecture diagram present
- [ ] All slash commands documented
- [ ] `pip install -r requirements.txt` installs all dependencies
- [ ] Instructions work on macOS and Linux

---

## Total Effort Estimate

| Phase | Focus | Issues | Est. Hours |
|-------|-------|--------|------------|
| 1 | TCP Foundations | TC-001, TC-002 | 3–5 |
| 2 | Wire Protocol | TC-003, TC-004 | 3–4 |
| 3 | Server Core | TC-005–TC-009 | 6–10 |
| 4 | CLI Client | TC-010 | 2–4 |
| 5 | TUI Layout | TC-011, TC-012 | 4–6 |
| 6 | TUI Integration | TC-013–TC-015 | 6–8 |
| 7 | Polish | TC-016–TC-018 | 4–6 |
| 8 | Testing & Docs | TC-019–TC-021 | 4–6 |
| | **Total** | **21 issues** | **32–49** |

**Critical path:** TC-001 → TC-002 → TC-003 → TC-004 → TC-005 → TC-006 → TC-007 → TC-010 → TC-011 → TC-012 → TC-013 → TC-014 → TC-018 → TC-019 → TC-020

**Parallel tracks:**
- Track A: TC-006 + TC-008 + TC-009 (all depend on TC-005, independent of each other)
- Track B: TC-014 + TC-015 (both depend on TC-013, independent of each other)
- Track C: TC-016 + TC-017 + TC-018 (all depend on TC-014, independent of each other)
