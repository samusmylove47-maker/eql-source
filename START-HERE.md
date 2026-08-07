# START HERE

You are about to open this project in Claude Code for the first time. This file
is written for exactly that moment. Follow it top to bottom. Nothing here
assumes you have done this before.

**Read this once before typing anything.** It is about fifteen minutes of setup,
most of which is waiting for downloads.

---

## What you are actually building

A static website that lives in a folder. There is no server, no database and
nothing to break at 3am. Three moving parts:

1. **This folder** — the website. HTML files, an image or two, some CSS.
2. **GitHub** — a free service that stores the folder and remembers every
   version of it. Think of it as Google Docs version history, for a folder.
3. **Netlify** — watches GitHub. When the folder changes, it publishes the new
   version to the internet automatically, in about thirty seconds.

Claude Code is a program that runs in your terminal, can read and edit the files
in this folder, and can run commands for you. It is not a chat window that
hands you code to copy and paste. It does the work in place.

---

## Step 0 — Things you need first

You need four accounts or programs. All free.

| What | Why | Where |
|---|---|---|
| A terminal | Where Claude Code runs | Already on your computer |
| Node.js | Claude Code is built on it | nodejs.org — take the LTS version |
| A GitHub account | Stores the site and runs the automation | github.com |
| GitHub CLI (`gh`) | Lets Claude talk to GitHub | cli.github.com |
| A Netlify account | Publishes the site | netlify.com — sign in *with GitHub* |

**Finding your terminal.** On a Mac, press Cmd+Space, type "Terminal", press
Enter. On Windows, press the Start key, type "PowerShell", press Enter.

**Everything in a grey box below is a command.** Type it (or paste it) into the
terminal and press Enter. Commands are case sensitive. If one fails, that is
normal and expected — skip to *When something goes wrong* at the bottom.

---

## Step 1 — Check Node.js is installed

```
node --version
```

If you see a version number, good. If you see "command not found", install
Node.js from nodejs.org first, then close and reopen the terminal.

## Step 2 — Install Claude Code

```
npm install -g @anthropic-ai/claude-code
```

On a Mac this may need `sudo npm install -g @anthropic-ai/claude-code` and your
password. The password will not appear as you type it. That is normal.

Check it worked:

```
claude --version
```

## Step 3 — Log in to GitHub from the terminal

```
gh auth login
```

Answer the prompts: **GitHub.com** → **HTTPS** → **Yes** authenticate with
credentials → **Login with a web browser**. It shows you a code, opens your
browser, you paste the code. Done.

## Step 4 — Put the website folder somewhere sensible

**If your site is already live on Netlify** (it is, at eqlsource.netlify.app),
you are replacing that drag-and-drop deploy with a proper Git-connected one.
Nothing is lost; the site keeps running while you do it.


Unzip `eql-source.zip` if you have not already. Move the folder somewhere
you will find again — your Documents folder is fine. Then point the terminal at
it:

```
cd ~/Documents/eql-source
```

Adjust the path to wherever you actually put it. On Windows it will look like
`cd C:\Users\YourName\Documents\eql-source`.

**Shortcut:** type `cd ` (with a space), then drag the folder from Finder or
File Explorer onto the terminal window. It fills in the path for you.

Confirm you are in the right place:

```
ls
```

You should see `index.html`, `assets`, `dungeons`, `raids`, `tools`.

## Step 5 — Turn the folder into a Git repository

```
git init -b main
git add -A
git commit -m "EQL Source — initial site"
```

Now create the GitHub repository and push it up:

```
gh repo create eql-source --public --source=. --remote=origin --push
```

Use `--private` instead if you would rather keep the source closed. Public has
one practical advantage: GitHub Actions minutes are free on public repositories,
and the twice-daily automation runs on those minutes. It also lets other players
send you corrections as pull requests, which for a community reference site is
the point.

## Step 6 — Connect Netlify to the repository

Your site is already on Netlify from the zip drop. Now point it at GitHub so
every push deploys automatically.

1. Go to **app.netlify.com** and open the **eqlsource** site.
2. **Site configuration** → **Build & deploy** → **Link repository**.
3. Choose GitHub, pick `eql-source`.
4. Leave the build command **empty**. Set publish directory to `.` (a single dot).
5. Save.

If Netlify will not relink an existing site, the alternative is just as good:
create a new site from the repo, then move the `eqlsource` name across under
**Domain management**. Netlify keeps every old deploy either way.

**From now on, anything pushed to the `main` branch goes live automatically.**
That is the whole deployment story.

## Step 7 — Site identity is already set

`site.config.json` holds the name, the tagline and the URL. It is filled in
already:

```json
{ "site_name": "EQL Source", "site_tagline": "Survey",
  "site_url": "https://eqlsource.netlify.app" }
```

If you ever move to a custom domain or rename the site, change it **here only**
and run `./build.sh`. Every page, the wordmark, the sitemap and robots.txt all
read from this one file.

## Step 8 — Start Claude Code, finally

```
claude
```

First run asks you to log in — a browser window opens, you approve, you come
back. Then you get a prompt. Type this exactly:

```
Read HANDOFF.md, then CLAUDE.md, then docs/BACKLOG.md. Run ./build.sh and
python3 scripts/check.py. Tell me what state the project is in and what you
propose to do first. Don't change anything yet.
```

That is your first real conversation. Claude reads `CLAUDE.md` automatically at
the start of every session, so it already knows the rules. `HANDOFF.md` tells it
the current state and the three jobs waiting: the aesthetic uplift, the new
tools, and closing the verification gaps.

Asking it to confirm what it understands before it edits anything is a good
habit — it catches misunderstandings before they become commits.

**Once it has reported back, a good second message is:**

```
Start on the aesthetic uplift. Use /uplift hero — read docs/DESIGN.md first,
show me screenshots before and after, and do only the hero band.
```

---

## Step 9 — Set up the automation

Do this **after** you have had one ordinary session and are comfortable. Inside
Claude Code:

```
/install-github-app
```

Follow the prompts. It installs the Claude GitHub App, stores your credential as
a repository secret, and opens a pull request adding the workflow files. Create
and merge that pull request.

Then, still inside Claude Code:

```
Set up the twice-daily survey refresh. The workflow file is already written at
.github/workflows/survey-refresh.yml — check it against the secret name that
/install-github-app actually created, fix the mismatch if there is one, commit
and push.
```

**How the automation behaves, so there are no surprises:**

- It runs at 06:00 and 18:00 UTC.
- It checks the wiki's Recent Changes feed for the pages this project watches.
- If nothing changed, it stops. Most runs will stop here, and that is the point.
- If something changed, it reads only the changed pages, drafts an update, and
  **opens a pull request.**
- **It never publishes anything by itself.** You get a pull request with a
  written explanation of every proposed change. You read it, and you merge it
  or you close it. Merging is what publishes.

You can approve from your phone. GitHub's mobile app shows the pull request, the
explanation and a Merge button.

---

## The five commands you will actually use

| Command | What it does |
|---|---|
| `claude` | Start a session in the current folder |
| `/clear` | Wipe the conversation, keep the project. Use between unrelated tasks |
| `/status` | What Claude currently knows and is allowed to do |
| `Ctrl+C` | Stop Claude mid-task |
| `exit` | End the session |

Custom commands built for this project live in `.claude/commands/`. Type `/`
inside Claude Code to see them.

---

## Rules of thumb for your first week

**Commit often.** Before any big change, tell Claude "commit what we have
first". A commit is a save point you can return to. There is no limit and no
cost.

**One task per conversation.** Finish a thing, `/clear`, start the next. Long
sprawling sessions get expensive and confused.

**Ask before you approve.** When Claude proposes something you do not follow,
say "explain that to me like I'm new" — this is not a wasted turn, it is the
whole point of working this way.

**You cannot break it permanently.** Everything is in Git. The worst outcome is
`git reset --hard HEAD` which throws away uncommitted changes and puts the folder
back to the last save point. If a deploy goes wrong, Netlify keeps every previous
version and has a one-click rollback under **Deploys**.

**Never merge a pull request you have not read.** This matters most for the
automated ones. The whole safety design of this project rests on that one habit.

---

## When something goes wrong

**"command not found"** — the program is not installed, or the terminal needs
restarting after installing it. Close the terminal, open a new one, try again.

**"permission denied"** — on Mac or Linux put `sudo ` in front of the command.

**Git asks for a username and password** — you skipped `gh auth login`, or it
expired. Run it again.

**Netlify deployed but the site looks wrong** — check the publish directory is
`.` and the build command is empty. Netlify tries to be clever and sometimes
guesses a build step this site does not need.

**Claude Code did something you did not want** — `git checkout .` throws away
uncommitted changes. If it is already committed, `git revert HEAD` undoes the
last commit safely.

**Genuinely stuck** — paste the exact error into Claude Code and say "this
happened, what do I do". It has the whole project in front of it.

---

## What to read next

- `HANDOFF.md` — what the project is, what state it is in, and the three jobs.
  This is what you point Claude at.
- `CLAUDE.md` — the project's rules. Claude reads this every session; you should
  read it once so you know what it has been told.
- `docs/BACKLOG.md` — the work, prioritised, with acceptance criteria.
- `docs/DESIGN.md` — the aesthetic brief.
- `docs/AUTOMATION.md` — how the twice-daily job works and how to change it.
- `docs/SOURCES.md` — the source hierarchy and the watchlist.
- `README.md` — the site's own structure and rebuild instructions.
