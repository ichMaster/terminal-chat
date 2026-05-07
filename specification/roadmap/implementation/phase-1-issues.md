# Phase 1 — TCP Foundations Issues

## Issues Summary Table

| # | ID | Title | Size | Stage | Dependencies |
|---|---|---|---|---|---|
| 1 | TC-001 | Synchronous echo server and client | S | 1 — TCP Foundations | -- |
| 2 | TC-002 | Async multi-client echo with broadcast | S | 1 — TCP Foundations | TC-001 |

**Size legend:** S = 1–2 hours, M = 2–4 hours, L = 4–6 hours

---

## Dependency Tree

```
TC-001 (echo server)
    |
TC-002 (async echo)
```

---

### TC-001 — Synchronous echo server and client

**Description:**
Build the simplest possible TCP server and client to understand the socket lifecycle — bind, listen, accept, read, write, close. This is intentionally blocking and single-client to expose the limitation that async solves.

**What needs to be done:**
- `echo_server.py` using `socket` module — bind `127.0.0.1:9000`, listen, accept, recv/sendall loop
- `echo_client.py` — connect, send lines from stdin, print echoed response
- Handle `ConnectionResetError` on abrupt client disconnect
- Print client address (IP + ephemeral port) on connect/disconnect

**Dependencies:** None

**Expected result:**
A blocking echo server that handles a full conversation with one telnet client. Connecting a second client demonstrates the blocking limitation.

**Acceptance criteria:**
- [ ] Server binds to `127.0.0.1:9000` and accepts a client
- [ ] Client can send multiple lines, each echoed back
- [ ] Second telnet connection hangs until first disconnects (demonstrates blocking)
- [ ] Server prints client address on connect/disconnect
- [ ] Graceful handling of abrupt client disconnect

---

### TC-002 — Async multi-client echo with broadcast

**Description:**
Rewrite the echo server using `asyncio.start_server` to handle multiple clients concurrently. Add broadcast capability — messages from one client are relayed to all others.

**What needs to be done:**
- `async_echo_server.py` using `asyncio.start_server` with `handle_client(reader, writer)` coroutine
- Track connected clients in a shared list
- Broadcast: when one client sends a message, relay it to all other connected clients
- Handle `ConnectionResetError` and clean up client list on disconnect
- Log connect/disconnect events with `peername`

**Dependencies:** TC-001

**Expected result:**
Three telnet clients connected simultaneously, with messages from any one broadcast to all others.

**Acceptance criteria:**
- [ ] Three telnet clients connect and receive messages simultaneously
- [ ] Message from client A appears on clients B and C (broadcast)
- [ ] Disconnecting one client does not affect others
- [ ] Server logs connections and disconnections with client address
- [ ] No unhandled exceptions on abrupt disconnect
