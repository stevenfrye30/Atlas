# 2025-05-08: Initial skeleton

## Decision

Build the first minimal continuity environment prototype according to the operational specification produced through the prior analytical sequence. Initial scope:

- Two regions: Death, Breath.
- Four initial entities: concept-death, term-marana, concept-breath, term-prana.
- Static-site generator written in Python stdlib only.
- Custom YAML-subset parser within the build script (no pyyaml dependency for the initial prototype).
- Markdown body rendering supporting paragraphs and second-level headings only — no lists, links, or block quotes in editorial bodies.
- Single hand-written CSS stylesheet.
- No JavaScript in the initial prototype.

## Reasoning

The first prototype tests whether the framework's principles can take operational form without compromise. Choosing the most restrained possible technical baseline does two things: it makes the prototype maximally durable, and it forces the disciplines to do the work rather than letting infrastructure substitute for them.

Custom YAML parsing (rather than pyyaml) was chosen to verify that stdlib-only is genuinely viable. If pyyaml proves necessary at scale, that decision can be made then, with a record of why.

Markdown rendering is intentionally tiny because editorial bodies do not need lists, links, or block quotes. The links between entities are rendered through the adjacency system, not through inline markdown links — this preserves editorial control over where adjacencies appear.

## Open questions

- How will translation toggles render once primary-source materials are added? Deferred until the second region has at least one full passage.
- How will original-script display work for entities whose script is not Latin? Deferred until first non-Latin material is added.
- Whether to include the third region (Self) in the first six months. Deferred to month-3 review.

## Stewards involved in this decision

(To be filled in when stewardship structure is established.)
