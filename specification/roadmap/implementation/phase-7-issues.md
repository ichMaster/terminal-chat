# Phase 7 — Polish Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 16 | TC-016 | Reconnection logic | M | 7 — Polish | TC-014 |
| 17 | TC-017 | Nickname prompt screen | S | 7 — Polish | TC-014 |
| 18 | TC-018 | UX polish (scroll, history, validation) | M | 7 — Polish | TC-014 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-014 (handlers) [Phase 6]
    |
    +--------+--------+
    v        v        v
TC-016   TC-017   TC-018
(reconn) (nick)   (UX)
```

**Parallelization hints:**

- TC-016, TC-017, and TC-018 can all run in parallel after TC-014

---

### TC-016 — Reconnection logic

**Description:**
Detect server disconnection and attempt to reconnect automatically with exponential backoff.

**What needs to be done:**
- On `Disconnected` event: show overlay with "Connection lost" message
- Retry with exponential backoff (1s, 2s, 4s, 8s, max 30s)
- On reconnect: re-send `join`, re-join previously joined rooms
- Show reconnection progress in overlay

**Dependencies:** TC-014

**Expected result:**
Client recovers from server restarts or network blips without manual intervention.

**Acceptance criteria:**
- [ ] Server kill triggers reconnection overlay
- [ ] Backoff increases on consecutive failures
- [ ] Successful reconnect restores rooms and clears overlay
- [ ] User can still see chat log while overlay is shown
- [ ] Manual quit during reconnect exits cleanly

---

### TC-017 — Nickname prompt screen

**Description:**
Show a Textual input screen on startup if nickname is not provided via CLI argument.

**What needs to be done:**
- If `--nick` omitted, show fullscreen `Input` widget prompting for nickname
- Client-side validation: 2–16 chars, `[a-zA-Z0-9_-]`
- On `nick_taken` error from server, return to prompt with error message
- On success, transition to main chat screen

**Dependencies:** TC-014

**Expected result:**
Seamless nickname entry experience — either via CLI flag or interactive prompt.

**Acceptance criteria:**
- [ ] App starts with nick prompt when `--nick` omitted
- [ ] Invalid format rejected client-side with inline error
- [ ] Taken nick rejected server-side, prompt re-shown with error
- [ ] Valid nick transitions to chat screen

---

### TC-018 — UX polish (scroll, history, validation)

**Description:**
Improve the user experience with scroll behavior, per-room message history, input validation, and clean exit handling.

**What needs to be done:**
- Auto-scroll to bottom on new messages; pause when user scrolls up
- Per-room message buffer: store last 200 messages client-side, restore on room switch
- Prevent sending empty messages, show inline error
- Timestamp formatting: local timezone, dimmed `[HH:MM]`
- Ctrl+C: send `quit` to server before exiting

**Dependencies:** TC-014

**Expected result:**
Polished UX with no jarring behaviors around scrolling, room switching, or input.

**Acceptance criteria:**
- [ ] New messages auto-scroll chat log to bottom
- [ ] Scrolling up pauses auto-scroll; new message indicator appears
- [ ] Switching rooms restores message history for that room
- [ ] Empty message submit shows error, does not send
- [ ] Timestamps display in local timezone
- [ ] Ctrl+C sends quit message before exiting
