---
tag: gated: original host terminal
rank: 30
---
# Release stale development port 8600

Do: stop protected oxid-server PID 59113 from the terminal/session that launched it, then run mk dev on the default port.
Done: port 8600 serves the C044 scaffold instead of the old app process.
⚠️ Current sandbox and approved escalation both receive Operation not permitted.
