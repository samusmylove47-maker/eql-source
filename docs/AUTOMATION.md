# Automation

How the twice-daily refresh works, what it can and cannot do, and how to change
it.

---

## The shape of it

```
06:00 and 18:00 UTC
        |
   GitHub Actions starts a runner
        |
   Claude Code asks the wiki API: what changed?
        |
        +-- nothing relevant --> commit the timestamp, stop.   (most runs)
        |
        +-- something changed
                |
           read only the changed pages (diff, not full scrape)
                |
           classify every change GREEN or RED
                |
           apply GREEN, write up RED
                |
           rebuild, run scripts/check.py
                |
           open a PULL REQUEST with PROPOSAL.md
                |
           STOP. Wait for you.
                |
        you read it and merge  -->  Netlify deploys  -->  live
```

**The gate is the merge.** Nothing reaches the site without you pressing a
button. That is not a limitation to be engineered away; it is the design.

---

## Green and red

**Green** is a single-source factual field with no interpretation. A ZEM value
changed from 130 to 119. A respawn timer changed from 28:00 to 9:28. A
coordinate was corrected. These get applied, with the old and new value stated
in the proposal so you can sanity-check them at a glance.

**Red** is everything else. New prose, a new named mob, a changed mechanic, a
conflict with something already published, or anything touching a known gap.
These are written up with reasoning and **not applied**. Claude recommends; you
decide.

A run that finds three green and one red produces a pull request titled
`Survey refresh — 3 green, 1 red`. You can approve the whole thing, or close it
and ask for just the green parts.

---

## Why it asks instead of scraping

eqlwiki is MediaWiki, so it publishes Recent Changes over an API. Asking "which
of my fifteen watched pages changed since revision X" is one small request.
Re-reading fifteen pages twice a day is thirty page loads a day against a
volunteer-run wiki, for information that changes maybe twice a week.

The API approach is cheaper in tokens, faster, more accurate — because you get
diffs rather than having to spot the difference — and it does not make you a
nuisance. `state/last-check.json` remembers the revision ids so each run knows
exactly what it has already seen.

---

## Two failure modes that look like success

Both have bitten this project before. They are called out in the workflow prompt
and in `docs/SOURCES.md`, and you should know them too.

**Stale revision.** A wiki fetch can silently return an old version of a page.
Nothing errors. The page looks fine. Defence: compare the `oldid` in the fetched
footer against the current revision id from the API.

**Empty page.** A fetch can return an empty document while reporting success. An
early version of The Hole's plate was built from one of these and had to be
thrown away entirely. Defence: an empty page is a failed fetch, never a page
with nothing on it.

If either happens, the proposal says so under FETCH PROBLEMS rather than
proceeding.

---

## Costs

Two separate meters:

- **GitHub Actions minutes.** Free tier is generous. A quiet run is a minute or
  two; a busy one maybe ten. Two runs a day will not trouble the free
  allowance on a private repository, and public repositories get Actions free.
- **Claude usage.** The workflow authenticates with `CLAUDE_CODE_OAUTH_TOKEN`,
  which draws on your Claude subscription rather than separate API billing. If
  `/install-github-app` set up `ANTHROPIC_API_KEY` instead, that bills per token
  — swap the line in the workflow if you would rather use the subscription.

Three guards are already in the workflow: `--max-turns 40`, `timeout-minutes:
25`, and a `concurrency` group so two runs can never overlap. Most runs exit at
step 2 having done almost nothing, which is the cheapest possible outcome and
the expected one.

---

## Changing it

**Different times.** Edit the `cron` line. It is UTC, and the format is
`minute hour day month weekday`. `"0 6,18 * * *"` is 06:00 and 18:00.
`"0 */6 * * *"` would be every six hours.

**Watch another page.** Add it to `wiki_pages` in `state/watchlist.json` and
document why in `docs/SOURCES.md`. Nothing else needs changing.

**Run it right now.** Actions tab, Survey refresh, Run workflow. Useful the
first time, to confirm the plumbing works before you trust it overnight.

**Turn it off.** Actions tab, Survey refresh, the "..." menu, Disable workflow.
Nothing else in the project depends on it.

---

## Things worth knowing

- **Scheduled workflows only run from the default branch.** Changes to the cron
  do not take effect until they are merged to `main`.
- **On a public repository GitHub disables a schedule after 60 days with no
  activity.** You will be active, but if the site goes quiet over a holiday,
  check the schedule is still enabled when you come back.
- **A scheduled run is attributed to whoever last edited the cron line.** If that
  ever becomes a bot account the run will be rejected.
- **Claude cannot merge.** It is denied in `.claude/settings.json` and it is not
  granted the permission in the workflow. Keep it that way.

---

## The one habit that keeps this safe

**Read the proposal before you merge.** Not the diff — the proposal. It is
written to be read on a phone in about a minute, and it tells you what changed,
what was deliberately not changed, and what went wrong.

An automated pipeline that publishes unread is a machine for producing confident
errors at scale. The whole value of this site is that it is right. Spending
sixty seconds reading is what buys that.
