# Start Here

A simple step-by-step guide to using ATLAS on your computer. Windows-friendly. Read this once; after that you will likely only need the README.

## What ATLAS is, in one paragraph

ATLAS is a small archive of markdown files. A Python script reads those files and turns them into a static website you can open in your browser. There is no database, no server-side application, and no third-party dependencies. You edit markdown; you run one command; you view the result.

## Just want to open ATLAS?

If you only want to view the site, **double-click `launch-atlas.bat`** in the project root. It builds the site, opens your browser, and starts a local server in one step. Press `Ctrl+C` in the terminal window (or close the window) to stop.

The rest of this document explains what is happening underneath and how to do it manually if you prefer or if you ever need to debug.

## What you need before starting

- **Python 3.8 or later.** Open a terminal and run `python --version`. If you see something like `Python 3.10.11`, you are set. If you get an error, install Python from [python.org/downloads](https://www.python.org/downloads/) and check the box for "Add Python to PATH" during installation.
- A web browser (any modern one).
- Optional: a text editor for editing markdown files (VS Code, Notepad++, or even Notepad).

## Step 1 — Open a terminal

On Windows, you have several options. Any of these will work:

- **Git Bash** (recommended if you have Git for Windows installed). Right-click in any folder and choose "Git Bash Here," or open it from the Start menu.
- **PowerShell**. Open from the Start menu.
- **Command Prompt** (`cmd`). Open from the Start menu.

You will type commands at the prompt. The commands below work the same in all three.

## Step 2 — Go to the ATLAS folder

The project folder is the one containing this `START_HERE.md` file. On the original setup it lives at:

```
C:\Users\steve\Documents\Claude Workspace\Atlas\prototype_continuity_0_1
```

(That folder is the ATLAS project. The name `prototype_continuity_0_1` is historical and does not affect anything; you can rename it locally if you want — see "Renaming the folder" near the bottom of this document.)

In your terminal:

```
cd "C:\Users\steve\Documents\Claude Workspace\Atlas\prototype_continuity_0_1"
```

(In Git Bash, you can use forward slashes: `cd "C:/Users/steve/Documents/Claude Workspace/Atlas/prototype_continuity_0_1"`.)

To confirm you are in the right place:

```
ls
```

You should see `README.md`, `START_HERE.md`, `content`, `scripts`, `static`, `stewardship`, `templates`, and (if you have built before) `public`.

## Step 3 — Build the site

```
python scripts/build.py
```

This reads the markdown files and writes the website into a folder called `public/`. It takes about one second.

If the build worked, you will see something like:

```
Built 24 entities across 2 regions.
Total authored relationships: 65
Output: C:\Users\steve\Documents\Claude Workspace\Atlas\prototype_continuity_0_1\public
```

If anything else appears (error, traceback), the build failed. Read the message — it names the file and what is wrong.

## Step 4 — Start a local web server

The site uses absolute URLs (e.g., `/static/style.css`), so opening `public/index.html` directly will not work properly. Instead, run a small local web server. Python has one built in.

```
cd public
python -m http.server 8000
```

You will see a line like:

```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

Leave that terminal window open. The server runs as long as the terminal is open.

## Step 5 — Open the site in your browser

Open any browser and go to:

```
http://localhost:8000
```

You should see the ATLAS homepage. Click around — region links, entity links, adjacencies — to confirm everything works.

## Step 6 — Stop the server

When you are done viewing, return to the terminal where the server is running and press:

```
Ctrl+C
```

The server stops. The terminal returns to a normal prompt.

## Step 7 — Make an edit

Open any source file. For example, to edit the term entity for *prāṇa*:

```
content/regions/breath/entities/term-prana.md
```

Make a small change (fix a typo, adjust a sentence). Save the file.

## Step 8 — Rebuild after editing

Back in the terminal, return to the project root if you are not already there:

```
cd "C:\Users\steve\Documents\Claude Workspace\Atlas\prototype_continuity_0_1"
```

(In Git Bash, forward slashes also work.)

Then rebuild:

```
python scripts/build.py
```

If the build succeeds, the change is already in `public/`. If the local server is still running, refresh the browser tab to see the change. If it is not running, restart it as in Step 4.

## Step 9 — Commit changes to GitHub

After a successful build, save your changes to GitHub:

```
git status
```

This shows what files you changed. Then:

```
git add .
git commit -m "Brief description of your edit"
git push
```

The first two commands stage and record your change locally. `git push` sends it to GitHub.

`public/` will not appear in `git status` because it is gitignored. Only your source edits will be staged.

## Doing it all in one terminal session

Here is a typical session, start to finish:

```
cd "C:\Users\steve\Documents\Claude Workspace\Atlas\prototype_continuity_0_1"
python scripts/build.py
cd public
python -m http.server 8000
```

Open `http://localhost:8000` in a browser. Make edits in another terminal or in your editor. To rebuild, open another terminal at the project root and run:

```
python scripts/build.py
```

Then refresh the browser.

## Renaming the folder (optional)

The folder is named `prototype_continuity_0_1` for historical reasons. If you want to rename it locally to something like `Atlas`, this is safe to do:

1. Stop any local server (`Ctrl+C` in the terminal running it).
2. Close any editor windows pointed at files inside the folder.
3. In File Explorer (or in a terminal): rename `prototype_continuity_0_1` to whatever you prefer. Git tracking will follow the folder; the `.git` directory inside it is self-contained.
4. From now on, use the new path:
   ```
   cd "C:\Users\steve\Documents\Claude Workspace\Atlas\<new-name>"
   ```

The GitHub repository name is independent of the local folder name. Renaming locally has no effect on GitHub.

## Common things to do

| I want to... | Run this |
|---|---|
| See if anything is broken | `python scripts/build.py` |
| View the site | `cd public && python -m http.server 8000`, then open `http://localhost:8000` |
| Stop the server | `Ctrl+C` |
| See what I changed | `git status` |
| Save changes to GitHub | `git add . && git commit -m "msg" && git push` |
| Get changes from GitHub on a new machine | `git clone <repo-url>`, then `cd` in, then `python scripts/build.py` |

## Things to remember

- **Never edit anything in `public/`.** It is rebuilt from scratch every time. Source files live in `content/`, `templates/`, `static/`, `scripts/`, and `stewardship/`.
- **Always rebuild after editing.** If you edit a markdown file but do not rebuild, the website does not update. Run `python scripts/build.py`.
- **The local server is just for viewing.** It does not need to be running unless you are looking at the site.
- **Errors name the file and the problem.** Read the message before guessing.

## When you are stuck

Most issues come from one of these:

1. **Forgot to rebuild after editing.** Run `python scripts/build.py` and refresh the browser.
2. **Editing the wrong file.** If your changes do not appear, check the file path. It should be inside `content/`, not `public/`.
3. **CSS not loading.** You opened `public/index.html` directly. Use the local server.
4. **Build error.** Read the message. It usually says "Missing field X in Y" or "Broken relationship A -> B."

For more detail, see [stewardship/local-use.md](stewardship/local-use.md).
