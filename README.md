# Open ATLAS

[Launch ATLAS](https://stevenfrye30.github.io/Atlas/)

---

A small static-site archive built from markdown files by a Python script. The link above opens the live reading environment in your browser; nothing else is required.

If you want to run or edit ATLAS locally, read on. New to the project? Read **[START_HERE.md](START_HERE.md)** first.

## One-click local launch (Windows)

Double-click `launch-atlas.bat` in the project root. It builds the site, opens your browser, and starts a local server. Press `Ctrl+C` in the terminal window (or close the window) to stop.

## Manual local build and view

```
python scripts/build.py
cd docs && python -m http.server 8000
```

Then open `http://localhost:8000`. Stop the server with `Ctrl+C`.

## Folder map

| Folder | What it is | Edit? |
|---|---|---|
| `content/` | Source: entity markdown files and region articulations | **Yes** |
| `stewardship/` | Source: documentation about how the project works | **Yes** |
| `templates/` | Source: HTML templates the build script uses | Carefully |
| `static/` | Source: CSS file | Carefully |
| `scripts/` | Source: the build script | Carefully |
| `docs/` | **Generated** — the rendered site, rebuilt by `python scripts/build.py`. Committed so GitHub Pages can serve it. | **No, ever** |

## What to edit

- Markdown files under `content/regions/<region>/entities/` — the entities themselves.
- The region articulations at `content/regions/<region>/_region.md`.
- Any markdown file under `stewardship/`.
- `README.md` and `START_HERE.md`.

## What not to touch

- Anything inside `docs/`. It is rebuilt from source on every `python scripts/build.py` run. Edits there are overwritten.

## Update workflow

```
# 1. edit source files under content/, stewardship/, templates/, static/, or scripts/
python scripts/build.py            # 2. regenerate docs/
git status                         # 3. see what changed
git add .                          # 4. stage edits + new docs/
git commit -m "brief message"      # 5. commit
git push                           # 6. push — GitHub Pages updates automatically
```

GitHub Pages serves `docs/` from the `main` branch. Pushing a commit that updates `docs/` updates the live site within about a minute.

## More documentation

For day-to-day local use:
- [START_HERE.md](START_HERE.md) — step-by-step beginner walkthrough
- [stewardship/local-use.md](stewardship/local-use.md) — practical workflow

For how the project is built and maintained:
- [stewardship/disciplines.md](stewardship/disciplines.md) — what the project commits to
- [stewardship/editorial-constitution.md](stewardship/editorial-constitution.md) — editorial work
- [stewardship/editorial-conventions.md](stewardship/editorial-conventions.md) — working conventions
- [stewardship/relationship-vocabulary.md](stewardship/relationship-vocabulary.md) — relationship types
- [stewardship/workflow.md](stewardship/workflow.md) — the day-to-day workflow
- [stewardship/cadence.md](stewardship/cadence.md) — pacing of editorial work
- [stewardship/apprenticeship.md](stewardship/apprenticeship.md) — onboarding new stewards
- [stewardship/decisions/](stewardship/decisions/) — record of editorial decisions

## Requirements

Python 3.8 or later. Standard library only — no `pip install` required.

## Troubleshooting

| Problem | Fix |
|---|---|
| Build fails with `VALIDATION ERROR` | Error names the file. Fix the front matter or relationship target. |
| Build fails with `BROKEN LINK` | Stale file in `docs/`. Delete `docs/` and rebuild. |
| Live site shows old content after pushing | Wait ~1 minute. GitHub Pages takes a moment to redeploy. Hard-refresh the browser (`Ctrl+F5`). |
| Live site is missing CSS or pages | Confirm `docs/` was committed and pushed. Check the GitHub Pages settings: source `main`, folder `/docs`. |
| Port 8000 in use locally | Use a different port: `python -m http.server 8001` |
| `python: command not found` | Try `python3`, or install Python from [python.org](https://www.python.org/downloads/). |
