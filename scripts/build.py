#!/usr/bin/env python3
"""
ATLAS continuity environment build script.

Reads source markdown files from content/, applies templates from templates/,
writes static HTML to public/. Stdlib only.

Run from the repository root:
    python scripts/build.py
"""

from __future__ import annotations

import html
import re
import shutil
import string
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
PUBLIC = ROOT / "public"


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

VALID_ENTITY_TYPES = {
    "concept",
    "language_term",
    "ritual_practice",
    "text",
    "passage",
    "body",
    "phenomenology",
    "place",
    "tradition",
    "person",
    "art_material",
    "state",
}

VALID_REGIONS = {"death", "breath", "self"}

# Default phrasings for relationship types in the adjacency block.
# A relationship may override these via an explicit `framing:` field.
RELATIONSHIP_FRAMINGS: dict[str, str] = {
    "relates_to": "Anchor:",
    "related_to": "Related:",
    "expressed_by_term": "Names this in canonical language:",
    "uses_term": "Uses the term:",
    "works_with": "Operates on:",
    "supports": "Supports:",
    "contains": "Contains:",
    "structurally_similar": "Typologically similar across civilizations:",
    "translated_as": "Translated as:",
    "contradicts": "In tension with:",
    "located_in_body": "Located in:",
    "belongs_to": "Belongs to:",
    "originated_in": "Originated in:",
    "appears_in": "Appears in:",
    "used_in": "Used in practice:",
}

# Custom framings keyed by an explicit `framing:` value.
FRAMING_OVERRIDES: dict[str, str] = {
    "anchor": "Anchor concept:",
    "structurally_similar": "Typologically similar across civilizations:",
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Entity:
    metadata: dict[str, Any]
    body: str
    source_path: Path

    @property
    def id(self) -> str:
        return self.metadata["id"]

    @property
    def title(self) -> str:
        return self.metadata["title"]

    @property
    def type(self) -> str:
        return self.metadata["type"]

    @property
    def region(self) -> str:
        return self.metadata["region"]


@dataclass
class Region:
    metadata: dict[str, Any]
    body: str
    source_path: Path
    entities: list[Entity] = field(default_factory=list)

    @property
    def id(self) -> str:
        # The region identifier is the parent directory name.
        return self.source_path.parent.name

    @property
    def title(self) -> str:
        return self.metadata["title"]


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class BuildError(Exception):
    pass


# ---------------------------------------------------------------------------
# Front-matter parser
# ---------------------------------------------------------------------------
# We support a small YAML subset:
#   - scalars: strings, numbers, dates (kept as strings)
#   - lists of mappings:
#       relationships:
#         - relates_to: concept-breath
#           framing: anchor
# Indentation: 2 spaces.

def split_front_matter(text: str) -> tuple[str, str]:
    """Split a markdown file into (front_matter_yaml, body_markdown)."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        raise BuildError("Front matter not closed with '---'")
    fm = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    return fm, body


def _unquote(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_front_matter(fm: str) -> dict[str, Any]:
    """Tiny YAML-subset parser sufficient for our front matter."""
    if not fm.strip():
        return {}

    lines = fm.splitlines()
    result: dict[str, Any] = {}
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            i += 1
            continue

        # Top-level keys must be at indent 0.
        if line.startswith(" "):
            raise BuildError(f"Unexpected indentation at top level: {line!r}")

        if ":" not in stripped:
            raise BuildError(f"Malformed front matter line: {line!r}")

        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()

        if rest:
            # Inline scalar value.
            result[key] = _unquote(rest)
            i += 1
            continue

        # No inline value — expect a list.
        items: list[Any] = []
        i += 1
        while i < len(lines):
            sub = lines[i]
            if not sub.strip():
                i += 1
                continue
            if not sub.startswith("  "):
                # End of the list.
                break
            if not sub.lstrip().startswith("- "):
                raise BuildError(
                    f"Expected list item under {key!r}, got: {sub!r}"
                )

            # Parse a mapping under this list item.
            first = sub.lstrip()[2:]  # drop '- '
            mapping: dict[str, str] = {}
            if ":" not in first:
                raise BuildError(
                    f"List item must be a mapping under {key!r}: {sub!r}"
                )
            sub_key, _, sub_val = first.partition(":")
            mapping[sub_key.strip()] = _unquote(sub_val.strip())

            i += 1
            # Continuation lines for this mapping are indented further (4 spaces).
            while i < len(lines):
                cont = lines[i]
                if not cont.strip():
                    i += 1
                    continue
                if cont.startswith("    ") and ":" in cont and not cont.lstrip().startswith("- "):
                    ck, _, cv = cont.strip().partition(":")
                    mapping[ck.strip()] = _unquote(cv.strip())
                    i += 1
                else:
                    break
            items.append(mapping)

        result[key] = items

    return result


# ---------------------------------------------------------------------------
# Markdown rendering (intentionally tiny)
# ---------------------------------------------------------------------------
# Supports: paragraphs, ## headings, ### headings, *italic*, **bold**,
# blank-line separation. No links, lists, or block quotes — the editorial
# articulations do not need them, and adjacency links are rendered separately.

ITALIC_RE = re.compile(r"\*([^*\n]+)\*")
BOLD_RE = re.compile(r"\*\*([^*\n]+)\*\*")


def render_inline(text: str) -> str:
    # quote=False: in body text, apostrophes and double-quotes don't need
    # to be entity-escaped. Escaping & < > is sufficient.
    text = html.escape(text, quote=False)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = ITALIC_RE.sub(r"<em>\1</em>", text)
    return text


def _render_blockquote(block: str) -> str:
    """Render a blockquote block. Lines start with '> '.

    The blockquote can contain:
      - Latin-script paragraphs (treated as a single paragraph for editorial
        prose, but original-script lines are preserved as-is so that line
        breaks in source poetry/dialogue are kept).
      - Lines marked with leading '## ' inside a blockquote are not supported;
        keep blockquotes simple.

    The first line of a blockquote may carry a `lang` attribute via a leading
    `[lang=xx]` marker, which is rendered as a class so original-script
    blockquotes can be styled distinctly. Example:

        > [lang=zh] 季路問事鬼神。子曰：「未能事人，焉能事鬼？」

    The marker is stripped from the rendered text.
    """
    lines = [ln[2:] if ln.startswith("> ") else ln[1:] for ln in block.splitlines()]
    # Detect leading [lang=xx] marker on first non-empty line.
    lang_class = ""
    if lines and lines[0].lstrip().startswith("[lang="):
        first = lines[0].lstrip()
        end = first.find("]")
        if end > 0:
            lang_code = first[6:end].strip()
            lang_class = f' class="lang-{html.escape(lang_code, quote=False)}"'
            lines[0] = first[end + 1:].lstrip()
    # If the blockquote lines are short (< 60 chars) and there are multiple
    # lines, preserve them as separate <br>-separated lines (poetry/dialogue).
    # Otherwise collapse into a single paragraph.
    nonempty = [ln for ln in lines if ln.strip()]
    if not nonempty:
        return ""
    short_lines = all(len(ln) < 80 for ln in nonempty)
    if len(nonempty) > 1 and short_lines:
        rendered = "<br>\n".join(render_inline(ln) for ln in nonempty)
    else:
        rendered = render_inline(" ".join(ln.strip() for ln in nonempty))
    return f"<blockquote{lang_class}>{rendered}</blockquote>"


def render_markdown(body: str) -> str:
    """Render the editorial prose body into HTML.

    Supported block constructs:
      - ATX headings (## and ###; # is allowed but discouraged in entity bodies)
      - Blockquotes (lines starting with '> ' or '>')
      - Attribution paragraphs (lines starting with '— ', em-dash + space)
      - Plain paragraphs

    No lists, links, fenced code, or block-level HTML pass-through. The
    discipline is intentionally narrow.
    """
    blocks = re.split(r"\n\s*\n", body.strip())
    out: list[str] = []
    for block in blocks:
        block = block.rstrip()
        if not block:
            continue
        if block.startswith("### "):
            out.append(f"<h3>{render_inline(block[4:].strip())}</h3>")
        elif block.startswith("## "):
            out.append(f"<h2>{render_inline(block[3:].strip())}</h2>")
        elif block.startswith("# "):
            out.append(f"<h1>{render_inline(block[2:].strip())}</h1>")
        elif all(ln.startswith(">") for ln in block.splitlines() if ln.strip()):
            rendered = _render_blockquote(block)
            if rendered:
                out.append(rendered)
        else:
            paragraph = " ".join(line.strip() for line in block.splitlines())
            # Detect attribution line (em-dash + space at start).
            if paragraph.startswith("— ") or paragraph.startswith("— "):
                out.append(
                    f'<p class="attribution">{render_inline(paragraph)}</p>'
                )
            else:
                out.append(f"<p>{render_inline(paragraph)}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Discovery and parsing
# ---------------------------------------------------------------------------

def discover_entities() -> list[Path]:
    return sorted((CONTENT / "regions").glob("*/entities/*.md"))


def discover_regions() -> list[Path]:
    return sorted((CONTENT / "regions").glob("*/_region.md"))


def parse_entity_file(path: Path) -> Entity:
    text = path.read_text(encoding="utf-8")
    fm, body = split_front_matter(text)
    metadata = parse_front_matter(fm)
    return Entity(metadata=metadata, body=body, source_path=path)


def parse_region_file(path: Path) -> Region:
    text = path.read_text(encoding="utf-8")
    fm, body = split_front_matter(text)
    metadata = parse_front_matter(fm)
    return Region(metadata=metadata, body=body, source_path=path)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

REQUIRED_ENTITY_FIELDS = ("id", "title", "type", "region")


def validate_entity(entity: Entity) -> list[str]:
    errors: list[str] = []
    md = entity.metadata
    rel_path = entity.source_path.relative_to(ROOT)

    for field_name in REQUIRED_ENTITY_FIELDS:
        if field_name not in md or not md[field_name]:
            errors.append(f"{rel_path}: missing field '{field_name}'")

    if md.get("type") and md["type"] not in VALID_ENTITY_TYPES:
        errors.append(f"{rel_path}: invalid type '{md['type']}'")

    if md.get("region") and md["region"] not in VALID_REGIONS:
        errors.append(f"{rel_path}: invalid region '{md['region']}'")

    expected_id = entity.source_path.stem
    if md.get("id") and md["id"] != expected_id:
        errors.append(
            f"{rel_path}: id '{md['id']}' does not match filename '{expected_id}'"
        )

    return errors


def validate_relationships(graph: dict[str, Entity]) -> list[str]:
    errors: list[str] = []
    for entity in graph.values():
        rels = entity.metadata.get("relationships") or []
        for rel in rels:
            target_id = _relationship_target(rel)
            if target_id is None:
                errors.append(
                    f"{entity.id}: relationship has no recognizable target: {rel!r}"
                )
                continue
            if target_id not in graph:
                errors.append(
                    f"{entity.id}: broken relationship -> {target_id}"
                )
    return errors


def _relationship_target(rel: dict[str, str]) -> str | None:
    """Return the target entity id for a relationship mapping."""
    for key, value in rel.items():
        if key == "framing":
            continue
        if key in RELATIONSHIP_FRAMINGS or key.replace("_", "").isalpha():
            return value
    return None


def _relationship_type(rel: dict[str, str]) -> str | None:
    for key in rel.keys():
        if key != "framing":
            return key
    return None


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def url_for_entity(entity: Entity) -> str:
    return f"/regions/{entity.region}/{entity.id}.html"


def url_for_region(region_id: str) -> str:
    return f"/regions/{region_id}/index.html"


def render_adjacency(entity: Entity, graph: dict[str, Entity]) -> str:
    rels = entity.metadata.get("relationships") or []
    if not rels:
        return ""

    items: list[str] = []
    for rel in rels:
        rel_type = _relationship_type(rel)
        target_id = _relationship_target(rel)
        if rel_type is None or target_id is None:
            continue
        target = graph.get(target_id)
        if target is None:
            continue

        framing_override = rel.get("framing")
        if framing_override and framing_override in FRAMING_OVERRIDES:
            framing = FRAMING_OVERRIDES[framing_override]
        else:
            framing = RELATIONSHIP_FRAMINGS.get(rel_type, "Related:")

        items.append(
            f'<li><span class="framing">{html.escape(framing, quote=False)}</span> '
            f'<a href="{url_for_entity(target)}">'
            f'{html.escape(target.title, quote=False)}</a></li>'
        )

    if not items:
        return ""

    return (
        '<section class="adjacency">'
        '<h2>Connected within ATLAS</h2>'
        f'<ul>{"".join(items)}</ul>'
        '</section>'
    )


def load_template(name: str) -> string.Template:
    path = TEMPLATES / name
    return string.Template(path.read_text(encoding="utf-8"))


def render_entity_page(entity: Entity, graph: dict[str, Entity]) -> str:
    template = load_template("entity.html")
    base = load_template("base.html")

    body_html = render_markdown(entity.body)
    adjacency_html = render_adjacency(entity, graph)

    transliteration = entity.metadata.get("transliteration", "")
    gloss = entity.metadata.get("gloss", "")
    type_label = entity.type.replace("_", " ")

    # quote=False everywhere in body-context HTML; entity values
    # never end up in attribute contexts where quote escaping matters.
    subtitle_parts: list[str] = []
    if transliteration and transliteration != entity.title:
        subtitle_parts.append(html.escape(transliteration, quote=False))
    if gloss:
        subtitle_parts.append(
            f'<span class="gloss">{html.escape(gloss, quote=False)}</span>'
        )
    subtitle = " &middot; ".join(subtitle_parts)
    subtitle_html = f'<p class="subtitle">{subtitle}</p>' if subtitle else ""

    inner = template.substitute(
        title=html.escape(entity.title, quote=False),
        subtitle=subtitle_html,
        type_label=html.escape(type_label, quote=False),
        region=html.escape(entity.region, quote=False),
        body=body_html,
        adjacency=adjacency_html,
    )

    return base.substitute(
        page_title=f"{entity.title} — ATLAS",
        content=inner,
        body_class="page-entity",
        site_root="/",
    )


def render_region_page(region: Region) -> str:
    template = load_template("region.html")
    base = load_template("base.html")

    body_html = render_markdown(region.body)

    # Group entities by type for editorial display.
    by_type: dict[str, list[Entity]] = {}
    for entity in region.entities:
        by_type.setdefault(entity.type, []).append(entity)

    # Editorial ordering: concepts first, then terms, then practices, etc.
    type_order = [
        "concept",
        "language_term",
        "ritual_practice",
        "state",
        "phenomenology",
        "body",
        "text",
        "passage",
        "person",
        "place",
        "tradition",
        "art_material",
    ]

    # Render in editorial order, then anything not in the order list at end.
    # An unknown type appearing here usually indicates that type_order is
    # behind the entity vocabulary; the entity is rendered (not silently
    # dropped) so the omission is visible to stewardship review.
    seen: set[str] = set()
    ordered_types: list[str] = []
    for t in type_order:
        if t in by_type:
            ordered_types.append(t)
            seen.add(t)
    for t in sorted(by_type.keys()):
        if t not in seen:
            ordered_types.append(t)

    sections: list[str] = []
    for t in ordered_types:
        entities = by_type[t]
        # Sort entities by id within type (stable, predictable).
        entities.sort(key=lambda e: e.id)
        label = t.replace("_", " ").capitalize()
        items = "".join(
            f'<li><a href="{url_for_entity(e)}">{html.escape(e.title, quote=False)}</a></li>'
            for e in entities
        )
        sections.append(
            f'<section class="entity-group">'
            f'<h2>{html.escape(label, quote=False)}</h2>'
            f'<ul>{items}</ul>'
            f'</section>'
        )

    inner = template.substitute(
        title=html.escape(region.title, quote=False),
        body=body_html,
        sections="\n".join(sections),
    )

    return base.substitute(
        page_title=f"{region.title} — ATLAS",
        content=inner,
        body_class="page-region",
        site_root="/",
    )


def render_homepage(regions: list[Region]) -> str:
    template = load_template("homepage.html")
    base = load_template("base.html")

    region_items = []
    for region in sorted(regions, key=lambda r: int(r.metadata.get("order", 99))):
        # Use the first paragraph of the region's body as a brief preview.
        first_para = region.body.strip().split("\n\n", 1)[0]
        first_para = " ".join(line.strip() for line in first_para.splitlines())
        region_items.append(
            '<article class="region-summary">'
            f'<h2><a href="{url_for_region(region.id)}">'
            f'{html.escape(region.title, quote=False)}</a></h2>'
            f'<p>{render_inline(first_para)}</p>'
            '</article>'
        )

    inner = template.substitute(regions="\n".join(region_items))

    return base.substitute(
        page_title="ATLAS",
        content=inner,
        body_class="page-home",
        site_root="/",
    )


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_page(path: Path, html_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")


def copy_static() -> None:
    target = PUBLIC / "static"
    if target.exists():
        shutil.rmtree(target)
    if STATIC.exists():
        shutil.copytree(STATIC, target)


# ---------------------------------------------------------------------------
# Build pipeline
# ---------------------------------------------------------------------------

def build() -> None:
    # Discovery and parsing.
    entity_paths = discover_entities()
    region_paths = discover_regions()

    entities = [parse_entity_file(p) for p in entity_paths]
    regions = [parse_region_file(p) for p in region_paths]

    # Validation.
    errors: list[str] = []
    for entity in entities:
        errors.extend(validate_entity(entity))
    if errors:
        for err in errors:
            print(f"VALIDATION ERROR: {err}", file=sys.stderr)
        raise BuildError(f"{len(errors)} validation error(s)")

    # Build graph and validate relationships.
    graph: dict[str, Entity] = {}
    for entity in entities:
        if entity.id in graph:
            raise BuildError(f"Duplicate entity id: {entity.id}")
        graph[entity.id] = entity

    rel_errors = validate_relationships(graph)
    if rel_errors:
        for err in rel_errors:
            print(f"RELATIONSHIP ERROR: {err}", file=sys.stderr)
        raise BuildError(f"{len(rel_errors)} relationship error(s)")

    # Attach entities to their regions.
    region_by_id = {r.id: r for r in regions}
    for entity in entities:
        region = region_by_id.get(entity.region)
        if region is None:
            raise BuildError(
                f"Entity {entity.id} references region '{entity.region}' "
                "which has no _region.md"
            )
        region.entities.append(entity)

    # Prepare output directory.
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    # Render entities.
    for entity in entities:
        out_path = PUBLIC / "regions" / entity.region / f"{entity.id}.html"
        write_page(out_path, render_entity_page(entity, graph))

    # Render regions.
    for region in regions:
        out_path = PUBLIC / "regions" / region.id / "index.html"
        write_page(out_path, render_region_page(region))

    # Render homepage.
    write_page(PUBLIC / "index.html", render_homepage(regions))

    # Static assets.
    copy_static()

    # Final validation: look for broken internal links in the rendered output.
    broken = check_internal_links(PUBLIC)
    if broken:
        for source, link in broken:
            print(f"BROKEN LINK in {source}: {link}", file=sys.stderr)
        raise BuildError(f"{len(broken)} broken internal link(s)")

    # Build report.
    print(f"Built {len(entities)} entities across {len(regions)} regions.")
    rel_count = sum(
        len(e.metadata.get("relationships") or []) for e in entities
    )
    print(f"Total authored relationships: {rel_count}")
    print(f"Output: {PUBLIC}")


# ---------------------------------------------------------------------------
# Internal link checker
# ---------------------------------------------------------------------------

LINK_RE = re.compile(r'href="([^"]+)"')


def check_internal_links(public: Path) -> list[tuple[Path, str]]:
    broken: list[tuple[Path, str]] = []
    for html_file in public.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        for link in LINK_RE.findall(text):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Resolve relative to public root.
            target_path = link.lstrip("/")
            if not (public / target_path).exists():
                broken.append((html_file.relative_to(public), link))
    return broken


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        build()
    except BuildError as e:
        print(f"\nBUILD FAILED: {e}", file=sys.stderr)
        sys.exit(1)
