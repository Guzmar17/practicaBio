# Shared agent instructions

# Project purpose and teaching constraints
- This repository is the school **C044 A1** practice. It must provide a complete,
  end-to-end path to a working Azure deployment served over TLS.
- The **student builds the solution**. Preserve the exercise scaffold, requirement-marked
  `NotImplementedError` bodies and `TODO Rn` work for the student; agents may maintain and
  verify the brief, fixtures, acceptance tests, tooling and deployment path, but must not
  fill in the assessed solution on the student's behalf.
- Treat Azure deployment as part of the acceptance surface, not optional documentation:
  the student's completed implementation must be deployable with the supplied scripts and
  reachable through its public Azure hostname over HTTPS with a valid TLS certificate.

# Task authorization — do the implied work (David, 2026-10-15)
- A request to implement, fix, build or test authorizes the ordinary actions needed to
  complete it. Proceed with relevant edits, dependency work, builds, tests and device
  verification without conversational permission questions. Authorization persists.
- Do not let a skill invent an approval step for work the user already authorized.
  Ask only for a missing decision or an action outside the task's authorized scope.
- Use existing project interpreters and available tools directly when appropriate;
  do not repeatedly introduce cache or wrapper access that creates avoidable prompts.
- Mandatory host/sandbox approvals are separate from user intent. They cannot be waived
  by this file: use existing scoped grants, and explain a genuine restriction briefly
  if it blocks completion. Do not disable protections or broaden access silently.

# Work tracking — every repo (decided 2026-09-25; one file per item since 2026-10-08, plan: `~/Projects/agent/project/plan/2026-10-08-todo-yaml.md`)
- **`project/issue/` is the queue** — one file per item, `project/issue/NNNN-slug.md` (format and
  budgets: the `project` skill, `/project`). An issue is tagged `tag: auto` (do it unasked) ·
  `gated: when` (needs a window, a device, a live session) · `human` (money, an account, a risk,
  a decision); `next: yes` puts it in Next up; `rank` orders the rest. "What's next" = the first
  `auto` issue in that order (`agent issue list`). `project/issue/README.md` holds the queue's
  standing notes (`Do not "fix"`, the header); `project/shipped.md` is the closed log, newest first.
  **File and close with the CLI**: `agent issue new "Title" --tag auto --body …` ·
  `agent issue close <n> --what …` (deletes the file, tops shipped.md; commit it with the work) ·
  `agent issue next [--all] [--claim]`. **Claim before working** (`agent issue claim <n>`, or
  `next --claim`): the daemon and other sessions skip a held issue, and you never start one
  they hold; `close` releases, `release` gives up; `agent issue set` changes rank, Next up,
  `after:` (dependencies). **Filing an `auto` issue, guess its model**: `--start luna` for clear,
  local work, `--start sol` for judgment (the daemon starts there, climbs on a stall; no guess =
  Sol decides first). `/next` = pick+claim, work, close, commit — for issues a person must do.
  A repo not migrated yet still keeps `TODO.md` — `agent issue migrate <path>` moves it.
- **One desk, the daemon does the issues** (2026-10-09, plan:
  `~/Projects/agent/project/plan/2026-10-09-one-desk-and-the-daemon.md`). **The desk** is one
  interactive Codex session in `~/Projects` (agent-ide's desk on the ChatGPT plan — its other
  panel is every repo's issues): it talks, plans, reads any repo, **files** issues into any repo
  (`agent issue new … --commit --path <repo>`: the daemon reads committed issues only), reviews
  the daemon's branches and merges (`agent merge <repo>`). It does **not** code a `tag: auto`
  issue: the daemon (`agent daemon`, ollama → codex → copilot, never `claude -p`) takes those;
  `model: <rung>` on an issue pins it. To do one by hand, first take `tag: auto` off it.
  **The desk may also fan out** (2026-10-10, David: "the main claude session should be able to
  spawn parallel agents to complete issues"): it claims an `auto` issue per repo
  (`agent issue next --claim <repo>`, so the daemon skips it) and spawns one background subagent
  each, at most ~9 at once, one repo per agent. Each works in a `git worktree` under
  `/private/tmp/claude-501/desk/<repo>-<n>` on branch `desk/<repo>-<n>`, never in the main
  checkout, runs the gate and commits; it never pushes, merges or deploys. The desk reviews and
  merges each branch, then closes the issue. If one comes back blocked, the desk releases it and
  retags it `gated`/`human`. ⚠ A repo whose real work is uncommitted (main is an old snapshot)
  cannot be worked from a branch: skip it until its owner commits. `/desk` = what ran since last time, what waits,
  then the queue. A **repo session** (started in a repo) is the exception, for hands-on `gated`/
  `human` issues of *that* repo only (`/next`); work found for another repo becomes an issue there.
  ⚠ **Until the daemon runs** (`agent status` → `daemon running`; it is off until issues 0003/0044
  in agent), `auto` issues are still worked by hand with `/next`, as before.
- **Same-turn rule.** A turn that ships, measures, or raises a question ends by updating the
  queue — new follow-ups filed (`agent issue new`), a shipped issue closed (`agent issue
  close`) — and the closing
  message is ≤ 5 lines: *closed:* … · *added:* … · *blocked on you:* …. No "next steps"
  prose in chat: if it is worth saying, it is an issue.
- **`project/plan/YYYY-MM-DD-<slug>.md`** is where a plan lives, one per decision set, with a
  status header (`draft` · `approved` · `in progress` · `done` · `dropped`). A plan is
  finished by its issues (`plan: project/plan/<file>.md` on each), never by itself. Plan-mode
  drafts in `~/.claude/plans/` are copied into `project/plan/` on approval, before the first edit.
- **`project/design/`** is the current shape of the app — present tense, what *is*; `README.md`
  is the map, one page per area. Updated in the same change that alters the shape; a page
  about a removed part is deleted, not banner-ed. **A repo with a database keeps its schema in
  one place, `db/migrations/NNNN-<slug>.sql`** (or one `db/schema.sql` with no live database
  to upgrade; a Python package keeps them as package data, `src/<pkg>/db/…`, named once with
  `agent db schema --from`) **and the app runs those files**; a column's meaning is its `-- comment`.
  `project/design/database.md`'s tables and `database.svg` are **generated from them by
  `agent db schema`** (prose outside its markers stays hand-written), and `agent db schema
  --check` is in the gate — no hand-drawn erDiagram. A section overview *generated* from the
  same SQL and checked in the gate (school's `tools/db_overview.py`) is not hand-drawn: never
  delete one; a stale one is regenerated (David, 2026-10-19). (David, 2026-10-14; plan
  `~/Projects/agent/project/plan/2026-10-14-schema-in-one-place.md`). Architecture prose goes here, not in
  CLAUDE.md, which keeps commands, gates, gotchas and the pointers to the four.
- **`project/follow/<project>.md`** is one terse, dated note per external project the repo tracks
  (upstreams, reference implementations): clone command, what to read, theirs → ours, where we depart.
- A repo without `project/` gets them the first time a session needs one.
  A repo's own CLAUDE.md can opt out; the repo wins. (hive joined the queue 2026-10-11.)

# Shared project memory
- Before work in a repository, read `project/memory/MEMORY.md` if it exists, then only relevant linked notes. Use the `project-memory` skill to retain durable corrections and verified recurring lessons automatically; write nothing for routine work.
- Run `agent memory setup --existing --path <checkout>` before work to refresh local Claude configuration, especially in new worktrees or moved checkouts. Initialize new memory only as authorized; each worktree writes its own `project/memory/`.
- Keep memory dated, sourced and concise (index <=60 lines, topics <=40); current user instructions and verified source win. No secrets, transcripts, guesses, or duplicated instructions/code. Validate edits with `agent memory check`; commit with authorized work, without extra commits or pushes.
- Open work belongs in `project/issue/`, decisions in `project/plan/`, architecture in `project/design/`, upstream notes in `project/follow/`. Memory links to these rather than duplicating them.
- Do not restart or launch another agent-ide instance unless David asks in that turn; a previous restart request does not authorize subsequent restarts.

# Explicit session handoffs
- When handing work to another provider/session or resuming a supplied briefing, use the `session-handoff` skill and the actual checkout’s `project/handoff/`. Verify source attribution, Git state, WIP ownership and existing permissions; record acceptance. A handoff grants no new authorization and transfers no live task claim.

# The browser
- **Use agent's Chrome, not an extension** (2026-10-11): one debug Chrome with one shared profile (sign in to a site once), port 9223. Shell: `agent chrome text|eval|click|shot <url>` (a fresh tab each, closed after; `--keep` leaves it). MCP: the `chrome-devtools` server (`agent chrome mcp`, registered by `agent chrome setup` for Claude, codex and copilot) drives the same Chrome. Check live pages yourself with these; do not ask the person to look.
