"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
let panel;
function activate(context) {
    // Command: Open Dashboard
    const openCmd = vscode.commands.registerCommand('aiflc-pdlc-dashboard.open', () => {
        if (panel) {
            panel.reveal();
            refreshPanel(context);
            return;
        }
        panel = vscode.window.createWebviewPanel('aiflcDashboard', 'AIFLC Dashboard', vscode.ViewColumn.Beside, {
            enableScripts: true,
            retainContextWhenHidden: true,
            localResourceRoots: [
                vscode.Uri.file(path.join(context.extensionPath, '..', 'ui'))
            ]
        });
        refreshPanel(context);
        panel.onDidDispose(() => { panel = undefined; });
        // Handle messages from webview
        panel.webview.onDidReceiveMessage((message) => {
            if (message.type === 'openFile' && message.path) {
                const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
                if (workspaceFolder) {
                    const filePath = path.join(workspaceFolder.uri.fsPath, message.path);
                    if (fs.existsSync(filePath)) {
                        vscode.window.showTextDocument(vscode.Uri.file(filePath));
                    }
                }
            }
        }, undefined, context.subscriptions);
    });
    // Command: Refresh Dashboard
    const refreshCmd = vscode.commands.registerCommand('aiflc-pdlc-dashboard.refresh', () => {
        if (panel) {
            refreshPanel(context);
        }
    });
    // File watcher: auto-refresh when any state file changes
    const watcher = vscode.workspace.createFileSystemWatcher('**/*-state.md');
    watcher.onDidChange(() => { if (panel) {
        refreshPanel(context);
    } });
    watcher.onDidCreate(() => { if (panel) {
        refreshPanel(context);
    } });
    context.subscriptions.push(openCmd, refreshCmd, watcher);
}
/**
 * Build the webview HTML — loads CSS + JS from the sibling ui/ folder,
 * injects live data from workspace state files.
 */
async function refreshPanel(context) {
    if (!panel)
        return;
    const data = await buildDashboardData();
    const dataJSON = JSON.stringify(data);
    // Find UI files from extension-relative paths
    let cssContent = '';
    let jsContent = '';
    const possibleUIPaths = [
        path.join(context.extensionPath, '..', 'ui'),
        path.join(context.extensionPath, 'ui')
    ];
    // Dynamically search workspace for the extension's UI files
    if (vscode.workspace.workspaceFolders) {
        for (const folder of vscode.workspace.workspaceFolders) {
            const root = folder.uri.fsPath;
            const candidates = [
                path.join(root, 'tools', 'extensions', 'AIFLC-PDLC-Dashboard', 'ui'),
                ...findDirsMatching(root, 'AIFLC-PDLC-Dashboard', 3)
            ];
            candidates.forEach(p => { if (!possibleUIPaths.includes(p))
                possibleUIPaths.push(p); });
        }
    }
    for (const uiPath of possibleUIPaths) {
        const cssFile = path.join(uiPath, 'styles.css');
        const jsFile = path.join(uiPath, 'dashboard.js');
        if (fs.existsSync(cssFile) && fs.existsSync(jsFile)) {
            cssContent = fs.readFileSync(cssFile, 'utf-8');
            jsContent = fs.readFileSync(jsFile, 'utf-8');
            break;
        }
    }
    if (!cssContent) {
        cssContent = '/* UI files not found */';
    }
    if (!jsContent) {
        jsContent = 'document.body.innerHTML="<p>Dashboard UI files not found.</p>";';
    }
    panel.webview.html = `<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIFLC Dashboard</title>
<style>${cssContent}</style>
</head>
<body>
<div class="topbar">
  <span class="topbar-title">AIFLC : AI-* PDLC Family</span>
  <span class="badge" id="overall-badge">0%</span>
  <button class="theme-toggle" onclick="toggleTheme()">\u2600/\uD83C\uDF19</button>
</div>
<div class="main">
  <div class="panel-left">
    <div class="tabs" id="left-tabs">
      <div class="tab active" data-tab="portfolio">Portfolio</div>
      <div class="tab" data-tab="ideas">Ideas</div>
      <div class="tab" data-tab="stats-left">Stats</div>
    </div>
    <div class="tab-content active" id="tc-portfolio"></div>
    <div class="tab-content" id="tc-ideas"></div>
    <div class="tab-content" id="tc-stats-left"></div>
  </div>
  <div class="panel-right">
    <h2 id="right-header" style="color:var(--text-heading);margin-bottom:12px;font-size:16px;">Select a project</h2>
    <div class="tabs" id="right-tabs">
      <div class="tab active" data-tab="pm">PM</div>
      <div class="tab" data-tab="po" style="display:none;">PO</div>
      <div class="tab" data-tab="architect" style="display:none;">Architect</div>
      <div class="tab" data-tab="ux" style="display:none;">UX</div>
      <div class="tab" data-tab="chain">Chain</div>
      <div class="tab" data-tab="mgmt">MF</div>
      <div class="tab" data-tab="stats-right">Stats</div>
    </div>
    <div class="tab-content active" id="tc-pm"></div>
    <div class="tab-content" id="tc-po"></div>
    <div class="tab-content" id="tc-architect"></div>
    <div class="tab-content" id="tc-ux"></div>
    <div class="tab-content" id="tc-chain"><div id="chain-container"><div class="mermaid" id="chain-mermaid"></div></div></div>
    <div class="tab-content" id="tc-mgmt"></div>
    <div class="tab-content" id="tc-stats-right"></div>
  </div>
</div>
<div class="footer">AIFLC PDLC Dashboard v0.1.0 <span id="footer-date"></span></div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>var D = ${dataJSON};</script>
<script>${jsContent}</script>
</body>
</html>`;
}
// ─── Data Building ──────────────────────────────────────────────────────────
async function buildDashboardData() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders)
        return emptyData();
    const stateFiles = await vscode.workspace.findFiles('**/*-state.md', '{**/node_modules/**,**/templates/**,**/rule-details/**}');
    if (stateFiles.length === 0)
        return emptyData();
    const packages = [];
    for (const file of stateFiles) {
        const bytes = await vscode.workspace.fs.readFile(file);
        const content = Buffer.from(bytes).toString('utf-8');
        const pkg = parseStateFile(content, vscode.workspace.asRelativePath(file));
        if (pkg)
            packages.push(pkg);
    }
    if (packages.length === 0)
        return emptyData();
    const total = packages.length;
    const overallProgress = total > 0
        ? Math.round(packages.reduce((sum, p) => sum + p.progress.pct, 0) / total)
        : 0;
    const projectName = path.basename(workspaceFolders[0].uri.fsPath);
    const allBlockers = [];
    packages.forEach(p => { if (p.blockers)
        allBlockers.push(...p.blockers); });
    return {
        generated: new Date().toISOString(),
        projects: [{
                id: 'PRJ-LIVE-001',
                name: projectName,
                status: packages.some(p => p.status === 'blocked') ? 'blocked' : 'active',
                priority: 1,
                progress: overallProgress,
                lastActivity: new Date().toISOString().split('T')[0],
                packages: packages,
                edges: inferEdges(packages),
                mgmt: { decisions: 0, risks: 0, changes: 0, actions: 0, issues: 0, lessons: 0 },
                mgmtDetail: { decisions: [], risks: [], changes: [], actions: [], issues: [], lessons: [] },
                po: null,
                arch: null,
                ux: null
            }],
        ideas: [],
        ppm: { totalProjects: 1, dispatched: 1, pending: 0, strategicFit: 0, topPriority: 'PRJ-LIVE-001' },
        health: { totalBlockers: allBlockers.length, stalledProjects: 0, overallProgress: overallProgress }
    };
}
function emptyData() {
    return {
        generated: new Date().toISOString(),
        projects: [],
        ideas: [],
        ppm: { totalProjects: 0, dispatched: 0, pending: 0, strategicFit: 0, topPriority: '' },
        health: { totalBlockers: 0, stalledProjects: 0, overallProgress: 0 }
    };
}
// ─── State File Parsing ─────────────────────────────────────────────────────
function parseStateFile(content, relativePath) {
    const filename = path.basename(relativePath);
    const codeMatch = filename.match(/^(\w[\w-]*)-state\.md$/);
    if (!codeMatch)
        return null;
    const shortCode = codeMatch[1].toUpperCase().replace(/-/g, '-');
    const code = shortCode.startsWith('AI-') ? shortCode : `AI-${shortCode}`;
    const frontMatter = extractFrontMatter(content);
    const statusRaw = frontMatter['status'] || extractField(content, 'Status') || 'active';
    const { completed, total } = countStages(content);
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    const status = normalizeStatus(statusRaw, pct);
    const currentPhase = extractField(content, 'Current Phase') || extractField(content, 'Phase') || '0';
    const totalPhases = extractField(content, 'Total Phases') || '0';
    const phaseName = extractField(content, 'Phase Name') || '';
    const stageName = extractField(content, 'Current Stage') || extractField(content, 'Last Stage Completed') || '';
    const blockers = extractBlockers(content);
    return {
        code,
        status,
        phase: { c: parseInt(currentPhase) || 0, t: parseInt(totalPhases) || total, name: phaseName },
        progress: { pct, done: completed, total },
        stage: { name: stageName },
        blockers,
        artifacts: []
    };
}
function extractFrontMatter(content) {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match)
        return {};
    const result = {};
    match[1].split('\n').forEach(line => {
        const kv = line.match(/^([\w-]+):\s*"?([^"]*)"?\s*$/);
        if (kv)
            result[kv[1]] = kv[2].trim();
    });
    return result;
}
function extractField(content, fieldName) {
    const re = new RegExp(`\\|\\s*\\*?\\*?${fieldName}\\*?\\*?\\s*\\|\\s*(.+?)\\s*\\|`, 'i');
    const match = content.match(re);
    if (match)
        return match[1].replace(/[{}]/g, '').trim();
    const re2 = new RegExp(`^-\\s*${fieldName}:\\s*(.+)$`, 'im');
    const match2 = content.match(re2);
    return match2 ? match2[1].trim() : '';
}
function countStages(content) {
    const tableMatch = content.match(/## Completed Stages[\s\S]*?\n(\|[\s\S]*?)(?=\n##|\n---|\n$)/);
    if (!tableMatch)
        return { completed: 0, total: 0 };
    const rows = tableMatch[1].split('\n').filter(r => r.startsWith('|') && !r.includes('---'));
    const dataRows = rows.slice(1);
    const total = dataRows.length;
    const completed = dataRows.filter(row => /\d{4}-\d{2}-\d{2}/.test(row)).length;
    return { completed, total };
}
function extractBlockers(content) {
    const section = content.match(/## Blockers?\n([\s\S]*?)(?=\n##|$)/);
    if (!section)
        return [];
    return section[1].split('\n')
        .filter(l => l.startsWith('- '))
        .map(l => l.replace(/^-\s*/, '').trim())
        .filter(l => l.toLowerCase() !== 'none' && !l.startsWith('{'));
}
function normalizeStatus(raw, percent) {
    const lower = raw.toLowerCase().replace(/["{} ]/g, '');
    if (lower.includes('complete') || percent >= 100)
        return 'complete';
    if (lower.includes('block'))
        return 'blocked';
    if (lower.includes('skip'))
        return 'skipped';
    if (lower.includes('pending') || percent === 0)
        return 'pending';
    return 'active';
}
function inferEdges(packages) {
    const chainOrder = ['AI-ILC', 'AI-PILC', 'AI-POLC', 'AI-UXD', 'AI-ADLC', 'AI-DWG', 'AI-GCE', 'AI-TGE'];
    const present = new Set(packages.map((p) => p.code));
    const edges = [];
    for (let i = 0; i < chainOrder.length - 1; i++) {
        if (present.has(chainOrder[i]) && present.has(chainOrder[i + 1])) {
            edges.push({ from: chainOrder[i], to: chainOrder[i + 1], type: 'handoff', label: '' });
        }
    }
    return edges;
}
/**
 * Recursively find directories matching a target name up to maxDepth levels.
 * Returns paths to `{match}/ui` if it exists.
 */
function findDirsMatching(root, targetName, maxDepth) {
    const results = [];
    function walk(dir, depth) {
        if (depth > maxDepth)
            return;
        try {
            const entries = fs.readdirSync(dir, { withFileTypes: true });
            for (const entry of entries) {
                if (!entry.isDirectory())
                    continue;
                if (entry.name === 'node_modules' || entry.name === '.git')
                    continue;
                const fullPath = path.join(dir, entry.name);
                if (entry.name === targetName) {
                    const uiPath = path.join(fullPath, 'ui');
                    if (fs.existsSync(uiPath))
                        results.push(uiPath);
                }
                else {
                    walk(fullPath, depth + 1);
                }
            }
        }
        catch { /* permission denied or broken symlink */ }
    }
    walk(root, 0);
    return results;
}
function deactivate() { }
//# sourceMappingURL=extension.js.map