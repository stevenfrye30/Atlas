# ATLAS

A small static-site archive built from markdown files by a Python script.

New here? Read **[START_HERE.md](START_HERE.md)** first.

## Quick start

```
python scripts/build.py
cd public && python -m http.server 8000
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
| `public/` | **Generated** — rebuilt every time you run the build | **No, ever** |

## What to edit

- Markdown files under `content/regions/<region>/entities/` — the entities themselves.
- The region articulations at `content/regions/<region>/_region.md`.
- Any markdown file under `stewardship/`.
- `README.md` and `START_HERE.md`.

## What not to touch

- Anything inside `public/`. It is rebuilt from source on every `python scripts/build.py` run. Edits there are overwritten.

## Rebuilding

After any edit:

```
python scripts/build.py
```

A successful build prints `Built N entities across M regions.` Errors name the file and the problem.

## GitHub workflow

```
git status                          # see what changed
git add <files>                     # stage your changes
git commit -m "brief message"       # commit
git push                            # send to GitHub
```

`public/` is gitignored and will not appear in `git status`.

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
| Build fails with `BROKEN LINK` | Stale file in `public/`. Delete `public/` and rebuild. |
| Page looks unstyled | You opened `public/index.html` directly. Use the local server (above). |
| Port 8000 in use | Use a different port: `python -m http.server 8001` |
| `python: command not found` | Try `python3`, or install Python from [python.org](https://www.python.org/downloads/). |
