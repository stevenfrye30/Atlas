# Editorial Constitution

This document articulates the editorial disciplines that govern stewardship work in ATLAS. It is operational, not aspirational — each rule has emerged from a specific moment in editorial work when honoring or violating the discipline produced a visible consequence.

The constitution is read by stewards considering an editorial decision. It is not read by readers of the architecture. Where an editorial principle should be visible to readers, the entity's own prose articulates it; where the principle is stewardship-internal, this constitution carries it.

The constitution is provisional. Stewards may refine it as further work reveals where its articulations need refinement. Refinements are recorded in `decisions/`.

## I. Material primacy

The architecture exists to support reader encounter with civilizationally significant material. Every editorial decision is evaluated against this purpose.

1. The reader's encounter is with the material, not with the architecture.
2. The architecture's work is to hold the material such that encounter remains possible; it is not to interpret the material on the reader's behalf.
3. When a decision would shift reader attention from the material to the architecture's framing of the material, the decision violates material primacy.

## II. Civilizational specificity

Each tradition is held within its own conceptual structure. Cross-civilizational comparison is preserved as resemblance, not as equivalence.

1. Source-language terms remain in their source languages where translation would import frames the source does not articulate (`asubha-bhāvanā` not "foulness meditation"; `lǐ` not "ritual propriety"; `prāṇa` not "breath/spirit").
2. Glosses are partial and gestural; they do not equate.
3. Civilizational frameworks are not absorbed into a comparative meta-position. The architecture refuses synthetic claims that would require a vantage from above the civilizations it engages.
4. Resemblances among civilizations are marked through `structurally_similar`, with explicit articulation in entity prose of what the resemblance is and is not.

## III. Editorial restraint

Editorial prose holds the entity at the depth the editorial work has actually been performed. Restraint is the default; further articulation must justify itself.

1. Entity bodies are typically 100–400 words. Longer is permitted where the material warrants; shorter is permitted where restraint applies.
2. Each editorial point is made once at the architecturally appropriate location and referenced (not repeated) elsewhere.
3. Where the same point would be made in a passage's prose and in the practice that the passage articulates, the more specific location carries the point.
4. Notes sections are stewardship reflection. They do not duplicate the entity's articulation.

## IV. Commentary boundaries

Commentary is warranted when reader encounter with the material would otherwise miss its structure. It is excessive when it begins doing the reader's interpretive work.

1. Commentary articulates structure; it does not articulate meaning. (The structure of the *Liji* passage's "third position" is articulable; what the third position means for the reader's life is not the architecture's editorial scope.)
2. When the material can carry its own structure on the page, commentary should be silent.
3. Commentary that explains the architecture's commitments belongs in stewardship documentation, not in entity prose.
4. The Notes section may articulate translation tension, civilizational specificity, or stewardship reasoning where these are necessary. It may not articulate philosophical positions the architecture should not take.

## V. Translation honesty

Three regimes are available: untranslated terms, established translations with attribution, and editorial paraphrase explicitly marked. Each has appropriate use.

1. Untranslated terms are used when standard translations import frames the source does not articulate, or when the term operates as a concept within the editorial work itself.
2. Established translations are rendered with full attribution: translator, edition, publisher, year, license status.
3. Editorial paraphrases are marked transparently as such with `[Editorial paraphrase]` or equivalent; they are not represented as scholarly translations.
4. Where multiple respected translations diverge substantively, both (or several) are rendered; the disagreement is articulated in the Notes section without resolution.
5. The architecture does not adjudicate among translations. The reader's relation to the translation question is the reader's.

## VI. Adjacency discipline

Each adjacency is a deliberate editorial judgment. Sparseness is the default.

1. Each entity typically has 3–6 adjacencies. Numbers below or above this range require justification.
2. The default answer to "should this adjacency exist?" is "no, unless the relation rises to the level of editorial inclusion."
3. Hub-formation is corruption. When an entity accumulates many adjacencies because it is structurally central, prefer chains (concept ← term ← practice) to star topologies.
4. `structurally_similar` is reserved for typological resemblance across civilizations and requires articulation in entity prose of what the resemblance is and is not.
5. `related_to` is the weakest adjacency type and the appropriate choice when relation is real but does not warrant a more specific type.
6. The relation between *practice-marana-sati* and *practice-li-mourning* is an example of where weak adjacency or no adjacency is correct: the practices are co-domain (death) but not typologically similar in the relevant sense.
7. Asymmetric authoring is permitted; mechanical bidirectionality is not required. The architecture permits A to link to B without B linking back if the editorial judgment differs at each side.

## VII. Ontology restraint

The relationship vocabulary and entity-type list are editorial infrastructure, not the editorial work itself. They expand only when prose can no longer carry the work.

1. New entity types are added only when an entity that genuinely belongs cannot be classified within existing types without distortion.
2. New relationship types are added only when the relation will recur and existing types cannot carry it with appropriate framing.
3. Front-matter fields are minimal. Each field is a small commitment that future stewards must understand and maintain.
4. Where the case is rare, prose carries the complexity. The *Liji*'s recension issues are carried in prose; the relationship vocabulary is not extended for one entity.
5. The dual-mechanism patterns (e.g., `related_to: X` with `framing: structurally_similar` versus `structurally_similar: X` directly) should be standardized. When a relation has its own type in the vocabulary, the direct type is used.

## VIII. Omission as editorial act

What the architecture does not contain is part of what it preserves. Visible omission is editorial; unmarked omission is silent failure.

1. Where the material exceeds current stewardship competence, the entity is deferred. Premature inclusion produces thinner work than non-inclusion does.
2. Visible incompleteness is structural — it prevents the reader from mistaking the architecture for the territory.
3. Entity prose acknowledges what is deferred where the deferral is significant. *concept-death*'s prose acknowledges other expressions; *practice-li-mourning*'s Notes acknowledge other dimensions.
4. The architecture does not promise eventual completeness. Some material will never be rendered; the discipline is to hold this honestly rather than as future work.
5. A civilization's absence from a region is not a deficit to be repaired by quick coverage; it is the architecture's honesty about its current scope.

## IX. Provenance visibility

Reader trust depends on knowing what they are reading and where it came from.

1. Every primary-source passage is rendered with full citation: text, edition, translator (where applicable), publisher, year, license status.
2. The editorial layer is visibly distinguished from the source layer. Editorial articulations are the architecture's voice; primary-source passages are not.
3. Editorial paraphrases are marked transparently; they do not pose as established translations.
4. Where source provenance is itself complex (compilation, recension, contested attribution), the complexity is articulated in the text entity's prose.
5. Provenance is articulated once at the appropriate level and referenced elsewhere.

## X. Boundedness

The architecture is small by structural commitment, not by current limitation.

1. Each region holds the number of entities the editorial work can sustain at the architecture's care-level. New entities are added when the editorial work is genuinely complete, not on a schedule.
2. New regions are not opened until existing regions have reached warranted depth and stewardship capacity exceeds what existing regions require.
3. The architecture does not pursue scale. Reach is not a goal; depth is.
4. Stewardship plurality is small (3–7 active stewards). Beyond this scale, shared editorial sensibility cannot be sustained.

## XI. Revisability

The architecture's commitments are open to refinement as understanding develops.

1. Entities may be revised when the editorial work no longer warrants what was previously claimed. Revisions are committed to git with clear reasoning.
2. Substantial revisions update `date_revised`. The git history preserves the development trajectory.
3. Where a revision withdraws a claim, the entity's Notes section may briefly acknowledge what was withdrawn and on what grounds.
4. The disciplines themselves are revisable. Where an articulation in this constitution is found inadequate, it may be revised, with reasoning recorded in `decisions/`.
5. Reversal is not failure of stewardship. Stewardship that cannot reverse will produce ossification.

## XII. Anti-totalization

The architecture refuses to claim total coverage, definitive interpretation, or universal application.

1. Coverage is partial by structural choice. The architecture acknowledges what it does not cover.
2. The interpretive work is the reader's. The architecture's articulations support reader encounter; they do not produce the interpretation that should result.
3. The architecture does not adjudicate disputes within or among traditions. It preserves the disputes where they exist.
4. The framework's own articulations (this constitution, `disciplines.md`) are operational, not metaphysical. They govern editorial work; they do not claim insight into "how things really are."
5. The architecture is one small site of continuity work. It does not claim to be the right form, the necessary form, or the universal form. It is what current stewardship has chosen to build under current conditions.

## XIII. Architectural invisibility

The architecture exists to hold material; over time it should disappear into that holding.

1. Entity prose refers to what the entity does, not to what the architecture commits to. Discipline-language ("the architecture is committed to...") belongs in stewardship documentation, not in entity bodies.
2. Notes sections discuss the specific entity, not the framework in general. Meta-commentary is justified when the reader needs to understand the editorial posture to encounter the material correctly; it is unjustified when it is general or self-referential.
3. The architecture's structure should be perceptible to readers who attend to it but should not press on every page. A reader who does not perceive the architecture's commitments has nonetheless been served by them.
4. Stewardship documentation may be elaborate; entity prose must not be. The two registers are different and should remain different.

## XIV. Stewardship as practice

Stewardship is not a profession or institutional role. It is a practice undertaken by people who have made themselves capable of it through disciplined work.

1. Stewardship work is editorial; it is not managerial, administrative, or curatorial in any institutional sense.
2. Stewardship requires capacities that are cultivated, not credentialed: sustained attention, civilizational humility, comfort with the unresolved, restraint as practice, disciplined reading, patience, tolerance of incompleteness.
3. Stewardship transmission is through apprenticeship. New stewards form by working alongside existing stewards on actual editorial decisions, over time.
4. Stewardship is invisible by structure. The work does not produce credit, recognition, or institutional standing within the architecture.
5. The steward who has begun perceiving themselves as "the steward" — a role with identity — has begun a drift the disciplines forbid. The discipline is to remain a person doing editorial work, not to become a custodian of editorial work.

## Application

When facing an editorial decision:

1. Identify which disciplines apply. Most non-trivial decisions touch multiple.
2. Where disciplines are in tension, articulate the tension before resolving. The articulation is itself stewardship work.
3. Where the right decision exceeds current understanding, defer rather than force. Deferral is permitted; premature decision is not.
4. Record substantive decisions in `decisions/` with reasoning. The record is part of the work.
5. Where the constitution is silent on a question, note this — the silence may indicate that the constitution should be extended, or that the question is properly outside the architecture's scope.

## Limits of the constitution

Several things this document cannot do:

- It cannot replace the editorial sensibility that makes the disciplines applicable to specific cases. The articulations help; the judgment is the steward's.
- It cannot anticipate every situation. Future editorial work will produce situations the constitution did not foresee; these are revisability cases.
- It cannot guarantee that following its rules produces good editorial work. Following rules without inhabited sensibility produces compliance, not stewardship.
- It cannot prevent corruption that occurs slowly. Slow drift is the standard pattern of small-scale work degrading; the constitution articulates the disciplines but stewardship vigilance enacts them.

The constitution is a tool, not a guarantee. Its existence does not preserve the architecture; the practice of inhabiting its disciplines preserves the architecture, and the practice is the steward's continuous work.
