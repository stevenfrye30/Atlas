# Editorial Conventions

The conventions below govern how editorial work is performed. They are operational guidance, not absolute rules. Stewards apply judgment within them.

## Prose register

Editorial articulations are written in restrained, careful prose. The register is closer to scholarly than to journalistic but does not perform scholarship — there are no citations of secondary literature in the editorial body, no arguments against other interpretations, no positioning of the entity within disciplinary debates. The prose holds the entity; it does not argue about it.

Tone is grave but not heavy. Atmospheric register emerges from how the material is held, not from emphatic language. Adjectives are sparse. Adverbs are sparser.

## Length

Most entity articulations are 100–400 words in the main body. Longer is permitted where the material warrants; shorter is permitted where the discipline of restraint applies. There is no standard length, only the length the editorial work produces.

## Structure

Entities have:

- Front matter (YAML).
- Main editorial articulation (paragraphs).
- Optional `## Notes` section for stewardship observations that should be visible to readers but are not part of the central articulation.

Avoid further structural complexity in editorial bodies. Sub-headings beyond `## Notes` are typically unnecessary.

## Untranslated terms

Source-language terms are preserved with diacritics in display. They appear in italics within editorial prose: *prāṇa*, *maraṇa*, *dharma*. The glossing in front matter is brief and pointing rather than equating.

When a term first appears in an editorial body, the gloss may be parenthetical: "*maraṇa* (death)". On subsequent appearances within the same entity, no gloss is needed.

## Cross-civilizational handling

When discussing relations among civilizational frameworks, prefer "typologically resembles" over "is equivalent to," "is the [civilization] counterpart of," etc. The structurally_similar relationship type carries the right ontological weight.

When in doubt about a comparative claim, hold the question open in the editorial prose. Notes sections are appropriate for marking what is currently unresolved.

## Front matter

Required fields:
- `id`: matches the filename (without `.md`).
- `title`: display title with diacritics and original-script characters.
- `type`: from the bounded vocabulary (see relationship-vocabulary.md).
- `region`: `death`, `breath`, or `self`.

Optional but encouraged:
- `provenance`: typically `editorial`.
- `date_created`, `date_revised`: ISO dates.
- `status`: `draft`, `published`, `under_revision`.
- `relationships`: list of relationship mappings.

Type-specific:
- For language_term: `script`, `transliteration`, `language`, `gloss`.
- For text: `author`, `date_range`, `original_language`, `tradition`.
- For passage: `text` (work id), `section`.
- For practice: `tradition`, `body_anchor`.

## Adding a new entity

1. Choose the entity ID following the `{type}-{name}` pattern.
2. Create the file at `content/regions/{region}/entities/{id}.md`.
3. Write front matter and editorial body.
4. Run `python scripts/build.py` to validate.
5. Review the rendered page locally.
6. If editing relationships on existing entities to point to the new one, update those entities too.
7. At least one other steward reviews before commit.
8. Commit with a message identifying the entity and the kind of work (added, revised, restructured).

## Revising an entity

Revisions follow the same workflow as additions. Substantial revisions update `date_revised`. Minor revisions (typo fixes, small wording adjustments) need not.

If a revision substantially changes how an entity is held, note the change in `decisions/` so successor stewards can understand the development.

## When in doubt

When unsure whether something rises to the level of editorial inclusion — a new entity, a new adjacency, an additional sentence — the default is to wait. The work survives waiting. It does not always survive premature inclusion.
