# Stewardship Workflow

This is the operational workflow stewards use day-to-day. It is intentionally low-tech.

## Tools required

- A text editor.
- Python 3.
- A terminal.
- A web browser.
- Git.

That is the entire toolchain.

## Adding a new entity

1. Decide the entity is warranted. Editorial discussion among stewards. Reference disciplines and editorial conventions.
2. Choose the entity ID: `{type}-{name}`, e.g., `practice-marana-sati`.
3. Create the file: `content/regions/{region}/entities/{id}.md`.
4. Write front matter (YAML between `---` markers) and editorial body (markdown).
5. Run the build:
   ```
   python scripts/build.py
   ```
6. If validation fails, fix the errors and rerun. The script reports specific issues.
7. Preview locally:
   ```
   cd public && python -m http.server 8000
   ```
   Open `http://localhost:8000`.
8. Read the rendered entity page. Read the region page. Follow the adjacencies. Confirm the work reads as intended.
9. If a relationship on this entity points to another entity, consider whether the reverse relationship (on that entity) is warranted. If so, edit it now in a separate change.
10. Commit:
    ```
    git add content/regions/{region}/entities/{id}.md
    git commit -m "Add {id}: brief description"
    ```
11. Push to the remote. Another steward reviews. After review, the change is on `main` and deploys on next deploy cycle.

## Revising an existing entity

Same workflow as adding. Update the `date_revised` field if the revision is substantial. Commit message identifies the kind of revision: "Revise {id}: brief description of change."

## Validating before commit

The build script validates:
- Required front matter fields present.
- Entity type is in the allowed vocabulary.
- Region is in the allowed vocabulary.
- Entity id matches filename.
- All relationship targets resolve to existing entities.
- No duplicate entity ids.
- All internal links in rendered output resolve.

If any check fails, the build exits non-zero. The commit should not proceed until validation passes.

## Local preview

```
python scripts/build.py
cd public && python -m http.server 8000
```

The site renders at `http://localhost:8000`. Reload the browser after each rebuild.

## Reviewing changes

Stewards reviewing another steward's change:

1. Pull the branch or fetch the changes.
2. Run the build locally.
3. Read the affected entities and any pages whose adjacencies reference them.
4. Consider:
   - Does the editorial prose match the conventions?
   - Are the relationships substantive and sparse?
   - Is the front matter complete and correct?
   - Is the work consistent with the disciplines?
5. Approve, request revision, or discuss.

## Deployment

Static hosting deploys automatically on push to `main`, or manually via:

```
rsync -av public/ user@host:/path/to/site/
```

(The actual deploy command depends on the chosen host. Document the specific command in this file when deployment is set up.)

## When something goes wrong

- **Build fails on validation**: read the error message. It identifies the file and the issue.
- **Site renders wrong**: clear `public/` and rebuild. If the rendering is still wrong, examine templates and CSS.
- **Local preview doesn't show recent changes**: rebuild first, then refresh the browser.
- **Broken links in production**: the build's link checker should catch these before deploy. If something gets through, fix the source and redeploy.

## Long-term stewardship tasks

Beyond the day-to-day work:

- Periodic review of all entities for editorial consistency.
- Periodic audit of citations and provenance.
- Periodic external link check (for entities that cite external resources).
- Periodic stewardship documentation review.
- Annual full backup verification (can the site be rebuilt from backups?).

These tasks are not urgent but should occur on slow rhythms. Annual reviews are reasonable for most. Stewardship documentation should be updated whenever significant operational learning occurs.
