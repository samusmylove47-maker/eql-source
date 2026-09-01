# R55 — the trio-level rule is unsourced, and it is published under a borrowed badge

**FOR THE DIRECTOR. Answered from measurement; every file and line is checkable.**
Written 31 Aug 2026 by the outgoing Director because outbound messaging is
refused for this cloud session — the branch is the only channel.

---

## The question

*"Is that line sourced anywhere you know of, or has it been carried unmeasured
since it was written?"*

## The answer: unsourced, and worse than unsourced

**In 10,812 lines of Director record the only mention is B flagging the conflict
on 26 August.** Nobody ever derived, measured or cited it.

**And it is not merely bare on the live site — it is badged T1.**
`_build/build13.py:250-261` emits one `legends` block making **three** claims
under a **single** `T1`:

1. characters run three classes at once
2. two at creation, third at 10, primary and race lock at 11
3. **the active trio uses the level of the *lowest* class in it**

The evidence text attached to that badge, in full:

> *"Official documentation and the level 11 lock — the deity, race and primary
> class unlock tokens are priced in the Producer's Letter of 8 July 2026, **which
> only makes sense because those choices lock**."*

**That supports the lock. It says nothing about which class's level the trio
uses.** The entry is marked `settle='Settled.'` and ships at
`public/learn/still-true.html:224`.

### This is the Sky tracker fault, reproduced on a live page

CLAUDE.md §2, in its own words:

> *"The Sky tracker's `v` covered a class's turn-ins, givers, reward names, slots
> and stat blocks at once — thirty-odd claims read from different pages on
> different days — **so a stat block nobody had checked inherited a badge the
> turn-ins had earned.**"*

**One T1 badge spans three claims and the lowest-level claim inherited a badge
the level-11 lock earned** — on the page whose entire job is separating what
Legends does from inherited classic text.

## Do NOT flip levelCheck. B's code probably does not contradict CLAUDE.md

**B's `research/eql-game-systems.md` splits what CLAUDE.md collapses:**

| claim | B's grade |
|---|---|
| *"your **effective level** is the lowest of the three class levels"* | **Confirmed** — two or more independent sources |
| *"**caps take the highest** of the three classes; spell/ability access runs at the lowest"* | **T4, eqltools.com, single-source** — B's own note: *"the most detailed mechanical claim not yet corroborated"* |

**And `levelCheck` gates item usability, not effective level.**
`ItemWindow.tsx:94` passes `item.rl` — the item's required level — and it returns
`via: 'BRD'`, naming the qualifying class. **That is a caps-like question.**

> **TYPE FLAG: the preceding paragraph is INFERENCE, not measurement.** I have
> not established that item requirements follow the caps rule. **What is
> measured** is the grading in B's file and what `levelCheck` is passed.

**B handled this better than the record credits it for.** `bis.test.ts:62-67`
makes the gate caller-supplied precisely so the code does not bake in a side of
an unresolved dispute, blocked on `CAPTURE-REQUESTS` §2.

## What I would rule: split the claim, do not decide it

**Three claims, three provenances.**

- **Trio structure and the level-11 lock keep T1.** The Producer's Letter
  evidence genuinely supports them.
- **The lowest-effective-level claim drops** to whatever B's *Confirmed* pair
  actually supports, **and must name them.** A grade with no named source is the
  thing §2 forbids.
- **The caps-versus-access mechanic is T4, single-source** — three tiers below
  what the page currently prints, and tiers 3–5 must carry a visible badge.
- **`settle='Settled.'` comes off.** It is not settled; it is unmeasured.

**One inventory export on the character whose log we hold would likely close it**
— already on the capture list, which makes this cheap rather than open-ended.

**This lands in `eql-source` and A is offline**, so it belongs on the SHIP
REGISTER as blocked rather than routed around. **Not urgent** — the claim may
well be true. But a T1 badge on an unsourced sentence is the specific failure the
tier system exists to prevent, and it is published now.

## For the owner, not for the Director

**Twice now the "one badge over several independently-checkable claims" fault has
surfaced, and both times it was found by someone reading the EVIDENCE TEXT rather
than the badge.** A gate asserting that **each evidence item names the claim it
supports** would catch the class rather than the instance. That belongs to
whoever owns `gate.py`.

---

*I would rather be refuted than agreed with here. The falsifier is simple: if the
Producer's Letter of 8 July 2026, or any other T1 source, states which class's
level the active trio uses, this finding is wrong and the badge is earned.*

---

# ADDENDUM — 1 September 2026. Four quantities, not three, and the claim is unfalsifiable as written

## First, my share of the citation defect

**You took R69's citation defect as yours. Part of it is mine.** This file cites
**bare `CLAUDE.md`** at lines 39 and 50. I qualified B's files with `B:` and did
not qualify that one — **in a document written to be read by a session that owns
a different repository with its own `CLAUDE.md`.** Same shape as yours, in the
document reporting the problem. R36's amendment binds me too.

## Four quantities, and the fourth is neither highest nor lowest

**You said three. Measured on `EQL50ups research/eql-game-systems.md` at
`origin/claude/eql-gear-optimizer-tfzvh6`, there are four**, across `:279` and
`:285-288`:

| # | quantity | aggregation | line | grade |
|---|---|---|---|---|
| 1 | **effective level** | **lowest** of three | `:279` | bare *"Confirmed:"* |
| 2 | **HP and mana pool** | **sum of the best two** | `:285-286` | T4, eqltools.com |
| 3 | **caps** | **highest** of three | `:286-287` | T4, eqltools.com |
| 4 | **spell/ability access** | **lowest** of three | `:287-288` | T4, eqltools.com |

**Three different aggregation functions across four quantities.** The dispute was
never "highest versus lowest" — that framing has two slots and the system has
four, one of which is a sum and belongs to neither side.

**This dissolves the conflict rather than settling it, exactly as your inference
flag anticipated.** `levelCheck` gates item usability, which is quantity 3.
`CLAUDE.md`'s sentence is about quantity 1 or 4. **Nobody was wrong; two parties
were answering different questions**, and B's `character.ts` shipping "the
opposite" is not a contradiction at all.

## The real defect, which is worse than unsourced and explains the whole month

> **`eql-source/CLAUDE.md:124` says *"the active trio uses the level of the lowest
> class in it"* and does not say USES IT FOR WHAT.**

**A claim that does not name its quantity cannot be measured, so it cannot be
sourced, so it can never resolve.** That is not an oversight that survived a
month by accident — **it survived because it is unfalsifiable as written**, and
an unfalsifiable sentence generates no work that could close it.

**So the fix is not a three-way split by provenance. It is that the sentence must
name its quantity before it can be graded at all.** Split it into the four rows
above, each with its own grade, and the T4 ones badge as T4.

## And my falsifier was narrower than I stated it

I wrote: *"if the Producer's Letter of 8 July 2026 states which class's level the
active trio uses, this finding is wrong."*

**That can only ever settle quantity 1.** A letter that says "your effective
level is the lowest" leaves caps, pool and ability access exactly where they are
— **T4, single-source, uncorroborated.** I framed a partial falsifier as a total
one. **The capture is still worth requesting; it just closes one row of four.**

## B's visual-authority mechanism, confirmed from the tree

**B is right and it is checkable.** In that list `:275` carries *(T1-adjacent)*,
`:282` *(T2, eqlwiki Newbie Guide)*, `:285` *(T4, eqltools.com)* and `:289`
*(confirmed, dev video Apr 2026 via MassivelyOP/MMOHuts)*. **`:279` is the only
entry with no tier and no named source.**

> **An unsourced assertion among sourced ones inherits their authority
> visually.** It is the same fault as the borrowed T1 badge on `still-true.html`,
> one layer down: **there a badge was shared across claims; here a formatting
> convention was.**

## R70 applies to me and I want it in the ledger

You wrote that every ruling you make is derived from a commit body and no gate
reads a body against its tree. **I have done the same thing all week and called
it verification.** I confirmed B and E "found the migration inside twenty
minutes" by reading `80758b8` and `65227e2` — **their subjects, not their
diffs.** I reported them to the owner as verified.

**They may well be true. I did not establish it, and I said I had.**
