# Relationship Vocabulary

The relationship vocabulary is bounded. Adding new types requires editorial discussion and a decision record. The existing vocabulary should suffice for most cases.

## Entity types

- `concept` — anchor entity for a region (Death, Breath).
- `language_term` — a word in a source language carrying conceptual structure.
- `ritual_practice` — an enacted discipline (e.g., maraṇa-sati).
- `text` — a complete work (e.g., Yoga Sūtras).
- `passage` — a specific section within a text.
- `body` — a body region or anatomy as held by a tradition.
- `phenomenology` — a structured first-person register (e.g., breath-attention).
- `state` — an inhabited register (e.g., mortality-awareness).
- `place` — a geographically located site significant within a tradition.
- `tradition` — a tradition treated as an entity.
- `person` — a named historical figure significant within a tradition.
- `art_material` — a physical or visual artifact category.

## Relationship types

Each is the YAML key in a relationship mapping; the value is the target entity id. An optional `framing:` field can override the default display phrasing.

| Type | Default framing | Use |
|------|-----------------|-----|
| `relates_to` | "Anchor:" | Hierarchical anchoring (term → concept). |
| `related_to` | "Related:" | Peer-link between entities of the same kind. |
| `expressed_by_term` | "Names this in canonical language:" | Concept → its linguistic expressions. |
| `uses_term` | "Uses the term:" | Passage or practice that uses a specific term. |
| `works_with` | "Operates on:" | Practice operates on an entity (e.g., a body anchor). |
| `supports` | "Supports:" | Body or practice supports another entity. |
| `contains` | "Contains:" | Text contains a passage. |
| `structurally_similar` | "Typologically similar across civilizations:" | Cross-civilization typological resemblance — never genealogical. |
| `translated_as` | "Translated as:" | Linguistic translation relation. |
| `contradicts` | "In tension with:" | Explicit unresolved tension. |
| `located_in_body` | "Located in:" | Phenomenology or practice located in a body anchor. |
| `belongs_to` | "Belongs to:" | Institutional or traditional belonging. |
| `originated_in` | "Originated in:" | Place of origin. |
| `appears_in` | "Appears in:" | Entity appears in a passage or text. |
| `used_in` | "Used in practice:" | Term used in a specific practice. |

## Framing overrides

The optional `framing:` field on a relationship maps to a custom display phrase. Currently recognized:

| Override | Display phrase |
|----------|----------------|
| `anchor` | "Anchor concept:" |
| `structurally_similar` | "Typologically similar across civilizations:" |

When introducing a new framing override, register it in `scripts/build.py` (`FRAMING_OVERRIDES`) and document it here.

## Discipline of sparseness

Each entity should have few relationships. The discipline:

- Concepts typically have 2–4 relationships (mostly to terms that name them).
- Language terms typically have 2–6 relationships (to concept, to practices that use them, to typological siblings).
- Practices typically have 3–6 relationships.
- Texts typically have 2–5 relationships.
- Passages typically have 3–6 relationships.

These are guides, not limits. The discipline at each candidate relationship is the substantive question, not the count.

## When a relationship is wrong

If a relationship turns out to be misleading, removing it is appropriate stewardship work. Document the removal in `decisions/` if the reasoning would not be obvious to a successor steward.
