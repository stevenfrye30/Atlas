# Local Use

Practical workflow for using the project on your own computer. Companion to README.md.

## Opening the project

1. Open a terminal (Git Bash, PowerShell, or Command Prompt).
2. `cd` into the project root:
   ```
   cd "C:/Users/steve/Documents/Claude Workspace/Atlas/prototype_continuity_0_1"
   ```
3. From here, all commands in the README run as written.

## Rebuilding after edits

After you edit any file in `content/`, `templates/`, or `static/`:

```
python scripts/build.py
```

This rewrites `public/` from scratch. Build time is under one second on this corpus.

You will see output like:

```
Built 24 entities across 2 regions.
Total authored relationships: 65
Output: C:\Users\steve\Documents\Claude Workspace\Atlas\prototype_continuity_0_1\public
```

If you see anything else (an error, a stack trace), the build failed. Fix the issue named in the error and run again. The site will not have updated on a failed build.

## Checking that the build worked

Visual check:

```
cd public
python -m http.server 8000
```

Open `http://localhost:8000` and click around. The pages you edited should reflect your changes. Stop the server with `Ctrl+C` when done.

Mechanical check:

The build script automatically validates:
- Required front matter on every entity
- Every `relationships:` target resolves to a real entity
- No broken internal links in the rendered HTML

If all of those pass, the build succeeded. The output line `Built N entities across M regions.` confirms it.

## Avoiding accidental edits to generated files

The danger: opening a file under `public/` thinking it is source, editing it, then losing those edits the next time the build runs.

How to avoid it:
- Never edit anything under `public/`.
- If you find yourself looking at a file path that contains `/public/`, you are looking at generated output. Close it. Find the corresponding source file under `content/` instead.
- Source files end in `.md` and live in `content/`, `stewardship/`, or the root.
- Generated files end in `.html` and live in `public/`.

If you ever doubt whether a file is source or generated: delete `public/`, run `python scripts/build.py`, and see whether the file came back. If it did, it was generated.

## Committing to GitHub

First time only:

```
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

Then create a repository on GitHub (web interface), and run the URL it gives you:

```
git remote add origin git@github.com:<your-username>/<your-repo>.git
git push -u origin main
```

Subsequent commits, after editing source:

```
python scripts/build.py     # confirm the build still works
git status                  # see what changed
git add <files-you-changed>
git commit -m "Brief description of the change"
git push
```

`public/` is gitignored, so it will not be included even if you `git add .`. You should never see `public/` in `git status` output.

## Pulling changes onto another machine

```
git clone git@github.com:<your-username>/<your-repo>.git
cd <repo-name>
python scripts/build.py
```

That gives you the source plus a freshly built `public/`. View locally as described above.

## What you should and should not edit

**Edit freely:**
- Files in `content/regions/<region>/entities/` — the entity markdown files.
- Files in `content/regions/<region>/_region.md` — the region articulations.
- `README.md`.
- Files in `stewardship/` — disciplines, conventions, decision records.

**Edit carefully:**
- `scripts/build.py` — changes here affect everything. Read the section you are changing fully before editing.
- `templates/*.html` — affect every rendered page.
- `static/style.css` — affects every rendered page's appearance.
- `.gitignore` — controls what git includes.

**Do not edit:**
- Anything under `public/`. Always overwritten on next build.

## Running on a new computer

If you move to another machine or set this up for the first time elsewhere:

1. Install Python 3.8 or later (most systems already have it; check with `python --version`).
2. Clone the repo (`git clone <url>`) or copy the folder.
3. Run `python scripts/build.py` to verify the build works.
4. Run `cd public && python -m http.server 8000` to view.

No `pip install`, no virtual environment, no other setup is required. The build uses only the Python standard library.

## When the build fails

Most failures are validation errors with clear messages naming the file and the issue. Common ones:

- `Missing field 'X' in <file>` — add the field to the YAML front matter.
- `Invalid type 'X' in <file>` — the `type:` field has a value not in the vocabulary. Check `stewardship/relationship-vocabulary.md`.
- `id 'X' does not match filename 'Y'` — the `id:` in front matter and the filename (without `.md`) must match.
- `Broken relationship: A -> B` — entity A points to entity B which does not exist. Either create B, or remove the relationship from A.
- `Duplicate entity id: X` — two files have the same `id:` field. Make them unique.
- `BROKEN LINK in <file>` — usually means a stale file in `public/`. Delete `public/` and rebuild.

## When something else goes wrong

If the build crashes with a Python traceback (not a validation error), something has gone wrong with the script itself. The traceback names the line. The script is in `scripts/build.py` and is small enough to read end-to-end if needed.

If the rendered site looks wrong (CSS broken, links wrong, content garbled), check:
1. Did you save the source file before rebuilding?
2. Did you actually rebuild? (`python scripts/build.py` after the edit.)
3. Is your browser caching old CSS? Hard-refresh (`Ctrl+F5` or `Cmd+Shift+R`).

If the local server (`python -m http.server`) won't start: another process is using port 8000. Use a different port (`python -m http.server 8001`).
