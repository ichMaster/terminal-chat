# Roadmap v1

## Phase 1 — TCP Foundations

**Goal:** Understand raw TCP socket lifecycle and evolve from blocking single-client echo to async multi-client broadcast.

**Milestone:** Three telnet clients connected to `async_echo_server.py`, broadcasting messages to each other in real time.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| | **Echo Server** | | |
| v1-1 | Synchronous echo server | Single-client blocking echo using `socket` module | Not started |
| v1-2 | Async multi-client echo | `asyncio.start_server` with concurrent client handling and broadcast | Not started |

**Dependencies:** None — this is the foundation.

---

## Phase 2 — Wire Protocol

**Goal:** Replace raw text with structured JSON messages. Build the shared protocol module with framing, serialization, and validation.

**Milestone:** `pytest tests/test_protocol.py` passes for all message types. Malformed JSON and oversized messages are rejected.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| v1-3 | Protocol module | `encode()`, `decode()`, `read_message()`, `write_message()` with newline-delimited JSON framing | Not started |
| v1-4 | Data models | `User`, `Room`, `ChatMessage` dataclasses | Not started |

**Dependencies:** Phase 1 complete.

---

## Phase 3 — Chat Server Core

**Goal:** Build the full chat server with nicknames, rooms, whisper, rate limiting, and graceful shutdown.

**Milestone:** Two async test clients can register nicks, join rooms, chat, whisper, and see join/leave notifications. Rate limiting triggers after burst.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| | **Connection** | | |
| v1-5 | Nickname registration | Join handshake with 10s timeout, validation (2-16 chars, `[a-zA-Z0-9_-]`), case-insensitive uniqueness | Not started |
| | **Rooms** | | |
| v1-6 | Room management | Auto-join `general`, create/join/leave rooms, auto-delete on empty, max 10 rooms | Not started |
| | **Messaging** | | |
| v1-7 | Chat and whisper routing | Broadcast to room, private whisper to nick, user_joined/user_left notifications | Not started |
| | **Safety** | | |
| v1-8 | Rate limiting | Token bucket per client (5 tokens, 1/sec refill), `rate_limited` error on violation | Not started |
| v1-9 | Graceful shutdown | SIGINT/SIGTERM handler, broadcast system message, close all connections | Not started |

**Dependencies:** Phase 2 complete.

---

## Phase 4 — CLI Client

**Goal:** Build a minimal non-TUI async client to validate the full protocol end-to-end before adding Textual complexity.

**Milestone:** All spec scenarios (Section 7) pass manually with the simple client. Every slash command works.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| v1-10 | Async CLI client | Concurrent stdin reader + socket reader using `run_in_executor`, slash command parsing | Not started |

**Dependencies:** Phase 3 complete.

---

## Phase 5 — TUI Layout

**Goal:** Build the Textual TUI shell with all layout regions using static/fake data. No network connection.

**Milestone:** TUI renders correctly with hardcoded messages, input clears on submit, keybindings toggle sidebar.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| v1-11 | TUI app shell | Textual `App` with Header, RichLog, sidebar (users + rooms), Input, Footer | Not started |
| v1-12 | TCSS styling | Layout sizing, colors, message styling (own, system, error, whisper) | Not started |

**Dependencies:** Phase 4 complete (protocol validated).

---

## Phase 6 — TUI Network Integration

**Goal:** Connect the TUI to the real server. Socket reader as Textual Worker, custom messages for UI updates.

**Milestone:** Full chat session through the TUI matches all spec scenarios. Two TUI clients can chat, whisper, switch rooms.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| v1-13 | Socket reader worker | `run_worker()` background task, `ServerMessage` / `Disconnected` custom events | Not started |
| v1-14 | TUI message handlers | Route server messages to widget updates (chat log, user list, room list) | Not started |
| v1-15 | Slash command integration | Parse `/join`, `/leave`, `/whisper`, `/rooms`, `/users`, `/help`, `/clear`, `/quit` from input | Not started |

**Dependencies:** Phase 5 complete.

---

## Phase 7 — Polish and Edge Cases

**Goal:** Harden the application with reconnection, scroll behavior, per-room message history, input validation.

**Milestone:** Robust chat app that handles disconnects, reconnects, and edge cases gracefully.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| v1-16 | Reconnection logic | Detect disconnect, show overlay, retry with exponential backoff | Not started |
| v1-17 | Nickname prompt screen | Textual input screen on startup if nick not passed via CLI | Not started |
| v1-18 | UX polish | Auto-scroll with pause on scroll-up, per-room 200-message buffer, input validation, Ctrl+C sends quit | Not started |

**Dependencies:** Phase 6 complete.

---

## Phase 8 — Testing and Documentation

**Goal:** Comprehensive automated test suite and complete README.

**Milestone:** `pytest` passes clean with coverage for all `src/` modules. README includes setup, architecture diagram, command reference.

| ID | Feature | Scope | Status |
|----|---------|-------|--------|
| v1-19 | Unit tests | Protocol encode/decode, nick validation, rate limiter, room logic | Not started |
| v1-20 | Integration tests | Server + real TCP clients, message round-trips, disconnect handling | Not started |
| v1-21 | README and docs | Setup instructions, architecture diagram, slash command reference | Not started |

**Dependencies:** Phase 7 complete.

---

## Phase Summary

| Phase | Focus | Features | Depends on |
|-------|-------|----------|------------|
| **1** | TCP foundations — echo server, async broadcast | v1-1, v1-2 | -- |
| **2** | Wire protocol — JSON framing, data models | v1-3, v1-4 | Phase 1 |
| **3** | Chat server — nicks, rooms, whisper, rate limit, shutdown | v1-5, v1-6, v1-7, v1-8, v1-9 | Phase 2 |
| **4** | CLI client — async stdin + socket, slash commands | v1-10 | Phase 3 |
| **5** | TUI layout — Textual shell with static data | v1-11, v1-12 | Phase 4 |
| **6** | TUI integration — socket worker, message handlers, commands | v1-13, v1-14, v1-15 | Phase 5 |
| **7** | Polish — reconnect, nick prompt, scroll, history | v1-16, v1-17, v1-18 | Phase 6 |
| **8** | Testing — unit, integration, documentation | v1-19, v1-20, v1-21 | Phase 7 |
