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

  Sub-commands:
    on       Enable auto-refresh + run one full publish immediately.
    off      Disable auto-refresh (shadow stays as a frozen snapshot).
    status   Report switch state, last publish time, and page count.
    deck     Build the curated executive-presentation deck ({family}-deck.html).
    offline  Full publish with Mermaid vendored + a zip bundle (no internet on view).
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
    "scope": {"exclude": ["*-state.md", "*_state.md", "flo-*.md", "flo", "flow"]},
    # nesting: top-level folders whose real phase lives one level below an id
    # segment (e.g. entities/{id}/{phase}, projects/{id}/{phase}). The engine
    # descends past the id and groups by the {phase} folder (KL-3/KL-5).
    "taxonomy": {"source": "FAMILY_STRUCTURE", "order": [], "groups": {},
                 "nesting": ["entities", "group", "projects"]},
    "mermaid": {"offline": False},
    "deck": {"enabled": False, "title": None, "subtitle": ""},
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
        # nested phase folders under projects/{projectId}/ (KL-5, resolved via nesting)
        "product":          (10, "1 - Product",           "#0e9f6e", "Product definition: vision, PIP, requirements, and UX."),
        "backlog":          (12, "Backlog",               "#0e9f6e", "Epics and stories."),
        "ux":               (14, "UX Design",             "#0e9f6e", "Interaction and experience designs."),
        "architecture":     (20, "2 - Architecture",      "#7c3aed", "Architecture: ADRs, component designs, and the technical package."),
        "decisions":        (22, "Architecture Decisions", "#7c3aed", "Architecture decision records (ADRs)."),
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
    # AI-BAV produces docs in motivation/ + requirements/, AI-BCM in capabilities/,
    # AI-VSM in value-streams/, AI-OMD in operating-model/, AI-BAG in target/ + governance/.
    "balc": {
        **_COMMON_GROUPS,
        "motivation":       (10, "1 - Business Motivation",       "#0e9f6e",
                             "Drivers, goals, requirements, principles, and the motivation model tracing back to strategy."),
        "requirements":     (15, "Requirements",                  "#64748b",
                             "Architecture requirements register (seeded by motivation, verified at target)."),
        "capabilities":     (20, "2 - Business Capabilities",     "#d97706",
                             "The capability model, heatmap, maturity assessment, and capability-to-value-stream mapping."),
        "value-streams":    (30, "3 - Value Streams",             "#7c3aed",
                             "Value stream maps, stages, enabling capabilities, and cross-stream dependencies."),
        "operating-model":  (40, "4 - Operating Model",           "#0969da",
                             "The operating-model design: organizational structure, process architecture, and technology alignment."),
        "target":           (50, "5 - Target Architecture",       "#e11d48",
                             "To-Be target business architecture, gap analysis (As-Is to To-Be per capability), and transition plateaus."),
    },

    # --- DALC (Data Architecture Life Cycle) ---
    # AI-DAD in discovery/, AI-DGV in governance-data/, AI-DMO in modeling/,
    # AI-DPL in pipelines/, AI-MDM in mdm/, AI-DPS in privacy/, AI-DRA in reference-arch/.
    "dalc": {
        **_COMMON_GROUPS,
        "discovery":        (10, "1 - Data Discovery and Strategy", "#0e9f6e",
                             "Data landscape discovery, current-state inventory, strategy definition, and data principles."),
        "governance-data":  (20, "2 - Data Governance",             "#d97706",
                             "Data governance framework, policies, stewardship model, quality rules, and lineage."),
        "modeling":         (30, "3 - Data Modeling",               "#7c3aed",
                             "Logical/physical models, feature stores, vector schemas, ontologies, and schema evolution."),
        "pipelines":        (40, "4 - Pipelines and Platform",     "#0969da",
                             "Data pipelines, platform design, orchestration, ingestion patterns, and observability."),
        "mdm":              (45, "5 - Master Data Management",     "#0969da",
                             "MDM strategy, golden records, matching/merging rules, and cross-domain master data."),
        "privacy":          (48, "6 - Privacy and Security",       "#475569",
                             "Data classification, PII/PHI controls, encryption, access policies, and compliance mapping."),
        "reference-arch":   (50, "7 - Data Reference Architecture","#e11d48",
                             "Target data architecture, reference patterns, and the Data-to-Application handoff contract."),
    },

    # --- AALC (Application Architecture Life Cycle) ---
    # AI-AAD in discovery/, AI-APM in portfolio/, AI-INT in integration/,
    # AI-AMD in design/, AI-AOA in ai-orchestration/, AI-AAG in target-app/.
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
        "ai-orchestration": (45, "5 - AI Orchestration",           "#0969da",
                             "Agentic patterns, AI orchestration architecture, model routing, and guardrails."),
        "target-app":       (50, "6 - Application Governance",     "#e11d48",
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


# --- optional FAMILY_STRUCTURE label enrichment (KL-1) ----------------------
# Populated once per run by do_publish from the family's FAMILY_STRUCTURE.md when
# one can be located near the workspace. Ranked BELOW the built-in table + config
# (which stay authoritative) but ABOVE generic Title-casing — so a phase folder
# that exists in FAMILY_STRUCTURE but not yet in the built-in table still gets a
# real label. Strictly guarded so a mis-parse degrades to Title-casing, never to
# garbage. `taxonomy.source: FAMILY_STRUCTURE` opts in (default); set it to
# anything else to skip the read entirely.
_FS_LABELS = {}

# `folder/` — Description  |  **folder/**: Description  |  - `folder/` — Description
# The description must start with a capital letter and avoid table pipes, so we
# do not grab numeric columns from a runtime-tree table row.
_FS_ROW_RE = re.compile(r"[`*]{0,2}([a-z][a-z0-9_\-]{1,30})/[`*]{0,2}\s*[—:\-]\s+([A-Z][^|`*\n]{2,59})")


def family_structure_candidates(src, workspace_root, family):
    """Ordered candidate locations for a family's FAMILY_STRUCTURE.md."""
    fam = (family or "").lower()
    names = ["FAMILY_STRUCTURE.md"]
    roots = [
        src, os.path.dirname(src), workspace_root,
        os.path.join(workspace_root, ".aiflc", fam),
        os.path.join(workspace_root, ".aiflc", fam, "%s-packages" % fam),
    ]
    return [os.path.join(r, n) for r in roots for n in names]


def load_family_structure_labels(candidates):
    """Best-effort parse of folder→label hints. Never raises; returns {} if no
    file is found or nothing passes the guards."""
    for path in candidates:
        try:
            if not path or not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        labels = {}
        for line in text.splitlines():
            m = _FS_ROW_RE.search(line)
            if not m:
                continue
            folder = m.group(1).strip().lower()
            label = re.sub(r"\s+", " ", m.group(2)).strip().rstrip(".")
            if folder and label and folder not in labels:
                labels[folder] = label
        if labels:
            return labels
    return {}

STATE_RE = re.compile(r"[-_]state\.md$", re.IGNORECASE)
EXTERNAL_RE = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.\-]*:|//)")

# Mermaid ES module: CDN by default; offline mode vendors this file into _assets/
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"
MERMAID_VENDOR_NAME = "mermaid.esm.min.mjs"


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

def group_of(rel_path, config=None):
    """Group key for a workspace-relative path.

    Normally the top-level subfolder (or '' for root files). For "nested"
    top-level folders — entities/{id}/{phase}, group/{id}/{phase},
    projects/{id}/{phase} (KL-3 / KL-5) — descend past the id segment and group
    by the real {phase} folder, so per-entity / per-project artifacts sort under
    their workflow phase instead of one undifferentiated bucket. Folders to
    descend into come from config taxonomy.nesting.
    """
    parts = rel_path.replace(os.sep, "/").split("/")
    if len(parts) <= 1:
        return ""
    top = parts[0]
    nesting = ((config or {}).get("taxonomy") or {}).get("nesting") or []
    if top in nesting and len(parts) >= 4:
        # entities/{id}/{phase}/….md -> {phase}
        return parts[2]
    return top


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
    if label is None and group in _FS_LABELS:   # KL-1 enrichment (below builtin/config)
        label = _FS_LABELS[group]
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
        grp = group_of(rel, config)
        order, _, _, _ = group_meta(grp, config, family)
        # (group order, creation-time tiebreaker within group, name)
        try:
            ct = os.path.getctime(p)
        except Exception:
            ct = 0
        return (order, ct, rel.lower())

    found.sort(key=sort_key)
    return found


def compute_seq_map(files, src, export_root):
    """Map each source .md (abs) → its output .html (abs), NN_-prefixed in order.
    Shared by the document mirror and the deck so links line up."""
    seq_map = {}
    for i, srcf in enumerate(files, start=1):
        rel = os.path.relpath(srcf, src)
        d = os.path.dirname(rel)
        base = os.path.splitext(os.path.basename(rel))[0]
        name = "%02d_%s.html" % (i, base)
        seq_map[srcf] = os.path.join(export_root, d, name) if d else os.path.join(export_root, name)
    return seq_map


def vendor_mermaid(export_root):
    """Copy a vendored Mermaid ES module into the export's _assets/ for offline
    rendering. Looks in the tool's templates/assets/ and in .publish/_vendor/.
    Returns the destination path, or None if no asset is available."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "templates", "assets", MERMAID_VENDOR_NAME),
        os.path.join(os.path.dirname(export_root), "_vendor", MERMAID_VENDOR_NAME),
    ]
    for srcf in candidates:
        if os.path.isfile(srcf):
            dest_dir = os.path.join(export_root, "_assets")
            os.makedirs(dest_dir, exist_ok=True)
            try:
                shutil.copy2(srcf, os.path.join(dest_dir, MERMAID_VENDOR_NAME))
                return os.path.join(dest_dir, MERMAID_VENDOR_NAME)
            except Exception:
                return None
    return None


def make_bundle(publish_root, export_root, family):
    """Zip the shadow site into {publish_root}/{family}-html.zip for handoff."""
    try:
        base = os.path.join(publish_root, "%s-html" % family)
        return shutil.make_archive(base, "zip", root_dir=export_root)
    except Exception as e:
        print("  note: could not create zip bundle (%r)" % e)
        return None


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


def render_front_matter(fm_text, data, fields=None):
    """Render front matter as a reader header.

    If `fields` (config readerHeader.fields) is given, those fields are
    *promoted* into the open reader header in that order; any remaining
    front-matter fields drop into a collapsed "More metadata" panel (KL-4).
    With no configured fields present, every field shows (back-compat).
    """
    if not fm_text or not fm_text.strip():
        return ""

    def esc(v):
        return html.escape(str(v))

    def render_val(v):
        if isinstance(v, list):
            return "<ul class='fm-list'>%s</ul>" % "".join("<li>%s</li>" % esc(i) for i in v)
        if isinstance(v, dict):
            return "<ul class='fm-list'>%s</ul>" % "".join(
                "<li><span class='fm-subkey'>%s</span>: %s</li>" % (esc(kk), esc(vv)) for kk, vv in v.items())
        return esc(v)

    if isinstance(data, dict):
        def rows_for(keys):
            return "".join("<tr><th scope='row'>%s</th><td>%s</td></tr>" % (esc(k), render_val(data[k])) for k in keys)
        promoted = [k for k in (fields or []) if k in data]
        if not promoted:  # no configured field present → show everything (back-compat)
            return ("<details class='frontmatter' open><summary>Document metadata</summary>"
                    "<table class='fm-table'><tbody>%s</tbody></table></details>" % rows_for(list(data.keys())))
        rest = [k for k in data.keys() if k not in promoted]
        block = ("<details class='frontmatter' open><summary>Document metadata</summary>"
                 "<table class='fm-table'><tbody>%s</tbody></table></details>" % rows_for(promoted))
        if rest:
            block += ("<details class='frontmatter'><summary>More metadata</summary>"
                      "<table class='fm-table'><tbody>%s</tbody></table></details>" % rows_for(rest))
        return block
    inner = "<pre class='fm-raw'>%s</pre>" % esc(fm_text.strip())
    return "<details class='frontmatter' open><summary>Document metadata</summary>%s</details>" % inner


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
            # in-workspace but out-of-set: point back to the source file
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
    return ("<nav class='toc'><details open><summary>Contents</summary><ul>%s</ul></details></nav>" % body) if body else ""


# --- assets (CSS/JS/templates) ---------------------------------------------

CSS = """
:root{--fg:#1f2328;--muted:#59636e;--border:#d1d9e0;--bg:#fff;--soft:#f6f8fa;--accent:#0969da;--th:#eef2f6;--zebra:#fafbfc;}
*{box-sizing:border-box;}
body{margin:0;color:var(--fg);background:#eaeef2;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;font-size:16px;}
.page{max-width:980px;margin:24px auto;background:var(--bg);border:1px solid var(--border);border-radius:10px;box-shadow:0 1px 3px rgba(27,31,36,.08);}
.topbar{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:12px;padding:14px 28px;background:linear-gradient(90deg,#0b3d66,#0969da);color:#fff;border-radius:10px 10px 0 0;box-shadow:0 2px 10px rgba(11,37,69,.18);}
.topbar .home{color:#fff;text-decoration:none;font-size:18px;opacity:.85;}.topbar .home:hover{opacity:1;}
.topbar .seq{font-weight:700;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);padding:2px 10px;border-radius:20px;font-size:13px;letter-spacing:.5px;}
.topbar .crumb{font-size:13px;opacity:.9;}.topbar .crumb b{opacity:1;}.topbar .grow{flex:1;}
.content{padding:8px 34px 34px;}
h1,h2,h3,h4{line-height:1.25;margin-top:1.4em;font-weight:600;scroll-margin-top:72px;}
h1{font-size:1.9em;margin-top:.6em;padding-bottom:.3em;border-bottom:2px solid var(--border);}
h2{font-size:1.45em;padding-bottom:.25em;border-bottom:1px solid var(--border);}
h3{font-size:1.2em;}h4{font-size:1.05em;}
a{color:var(--accent);text-decoration:none;}a:hover{text-decoration:underline;}
p,li{overflow-wrap:break-word;}
blockquote{margin:1em 0;padding:.4em 1em;color:var(--muted);border-left:4px solid var(--border);background:var(--soft);border-radius:0 6px 6px 0;}
blockquote p{margin:.4em 0;}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--soft);padding:.15em .4em;border-radius:6px;font-size:.88em;}
pre{background:var(--soft);border:1px solid var(--border);border-radius:8px;padding:14px 16px;overflow:auto;font-size:.85em;}
pre code{background:none;padding:0;}
.table-wrap{overflow-x:auto;margin:1em 0;border-radius:8px;}
table{border-collapse:collapse;width:100%;font-size:.92em;}
th,td{border:1px solid var(--border);padding:8px 11px;text-align:left;vertical-align:top;}
th{background:var(--th);font-weight:600;}tbody tr:nth-child(even){background:var(--zebra);}
hr{border:0;border-top:1px solid var(--border);margin:2em 0;}
ul,ol{padding-left:1.5em;}img{max-width:100%;}
.frontmatter{margin:16px 0 4px;border:1px solid var(--border);border-radius:8px;background:var(--soft);}
.frontmatter>summary{cursor:pointer;padding:8px 14px;font-weight:600;color:var(--muted);font-size:.85em;text-transform:uppercase;letter-spacing:.6px;}
.fm-table{margin:0;font-size:.86em;}
.fm-table th{width:210px;background:#fff;color:var(--muted);font-weight:600;white-space:nowrap;vertical-align:top;}
.fm-table td{background:#fff;}.fm-list{margin:0;padding-left:1.1em;}.fm-subkey{font-weight:600;color:var(--muted);}
.fm-raw{margin:0;border:0;background:#fff;}
.toc{margin:18px 0;border:1px solid var(--border);border-radius:8px;background:#fff;}
.toc>details>summary{cursor:pointer;padding:8px 14px;font-weight:600;color:var(--muted);font-size:.85em;text-transform:uppercase;letter-spacing:.6px;}
.toc ul{padding-left:1.2em;margin:.3em 0;}.toc>details>ul{padding:4px 20px 12px;}
.toc a{color:var(--fg);}.toc a:hover{color:var(--accent);}
.docfoot{margin-top:2.5em;padding-top:14px;border-top:1px solid var(--border);color:var(--muted);font-size:.8em;}
.topbar .tnav{color:#fff;text-decoration:none;font-size:12.5px;font-weight:600;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);border-radius:20px;padding:4px 11px;margin-left:8px;white-space:nowrap;}
.topbar .tnav:hover{background:rgba(255,255,255,.28);}
.pagenav{display:flex;justify-content:space-between;gap:14px;margin:30px 0 4px;}
.pagenav .pn{flex:1 1 0;max-width:48%;text-decoration:none;border:1px solid var(--border);border-radius:10px;padding:11px 15px;background:#fff;display:flex;flex-direction:column;gap:2px;transition:border-color .12s,box-shadow .12s,transform .12s;}
.pagenav .pn:hover{border-color:var(--accent);box-shadow:0 3px 10px rgba(9,105,218,.12);transform:translateY(-1px);}
.pagenav .pn.next{align-items:flex-end;text-align:right;}
.pagenav .pn .lab{font-size:.72em;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);font-weight:700;}
.pagenav .pn .ttl{color:var(--fg);font-weight:600;font-size:.95em;}
.pagenav .pn.empty{visibility:hidden;border:0;background:none;box-shadow:none;}
.mermaid-fig{position:relative;margin:1.2em 0;border:1px solid var(--border);border-radius:8px;background:#fff;padding:6px;}
.mermaid-fig>.mermaid{border:0;margin:0;background:#fff;text-align:center;}
.mm-toolbar{position:absolute;top:8px;right:8px;z-index:3;opacity:.35;transition:opacity .15s;}
.mermaid-fig:hover .mm-toolbar,.mm-toolbar:focus-within{opacity:1;}
.mm-btn{font:600 12px/1.2 -apple-system,"Segoe UI",Roboto,sans-serif;background:#0969da;color:#fff;border:0;border-radius:6px;padding:7px 11px;cursor:pointer;}
.mm-btn:hover{background:#0b3d66;}
.mm-overlay{position:fixed;inset:0;z-index:99999;background:#fff;display:flex;flex-direction:column;}
.mm-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;border-bottom:1px solid var(--border);background:#f6f8fa;flex:0 0 auto;}
.mm-bar .sp{flex:1;}.mm-bar .hint{color:var(--muted);font-size:12px;}.mm-bar strong{font-size:14px;}
.mm-stage{flex:1 1 auto;overflow:hidden;position:relative;cursor:grab;touch-action:none;background-image:linear-gradient(45deg,#f0f3f6 25%,transparent 25%,transparent 75%,#f0f3f6 75%),linear-gradient(45deg,#f0f3f6 25%,#fff 25%,#fff 75%,#f0f3f6 75%);background-size:24px 24px;background-position:0 0,12px 12px;}
.mm-stage.grabbing{cursor:grabbing;}
.mm-stage svg{position:absolute;top:0;left:0;transform-origin:0 0;}
@media(max-width:640px){.content{padding:8px 18px 24px;}.topbar{padding:12px 18px;}.fm-table th{width:auto;}}
"""

JS = """
import mermaid from '%%MERMAIDSRC%%';
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
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<style>%%CSS%%</style>
</head>
<body>
<div class="page">
<div class="topbar"><a class="home" href="%%INDEXHREF%%" title="Back to index">&#8962;</a><span class="seq">%%SEQ%%</span><span class="crumb">%%CRUMB%%</span><span class="grow"></span>%%TOPNAV%%</div>
<div class="content">
%%META%%
%%TOC%%
%%BODY%%
%%PAGENAV%%
<div class="docfoot">Generated from <code>%%SRC%%</code> on %%DATE%% &middot; sequence %%SEQ%% &middot; <a href="%%INDEXHREF%%">back to index</a>. This HTML is a read-only view; the Markdown source is authoritative.</div>
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

    if bool((config.get("mermaid") or {}).get("offline")):
        mermaid_src = os.path.relpath(os.path.join(export_root, "_assets", MERMAID_VENDOR_NAME),
                                      os.path.dirname(out_abs)).replace(os.sep, "/")
    else:
        mermaid_src = MERMAID_CDN
    js = JS.replace("%%MERMAIDSRC%%", mermaid_src)

    page = (PAGE.replace("%%TITLE%%", html.escape(title)).replace("%%CSS%%", CSS).replace("%%JS%%", js)
            .replace("%%SEQ%%", "%02d" % seq).replace("%%CRUMB%%", crumb)
            .replace("%%INDEXHREF%%", index_href)
            .replace("%%META%%", render_front_matter(fm_text, fm_data, (config.get("readerHeader") or {}).get("fields")))
            .replace("%%TOC%%", render_toc(toc_tokens)).replace("%%BODY%%", html_body)
            .replace("%%TOPNAV%%", top_prev + top_next).replace("%%PAGENAV%%",
                     '<nav class="pagenav">%s%s</nav>' % (pn_prev, pn_next))
            .replace("%%SRC%%", html.escape(rel))
            .replace("%%DATE%%", datetime.date.today().isoformat()))

    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    with open(out_abs, "w", encoding="utf-8") as f:
        f.write(page)

    stage = fm_field(fm_data, "stage")
    reader_fields = (config.get("readerHeader") or {}).get("fields") or []
    status = fm_field(fm_data, "status") if "status" in reader_fields else ""
    return {"seq": seq, "group": group_of(rel, config),
            "href": os.path.relpath(out_abs, export_root).replace(os.sep, "/"),
            "title": title, "stage": stage, "status": status}


# --- landing page ----------------------------------------------------------

INDEX_CSS = """
:root{--fg:#1f2328;--muted:#59636e;--border:#d1d9e0;--soft:#f6f8fa;--accent:#0969da;}
*{box-sizing:border-box;}
body{margin:0;color:var(--fg);background:#eaeef2;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;}
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
.card-status{display:inline-block;margin-top:4px;font-size:.68em;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:#0969da;background:#ddf4ff;border:1px solid #b6e3ff;border-radius:20px;padding:1px 8px;width:fit-content;}
.card-file{color:#8a94a0;font-size:.73em;margin-top:4px;font-family:ui-monospace,Consolas,monospace;overflow-wrap:anywhere;}
.foot{margin-top:30px;color:var(--muted);font-size:.82em;text-align:center;}
@media(max-width:560px){.cards{grid-template-columns:1fr;}}
"""

INDEX_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%% &mdash; Document Index</title>
<style>%%CSS%%</style>
</head>
<body>
<div class="wrap">
<div class="hero">
<h1>%%TITLE%%</h1>
<div class="sub">%%SUBTITLE%%</div>
<div class="stats"><span><b>%%TOTAL%%</b> documents</span><span><b>%%GROUPS%%</b> stages</span><span>generated %%DATE%%</span></div>
<div class="note">This site is a read-only view of the workspace. The Markdown files are the single source of truth.</div>
</div>
%%SECTIONS%%
<div class="foot">Sequence numbers (NN) follow workflow-stage order. State markers and routing artifacts are excluded from the site.</div>
</div>
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
            badges = ""
            if d.get("stage"):
                badges += "<span class='card-stage'>%s</span>" % html.escape(d["stage"])
            if d.get("status"):
                badges += "<span class='card-status'>%s</span>" % html.escape(d["status"])
            cards.append("<a class='card' href='%s'><span class='card-seq'>%02d</span>"
                         "<span class='card-body'><span class='card-title'>%s</span>%s"
                         "<span class='card-file'>%s</span></span></a>"
                         % (d["href"], d["seq"], html.escape(d["title"]), badges,
                            html.escape(os.path.basename(d["href"]))))
        sections.append("<section class='group' style='--accent:%s'>"
                        "<div class='group-head'><h2>%s</h2><span class='group-meta'>%d docs &middot; seq %s</span></div>"
                        "<p class='group-desc'>%s</p><div class='cards'>%s</div></section>"
                        % (accent, html.escape(label), len(docs), rng, html.escape(desc), "".join(cards)))

    landing = config.get("landing") or {}
    title = landing.get("title") or ("%s Workspace" % family.upper())
    subtitle = landing.get("subtitle") or ""
    page = (INDEX_PAGE.replace("%%TITLE%%", html.escape(title))
            .replace("%%SUBTITLE%%", html.escape(subtitle)).replace("%%CSS%%", INDEX_CSS)
            .replace("%%TOTAL%%", str(shown_total)).replace("%%GROUPS%%", str(len(order)))
            .replace("%%DATE%%", datetime.date.today().isoformat()).replace("%%SECTIONS%%", "".join(sections)))
    out = os.path.join(export_root, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    return out


# --- executive deck (Phase 4) ----------------------------------------------

DECK_CSS = """
:root{--fg:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--bg:#0b1220;--card:#111c30;}
*{box-sizing:border-box;}
html,body{margin:0;height:100%;}
body{background:var(--bg);color:var(--fg);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
.deck{height:100vh;}
.slide{min-height:100vh;display:none;flex-direction:column;justify-content:center;padding:6vh 9vw;gap:14px;border-top:6px solid var(--accent);}
.slide.title{align-items:flex-start;}
.slide .kicker{color:var(--accent);font-size:.9rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;}
.slide h1{font-size:3rem;margin:.1em 0;line-height:1.1;}
.slide h2{font-size:2.1rem;margin:.1em 0;color:#e2e8f0;}
.slide .sub{font-size:1.3rem;color:var(--muted);}
.slide .meta{color:var(--muted);font-size:.9rem;margin-top:22px;}
.slide .desc{color:var(--muted);font-size:1.05rem;max-width:60ch;}
.slide ul{font-size:1.15rem;line-height:1.9;max-width:70ch;}
.slide ul.docs{list-style:none;padding:0;}
.slide ul.docs li a{color:var(--fg);text-decoration:none;display:flex;gap:12px;align-items:baseline;padding:6px 0;border-bottom:1px solid #1e2c44;}
.slide ul.docs li a:hover{color:var(--accent);}
.slide ul.docs .n{color:var(--accent);font-weight:700;font-variant-numeric:tabular-nums;}
.slide.note ul li{margin:.5em 0;}
.nav{position:fixed;bottom:18px;right:22px;display:flex;gap:10px;align-items:center;background:rgba(17,28,48,.9);border:1px solid #24344f;border-radius:30px;padding:6px 12px;}
.nav button{background:var(--accent);color:#04121f;border:0;border-radius:20px;width:34px;height:30px;font-size:16px;font-weight:700;cursor:pointer;}
.nav #counter{color:var(--muted);font-size:.85rem;min-width:56px;text-align:center;}
@media print{
  .slide{display:flex!important;min-height:auto;page-break-after:always;border-top:4px solid #0969da;background:#fff;color:#111;}
  body{background:#fff;color:#111;}.slide h2,.slide h1{color:#0b3d66;}.slide .sub,.slide .desc,.slide .meta,.nav #counter{color:#555;}
  .slide ul.docs li a{color:#111;}.nav{display:none;}
}
"""

DECK_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%% &mdash; Deck</title>
<style>%%CSS%%</style>
</head>
<body>
<div class="deck">%%SLIDES%%</div>
<div class="nav"><button id="prev" title="Previous">&#8249;</button><span id="counter">1 / %%COUNT%%</span><button id="next" title="Next">&#8250;</button></div>
<script>
const slides=[...document.querySelectorAll('.slide')];let i=0;
function show(n){i=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,k)=>s.style.display=(k===i?'flex':'none'));document.getElementById('counter').textContent=(i+1)+' / '+slides.length;}
document.getElementById('prev').onclick=()=>show(i-1);
document.getElementById('next').onclick=()=>show(i+1);
document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(i-1);else if(e.key==='ArrowRight'||e.key===' ')show(i+1);else if(e.key.toLowerCase()==='p')window.print();});
show(0);
</script>
</body>
</html>
"""


def build_deck(items, publish_root, family, config):
    """Build a curated executive-presentation deck shell at
    {publish_root}/{family}-deck.html. The tool provides the navigable shell +
    print-to-PDF framework + the plain-language content contract; curated
    narrative is assembled on top per that contract (design §6)."""
    deck_cfg = config.get("deck") or {}
    landing = config.get("landing") or {}
    title = deck_cfg.get("title") or landing.get("title") or ("%s Executive Overview" % family.upper())
    subtitle = deck_cfg.get("subtitle") or landing.get("subtitle") or ""

    groups = {}
    for it in items:
        groups.setdefault(it["group"], []).append(it)

    def gkey(g):
        order, _, _, _ = group_meta(g, config, family)
        return (order, min(x["seq"] for x in groups[g]))

    order = sorted(groups.keys(), key=gkey)
    slides = []
    slides.append("<section class='slide title'><div class='kicker'>Executive Overview</div>"
                  "<h1>%s</h1><p class='sub'>%s</p>"
                  "<p class='meta'>Generated %s &middot; Markdown is the single source of truth</p></section>"
                  % (html.escape(title), html.escape(subtitle), datetime.date.today().isoformat()))
    slides.append("<section class='slide note'><div class='kicker'>How to use this deck</div><h2>About this deck</h2><ul>"
                  "<li>Navigable <b>shell</b> generated from the workspace &mdash; use &larr; / &rarr; (or Space) to move; press <b>P</b> to print to PDF.</li>"
                  "<li>Curated narrative is layered per the <b>plain-language contract</b>: expand every abbreviation and code in prose, remove internal citations, and mark quantified targets <b>provisional</b> until leadership confirms.</li>"
                  "<li>Each item links to the full document in the read-only HTML shadow; the Markdown source stays authoritative.</li>"
                  "</ul></section>")
    for g in order:
        _, label, accent, desc = group_meta(g, config, family)
        docs = sorted(groups[g], key=lambda x: x["seq"])
        lis = "".join("<li><a href='%s'><span class='n'>%02d</span> %s</a></li>"
                      % (d["href"], d["seq"], html.escape(d["title"])) for d in docs)
        slides.append("<section class='slide' style='--accent:%s'><div class='kicker'>%s</div>"
                      "<h2>%s</h2><p class='desc'>%s</p><ul class='docs'>%s</ul></section>"
                      % (accent, html.escape(label), html.escape(label), html.escape(desc or ""), lis))
    slides.append("<section class='slide title'><h1>Thank you</h1>"
                  "<p class='sub'>Full detail lives in the workspace HTML shadow.</p></section>")

    page = (DECK_PAGE.replace("%%TITLE%%", html.escape(title)).replace("%%CSS%%", DECK_CSS)
            .replace("%%SLIDES%%", "".join(slides)).replace("%%COUNT%%", str(len(slides))))
    os.makedirs(publish_root, exist_ok=True)
    out = os.path.join(publish_root, "%s-deck.html" % family)
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
                "*-html/\n*-html.zip\n*-deck.html\n")
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


def cmd_deck(src, family, workspace_root, config_path):
    """HTM__ deck — build the curated executive-presentation deck shell."""
    publish_root = os.path.join(workspace_root, ".publish")
    export_root = os.path.join(publish_root, "%s-html" % family)
    bootstrap_config(config_path, family)
    config, _ = load_config(config_path)
    if not config.get("enabled", True):
        print("Publishing is disabled for '%s' (enabled: false); deck not built." % family)
        return
    export_abs = os.path.abspath(export_root)
    files = collect_files(src, export_abs, config, family)
    if not files:
        print("No publishable .md files found; nothing to build a deck from.")
        return
    seq_map = compute_seq_map(files, src, export_root)
    items = []
    for i, srcf in enumerate(files, start=1):
        rel = os.path.relpath(srcf, src)
        href = "%s-html/%s" % (family, os.path.relpath(seq_map[srcf], export_root).replace(os.sep, "/"))
        items.append({"seq": i, "group": group_of(rel, config), "title": get_title(srcf), "href": href})
    out = build_deck(items, publish_root, family, config)
    print("Deck: %s (%d docs across the chain)" % (os.path.relpath(out, workspace_root).replace(os.sep, "/"), len(items)))
    print("  Note: slides link into the %s-html/ shadow — run a full HTM__ publish so those pages exist." % family)


def cmd_offline(src, family, workspace_root, config_path):
    """HTM__ offline — full publish with Mermaid vendored + a zip bundle."""
    bootstrap_config(config_path, family)
    print("Offline build for '%s' (vendored Mermaid + zip bundle)..." % family)
    return do_publish(src, family, workspace_root, config_path, force=False, force_offline=True)


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

    # Detect sub-command as the first arg (on|off|status|deck|offline) before parsing
    subcmds = {"on", "off", "status", "deck", "offline"}
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
    workspace_root = os.path.abspath(args.out_root) if args.out_root else os.path.dirname(src)
    publish_root = os.path.join(workspace_root, ".publish")
    config_path = args.config or os.path.join(publish_root, "%s.config.yaml" % family)

    # Dispatch
    if command == "on":
        cmd_on(src, family, workspace_root, config_path)
    elif command == "off":
        cmd_off(src, family, workspace_root, config_path)
    elif command == "status":
        cmd_status(src, family, workspace_root, config_path)
    elif command == "deck":
        cmd_deck(src, family, workspace_root, config_path)
    elif command == "offline":
        cmd_offline(src, family, workspace_root, config_path)
    else:
        do_publish(src, family, workspace_root, config_path, force=args.force)


def do_publish(src, family, workspace_root, config_path, force=False, force_offline=False):
    """Full idempotent publish. Returns the page count."""
    publish_root = os.path.join(workspace_root, ".publish")
    export_root = os.path.join(publish_root, "%s-html" % family)

    # Bootstrap config on first run (write-if-absent — never clobbers edits)
    bootstrap_config(config_path, family)

    config, had_cfg = load_config(config_path)
    if force_offline:  # HTM__ offline forces vendored Mermaid for this run only
        config.setdefault("mermaid", {})["offline"] = True
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

    # KL-1: optionally enrich group labels from FAMILY_STRUCTURE.md (best-effort,
    # ranked below the built-in table + config; a mis-parse degrades to Title-casing).
    global _FS_LABELS
    _FS_LABELS = {}
    if str((config.get("taxonomy") or {}).get("source") or "").upper() == "FAMILY_STRUCTURE":
        _FS_LABELS = load_family_structure_labels(
            family_structure_candidates(src, workspace_root, family))
        if _FS_LABELS:
            print("Taxonomy:   enriched %d group label(s) from FAMILY_STRUCTURE.md" % len(_FS_LABELS))

    files = collect_files(src, export_abs, config, family)
    if not files:
        print("No publishable .md files found.")
        os.makedirs(export_root, exist_ok=True)
        build_index([], export_root, family, config)
        ensure_gitignore(publish_root, (config.get("git") or {}).get("commitShadow", False))
        return 0

    seq_map = compute_seq_map(files, src, export_root)

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

    if (config.get("mermaid") or {}).get("offline"):
        if vendor_mermaid(export_root):
            print("Offline:    vendored Mermaid into _assets/ (diagrams render with no internet).")
        else:
            print("Offline:    NOTE - no vendored Mermaid asset found. Place '%s' in the tool's "
                  "templates/assets/ (or in .publish/_vendor/) so diagrams render offline; "
                  "pages reference _assets/%s." % (MERMAID_VENDOR_NAME, MERMAID_VENDOR_NAME))
        bundle = make_bundle(publish_root, export_root, family)
        if bundle:
            print("Bundle:     %s" % os.path.relpath(bundle, workspace_root).replace(os.sep, "/"))

    print("Done: %d/%d pages + index -> %s" % (ok, len(files), os.path.relpath(idx, workspace_root).replace(os.sep, "/")))
    return ok


if __name__ == "__main__":
    main()
