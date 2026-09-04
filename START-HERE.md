# Working on this site

Setup is done. This file describes how the project is wired and how to work on
it day to day. It is a reference, not a checklist to run.

---

## The three moving parts

1. **This folder** — the website itself. HTML, CSS, and the Python scripts that
   generate the pages.
2. **GitHub** — `samusmylove47-maker/eql-source`, private. Stores the folder and
   remembers every version of it.
3. **Cloudflare** — watches GitHub. Anything that reaches the `main` branch is
   published to eqlsource.com within about a minute or two.

   This said *Netlify* until 4 September 2026 and had been wrong for weeks.
   `curl -I https://eqlsource.com` answers `Server: cloudflare`. A `netlify.toml`
   file is still in the folder and **nothing reads it** — it is history, kept
   until somebody removes it deliberately.

**Merging is what publishes.** Nothing else does.

---

## How the setup is wired

| Piece | State |
|---|---|
| Python | 3.12, at `AppData\Local\Programs\Python\Python312` |
| `python3` command | A copy of `python.exe`, because Windows ships only `python` |
| Git | Repository on `main`, line endings pinned to LF |
| GitHub | `gh` authenticated as `samusmylove47-maker` |
| Cloudflare | A Worker serving static assets. `wrangler.jsonc` sets the served folder to `./public` |
| Automation | Workflow file present but **not yet running** — needs a credential |

---

## A normal session

Start Claude Code in this folder, then say what you want done. Two habits worth
keeping:

**One task per conversation.** Finish a thing, `/clear`, start the next. Long
sessions get expensive and lose the thread.

**Ask when you do not follow something.** "Explain that like I'm new" is not a
wasted turn.

### Rebuilding and checking

```bash
./build.sh
```

```bash
python3 scripts/check.py
```

`build.sh` regenerates every page from the originals in `_build/source/` and the
data in `assets/zones-index.json`. `check.py` validates the result — broken
links, missing chrome, duplicate zone accents, CDN dependencies, and any page
claiming more verified plates than the data supports. A failure blocks a commit.

### Custom commands

Project commands live in `.claude/commands/`. Type `/` in Claude Code to list
them. `/newzone`, `/verify`, `/gaps` and `/ship` are the built ones.

---

## Safety

**You cannot break this permanently.** Every version is in Git.

- Uncommitted changes you want to discard: `git checkout .`
- A commit you want to undo: `git revert HEAD`
- A bad deploy: **undo it the same way you shipped it.** `git revert` the merge
  on `main`, open that as a pull request, and merging it publishes the fix — the
  same one route everything else takes. Cloudflare keeps previous versions too,
  but the revert is the path this project actually uses and the one these notes
  can vouch for.

**Never merge a pull request you have not read.** This matters most for the
automated ones, once they start. The safety design rests on it.

---

## Turning on the automation

Not yet running. It needs a credential stored in GitHub as a repository secret.
Inside Claude Code:

```
/install-github-app
```

That installs the Claude GitHub App, stores the credential, and opens a pull
request. Merge it, then check that the secret name matches the one
`.github/workflows/survey-refresh.yml` expects.

Once live it runs at 06:00 and 18:00 UTC, checks the wiki's Recent Changes feed
for the watched pages, and stops if nothing changed — which is what most runs
should do. If something did change it reads only the changed pages, drafts an
update and **opens a pull request**. It never publishes by itself. You can
approve from GitHub's mobile app.

---

## When something goes wrong

**"command not found"** — the program is not installed, or the terminal needs
restarting after installing it.

**"Python was not found"** — the terminal is holding a PATH captured before
Python was installed. Open a new one.

**Git asks for a username and password** — the GitHub login expired. Run
`gh auth login`.

**It deployed but the site looks wrong** — first check the change is really on
`main`: `git log --oneline -3 origin/main`. A pull request can merge without your
last commit in it, which has happened twice. If it is there and the page is still
wrong, the served folder is `./public` in `wrangler.jsonc`, and anything outside
that folder is not published at all.

**Genuinely stuck** — paste the exact error into Claude Code. It has the whole
project in front of it.

---

## What to read next

- `CLAUDE.md` — the project's rules. Claude reads this every session; read it
  once so you know what it has been told.
- `HANDOFF.md` — current state and the open work.
- `docs/BACKLOG.md` — the work, prioritised.
- `docs/DESIGN.md` — the aesthetic brief.
- `README.md` — structure and rebuild instructions.
