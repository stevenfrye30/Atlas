# ATLAS

A small static-site archive built from markdown source files by a Python script.

## Requirements

- Python 3.8 or later. Standard library only — no `pip install` needed.

## Build

From the project root:

```
python scripts/build.py
```

The build reads `content/`, applies templates from `templates/`, copies `static/`, and writes the rendered site to `public/`.

If the build fails, the error message names the file and the problem. Fix and run again.

## View locally

`public/index.html` uses absolute URLs and will not work when opened directly in a browser. Run a local server instead:

```
cd public
python -m http.server 8000
```

Then open `http://localhost:8000` in any browser. Stop the server with `Ctrl+C`.

## Folder structure

| Folder | Purpose | Edit? |
|---|---|---|
| `content/` | Source: entity markdown files and region articulations | Yes |
| `templates/` | Source: HTML templates | Carefully |
| `static/` | Source: CSS and other static assets | Carefully |
| `scripts/` | Source: the build script | Carefully |
| `stewardship/` | Source: disciplines, conventions, decision records | Yes |
| `public/` | Generated: rebuilt by every `build.py` run | **No** — overwritten on rebuild |
| `README.md` | This file | Yes |
| `.gitignore` | Tells git what to skip (incl. `public/`) | If needed |

## Adding a new entity

1. Read `stewardship/editorial-conventions.md` and `stewardship/cadence.md`.
2. Decide whether the entity is genuinely warranted. The default answer is "not yet."
3. Create a new markdown file under the appropriate path, e.g. `content/regions/death/entities/new-entity.md`.
4. Write the YAML front matter (see existing entities for the pattern) and the body.
5. Run `python scripts/build.py`. Fix any validation errors.
6. View the result at `http://localhost:8000`.
7. Commit when satisfied.

## Common tasks

**Rebuild after editing source:**
```
python scripts/build.py
```

**Rebuild and view in one go (Bash):**
```
python scripts/build.py && cd public && python -m http.server 8000
```

**Discard the generated site and start fresh:**
```
rm -rf public
python scripts/build.py
```

(On Windows Command Prompt: `rmdir /s /q public` instead of `rm -rf public`.)

## Committing to GitHub

The project is git-ready. To initialize and push for the first time:

```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

`public/` will be ignored automatically. No secrets or credentials are stored in any source file. Everything in the repo is safe to commit.

For ongoing changes: edit source files → run `python scripts/build.py` to verify the build succeeds → `git add` and `git commit` the source changes (not `public/`).

## Troubleshooting

**`python: command not found`**
Use `python3` instead, or install Python 3 from python.org.

**The build fails with `VALIDATION ERROR: ...`**
The error names a specific file and field. Fix the front matter or the relationship target it complains about, then re-run.

**The build fails with `RELATIONSHIP ERROR: ... -> some-id`**
You referenced an entity that does not exist. Either create it, or remove the reference from the entity's `relationships:` list.

**The build fails with `BROKEN LINK in ...`**
A page references a file that the build did not produce. Usually this means a stale file in `public/`. Delete `public/` and rebuild.

**`http://localhost:8000` shows nothing or "directory listing"**
Make sure you are running `python -m http.server 8000` from inside `public/`, not from the project root.

**CSS doesn't load when I open `public/index.html` directly**
This is expected — see "View locally" above. Use the local server.

**Port 8000 is already in use**
Pick another port: `python -m http.server 8001` and open `http://localhost:8001`.

## More documentation

- `stewardship/disciplines.md` — what the project commits to and refuses.
- `stewardship/editorial-constitution.md` — how editorial work is performed.
- `stewardship/editorial-conventions.md` — working conventions for adding/editing entities.
- `stewardship/relationship-vocabulary.md` — the relationship type list.
- `stewardship/workflow.md` — the day-to-day workflow.
- `stewardship/apprenticeship.md` — how new stewards are formed.
- `stewardship/cadence.md` — rhythm and pacing of editorial work.
- `stewardship/local-use.md` — practical local-machine workflow (this document's companion).
- `stewardship/decisions/` — record of editorial and structural decisions.
