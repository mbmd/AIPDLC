# -*- coding: utf-8 -*-
"""
AIFLC HTML Export - engine
==========================
Publishes an AIFLC family workspace ({family}-ws) of Markdown artifacts as a
self-contained, browsable HTML site with a grouped landing page.

FIRST PRINCIPLE - Markdown is the source of truth; HTML is a shadow.
  - The .md files under the workspace are the SINGLE source of truth.
  - This tool ONLY writes HTML, under {workspace-root}/.publish/ - it NEVER
    writes, moves, or deletes a .md file.
  - Nothing reads the HTML back as data; it is a read-only view for people.
  - The output is disposable and fully rebuildable from the Markdown.

FAMILY-AGNOSTIC
  One copy serves every AIFLC family. Reading order + grouping are DETERMINISTIC
  and come from (1) the per-family config's taxonomy, then (2) a generic built-in
  stage table, then (3) creation-time only as a within-group tiebreaker - never
  creation-time as the primary sort (that is not reproducible across machines).

OUTPUT
  {workspace-root}/.publish/{family}-html/   <- the site (the shadow; disposable)
  {workspace-root}/.publish/{family}.config.yaml  <- settings (stable; a sibling)

DEPENDENCIES
  Python 3.8+ ; `markdown` (required: pip install markdown) ;
  `PyYAML` (optional: nicer config + document-metadata cards).
  Diagrams render from a CDN on first view unless the offline build is used.

USAGE
  python publish.py [WORKSPACE]  [--family CODE] [--out-root DIR]
                                 [--config FILE] [--force]
  python publish.py on   [WORKSPACE] [--family CODE] [--out-root DIR]
  python publish.py off  [WORKSPACE] [--family CODE] [--out-root DIR]
  python publish.py status [WORKSPACE] [--family CODE] [--out-root DIR]

  WORKSPACE  the {family}-ws directory (defaults to a sibling *-ws of this file).
  --force    publish even when the config switch is off (for testing).

  Sub-commands (Phase 2 — the switch):
    on       Enable auto-refresh + run one full publish immediately.
    off      Disable auto-refresh (shadow stays as a frozen snapshot).
    status   Report switch state, last publish time, and page count.
"""
import os
import re
import sys
import html
import shutil
import fnmatch
import argparse
import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import markdown
except ImportError:
    print("ERROR: the 'markdown' package is required. Install with: pip install markdown")
    sys.exit(1)

try:
    import yaml  # optional
    _HAVE_YAML = True
except Exception:
    _HAVE_YAML = False


# --- configuration ---------------------------------------------------------

DEFAULT_CONFIG = {
    "enabled": True,
    "autoRefresh": True,
    "landing": {"title": None, "subtitle": "", "hideFromLanding": ["data"]},
    # scope.exclude globs are matched against the basename, the workspace-relative
    # posix path, AND each directory segment (so a bare folder name like "flo"
    # excludes that folder at any depth). Dot-folders/files are always excluded.
    "scope": {"exclude": ["*-state.md", "*_state.md", "flo-*.md", "flo", "flow", "tools"]},
    "taxonomy": {"source": "FAMILY_STRUCTURE", "order": [], "groups": {}},
    "mermaid": {"offline": False},
    "deck": {"enabled": False},
    "readerHeader": {"fields": ["stage", "status", "snapshotId", "generatedOn"]},
    "git": {"commitShadow": False},
}

# Per-family built-in stage tables. Used ONLY as a fallback when the per-family
# config does not specify a group. Config (taxonomy.order / taxonomy.groups) is
# authoritative; these tables just give sensible out-of-the-box ordering/labels
# so the tool works without any config on first run.
# folder -> (order, label, accent-colour, description)

_COMMON_GROUPS = {
    "":                     (1,  "Overview",              "#0b3d66", "Top-level workspace documents."),
    "data":                 (5,  "Data Foundation",       "#64748b", "Shared data fabric the downstream stages snapshot against."),
    "requirements":         (12, "Requirements",          "#d97706", "Architecture/technology requirements register — inputs and constraints for downstream design."),
    "entities":             (60, "Entities",              "#0969da", "Per-entity artifacts (group / multi-entity runs)."),
    "group":                (62, "Group",                 "#0969da", "Consolidated group-level artifacts."),
    "governance":           (80, "Governance",            "#475569", "Governance model, decisions, and controls."),
    "management_framework": (90, "Management Framework",  "#475569", "Governance spine: decision / issue / action / change registers and lessons."),
    "sources":              (95, "Sources and References", "#64748b", "The citation registry."),
}

FAMILY_GROUP_META = {
    # --- PDLC (Product Development Life Cycle) ---
    "pdlc": {
        **_COMMON_GROUPS,
        "projects":         (3,  "Projects",              "#0b3d66", "Per-project artifacts and registry."),
    },

    # --- SFLC (Strategy Formulation Life Cycle) ---
    # AI-SES produces ~8 docs in environment/, AI-SDA ~5 in diagnosis/, AI-SVM ~4 in vision/,
    # AI-SCP ~6 in choices/, AI-SAG ~5 in articulation/, governance spine ~7 in management_framework/.
    "sflc": {
        **_COMMON_GROUPS,
        "environment":      (10, "1 - Environmental Scan",    "#0e9f6e",
                             "External environment: scan scope, PESTEL, Porter Five Forces, competitor profiles, trend radar, and the synthesis."),
        "diagnosis":        (20, "2 - Strategic Diagnosis",   "#d97706",
                             "Internal assessment: data collection, SWOT/TOWS, VRIO, core-competency gaps, and the diagnostic baseline."),
        "vision":           (30, "3 - Vision and Direction",  "#7c3aed",
                             "Purpose framing, strategic themes, measurable objectives, and coherence validation."),
        "choices":          (40, "4 - Strategic Choices",     "#0969da",
                             "Where-to-play / how-to-win, growth options, scenario stress-testing, resource allocation, and the locked choice set."),
        "articulation":     (50, "5 - Strategy Articulation", "#e11d48",
                             "Communicable outputs: strategy statement, strategy map, guardrails, coherence check, governance model, and chain contracts."),
    },

    # --- SXLC (Strategy Execution Life Cycle) ---
    # AI-SXI produces docs in intake/, AI-OKR in okr/, AI-BSC in scorecard/,
    # AI-SIP in initiatives/, AI-SPR in performance/.
    "sxlc": {
        **_COMMON_GROUPS,
        "intake":           (10, "1 - Strategy Execution Intake", "#0e9f6e",
                             "Intake and handoff from strategy formulation: strategy contract validation, execution context, scope boundaries, and readiness assessment."),
        "okr":              (20, "2 - OKR and Goal Cascade",      "#d97706",
                             "OKR/goal cascade: objective hierarchy, key results, alignment mapping, scoring model, and organizational cascade."),
        "scorecard":        (30, "3 - Balanced Scorecard",        "#7c3aed",
                             "Balanced scorecard: four perspectives, strategy map, KPI definitions, targets, and measurement framework."),
        "initiatives":      (40, "4 - Strategic Initiatives",     "#0969da",
                             "Initiative portfolio: initiative register, prioritization matrix, resource allocation, interdependencies, and phasing."),
        "performance":      (50, "5 - Performance Review",        "#e11d48",
                             "Performance governance: review cadence, variance analysis, corrective actions, re-formulation triggers, and cycle governance."),
    },

    # --- BALC (Business Architecture Life Cycle) ---
    # AI-BAV produces docs in vision/ + requirements/, AI-BCM in capabilities/,
    # AI-VSM in value-streams/, AI-OMD in operating-model/, AI-BAG in governance/.
    "balc": {
        **_COMMON_GROUPS,
        "vision":           (10, "1 - Vision and Grounding",      "#0e9f6e",
                             "Strategy grounding, EA mandate, stakeholder mapping, architecture vision, and the vision baseline."),
        "requirements":     (15, "Requirements",                  "#64748b",
                             "Architecture requirements register (seeded by motivation, verified at target)."),
        "capabilities":     (20, "2 - Business Capabilities",     "#d97706",
                             "The capability model, heatmap, maturity assessment, and capability-to-value-stream mapping."),
        "value-streams":    (30, "3 - Value Streams",             "#7c3aed",
                             "Value stream maps, stages, enabling capabilities, and cross-stream dependencies."),
        "operating-model":  (40, "4 - Operating Model",           "#0969da",
                             "The operating-model design: organizational structure, process architecture, and technology alignment."),
        "governance":       (50, "5 - Governance and Target",     "#e11d48",
                             "Target business architecture, gap analysis, governance model, and chain contracts."),
    },

    # --- DALC (Data Architecture Life Cycle) ---
    # AI-DAD in discovery/, AI-DGV in governance/, AI-DMO in models/,
    # AI-DPL in platform/, AI-MDM in mdm/, AI-DPS in privacy-security/, AI-DRA in reference-architecture/.
    "dalc": {
        **_COMMON_GROUPS,
        "discovery":              (10, "1 - Data Discovery and Strategy", "#0e9f6e",
                                   "Data landscape discovery, current-state inventory, strategy definition, and data principles."),
        "governance":             (20, "2 - Data Governance",             "#d97706",
                                   "Data governance framework, policies, stewardship model, quality rules, and lineage."),
        "models":                 (30, "3 - Data Modeling",               "#7c3aed",
                                   "Logical/physical models, feature stores, vector schemas, ontologies, and schema evolution."),
        "platform":               (40, "4 - Pipelines and Platform",     "#0969da",
                                   "Data pipelines, platform design, orchestration, ingestion patterns, and observability."),
        "mdm":                    (45, "5 - Master Data Management",     "#0969da",
                                   "MDM strategy, golden records, matching/merging rules, and cross-domain master data."),
        "privacy-security":       (48, "6 - Privacy and Security",       "#475569",
                                   "Data classification, PII/PHI controls, encryption, access policies, and compliance mapping."),
        "reference-architecture": (50, "7 - Data Reference Architecture","#e11d48",
                                   "Target data architecture, reference patterns, and the Data-to-Application handoff contract."),
    },

    # --- AALC (Application Architecture Life Cycle) ---
    # AI-AAD in discovery/, AI-APM in portfolio/, AI-INT in integration/,
    # AI-AMD in design/, AI-AOA in orchestration/, AI-AAG in governance/.
    "aalc": {
        **_COMMON_GROUPS,
        "discovery":        (10, "1 - Application Discovery",      "#0e9f6e",
                             "Application landscape discovery, intake from data architecture, and current-state catalog."),
        "portfolio":        (20, "2 - Application Portfolio",      "#d97706",
                             "TIME analysis, rationalization decisions, portfolio heatmap, and lifecycle state mapping."),
        "integration":      (30, "3 - Integration Architecture",   "#7c3aed",
                             "EDA patterns, API-led connectivity, AI service APIs, event catalog, and integration contracts."),
        "design":           (40, "4 - Application Design",         "#0969da",
                             "Microservices/monolith decisions, modernization roadmap, bounded contexts, and ADRs."),
        "orchestration":    (45, "5 - AI Orchestration",           "#0969da",
                             "Agentic patterns, AI orchestration architecture, model routing, and guardrails."),
        "governance":       (50, "6 - Application Governance",     "#e11d48",
                             "Target application architecture, governance handoff, and the Application-to-Technology contract."),
    },

    # --- TALC (Technology Architecture Life Cycle) ---
    # AI-TAD in discovery/, AI-CIS in cloud/, AI-RES in resilience/, AI-SEC in security/,
    # AI-PEM in platform/, AI-TGF in tech-governance/, AI-ERM in roadmap/.
    "talc": {
        **_COMMON_GROUPS,
        "discovery":        (10, "1 - Technology Discovery",        "#0e9f6e",
                             "Technology landscape discovery, intake from application architecture, and current-state inventory."),
        "cloud":            (20, "2 - Cloud and Infrastructure",    "#d97706",
                             "Cloud strategy, landing zones, infrastructure patterns, multi-cloud decisions, and cost models."),
        "resilience":       (30, "3 - Resilience and Networking",   "#7c3aed",
                             "Resilience patterns, DR/BCP, networking topology, edge compute, and observability."),
        "security":         (40, "4 - Security Architecture",      "#0969da",
                             "Security architecture, zero-trust model, identity/access, encryption, and threat modeling."),
        "platform":         (45, "5 - Platform Engineering",       "#0969da",
                             "Platform engineering, MLOps, developer experience, IDP design, and self-service capabilities."),
        "tech-governance":  (50, "6 - Technology Governance",       "#e11d48",
                             "FinOps, technology debt governance, standards enforcement, and architecture-board criteria."),
        "roadmap":          (55, "7 - Enterprise Roadmap",          "#e11d48",
                             "Enterprise roadmap, migration sequencing, transition architecture, and the cross-family capstone."),
    },
}


def _get_builtin_for_family(family):
    """Return the per-family built-in group meta, falling back to common-only."""
    key = (family or "").lower().strip()
    return FAMILY_GROUP_META.get(key, _COMMON_GROUPS)

STATE_RE = re.compile(r"[-_]state\.md$", re.IGNORECASE)
EXTERNAL_RE = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.\-]*:|//)")


def _deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(config_path):
    """Merge a per-family config file over DEFAULT_CONFIG. Missing/!yaml -> defaults."""
    if not config_path or not os.path.isfile(config_path):
        return dict(DEFAULT_CONFIG), False
    if not _HAVE_YAML:
        print("  note: PyYAML not installed - config file ignored, using defaults "
              "(pip install pyyaml to honour %s)" % os.path.basename(config_path))
        return dict(DEFAULT_CONFIG), False
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            return dict(DEFAULT_CONFIG), False
        return _deep_merge(DEFAULT_CONFIG, data), True
    except Exception as e:
        print("  note: could not parse %s (%r) - using defaults" % (config_path, e))
        return dict(DEFAULT_CONFIG), False


# --- collection & ordering -------------------------------------------------

def group_of(rel_path):
    """Top-level subfolder of a workspace-relative path, or '' for root files."""
    parts = rel_path.replace(os.sep, "/").split("/")
    return parts[0] if len(parts) > 1 else ""


def group_meta(group, config, family=None):
    """Resolve (order, label, colour, description) for a group. Config wins."""
    cfg_groups = (config.get("taxonomy") or {}).get("groups") or {}
    order_list = (config.get("taxonomy") or {}).get("order") or []
    builtin_table = _get_builtin_for_family(family)
    builtin = builtin_table.get(group)
    # order: explicit config order list > config group.order > builtin > alpha tail
    if group in order_list:
        order = order_list.index(group)
    elif group in cfg_groups and "order" in cfg_groups[group]:
        order = cfg_groups[group]["order"]
    elif builtin:
        order = builtin[0]
    else:
        order = 1000
    label = None
    colour = None
    desc = None
    if group in cfg_groups:
        label = cfg_groups[group].get("label")
        colour = cfg_groups[group].get("colour") or cfg_groups[group].get("color")
        desc = cfg_groups[group].get("description")
    if builtin:
        label = label or builtin[1]
        colour = colour or builtin[2]
        desc = desc if desc is not None else builtin[3]
    label = label or (group.replace("-", " ").replace("_", " ").title() if group else "Overview")
    colour = colour or "#0969da"
    desc = desc or ""
    return order, label, colour, desc


def is_excluded(rel_path, exclude_globs):
    parts = rel_path.replace(os.sep, "/").split("/")
    # any dot-folder / dot-file segment
    for p in parts:
        if p.startswith("."):
            return True
    rel_posix = rel_path.replace(os.sep, "/")
    base = parts[-1]
    dir_segments = parts[:-1]
    for g in exclude_globs:
        if fnmatch.fnmatch(base, g) or fnmatch.fnmatch(rel_posix, g):
            return True
        # folder-style excludes: match a glob against any directory segment
        for seg in dir_segments:
            if fnmatch.fnmatch(seg, g):
                return True
    return False


def collect_files(src, export_abs, config, family=None):
    """Return .md files (abs paths) in deterministic reading order."""
    exclude_globs = (config.get("scope") or {}).get("exclude") or []
    found = []
    for dirpath, dirnames, filenames in os.walk(src):
        # prune dot-dirs and anything inside the export tree (defensive)
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if os.path.abspath(dirpath).startswith(export_abs):
            continue
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            ap = os.path.join(dirpath, fn)
            rel = os.path.relpath(ap, src)
            if is_excluded(rel, exclude_globs):
                continue
            found.append(ap)

    def sort_key(p):
        rel = os.path.relpath(p, src)
        grp = group_of(rel)
        order, _, _, _ = group_meta(grp, config, family)
        # (group order, creation-time tiebreaker within group, name)
        try:
            ct = os.path.getctime(p)
        except Exception:
            ct = 0
        return (order, ct, rel.lower())

    found.sort(key=sort_key)
    return found


# --- front matter ----------------------------------------------------------

def split_front_matter(text):
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.DOTALL)
    return (m.group(1), text[m.end():]) if m else (None, text)


def parse_fm(fm_text):
    if not fm_text or not fm_text.strip() or not _HAVE_YAML:
        return None
    try:
        d = yaml.safe_load(fm_text)
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def render_front_matter(fm_text, data):
    if not fm_text or not fm_text.strip():
        return ""

    def esc(v):
        return html.escape(str(v))

    if isinstance(data, dict):
        rows = []
        for k, v in data.items():
            if isinstance(v, list):
                val = "<ul class='fm-list'>%s</ul>" % "".join("<li>%s</li>" % esc(i) for i in v)
            elif isinstance(v, dict):
                val = "<ul class='fm-list'>%s</ul>" % "".join(
                    "<li><span class='fm-subkey'>%s</span>: %s</li>" % (esc(kk), esc(vv)) for kk, vv in v.items())
            else:
                val = esc(v)
            rows.append("<tr><th scope='row'>%s</th><td>%s</td></tr>" % (esc(k), val))
        inner = "<table class='fm-table'><tbody>%s</tbody></table>" % "".join(rows)
    else:
        inner = "<pre class='fm-raw'>%s</pre>" % esc(fm_text.strip())
    return "<details class='frontmatter'><summary>Document metadata</summary>%s</details>" % inner


def fm_field(data, name):
    if isinstance(data, dict) and data.get(name) not in (None, ""):
        return str(data.get(name))
    return ""


# --- mermaid ---------------------------------------------------------------

MERMAID_RE = re.compile(r"```mermaid[ \t]*\r?\n(.*?)\r?\n```", re.DOTALL)


def extract_mermaid(body):
    blocks = []

    def repl(m):
        blocks.append(m.group(1))
        return "\n\nxmermaidblockx%dx\n\n" % (len(blocks) - 1)

    return MERMAID_RE.sub(repl, body), blocks


def reinsert_mermaid(html_text, blocks):
    for idx, raw in enumerate(blocks):
        token = "xmermaidblockx%dx" % idx
        fig = ('<figure class="mermaid-fig"><div class="mm-toolbar">'
               '<button type="button" class="mm-btn mm-full" title="Open this diagram full screen">'
               '&#x26F6; Full screen</button></div><pre class="mermaid">%s</pre></figure>') % html.escape(raw)
        html_text = html_text.replace("<p>%s</p>" % token, fig).replace(token, fig)
    return html_text


# --- links -----------------------------------------------------------------

HREF_RE = re.compile(r'href="([^"]*)"')
URL_TEXT_RE = re.compile(r'https?://[^\s<>"]+')
SKIP_TAGS = {"a", "code", "pre"}


def _resolve_cross_ws_html(target_md_abs, current_src_root, current_export_dir):
    """Resolve a cross-workspace .md link to its published HTML equivalent.
    
    Given a target like /workspace/balc-ws/capabilities/capability-decomposition.md,
    find the matching HTML file in /workspace/.publish/balc-html/capabilities/NN_capability-decomposition.html.
    Returns a relative href from current_export_dir, or None if not found.
    """
    # Find the workspace root (parent of *-ws folders)
    ws_root = os.path.dirname(current_src_root)
    # Determine which {family}-ws the target belongs to
    target_norm = target_md_abs.replace(os.sep, "/")
    ws_root_norm = ws_root.replace(os.sep, "/")
    if not target_norm.startswith(ws_root_norm):
        return None
    rel_to_root = target_norm[len(ws_root_norm):].lstrip("/")
    parts = rel_to_root.split("/")
    if len(parts) < 2 or not parts[0].endswith("-ws"):
        return None
    target_family = parts[0][:-3]  # e.g., "balc-ws" -> "balc"
    target_rel_md = "/".join(parts[1:])  # e.g., "capabilities/capability-decomposition.md"
    # Look for the HTML equivalent in .publish/{family}-html/
    publish_dir = os.path.join(ws_root, ".publish", "%s-html" % target_family)
    if not os.path.isdir(publish_dir):
        return None
    # The HTML file is named NN_{basename}.html in the same subfolder structure
    target_dir = os.path.dirname(target_rel_md)
    target_base = os.path.splitext(os.path.basename(target_rel_md))[0]
    search_dir = os.path.join(publish_dir, target_dir) if target_dir else publish_dir
    if not os.path.isdir(search_dir):
        return None
    # Find the file matching *_{target_base}.html
    for fn in os.listdir(search_dir):
        if fn.lower().endswith("_%s.html" % target_base.lower()):
            html_abs = os.path.join(search_dir, fn)
            return os.path.relpath(html_abs, current_export_dir).replace(os.sep, "/")
    return None


def make_link_rewriter(src_abs, src_root, seq_map):
    src_dir = os.path.dirname(src_abs)
    this_export_dir = os.path.dirname(seq_map[src_abs])

    def href_to(target_abs):
        return os.path.relpath(target_abs, this_export_dir).replace(os.sep, "/")

    def rewrite(m):
        href = m.group(1)
        if not href or href.startswith("#"):
            return m.group(0)
        if EXTERNAL_RE.match(href):
            return 'href="%s" target="_blank" rel="noopener noreferrer"' % href
        if "#" in href:
            path_part, frag = href.split("#", 1)
            anchor = "#" + frag
        else:
            path_part, anchor = href, ""
        if path_part == "":
            return m.group(0)
        target_abs = os.path.normpath(os.path.join(src_dir, path_part))
        if target_abs in seq_map:
            return 'href="%s"' % (href_to(seq_map[target_abs]) + anchor)
        if os.path.exists(target_abs):
            # Cross-workspace .md link: resolve to sibling HTML publish folder
            if target_abs.lower().endswith(".md"):
                resolved_html = _resolve_cross_ws_html(target_abs, src_root, this_export_dir)
                if resolved_html:
                    return 'href="%s"' % (resolved_html + anchor)
            # fallback: point back to the source file
            return 'href="%s"' % (os.path.relpath(target_abs, this_export_dir).replace(os.sep, "/") + anchor)
        return m.group(0)

    return rewrite


def _wrap_url(m):
    url = m.group(0)
    trail = ""
    while url and url[-1] in ".,;:!?":
        trail = url[-1] + trail
        url = url[:-1]
    if url.endswith(")") and url.count("(") < url.count(")"):
        trail = ")" + trail
        url = url[:-1]
    if not url:
        return m.group(0)
    return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s' % (url, url, trail)


def linkify_bare_urls(html_text):
    parts = re.split(r"(<[^>]+>)", html_text)
    skip = 0
    out = []
    for part in parts:
        if part[:1] == "<" and part[-1:] == ">":
            mt = re.match(r"</?\s*([a-zA-Z][a-zA-Z0-9]*)", part)
            tag = mt.group(1).lower() if mt else ""
            if tag in SKIP_TAGS:
                if part[:2] == "</":
                    skip = max(0, skip - 1)
                elif part[-2:] != "/>":
                    skip += 1
            out.append(part)
        else:
            out.append(URL_TEXT_RE.sub(_wrap_url, part) if (skip == 0 and "http" in part) else part)
    return "".join(out)


# --- toc -------------------------------------------------------------------

def render_toc(tokens):
    def walk(items):
        return "".join("<li><a href='#%s'>%s</a>%s</li>"
                       % (it["id"], html.escape(it["name"]), kids(it.get("children", [])))
                       for it in items if it["level"] <= 3)

    def kids(items):
        inner = walk(items)
        return "<ul>%s</ul>" % inner if inner else ""

    top = list(tokens)
    if len(top) == 1 and top[0]["level"] == 1:
        top = top[0].get("children", [])
    body = walk(top)
    return ("<nav class='toc' id='toc-panel'><ul>%s</ul></nav><button class='toc-toggle' id='toc-btn' title='Toggle Contents'>&#9776;</button>" % body) if body else ""


# --- assets (CSS/JS/templates) ---------------------------------------------

CSS = """
:root{--fg:#1a1f36;--muted:#4a5568;--border:#e2e8f0;--bg:#ffffff;--soft:#f7fafc;--accent:#2b6cb0;--accent-light:#ebf4ff;--th:#edf2f7;--zebra:#f7fafc;--gradient-start:#1a365d;--gradient-end:#2b6cb0;--shadow:0 4px 6px -1px rgba(0,0,0,.07),0 2px 4px -1px rgba(0,0,0,.04);--shadow-lg:0 10px 15px -3px rgba(0,0,0,.08),0 4px 6px -2px rgba(0,0,0,.04);}
*{box-sizing:border-box;}
body{margin:0;color:var(--fg);background:linear-gradient(135deg,#f0f4f8 0%,#e2e8f0 100%);font-family:'Source Sans Pro','Noto Sans',-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.7;font-size:16px;min-height:100vh;}
.page{max-width:1020px;margin:32px auto;background:var(--bg);border:0;border-radius:16px;box-shadow:var(--shadow-lg);position:relative;}
.topbar{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;padding:16px 32px;background:linear-gradient(135deg,var(--gradient-start),var(--gradient-end));color:#fff;border-radius:16px 16px 0 0;box-shadow:0 4px 12px rgba(26,54,93,.2);}
.topbar .home{color:#fff;text-decoration:none;font-size:18px;opacity:.85;transition:opacity .2s;}.topbar .home:hover{opacity:1;}
.topbar .seq{font-weight:700;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:3px 12px;border-radius:20px;font-size:12px;letter-spacing:.8px;backdrop-filter:blur(4px);}
.topbar .crumb{font-size:13px;opacity:.9;}.topbar .crumb b{opacity:1;}.topbar .grow{flex:1;}
.content{padding:12px 40px 40px;}
h1,h2,h3,h4{line-height:1.3;margin-top:1.6em;font-weight:700;scroll-margin-top:80px;letter-spacing:-.02em;}
h1{font-size:2em;margin-top:.7em;padding-bottom:.4em;border-bottom:3px solid var(--accent-light);color:var(--gradient-start);}
h2{font-size:1.5em;padding-bottom:.3em;border-bottom:2px solid var(--border);color:#2d3748;}
h3{font-size:1.2em;color:#2d3748;}h4{font-size:1.05em;color:#4a5568;}
a{color:var(--accent);text-decoration:none;transition:color .15s;}a:hover{color:#1a4971;text-decoration:underline;}
p,li{overflow-wrap:break-word;}
blockquote{margin:1.2em 0;padding:.6em 1.2em;color:var(--muted);border-left:4px solid var(--accent);background:var(--accent-light);border-radius:0 8px 8px 0;}
blockquote p{margin:.4em 0;}
blockquote table{font-size:.75em;}
details.legend{margin:1em 0;border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;background:var(--accent-light);}
details.legend>summary{cursor:pointer;padding:8px 14px;font-weight:600;font-size:.8em;color:var(--accent);list-style:none;}
details.legend>summary::before{content:'▶ ';font-size:.75em;}
details.legend[open]>summary::before{content:'▼ ';}
details.legend>.legend-body{padding:4px 14px 10px;font-size:.78em;color:var(--muted);}
details.legend>.legend-body table{font-size:.85em;margin:0;}
details.legend>.legend-body th,details.legend>.legend-body td{padding:3px 8px;line-height:1.3;}
details.legend>.legend-body th{background:var(--soft);color:var(--muted);font-weight:600;border-color:var(--border);}
details.legend>.legend-body td{background:#fff;border-color:var(--border);}
code{font-family:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--soft);padding:.2em .5em;border-radius:6px;font-size:.86em;border:1px solid var(--border);}
pre{background:#1a1f36;color:#e2e8f0;border:0;border-radius:10px;padding:18px 20px;overflow:auto;font-size:.84em;box-shadow:inset 0 2px 4px rgba(0,0,0,.2);}
pre code{background:none;padding:0;border:0;color:inherit;}
.table-wrap{overflow-x:auto;margin:1.2em 0;border-radius:10px;box-shadow:var(--shadow);}
table{border-collapse:collapse;width:100%;font-size:.9em;}
th,td{border:1px solid var(--border);padding:10px 14px;text-align:left;vertical-align:top;}
th{background:var(--gradient-start);color:#fff;font-weight:600;border-color:rgba(255,255,255,.1);}
tbody tr:nth-child(even){background:var(--zebra);}tbody tr:hover{background:var(--accent-light);}
hr{border:0;border-top:2px solid var(--border);margin:2.5em 0;}
ul,ol{padding-left:1.6em;}img{max-width:100%;border-radius:8px;}
.frontmatter{margin:16px 0 8px;border:1px solid var(--border);border-radius:10px;background:var(--soft);transition:box-shadow .2s;}
.frontmatter:hover{box-shadow:var(--shadow);}
.frontmatter>summary{cursor:pointer;padding:10px 16px;font-weight:600;color:var(--muted);font-size:.82em;text-transform:uppercase;letter-spacing:.8px;}
.fm-table{margin:0;font-size:.86em;}
.fm-table th{width:210px;background:#fff;color:var(--muted);font-weight:600;white-space:nowrap;vertical-align:top;border-color:var(--border);}
.fm-table td{background:#fff;border-color:var(--border);}.fm-list{margin:0;padding-left:1.1em;}.fm-subkey{font-weight:600;color:var(--muted);}
.fm-raw{margin:0;border:0;background:#fff;}
.toc{position:fixed;top:72px;right:0;width:240px;height:calc(100vh - 72px);background:#fff;border-left:1px solid var(--border);box-shadow:-2px 0 8px rgba(0,0,0,.06);overflow-y:auto;padding:14px 0;transform:translateX(100%);transition:transform .25s ease;z-index:20;font-size:.82em;}
.toc.open{transform:translateX(0);}
.toc-toggle{position:fixed;top:80px;right:8px;z-index:21;background:var(--accent);color:#fff;border:0;border-radius:8px 0 0 8px;padding:8px 10px;font-size:13px;font-weight:700;cursor:pointer;box-shadow:var(--shadow);transition:right .25s ease,background .2s;}
.toc-toggle.shifted{right:248px;}
.toc-toggle:hover{background:var(--gradient-start);}
.toc ul{padding-left:1em;margin:.2em 0;list-style:none;}
.toc>ul{padding:0 12px;}
.toc li{margin:1px 0;}
.toc a{color:var(--muted);text-decoration:none;display:block;padding:3px 8px;border-radius:4px;border-left:2px solid transparent;transition:all .15s;line-height:1.4;}
.toc a:hover{color:var(--accent);background:var(--accent-light);}
.toc a.active{color:var(--accent);font-weight:600;border-left-color:var(--accent);background:var(--accent-light);}
@media(min-width:1300px){.toc{left:auto;right:0;width:220px;border-radius:10px 0 0 10px;border:1px solid var(--border);border-right:0;top:100px;height:calc(100vh - 120px);box-shadow:var(--shadow);}.toc.open{transform:translateX(0);}.toc-toggle{right:8px;}.toc-toggle.shifted{right:228px;}}
@media(max-width:640px){.toc{width:200px;}.toc-toggle.shifted{right:208px;}}
.docfoot{margin-top:3em;padding-top:16px;border-top:2px solid var(--border);color:var(--muted);font-size:.8em;}
.topbar .tnav{color:#fff;text-decoration:none;font-size:12px;font-weight:600;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:20px;padding:5px 13px;margin-left:8px;white-space:nowrap;transition:background .2s;}
.topbar .tnav:hover{background:rgba(255,255,255,.25);}
.pagenav{display:flex;justify-content:space-between;gap:16px;margin:36px 0 8px;}
.pagenav .pn{flex:1 1 0;max-width:48%;text-decoration:none;border:1px solid var(--border);border-radius:12px;padding:14px 18px;background:#fff;display:flex;flex-direction:column;gap:3px;transition:all .2s ease;}
.pagenav .pn:hover{border-color:var(--accent);box-shadow:var(--shadow-lg);transform:translateY(-2px);}
.pagenav .pn.next{align-items:flex-end;text-align:right;}
.pagenav .pn .lab{font-size:.7em;text-transform:uppercase;letter-spacing:.8px;color:var(--muted);font-weight:700;}
.pagenav .pn .ttl{color:var(--fg);font-weight:600;font-size:.95em;}
.pagenav .pn.empty{visibility:hidden;border:0;background:none;box-shadow:none;}
.mermaid-fig{position:relative;margin:1.5em 0;border:1px solid var(--border);border-radius:12px;background:#fff;padding:8px;box-shadow:var(--shadow);}
.mermaid-fig>.mermaid{border:0;margin:0;background:#fff;text-align:center;}
.mm-toolbar{position:absolute;top:10px;right:10px;z-index:3;opacity:.3;transition:opacity .2s;}
.mermaid-fig:hover .mm-toolbar,.mm-toolbar:focus-within{opacity:1;}
.mm-btn{font:600 12px/1.2 'Inter',-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--accent);color:#fff;border:0;border-radius:8px;padding:8px 12px;cursor:pointer;transition:background .2s;}
.mm-btn:hover{background:var(--gradient-start);}
.mm-overlay{position:fixed;inset:0;z-index:99999;background:#fff;display:flex;flex-direction:column;}
.mm-bar{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--border);background:var(--soft);flex:0 0 auto;}
.mm-bar .sp{flex:1;}.mm-bar .hint{color:var(--muted);font-size:12px;}.mm-bar strong{font-size:14px;}
.mm-stage{flex:1 1 auto;overflow:hidden;position:relative;cursor:grab;touch-action:none;background-image:linear-gradient(45deg,#f0f4f8 25%,transparent 25%,transparent 75%,#f0f4f8 75%),linear-gradient(45deg,#f0f4f8 25%,#fff 25%,#fff 75%,#f0f4f8 75%);background-size:24px 24px;background-position:0 0,12px 12px;}
.mm-stage.grabbing{cursor:grabbing;}
.mm-stage svg{position:absolute;top:0;left:0;transform-origin:0 0;}
@media(min-width:1400px){.page{max-width:1200px;}.content{padding:12px 56px 48px;}}
@media(min-width:1800px){.page{max-width:1440px;}.content{padding:16px 72px 56px;}table{font-size:.94em;}}
@media(max-width:640px){.content{padding:8px 18px 24px;}.topbar{padding:12px 18px;gap:8px;}.topbar .seq{font-size:11px;padding:2px 8px;}.topbar .crumb{font-size:11px;}.topbar .tnav{font-size:11px;padding:3px 9px;margin-left:4px;}.fm-table th{width:auto;}h1{font-size:1.5em;}h2{font-size:1.25em;}.page{margin:8px;border-radius:10px;}table{font-size:.8em;}th,td{padding:6px 8px;}.pagenav{flex-direction:column;}.pagenav .pn{max-width:100%;}.mermaid-fig{margin:1em -12px;border-radius:4px;}}
@media(max-width:480px){.content{padding:6px 12px 18px;}.topbar{flex-wrap:wrap;padding:10px 14px;}.topbar .grow{display:none;}h1{font-size:1.3em;}h2{font-size:1.1em;}table{font-size:.75em;}th,td{padding:4px 6px;}}
"""

JS = """
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad:false, securityLevel:'loose', theme:'default' });
try { await mermaid.run({ querySelector: '.mermaid' }); } catch (e) { console.error('mermaid render failed', e); }
function initPanZoom(stage, svg){
  let scale=1, tx=0, ty=0; const MIN=0.05, MAX=40;
  const vb = svg.viewBox && svg.viewBox.baseVal;
  const natW = (vb && vb.width) ? vb.width : (svg.getBoundingClientRect().width || 800);
  const natH = (vb && vb.height) ? vb.height : (svg.getBoundingClientRect().height || 600);
  svg.style.transformOrigin='0 0'; svg.style.maxWidth='none'; svg.style.width=natW+'px'; svg.style.height=natH+'px';
  const apply=()=>{ svg.style.transform='translate('+tx+'px,'+ty+'px) scale('+scale+')'; };
  function fit(){ const r=stage.getBoundingClientRect(); let s=Math.min(r.width/natW, r.height/natH);
    if(!isFinite(s)||s<=0) s=1; s*=0.92; scale=s; tx=(r.width-natW*scale)/2; ty=(r.height-natH*scale)/2; apply(); }
  function zoomAt(cx,cy,f){ let ns=Math.max(MIN, Math.min(MAX, scale*f));
    tx=cx-(cx-tx)*(ns/scale); ty=cy-(cy-ty)*(ns/scale); scale=ns; apply(); }
  stage.addEventListener('wheel', e=>{ e.preventDefault(); const r=stage.getBoundingClientRect();
    zoomAt(e.clientX-r.left, e.clientY-r.top, e.deltaY<0?1.12:1/1.12); }, {passive:false});
  let drag=false, lx=0, ly=0;
  stage.addEventListener('pointerdown', e=>{ drag=true; lx=e.clientX; ly=e.clientY; stage.classList.add('grabbing'); try{stage.setPointerCapture(e.pointerId);}catch(_){}} );
  stage.addEventListener('pointermove', e=>{ if(!drag) return; tx+=e.clientX-lx; ty+=e.clientY-ly; lx=e.clientX; ly=e.clientY; apply(); });
  const end=()=>{ drag=false; stage.classList.remove('grabbing'); };
  stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end); stage.addEventListener('pointerleave', end);
  stage.addEventListener('dblclick', fit);
  return { fit, zoomBy:(f)=>{ const r=stage.getBoundingClientRect(); zoomAt(r.width/2, r.height/2, f); } };
}
function closeOverlay(ov){ if(ov._closed) return; ov._closed=true;
  document.removeEventListener('keydown', ov._onkey); document.removeEventListener('fullscreenchange', ov._fs);
  if(document.fullscreenElement) document.exitFullscreen().catch(()=>{}); ov.remove(); }
function openOverlay(fig){
  const svg = fig.querySelector('.mermaid svg') || fig.querySelector('svg'); if(!svg) return;
  const ov=document.createElement('div'); ov.className='mm-overlay';
  const bar=document.createElement('div'); bar.className='mm-bar';
  bar.innerHTML='<strong>Diagram</strong><span class="hint">drag to pan &middot; scroll to zoom &middot; double-click to fit</span><span class="sp"></span>'+
    '<button type="button" class="mm-btn" data-a="out">&#8722;</button><button type="button" class="mm-btn" data-a="in">&#43;</button>'+
    '<button type="button" class="mm-btn" data-a="reset">Fit</button><button type="button" class="mm-btn" data-a="close">Close &#10005;</button>';
  const stage=document.createElement('div'); stage.className='mm-stage'; stage.appendChild(svg.cloneNode(true));
  ov.appendChild(bar); ov.appendChild(stage); document.body.appendChild(ov);
  const pz=initPanZoom(stage, stage.querySelector('svg')); requestAnimationFrame(()=>pz.fit());
  bar.addEventListener('click', e=>{ const b=e.target.closest('button'); if(!b) return; const a=b.getAttribute('data-a');
    if(a==='in') pz.zoomBy(1.25); else if(a==='out') pz.zoomBy(1/1.25); else if(a==='reset') pz.fit(); else if(a==='close') closeOverlay(ov); });
  ov._onkey=(e)=>{ if(e.key==='Escape') closeOverlay(ov); }; document.addEventListener('keydown', ov._onkey);
  ov._fs=()=>{ if(document.fullscreenElement===ov){ setTimeout(()=>pz.fit(),60); } else if(ov._wasFs){ closeOverlay(ov); } };
  document.addEventListener('fullscreenchange', ov._fs);
  if(ov.requestFullscreen){ ov.requestFullscreen().then(()=>{ ov._wasFs=true; setTimeout(()=>pz.fit(),60); }).catch(()=>{}); }
}
document.querySelectorAll('.mermaid-fig .mm-full').forEach(btn=>{ btn.addEventListener('click', ()=> openOverlay(btn.closest('.mermaid-fig'))); });
const _pv=document.querySelector('.pn.prev'), _nx=document.querySelector('.pn.next');
document.addEventListener('keydown', e=>{
  if(document.querySelector('.mm-overlay')) return;
  const t=e.target.tagName; if(t==='INPUT'||t==='TEXTAREA') return;
  if(e.key==='ArrowLeft' && _pv){ location.href=_pv.getAttribute('href'); }
  else if(e.key==='ArrowRight' && _nx){ location.href=_nx.getAttribute('href'); }
});
/* Conditional cell coloring for comparative columns */
(function(){
  /* Collapsible blockquote legends — wrap in <details> */
  document.querySelectorAll('blockquote').forEach(bq=>{
    const first=bq.querySelector('p>strong')||bq.querySelector('strong');
    if(!first||!first.textContent.includes('Column Legend')) return;
    const det=document.createElement('details');
    det.className='legend';
    const sum=document.createElement('summary');
    sum.textContent='Column Legend';
    const body=document.createElement('div');
    body.className='legend-body';
    while(bq.firstChild){
      if(bq.firstChild.nodeType===1 && bq.firstChild.tagName==='P' && bq.firstChild.querySelector('strong') && bq.firstChild.textContent.trim().startsWith('Column Legend')){
        bq.removeChild(bq.firstChild);
        continue;
      }
      body.appendChild(bq.firstChild);
    }
    det.appendChild(sum);
    det.appendChild(body);
    bq.replaceWith(det);
  });
  /* TOC sidebar toggle + scroll-spy */
  (function(){
    const toc=document.getElementById('toc-panel');
    const btn=document.getElementById('toc-btn');
    if(!toc||!btn) return;
    btn.addEventListener('click',()=>{toc.classList.toggle('open');btn.classList.toggle('shifted');});
    const links=toc.querySelectorAll('a[href^="#"]');
    if(!links.length) return;
    const headings=[];
    links.forEach(a=>{const id=a.getAttribute('href').slice(1);const el=document.getElementById(id);if(el)headings.push({el,a});});
    let raf=0;
    function onScroll(){cancelAnimationFrame(raf);raf=requestAnimationFrame(()=>{
      let cur=null;const top=window.scrollY+100;
      for(let i=headings.length-1;i>=0;i--){if(headings[i].el.offsetTop<=top){cur=headings[i];break;}}
      links.forEach(a=>a.classList.remove('active'));
      if(cur){cur.a.classList.add('active');cur.a.scrollIntoView({block:'nearest',behavior:'smooth'});}
    });}
    window.addEventListener('scroll',onScroll,{passive:true});
    onScroll();
  })();
  const colors={
    'critical':['#fef2f2','#991b1b'],'very high':['#fef2f2','#991b1b'],
    'high':['#fff7ed','#9a3412'],'significant':['#fff7ed','#9a3412'],
    'medium':['#fefce8','#854d0e'],'moderate':['#fefce8','#854d0e'],
    'low':['#f0fdf4','#166534'],'minor':['#f0fdf4','#166534'],
    'very low':['#f0fdf4','#166534'],'negligible':['#f0fdf4','#166534'],
    'adopt':['#f0fdf4','#166534'],'trial':['#eff6ff','#1e40af'],
    'assess':['#fefce8','#854d0e'],'hold':['#fef2f2','#991b1b'],
    'yes':['#f0fdf4','#166534'],'no':['#fef2f2','#991b1b'],'partial':['#fefce8','#854d0e'],
    'strong':['#f0fdf4','#166534'],'weak':['#fef2f2','#991b1b'],
    'strength':['#f0fdf4','#166534'],'weakness':['#fef2f2','#991b1b'],
    'opportunity':['#eff6ff','#1e40af'],'threat':['#fff7ed','#9a3412'],
    'completed':['#f0fdf4','#166534'],'in-progress':['#eff6ff','#1e40af'],'not started':['#fef2f2','#991b1b'],
    'resolved':['#f0fdf4','#166534'],'open':['#fef2f2','#991b1b'],'mitigated':['#fefce8','#854d0e']
  };
  /* Text-based coloring */
  document.querySelectorAll('td').forEach(td=>{
    const txt=td.textContent.trim().toLowerCase();
    const c=colors[txt];
    if(c){td.style.background=c[0];td.style.color=c[1];td.style.fontWeight='600';}
  });
  /* Numeric gradient coloring for score/weight columns */
  document.querySelectorAll('table').forEach(tbl=>{
    const ths=tbl.querySelectorAll('thead th, tr:first-child th');
    if(!ths.length) return;
    const scoreKw=/score|significance|weight|priority|impact|severity|rating|rank|maturity|readiness|risk|ev\b|p.i\b/i;
    ths.forEach((th,ci)=>{
      if(!scoreKw.test(th.textContent)) return;
      const cells=[]; let min=Infinity, max=-Infinity;
      tbl.querySelectorAll('tbody tr, tr:not(:first-child)').forEach(tr=>{
        const td=tr.querySelectorAll('td')[ci]; if(!td) return;
        const v=parseFloat(td.textContent.replace(/[^0-9.\-]/g,''));
        if(!isNaN(v)){cells.push({td,v}); if(v<min)min=v; if(v>max)max=v;}
      });
      if(cells.length<2||min===max) return;
      cells.forEach(({td,v})=>{
        const t=(v-min)/(max-min);
        const r=Math.round(254-(t*115));
        const g=Math.round(202+(t*50));
        const b=Math.round(202-(t*90));
        td.style.background='rgb('+r+','+g+','+b+')';
        td.style.color=t>0.7?'#14532d':t<0.3?'#7f1d1d':'#713f12';
        td.style.fontWeight='600';
      });
    });
  });
})();
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<title>%%TITLE%%</title>
<style>%%CSS%%</style>
</head>
<body>
%%TOC%%
<div class="page">
<div class="topbar"><a class="home" href="%%INDEXHREF%%" title="Back to index">&#8962;</a><span class="seq">%%SEQ%%</span><span class="crumb">%%CRUMB%%</span><span class="grow"></span>%%TOPNAV%%</div>
<div class="content">
%%META%%
%%BODY%%
%%PAGENAV%%
<div class="docfoot">Generated from <code>%%SRC%%</code> on %%DATE%% &middot; sequence %%SEQ%% &middot; <a href="%%INDEXHREF%%">back to index</a>. This HTML is a read-only view; the Markdown source is authoritative.<br><br><strong>AIFLC</strong> (AI Full Life Cycle) &mdash; a structured, AI-driven enterprise strategy and architecture methodology. Built with the <strong>AIFLC HTML Export</strong> engine. <a href="https://github.com/mbmd/AIFLC" target="_blank" rel="noopener noreferrer">GitHub</a><br>Created by <strong>Mohammad Maheri</strong> &mdash; <a href="https://www.linkedin.com/in/mohammad-maheri-8399565b" target="_blank" rel="noopener noreferrer">LinkedIn</a></div>
</div>
</div>
<script type="module">%%JS%%</script>
</body>
</html>
"""


def get_title(src_abs):
    try:
        with open(src_abs, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return os.path.splitext(os.path.basename(src_abs))[0]
    _, body = split_front_matter(text)
    m = re.search(r"(?m)^#[ \t]+(.+?)[ \t]*#*[ \t]*$", body)
    if not m:
        return os.path.splitext(os.path.basename(src_abs))[0]
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", m.group(1))
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[*`_]+", "", t)
    return t.strip() or os.path.splitext(os.path.basename(src_abs))[0]


def convert_one(src_abs, src_root, export_root, seq, seq_map, config, prev=None, nxt=None):
    with open(src_abs, "r", encoding="utf-8") as f:
        text = f.read()
    fm_text, body = split_front_matter(text)
    fm_data = parse_fm(fm_text)
    body, mermaid_blocks = extract_mermaid(body)

    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"], output_format="html5")
    html_body = md.convert(body)
    toc_tokens = getattr(md, "toc_tokens", [])

    html_body = reinsert_mermaid(html_body, mermaid_blocks)
    html_body = html_body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    html_body = HREF_RE.sub(make_link_rewriter(src_abs, src_root, seq_map), html_body)
    html_body = linkify_bare_urls(html_body)

    tm = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
    title = re.sub(r"<[^>]+>", "", tm.group(1)).strip() if tm else os.path.splitext(os.path.basename(src_abs))[0]

    rel = os.path.relpath(src_abs, src_root).replace(os.sep, "/")
    crumb_dir = os.path.dirname(rel)
    crumb = ("<b>%s</b> / %s" % (html.escape(crumb_dir), html.escape(os.path.basename(rel)))
             if crumb_dir else "<b>%s</b>" % html.escape(os.path.basename(rel)))

    out_abs = seq_map[src_abs]
    index_href = os.path.relpath(os.path.join(export_root, "index.html"),
                                 os.path.dirname(out_abs)).replace(os.sep, "/")

    if prev:
        top_prev = '<a class="tnav" href="%s" title="%s">&#8249; Prev</a>' % (prev[0], html.escape(prev[1]))
        pn_prev = ('<a class="pn prev" href="%s"><span class="lab">&#8592; Previous</span>'
                   '<span class="ttl">%s</span></a>') % (prev[0], html.escape(prev[1]))
    else:
        top_prev, pn_prev = "", '<span class="pn empty"></span>'
    if nxt:
        top_next = '<a class="tnav" href="%s" title="%s">Next &#8250;</a>' % (nxt[0], html.escape(nxt[1]))
        pn_next = ('<a class="pn next" href="%s"><span class="lab">Next &#8594;</span>'
                   '<span class="ttl">%s</span></a>') % (nxt[0], html.escape(nxt[1]))
    else:
        top_next, pn_next = "", '<span class="pn empty"></span>'

    page = (PAGE.replace("%%TITLE%%", html.escape(title)).replace("%%CSS%%", CSS).replace("%%JS%%", JS)
            .replace("%%SEQ%%", "%02d" % seq).replace("%%CRUMB%%", crumb)
            .replace("%%INDEXHREF%%", index_href)
            .replace("%%META%%", render_front_matter(fm_text, fm_data))
            .replace("%%TOC%%", render_toc(toc_tokens)).replace("%%BODY%%", html_body)
            .replace("%%TOPNAV%%", top_prev + top_next).replace("%%PAGENAV%%",
                     '<nav class="pagenav">%s%s</nav>' % (pn_prev, pn_next))
            .replace("%%SRC%%", html.escape(rel))
            .replace("%%DATE%%", datetime.date.today().isoformat()))

    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    with open(out_abs, "w", encoding="utf-8") as f:
        f.write(page)

    stage = fm_field(fm_data, "stage")
    return {"seq": seq, "group": (crumb_dir.split("/")[0] if crumb_dir else ""),
            "href": os.path.relpath(out_abs, export_root).replace(os.sep, "/"),
            "title": title, "stage": stage}


# --- landing page ----------------------------------------------------------

INDEX_CSS = """
:root{--fg:#1a1f36;--muted:#4a5568;--border:#e2e8f0;--soft:#f7fafc;--accent:#2b6cb0;}
*{box-sizing:border-box;}
body{margin:0;color:var(--fg);background:linear-gradient(135deg,#f0f4f8 0%,#e2e8f0 100%);font-family:'Source Sans Pro','Noto Sans',-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.7;}
.wrap{max-width:1080px;margin:24px auto;padding:0 18px 48px;}
.hero{background:linear-gradient(120deg,#0b3d66,#0969da);color:#fff;border-radius:14px;padding:30px 34px;box-shadow:0 2px 8px rgba(27,31,36,.12);}
.hero h1{margin:0 0 6px;font-size:2em;}.hero .sub{font-size:1.05em;opacity:.92;}
.hero .stats{margin-top:14px;font-size:.86em;opacity:.9;display:flex;gap:18px;flex-wrap:wrap;}.hero .stats b{font-size:1.15em;}
.hero .note{margin-top:12px;font-size:.8em;opacity:.85;}
.group{margin-top:26px;background:#fff;border:1px solid var(--border);border-left:6px solid var(--accent);border-radius:10px;padding:18px 22px 22px;box-shadow:0 1px 3px rgba(27,31,36,.06);}
.group-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;}
.group-head h2{margin:0;font-size:1.3em;color:var(--accent);}
.group-meta{color:var(--muted);font-size:.82em;font-weight:600;letter-spacing:.3px;}
.group-desc{color:var(--muted);margin:.4em 0 1em;font-size:.92em;}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;}
.card{display:flex;gap:12px;align-items:flex-start;padding:12px 14px;border:1px solid var(--border);border-radius:9px;background:#fff;text-decoration:none;color:inherit;transition:border-color .12s,box-shadow .12s,transform .12s;}
.card:hover{border-color:var(--accent);box-shadow:0 3px 10px rgba(9,105,218,.14);transform:translateY(-1px);}
.card-seq{flex:0 0 auto;font-weight:700;font-size:.9em;color:#fff;background:var(--accent);border-radius:8px;padding:4px 9px;min-width:34px;text-align:center;}
.card-body{display:flex;flex-direction:column;min-width:0;}
.card-title{font-weight:600;color:var(--fg);line-height:1.3;}
.card-stage{color:var(--muted);font-size:.78em;margin-top:2px;}
.card-file{color:#8a94a0;font-size:.73em;margin-top:4px;font-family:ui-monospace,Consolas,monospace;overflow-wrap:anywhere;}
.foot{margin-top:30px;color:var(--muted);font-size:.82em;text-align:center;}
.portal-back{display:inline-block;color:#fff;opacity:.85;font-size:.85em;font-weight:600;text-decoration:none;margin-bottom:12px;padding:5px 14px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:20px;transition:all .2s;}
.portal-back:hover{opacity:1;background:rgba(255,255,255,.25);text-decoration:none;}
.toc{position:fixed;top:72px;right:0;width:240px;height:calc(100vh - 72px);background:#fff;border-left:1px solid var(--border);box-shadow:-2px 0 8px rgba(0,0,0,.06);overflow-y:auto;padding:14px 0;transform:translateX(100%);transition:transform .25s ease;z-index:20;font-size:.82em;}
.toc.open{transform:translateX(0);}
.toc-toggle{position:fixed;top:80px;right:8px;z-index:21;background:var(--accent);color:#fff;border:0;border-radius:8px 0 0 8px;padding:8px 10px;font-size:13px;font-weight:700;cursor:pointer;box-shadow:0 4px 6px -1px rgba(0,0,0,.07);transition:right .25s ease,background .2s;}
.toc-toggle.shifted{right:248px;}
.toc-toggle:hover{background:#1a365d;}
.toc ul{padding-left:0;margin:.2em 0;list-style:none;}
.toc>ul{padding:0 12px;}
.toc li{margin:1px 0;}
.toc a{color:var(--muted);text-decoration:none;display:block;padding:5px 10px;border-radius:4px;border-left:2px solid transparent;transition:all .15s;line-height:1.4;font-size:.92em;}
.toc a:hover{color:var(--accent);background:#ebf4ff;}
.toc a.active{color:var(--accent);font-weight:600;border-left-color:var(--accent);background:#ebf4ff;}
@media(min-width:1400px){.wrap{max-width:1280px;}.cards{grid-template-columns:repeat(auto-fill,minmax(360px,1fr));}.toc{width:220px;border-radius:10px 0 0 10px;border:1px solid var(--border);border-right:0;top:100px;height:calc(100vh - 120px);}.toc-toggle.shifted{right:228px;}}
@media(max-width:560px){.cards{grid-template-columns:1fr;}.wrap{padding:0 12px 32px;}.hero{padding:22px 18px;border-radius:10px;}.hero h1{font-size:1.5em;}.hero .stats{gap:10px;font-size:.8em;}.group{padding:14px 16px;}.group-head h2{font-size:1.1em;}.card{padding:10px 12px;}.toc{width:200px;}.toc-toggle.shifted{right:208px;}}
"""

INDEX_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet">
<title>%%TITLE%% &mdash; Document Index</title>
<style>%%CSS%%</style>
</head>
<body>
%%TOC%%
<div class="wrap">
<div class="hero">
<a class="portal-back" href="../index.html">&larr; Back to Portal</a>
<h1>%%TITLE%%</h1>
<div class="sub">%%SUBTITLE%%</div>
<div class="stats"><span><b>%%TOTAL%%</b> documents</span><span><b>%%GROUPS%%</b> stages</span><span>generated %%DATE%%</span></div>
<div class="note">This site is a read-only view of the workspace. The Markdown files are the single source of truth.</div>
</div>
%%SECTIONS%%
<div class="foot">Sequence numbers (NN) follow workflow-stage order. State markers and routing artifacts are excluded from the site.<br><strong>AIFLC</strong> (AI Full Life Cycle) &mdash; a structured, AI-driven enterprise strategy and architecture methodology. Built with the <strong>AIFLC HTML Export</strong> engine. <a href="https://github.com/mbmd/AIFLC" target="_blank" rel="noopener noreferrer">GitHub</a><br>Created by <strong>Mohammad Maheri</strong> &mdash; <a href="https://www.linkedin.com/in/mohammad-maheri-8399565b" target="_blank" rel="noopener noreferrer">LinkedIn</a></div>
</div>
<script>
(function(){
  var toc=document.getElementById('toc-panel');
  var btn=document.getElementById('toc-btn');
  if(!toc||!btn) return;
  btn.addEventListener('click',function(){toc.classList.toggle('open');btn.classList.toggle('shifted');});
  var links=toc.querySelectorAll('a[href^="#"]');
  if(!links.length) return;
  var sections=[];
  links.forEach(function(a){var id=a.getAttribute('href').slice(1);var el=document.getElementById(id);if(el)sections.push({el:el,a:a});});
  var raf=0;
  function onScroll(){cancelAnimationFrame(raf);raf=requestAnimationFrame(function(){
    var cur=null,top=window.scrollY+120;
    for(var i=sections.length-1;i>=0;i--){if(sections[i].el.offsetTop<=top){cur=sections[i];break;}}
    links.forEach(function(a){a.classList.remove('active');});
    if(cur){cur.a.classList.add('active');cur.a.scrollIntoView({block:'nearest',behavior:'smooth'});}
  });}
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();
})();
</script>
</body>
</html>
"""


def build_index(items, export_root, family, config):
    hide = set((config.get("landing") or {}).get("hideFromLanding") or [])
    groups = {}
    for it in items:
        if it["group"] in hide:
            continue
        groups.setdefault(it["group"], []).append(it)

    def gkey(g):
        order, _, _, _ = group_meta(g, config, family)
        return (order, min(x["seq"] for x in groups[g]))

    order = sorted(groups.keys(), key=gkey)
    shown_total = sum(len(v) for v in groups.values())
    sections = []
    for g in order:
        _, label, accent, desc = group_meta(g, config, family)
        docs = sorted(groups[g], key=lambda x: x["seq"])
        lo, hi = docs[0]["seq"], docs[-1]["seq"]
        rng = "%02d" % lo if lo == hi else "%02d-%02d" % (lo, hi)
        cards = []
        for d in docs:
            stage = ("<span class='card-stage'>%s</span>" % html.escape(d["stage"])) if d["stage"] else ""
            cards.append("<a class='card' href='%s'><span class='card-seq'>%02d</span>"
                         "<span class='card-body'><span class='card-title'>%s</span>%s"
                         "<span class='card-file'>%s</span></span></a>"
                         % (d["href"], d["seq"], html.escape(d["title"]), stage,
                            html.escape(os.path.basename(d["href"]))))
        sections.append("<section class='group' id='grp-%s' style='--accent:%s'>"
                        "<div class='group-head'><h2>%s</h2><span class='group-meta'>%d docs &middot; seq %s</span></div>"
                        "<p class='group-desc'>%s</p><div class='cards'>%s</div></section>"
                        % (html.escape(g or "overview"), accent, html.escape(label), len(docs), rng, html.escape(desc), "".join(cards)))

    # Build TOC for the right-panel navigation
    toc_items = []
    for g in order:
        _, label, _, _ = group_meta(g, config, family)
        anchor = "grp-%s" % (g or "overview")
        toc_items.append("<li><a href='#%s'>%s</a></li>" % (html.escape(anchor), html.escape(label)))
    toc_html = ("<nav class='toc' id='toc-panel'><ul>%s</ul></nav>"
                "<button class='toc-toggle' id='toc-btn' title='Toggle Contents'>&#9776;</button>"
                % "".join(toc_items)) if toc_items else ""

    landing = config.get("landing") or {}
    title = landing.get("title") or ("%s Workspace" % family.upper())
    subtitle = landing.get("subtitle") or ""
    page = (INDEX_PAGE.replace("%%TITLE%%", html.escape(title))
            .replace("%%SUBTITLE%%", html.escape(subtitle)).replace("%%CSS%%", INDEX_CSS)
            .replace("%%TOTAL%%", str(shown_total)).replace("%%GROUPS%%", str(len(order)))
            .replace("%%DATE%%", datetime.date.today().isoformat())
            .replace("%%TOC%%", toc_html)
            .replace("%%SECTIONS%%", "".join(sections)))
    out = os.path.join(export_root, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    return out


# --- git ignore (D-E: default-ignore the shadow, keep config tracked) -------

def ensure_gitignore(publish_root, commit_shadow):
    path = os.path.join(publish_root, ".gitignore")
    if commit_shadow:
        body = ("# AIFLC HTML Export - committing the shadow (git.commitShadow: true)\n"
                "# The site is committed (e.g. for static hosting).\n")
    else:
        body = ("# AIFLC HTML Export - the HTML site is a derived, disposable shadow.\n"
                "# It is git-ignored by default; the .config.yaml settings stay tracked.\n"
                "*-html/\n*-deck.html\n")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
    except Exception as e:
        print("  note: could not write %s (%r)" % (path, e))


# --- config bootstrap (Phase 2) --------------------------------------------

def _template_path():
    """Path to the bundled config template shipped with the extension."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "templates", "publish-config.yaml")


def bootstrap_config(config_path, family):
    """Write-if-absent: copy the template to config_path on first run.
    Never overwrites an existing file (user edits are sacred)."""
    if os.path.isfile(config_path):
        return False  # already exists — nothing to do
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    tmpl = _template_path()
    if os.path.isfile(tmpl):
        with open(tmpl, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # Fallback if template is missing (shouldn't happen in a proper install)
        content = ("# AIFLC HTML Export — per-family config for %s\n"
                   "enabled: true\nautoRefresh: true\n" % family)
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  Created config: %s" % config_path)
    return True


def set_config_field(config_path, field, value):
    """Set a top-level YAML field in-place while preserving comments.
    Minimal YAML editing — avoids rewriting the whole file."""
    if not os.path.isfile(config_path):
        return
    with open(config_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    pat = re.compile(r"^(%s\s*:)\s*(.*)$" % re.escape(field))
    found = False
    for i, line in enumerate(lines):
        m = pat.match(line)
        if m:
            lines[i] = "%s %s\n" % (m.group(1), value)
            found = True
            break
    if not found:
        lines.append("%s: %s\n" % (field, value))
    with open(config_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


# --- sub-commands (Phase 2 — the switch) ------------------------------------

def cmd_on(src, family, workspace_root, config_path):
    """HTM__ on — enable auto-refresh, bootstrap config, then run a full publish."""
    publish_root = os.path.join(workspace_root, ".publish")
    os.makedirs(publish_root, exist_ok=True)
    bootstrap_config(config_path, family)
    set_config_field(config_path, "enabled", "true")
    set_config_field(config_path, "autoRefresh", "true")
    print("Switch ON for '%s'. autoRefresh enabled (gate-driven + on-demand HTM__)." % family)
    print("Running full publish...")
    # Run the full publish with force=True (the switch is now on)
    return do_publish(src, family, workspace_root, config_path, force=True)


def cmd_off(src, family, workspace_root, config_path):
    """HTM__ off — disable auto-refresh. The shadow stays as a frozen snapshot."""
    publish_root = os.path.join(workspace_root, ".publish")
    os.makedirs(publish_root, exist_ok=True)
    bootstrap_config(config_path, family)
    set_config_field(config_path, "autoRefresh", "false")
    print("Switch OFF for '%s'. Auto-refresh disabled; shadow stays frozen." % family)
    print("Manual HTM__ still works (enabled stays true).")


def cmd_status(src, family, workspace_root, config_path):
    """HTM__ status — report switch state, last publish time, page count."""
    publish_root = os.path.join(workspace_root, ".publish")
    export_root = os.path.join(publish_root, "%s-html" % family)
    config, had_cfg = load_config(config_path)
    enabled = config.get("enabled", True)
    auto = config.get("autoRefresh", True)
    # count pages
    pages = 0
    if os.path.isdir(export_root):
        for _, _, fns in os.walk(export_root):
            pages += sum(1 for f in fns if f.endswith(".html") and f != "index.html")
    # last publish time (index.html mtime)
    idx = os.path.join(export_root, "index.html")
    if os.path.isfile(idx):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(idx)).isoformat(timespec="seconds")
    else:
        mtime = "(never published)"
    print("HTM__ status for '%s'" % family)
    print("  Config:       %s%s" % (config_path, "" if had_cfg else " (defaults - file not found)"))
    print("  Enabled:      %s" % enabled)
    print("  Auto-refresh: %s" % auto)
    print("  Pages:        %d" % pages)
    print("  Last publish: %s" % mtime)
    print("  Output:       %s" % export_root)


# --- main ------------------------------------------------------------------

def resolve_family(src, explicit):
    if explicit:
        return explicit
    base = os.path.basename(os.path.normpath(src))
    return base[:-3] if base.lower().endswith("-ws") else base


def find_default_workspace(here):
    for name in sorted(os.listdir(here)):
        p = os.path.join(here, name)
        if os.path.isdir(p) and name.lower().endswith("-ws"):
            return p
    return os.path.join(here, "workspace")


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    raw_args = argv if argv is not None else sys.argv[1:]

    # Detect sub-command as the first arg (on | off | status) before parsing
    subcmds = {"on", "off", "status"}
    command = None
    if raw_args and raw_args[0] in subcmds:
        command = raw_args[0]
        raw_args = raw_args[1:]

    ap = argparse.ArgumentParser(description="AIFLC HTML Export — publish a {family}-ws to a browsable HTML shadow.")
    ap.add_argument("workspace", nargs="?", help="the {family}-ws directory")
    ap.add_argument("--family", help="family code (default: derived from workspace folder name)")
    ap.add_argument("--out-root", help="workspace root for .publish/ (default: parent of workspace)")
    ap.add_argument("--config", help="config yaml path")
    ap.add_argument("--force", action="store_true", help="publish even if the config switch is off")
    args = ap.parse_args(raw_args)

    # Resolve workspace + family + paths
    src = os.path.abspath(args.workspace) if args.workspace else find_default_workspace(here)
    if not os.path.isdir(src):
        print("Workspace not found: %s" % src)
        print("Usage: python %s [on|off|status] [WORKSPACE]" % os.path.basename(__file__))
        sys.exit(1)

    family = resolve_family(src, args.family)

    # --- FIX: workspace_root resolution guard (IMP-006) ---
    # The tool is designed for {family}-ws directories. When src ends with "-ws",
    # workspace_root is correctly its parent. But if src does NOT end with "-ws"
    # (e.g., someone passes the workspace root itself), using os.path.dirname(src)
    # would escape one level too high and publish into the wrong location.
    src_basename = os.path.basename(os.path.normpath(src)).lower()
    if args.out_root:
        workspace_root = os.path.abspath(args.out_root)
    elif src_basename.endswith("-ws"):
        workspace_root = os.path.dirname(src)
    else:
        # src IS the workspace root (not a {family}-ws subfolder) — anchor here
        print("WARNING: '%s' does not end with '-ws'. Treating it as the workspace root itself." % src_basename)
        print("  If this is wrong, pass --out-root explicitly.")
        workspace_root = src
    # --- END FIX ---

    publish_root = os.path.join(workspace_root, ".publish")
    config_path = args.config or os.path.join(publish_root, "%s.config.yaml" % family)

    # Dispatch
    if command == "on":
        cmd_on(src, family, workspace_root, config_path)
    elif command == "off":
        cmd_off(src, family, workspace_root, config_path)
    elif command == "status":
        cmd_status(src, family, workspace_root, config_path)
    else:
        do_publish(src, family, workspace_root, config_path, force=args.force)


def do_publish(src, family, workspace_root, config_path, force=False):
    """Full idempotent publish. Returns the page count."""
    publish_root = os.path.join(workspace_root, ".publish")
    export_root = os.path.join(publish_root, "%s-html" % family)

    # Bootstrap config on first run (write-if-absent — never clobbers edits)
    bootstrap_config(config_path, family)

    config, had_cfg = load_config(config_path)
    if not config.get("enabled", True) and not force:
        print("Publishing is disabled for '%s' (config enabled: false). Use --force to override." % family)
        return 0

    export_abs = os.path.abspath(export_root)
    # SSOT-Shadow guard: the shadow must never live inside the source workspace.
    if export_abs == os.path.abspath(src) or export_abs.startswith(os.path.abspath(src) + os.sep):
        print("REFUSING: the output (%s) would be inside the source workspace. "
              "The shadow must be separate from the source of truth." % export_root)
        sys.exit(1)

    print("Family:     %s" % family)
    print("Workspace:  %s" % src)
    print("Output:     %s" % export_root)
    print("Config:     %s%s" % (config_path, "" if had_cfg else "  (defaults - not found)"))

    # The shadow is disposable (SSOT-Shadow): clear it each run so the site is an
    # exact, orphan-free mirror of the current Markdown (no stale/renamed pages).
    if os.path.isdir(export_root):
        shutil.rmtree(export_root, ignore_errors=True)

    files = collect_files(src, export_abs, config, family)
    if not files:
        print("No publishable .md files found.")
        os.makedirs(export_root, exist_ok=True)
        build_index([], export_root, family, config)
        ensure_gitignore(publish_root, (config.get("git") or {}).get("commitShadow", False))
        return 0

    seq_map = {}
    for i, srcf in enumerate(files, start=1):
        rel = os.path.relpath(srcf, src)
        d = os.path.dirname(rel)
        base = os.path.splitext(os.path.basename(rel))[0]
        name = "%02d_%s.html" % (i, base)
        seq_map[srcf] = os.path.join(export_root, d, name) if d else os.path.join(export_root, name)

    def relhref(cur, tgt):
        return os.path.relpath(seq_map[tgt], os.path.dirname(seq_map[cur])).replace(os.sep, "/")

    titles = [get_title(s) for s in files]
    print("Converting %d files..." % len(files))
    items, ok = [], 0
    for i, srcf in enumerate(files, start=1):
        prev = (relhref(srcf, files[i - 2]), titles[i - 2]) if i > 1 else None
        nxt = (relhref(srcf, files[i]), titles[i]) if i < len(files) else None
        try:
            meta = convert_one(srcf, src, export_root, i, seq_map, config, prev, nxt)
            items.append(meta)
            ok += 1
            print("  [ok] %02d %s" % (i, meta["href"]))
        except Exception as e:
            print("  [FAIL] %02d %s -> %r" % (i, os.path.relpath(srcf, src), e))

    idx = build_index(items, export_root, family, config)
    ensure_gitignore(publish_root, (config.get("git") or {}).get("commitShadow", False))
    print("Done: %d/%d pages + index -> %s" % (ok, len(files), os.path.relpath(idx, workspace_root).replace(os.sep, "/")))
    return ok


if __name__ == "__main__":
    main()
