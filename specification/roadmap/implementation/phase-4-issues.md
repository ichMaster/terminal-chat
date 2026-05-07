# Phase 4 — CLI Client Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 10 | TC-010 | Async CLI client | M | 4 — CLI Client | TC-007 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-007 (chat/whisper) [Phase 3]
    |
TC-010 (CLI client)
```

---

### TC-010 — Async CLI client

**Description:**
Build a minimal non-TUI async client to validate the full protocol end-to-end. Two concurrent tasks: one reads server messages and prints them, one reads stdin and sends messages.

**What needs to be done:**
- `simple_client.py` with `argparse`: `--host`, `--port`, `--nick`
- Connect via `asyncio.open_connection`, send `join`, await `welcome`
- `receive_loop()` — read and format server messages
- `send_loop()` — read stdin via `run_in_executor`, parse slash commands or send chat
- Format output: timestamps `[HH:MM]`, system messages `--`, errors `[!]`
- All slash commands: `/join`, `/leave`, `/rooms`, `/users`, `/whisper`, `/nick`, `/help`, `/clear`, `/quit`

**Dependencies:** TC-007

**Expected result:**
Two CLI clients can have a complete chat session — register, join rooms, chat, whisper, and see join/leave notifications.

**Acceptance criteria:**
- [ ] Client connects and receives `welcome` message
- [ ] Two clients can chat back and forth
- [ ] All slash commands work correctly
- [ ] Server disconnect detected and reported
- [ ] Formatted output (timestamps, system prefix, error styling)
- [ ] All spec scenarios (Section 7) pass manually
