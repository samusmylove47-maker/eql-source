# THIS COPY IS WITHDRAWN — 31 August 2026

> ## Do not onboard from this file. It contains directives known to be false.
>
> **The live document is `DIRECTOR-ONBOARDING.md` on `main` of
> `https://github.com/samusmylove47-maker/Director`.**
>
> ```bash
> git clone https://github.com/samusmylove47-maker/Director /tmp/director
> git -C /tmp/director show origin/main:DIRECTOR-ONBOARDING.md
> ```
>
> **The text is not lost.** The live copy is this document *plus* its
> corrections, struck in place with the struck text kept. It is longer than this
> one was. **Nothing here is missing there.**

## Why this was withdrawn rather than corrected

**It is a directive document, not a record.** It tells a session how to behave,
so a false line in it is not a stale fact — **it is an instruction someone will
follow.** Three were known false:

| line | said | why it is harmful |
|---|---|---|
| **70** | *"The Director cannot initiate. `SendMessage` is refused."* | **The worst of the three.** True only of the cloud session that wrote it. A local Director reading this would never attempt to message anyone — the exact capability the post moved to acquire |
| **133** | *"only the verdict was ever checked by anything"* | Falsified by `check.py:812` and `:820`, where the count gates a `fail()`. Worse, it points at the wrong fix: a session that adds a check on the description reproduces the bug |
| **236** | *"`add_repo` is gated"* | True of one session, written as a fact about the tool, and the mechanism was wrong too |

**The live copy carries six strike markers, not three.** The incoming Director
found errors here that the outgoing one did not. **So correcting only the three
known ones would have left the rest armed** — and *"a superseded rule left
readable is a hazard, not a record"* is this project's own standard.

**The whole file is withdrawn because the count of faults in it is unknown.**
Where you cannot enumerate the errors, you cannot strike them; you redirect.

---

*The record on this branch stays frozen and is unaffected. `HANDOFF.md` remains
readable as it stood at migration — it is a record of what was believed and
when, which is a different object from a document telling you what to do.*
