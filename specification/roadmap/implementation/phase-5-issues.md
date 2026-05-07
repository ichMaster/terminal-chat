# Phase 5 — TUI Layout Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 11 | TC-011 | TUI app shell and custom widgets | M | 5 — TUI Layout | TC-010 |
| 12 | TC-012 | TCSS styling and layout | S | 5 — TUI Layout | TC-011 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-010 (CLI client) [Phase 4]
    |
TC-011 (TUI shell)
    |
TC-012 (TCSS)
```

---

### TC-011 — TUI app shell and custom widgets

**Description:**
Build the Textual application shell with all layout regions from the spec. Feed it hardcoded data to verify layout before adding network complexity.

**What needs to be done:**
- Create `src/tui/` package with `app.py`, `widgets.py`, `styles.tcss`
- `ChatApp(App)` with `compose()`: Header, Horizontal(RichLog + Vertical sidebar), Input, Footer
- Sidebar: Users list + Rooms list
- Custom widgets: `ChatLog` (styled message rendering), `UserList`, `RoomList` (click-to-switch)
- Keybindings: F1 Help, F2 Rooms, F3 Users, F4 Whisper, Ctrl+C Quit
- `on_input_submitted()` clears input
- `on_mount()` populates with sample data

**Dependencies:** TC-010

**Expected result:**
TUI renders correctly matching the spec diagram. Input clears on submit. Keybindings work.

**Acceptance criteria:**
- [ ] Layout matches spec diagram (header, chat log, sidebar, input, footer)
- [ ] Chat log displays hardcoded messages with correct styling
- [ ] User list and room list render in sidebar
- [ ] Input clears on Enter
- [ ] F-key bindings respond
- [ ] Terminal resize doesn't break layout

---

### TC-012 — TCSS styling and layout

**Description:**
Define the Textual CSS for layout sizing, colors, and message styling.

**What needs to be done:**
- `src/tui/styles.tcss` with layout rules
- Chat-log takes remaining width; sidebar fixed 25 chars, docked right
- Message styles: own (highlighted), system (dimmed), error (red), whisper (italic)
- Timestamp dimmed, header with room indicator, footer with keybindings

**Dependencies:** TC-011

**Expected result:**
Visually polished TUI with distinct message styles matching the spec.

**Acceptance criteria:**
- [ ] Sidebar stays fixed width on resize
- [ ] Own messages visually distinct from others
- [ ] System messages dimmed with `--` prefix
- [ ] Error messages red with `[!]` prefix
- [ ] Whisper messages italic
