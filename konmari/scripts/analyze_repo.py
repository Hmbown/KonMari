#!/usr/bin/env python3
"""
KonMari Repository Analyzer
Authentic repository decluttering inspired by Marie Kondo's KonMari Method.

Analyzes repositories following the sacred KonMari order:
1. Dead Files (Clothing) - easiest wins
2. Dependencies (Books) - clear utility judgment
3. Documentation (Papers) - requires context awareness
4. Configuration (Komono) - scattered, needs attention
5. Legacy Code (Sentimental) - hardest, requires honed judgment

Outputs structured JSON for an AI assistant to present as a cleanup ceremony.
"""

import os
import sys
import json
import subprocess
import re
import ast
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Any

# =============================================================================
# KONMARI CATEGORY 1: DEAD FILES (Clothing)
# =============================================================================

DEAD_FILE_PATTERNS = [
    # Backup patterns
    r".*_old\.(md|py|js|ts|jsx|tsx|go|rs|txt|json|yaml|yml)$",
    r".*_backup\.(md|py|js|ts|jsx|tsx|go|rs|txt|json|yaml|yml)$",
    r".*_bak\.(md|py|js|ts|jsx|tsx|go|rs|txt|json|yaml|yml)$",
    r".*\.bak$",
    r".*\.backup$",
    r".*\.old$",
    r"^backup_.*",
    r"^old_.*",
    # Temporary patterns
    r"^temp_.*",
    r"^tmp_.*",
    r".*\.tmp$",
    r".*\.temp$",
    # Version patterns
    r".*_v\d+\.(md|py|js|ts|jsx|tsx|go|rs|txt)$",
    r".*_copy\.(md|py|js|ts|jsx|tsx|go|rs|txt)$",
    r".*_copy\d*\.(md|py|js|ts|jsx|tsx|go|rs|txt)$",
    r".*\sCopy\.(md|py|js|ts|jsx|tsx|go|rs|txt)$",
    r".*\s\(\d+\)\.(md|py|js|ts|jsx|tsx|go|rs|txt)$",
    # Draft patterns
    r"^draft_.*",
    r"^scratch_.*",
    r"^notes_.*\.md$",
    # Orphan experimental scripts
    r"^test_.*\.py$",
    r"^debug_.*\.(py|js|ts)$",
    r"^scratch.*\.(py|js|ts)$",
    r"^experiment.*\.(py|js|ts)$",
    r"^try_.*\.(py|js|ts)$",
    r"^check_.*\.(py|js|ts)$",
    r"^verify_.*\.(py|js|ts)$",
]

# AI tool session artifacts (expand as needed for your stack)
AI_TOOL_ARTIFACTS = [
    r"^CLAUDE-CONTEXT\.md$",
    r"^PLAN\.md$",
    r"^DEBUG\.md$",
    r"^TODO-claude\.md$",
    r"^NOTES\.md$",
    r"^context\.md$",
    r"^session-notes\.md$",
    r"^AI-CONTEXT\.md$",
    r"^AI-NOTES\.md$",
    r"^TODO-ai\.md$",
]

# =============================================================================
# KONMARI CATEGORY 2: DEPENDENCIES (Books)
# =============================================================================

ECOSYSTEM_MARKERS = {
    "python": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
    "javascript": ["package.json"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
}

# =============================================================================
# AI COMMIT DETECTION
# =============================================================================

AI_COMMIT_PATTERNS = [
    r"^(feat|fix|chore|docs|style|refactor|test|build|ci)(\(.+\))?:",
    r"update(d)?\s+(readme|documentation|docs)",
    r"add(ed)?\s+(new\s+)?(feature|functionality|support)",
    r"implement(ed)?\s+",
    r"refactor(ed)?\s+",
    r"clean(ed)?\s*up",
    r"fix(ed)?\s+(bug|issue|typo|error)",
    r"initial\s+commit",
    r"^wip\b",
    r"minor\s+(changes|updates|fixes)",
]

AI_COMMIT_SIGNATURES = [
    "Generated with Claude Code",
    "Co-Authored-By: Claude",
    "Co-Authored-By: GitHub Copilot",
    "Generated with Copilot",
    "Co-Authored-By: OpenAI Codex",
    "Generated with Codex",
    "Co-Authored-By: Cursor",
    "Generated with Cursor",
]

# =============================================================================
# CONTEXT LIMITS
# =============================================================================

MAX_RECOMMENDED_LINES = 500
MAX_RECOMMENDED_TOKENS = 4000
CONTEXT_HEAVY_EXTENSIONS = [".md", ".txt", ".rst", ".json", ".yaml", ".yml"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def run_git_command(cmd: List[str], cwd: Optional[str] = None) -> Optional[str]:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def get_repo_root(path: str) -> str:
    """Find git repo root from given path."""
    result = run_git_command(["git", "rev-parse", "--show-toplevel"], cwd=path)
    return result if result else path


def is_git_repo(path: str) -> bool:
    """Check if path is inside a git repository."""
    return run_git_command(["git", "rev-parse", "--git-dir"], cwd=path) is not None


def count_files(path: str) -> int:
    """Count total files in directory (excluding hidden and common ignore patterns)."""
    count = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in [
                "node_modules",
                "venv",
                "__pycache__",
                "dist",
                "build",
                "target",
                ".git",
            ]
        ]
        count += len(files)
    return count


def estimate_tokens(text: str) -> int:
    """Rough token estimation: ~4 chars per token."""
    return len(text) // 4


def calculate_age_days(mtime: float) -> int:
    """Calculate age in days from modification time."""
    return (datetime.now() - datetime.fromtimestamp(mtime)).days


# =============================================================================
# CONFIDENCE SCORING
# =============================================================================


def calculate_confidence(
    file_info: Dict,
    matches_pattern: bool = False,
    is_ai_artifact: bool = False,
    is_duplicate: bool = False,
    is_imported: bool = False,
    age_days: int = 0,
) -> int:
    """
    Calculate confidence score for deletion recommendation.

    Returns 0-100 where:
    - 80-100: High confidence (Quick Wins)
    - 50-79: Medium confidence (Decisions Needed)
    - 0-49: Low confidence (Keep or Investigate)
    """
    score = 50  # Base score

    # Positive signals (increase confidence to delete)
    if matches_pattern:
        score += 20
    if is_ai_artifact:
        score += 15
    if is_duplicate:
        score += 15
    if age_days > 180:
        score += 15
    elif age_days > 90:
        score += 10
    elif age_days > 60:
        score += 5

    # Negative signals (decrease confidence)
    if age_days < 14:
        score -= 35  # Recently modified = probably needed
    elif age_days < 30:
        score -= 20
    if is_imported:
        score -= 40  # Referenced elsewhere = definitely needed

    return max(0, min(100, score))


# =============================================================================
# CATEGORY 1: DEAD FILES ANALYSIS
# =============================================================================


def find_dead_files(repo_path: str) -> List[Dict]:
    """Find files matching dead/stale patterns (Category 1: Clothing)."""
    dead_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]

        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, repo_path)

            matched_pattern = None
            is_ai_artifact = False

            # Check AI tool artifacts first
            for pattern in AI_TOOL_ARTIFACTS:
                if re.match(pattern, file, re.IGNORECASE):
                    matched_pattern = pattern
                    is_ai_artifact = True
                    break

            # Check dead file patterns
            if not matched_pattern:
                for pattern in DEAD_FILE_PATTERNS:
                    if re.match(pattern, file, re.IGNORECASE):
                        matched_pattern = pattern
                        break

            if matched_pattern:
                try:
                    stat = os.stat(filepath)
                    age_days = calculate_age_days(stat.st_mtime)

                    confidence = calculate_confidence(
                        {"path": rel_path},
                        matches_pattern=True,
                        is_ai_artifact=is_ai_artifact,
                        age_days=age_days,
                    )

                    dead_files.append(
                        {
                            "path": rel_path,
                            "pattern": matched_pattern,
                            "size_bytes": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).strftime(
                                "%Y-%m-%d"
                            ),
                            "age_days": age_days,
                            "confidence": confidence,
                            "is_ai_artifact": is_ai_artifact,
                            "category": "dead_files",
                            "category_name": "Dead Files (Clothing)",
                            "gratitude": generate_gratitude(
                                "dead_file", rel_path, age_days
                            ),
                        }
                    )
                except OSError:
                    continue

    return sorted(dead_files, key=lambda x: x["confidence"], reverse=True)


def find_duplicates(repo_path: str) -> List[Dict]:
    """Find files with similar names suggesting duplicates."""
    files_by_stem = defaultdict(list)

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]

        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, repo_path)

            # Normalize filename to find potential duplicates
            stem = Path(file).stem.lower()
            ext = Path(file).suffix.lower()

            # Remove common suffixes
            for suffix in [
                "_old",
                "_backup",
                "_copy",
                "_new",
                "_v1",
                "_v2",
                "_v3",
                "_final",
                "_draft",
                "_bak",
                " copy",
                " (1)",
                " (2)",
            ]:
                stem = stem.replace(suffix, "")

            # Group by normalized stem + extension
            files_by_stem[(stem, ext)].append(rel_path)

    duplicates = []
    for (stem, ext), paths in files_by_stem.items():
        if len(paths) > 1:
            duplicates.append(
                {
                    "base_name": f"{stem}{ext}",
                    "files": sorted(paths),
                    "count": len(paths),
                    "category": "dead_files",
                    "category_name": "Dead Files (Clothing)",
                    "confidence": 70,  # Duplicates are usually safe to consolidate
                    "reason": "potential_duplicates",
                    "gratitude": generate_gratitude("duplicate", stem, 0),
                }
            )

    return sorted(
        [d for d in duplicates if d["count"] > 1],
        key=lambda x: x["count"],
        reverse=True,
    )[:20]


# =============================================================================
# CATEGORY 2: DEPENDENCIES ANALYSIS
# =============================================================================


def detect_ecosystems(repo_path: str) -> Dict[str, List[str]]:
    """Detect which ecosystems are present in the repo."""
    detected = {}

    for ecosystem, markers in ECOSYSTEM_MARKERS.items():
        found_markers = []
        for marker in markers:
            # Check root
            if os.path.exists(os.path.join(repo_path, marker)):
                found_markers.append(marker)
            # Check subdirectories for monorepos
            for root, dirs, files in os.walk(repo_path):
                dirs[:] = [
                    d
                    for d in dirs
                    if not d.startswith(".")
                    and d
                    not in [
                        "node_modules",
                        "venv",
                        "__pycache__",
                        "dist",
                        "build",
                        "target",
                    ]
                ]
                if marker in files:
                    rel_path = os.path.relpath(os.path.join(root, marker), repo_path)
                    if rel_path not in found_markers:
                        found_markers.append(rel_path)

        if found_markers:
            detected[ecosystem] = found_markers

    return detected


def find_orphaned_python_deps(repo_path: str) -> List[Dict]:
    """Find Python packages in requirements that are never imported."""
    orphans = []

    # Find all imports in Python files
    all_imports = set()
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    all_imports.add(alias.name.split(".")[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    all_imports.add(node.module.split(".")[0])
                    except SyntaxError:
                        # Fallback to regex for files with syntax errors
                        imports = re.findall(
                            r"^(?:from|import)\s+(\w+)", content, re.MULTILINE
                        )
                        all_imports.update(imports)
                except (IOError, OSError):
                    continue

    # Parse requirements files
    for req_file in [
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
    ]:
        req_path = os.path.join(repo_path, req_file)
        if os.path.exists(req_path):
            try:
                with open(req_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if (
                            line
                            and not line.startswith("#")
                            and not line.startswith("-")
                        ):
                            # Extract package name (before ==, >=, etc.)
                            pkg = re.split(r"[=<>!~\[\]]", line)[0].strip()
                            # Normalize package name (- to _)
                            pkg_normalized = pkg.replace("-", "_").lower()

                            # Check if imported (accounting for name differences)
                            imported = any(
                                imp.lower() == pkg_normalized
                                or imp.lower() == pkg.lower()
                                or imp.lower().replace("-", "_") == pkg_normalized
                                for imp in all_imports
                            )

                            if not imported and pkg:
                                orphans.append(
                                    {
                                        "package": pkg,
                                        "source": req_file,
                                        "ecosystem": "python",
                                        "category": "dependencies",
                                        "category_name": "Dependencies (Books)",
                                        "confidence": 65,
                                        "reason": "package_not_imported",
                                        "gratitude": generate_gratitude(
                                            "dependency", pkg, 0
                                        ),
                                    }
                                )
            except (IOError, OSError):
                continue

    return orphans


def find_orphaned_js_deps(repo_path: str) -> List[Dict]:
    """Find npm packages in package.json that are never imported."""
    orphans = []

    package_json_path = os.path.join(repo_path, "package.json")
    if not os.path.exists(package_json_path):
        return orphans

    try:
        with open(package_json_path, "r", encoding="utf-8") as f:
            pkg_data = json.load(f)
    except (IOError, json.JSONDecodeError):
        return orphans

    # Collect all declared dependencies
    declared_deps = set()
    for dep_type in ["dependencies", "devDependencies", "peerDependencies"]:
        if dep_type in pkg_data:
            declared_deps.update(pkg_data[dep_type].keys())

    # Find all imports in JS/TS files
    all_imports = set()
    import_patterns = [
        r'require\([\'"]([^\'"\./][^\'"]*?)[\'"]\)',  # require('package')
        r'from\s+[\'"]([^\'"\./][^\'"]*?)[\'"]',  # from 'package'
        r'import\s+[\'"]([^\'"\./][^\'"]*?)[\'"]',  # import 'package'
    ]

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]

        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for pattern in import_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # Get base package name (e.g., @scope/package or package)
                            if match.startswith("@"):
                                parts = match.split("/")
                                if len(parts) >= 2:
                                    all_imports.add("/".join(parts[:2]))
                            else:
                                all_imports.add(match.split("/")[0])
                except (IOError, OSError):
                    continue

    # Find orphaned packages
    for pkg in declared_deps:
        if pkg not in all_imports:
            orphans.append(
                {
                    "package": pkg,
                    "source": "package.json",
                    "ecosystem": "javascript",
                    "category": "dependencies",
                    "category_name": "Dependencies (Books)",
                    "confidence": 60,  # Lower confidence - build tools often not directly imported
                    "reason": "package_not_imported",
                    "gratitude": generate_gratitude("dependency", pkg, 0),
                }
            )

    return orphans


def find_orphaned_go_deps(repo_path: str) -> List[Dict]:
    """Find Go modules in go.mod that are never imported."""
    orphans = []

    go_mod_path = os.path.join(repo_path, "go.mod")
    if not os.path.exists(go_mod_path):
        return orphans

    # Parse go.mod for requires
    declared_deps = set()
    try:
        with open(go_mod_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Match require blocks and single requires
        requires = re.findall(r"require\s+(\S+)\s+v", content)
        requires.extend(re.findall(r"^\s+(\S+)\s+v", content, re.MULTILINE))
        declared_deps.update(requires)
    except (IOError, OSError):
        return orphans

    # Find all imports in Go files
    all_imports = set()
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["vendor", ".git", "node_modules"]
        ]

        for file in files:
            if file.endswith(".go"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    imports = re.findall(
                        r'import\s+(?:\(\s*)?["\']([^"\']+)["\']', content
                    )
                    imports.extend(
                        re.findall(r'^\s+["\']([^"\']+)["\']', content, re.MULTILINE)
                    )
                    all_imports.update(imports)
                except (IOError, OSError):
                    continue

    # Find orphaned modules
    for mod in declared_deps:
        if not any(imp.startswith(mod) or mod in imp for imp in all_imports):
            orphans.append(
                {
                    "package": mod,
                    "source": "go.mod",
                    "ecosystem": "go",
                    "category": "dependencies",
                    "category_name": "Dependencies (Books)",
                    "confidence": 65,
                    "reason": "module_not_imported",
                    "gratitude": generate_gratitude("dependency", mod, 0),
                }
            )

    return orphans


def find_orphaned_rust_deps(repo_path: str) -> List[Dict]:
    """Find Rust crates in Cargo.toml that are never used."""
    orphans = []

    cargo_path = os.path.join(repo_path, "Cargo.toml")
    if not os.path.exists(cargo_path):
        return orphans

    # Parse Cargo.toml for dependencies
    declared_deps = set()
    try:
        with open(cargo_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Simple TOML parsing for dependencies
        in_deps = False
        for line in content.split("\n"):
            if re.match(r"\[(.*dependencies.*)\]", line):
                in_deps = True
                continue
            if line.startswith("[") and in_deps:
                in_deps = False
            if in_deps and "=" in line:
                crate = line.split("=")[0].strip()
                if crate and not crate.startswith("#"):
                    declared_deps.add(crate)
    except (IOError, OSError):
        return orphans

    # Find all uses in Rust files
    all_uses = set()
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["target", "node_modules"]
        ]

        for file in files:
            if file.endswith(".rs"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    # Match use statements and extern crate
                    uses = re.findall(r"use\s+(\w+)", content)
                    uses.extend(re.findall(r"extern\s+crate\s+(\w+)", content))
                    # Also check for crate:: references
                    uses.extend(re.findall(r"(\w+)::", content))
                    all_uses.update(uses)
                except (IOError, OSError):
                    continue

    # Find orphaned crates
    for crate in declared_deps:
        # Normalize crate name (- to _)
        crate_normalized = crate.replace("-", "_")
        if crate_normalized not in all_uses and crate not in all_uses:
            orphans.append(
                {
                    "package": crate,
                    "source": "Cargo.toml",
                    "ecosystem": "rust",
                    "category": "dependencies",
                    "category_name": "Dependencies (Books)",
                    "confidence": 65,
                    "reason": "crate_not_used",
                    "gratitude": generate_gratitude("dependency", crate, 0),
                }
            )

    return orphans


def find_all_orphaned_deps(repo_path: str) -> List[Dict]:
    """Find orphaned dependencies across all detected ecosystems."""
    ecosystems = detect_ecosystems(repo_path)
    all_orphans = []

    if "python" in ecosystems:
        all_orphans.extend(find_orphaned_python_deps(repo_path))
    if "javascript" in ecosystems:
        all_orphans.extend(find_orphaned_js_deps(repo_path))
    if "go" in ecosystems:
        all_orphans.extend(find_orphaned_go_deps(repo_path))
    if "rust" in ecosystems:
        all_orphans.extend(find_orphaned_rust_deps(repo_path))

    return all_orphans


# =============================================================================
# CATEGORY 3: DOCUMENTATION ANALYSIS
# =============================================================================


def find_documentation_drift(repo_path: str) -> List[Dict]:
    """Find documentation that references non-existent files or functions."""
    drift_issues = []

    # Collect all existing file paths
    existing_files = set()
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), repo_path)
            existing_files.add(rel_path)
            existing_files.add(os.path.basename(file))

    # Find markdown files
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d not in ["node_modules", "venv", "__pycache__", "dist", "build"]
        ]

        for file in files:
            if file.endswith((".md", ".rst", ".txt")) and not file.startswith("."):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, repo_path)

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    broken_refs = []

                    # Check markdown links to local files
                    # Pattern: [text](path) or [text](./path)
                    md_links = re.findall(
                        r"\[([^\]]+)\]\((?:\./)?([^)#]+?)(?:#[^)]*)?\)", content
                    )
                    for link_text, link_path in md_links:
                        if not link_path.startswith(("http://", "https://", "mailto:")):
                            # Resolve relative path
                            doc_dir = os.path.dirname(filepath)
                            full_path = os.path.normpath(
                                os.path.join(doc_dir, link_path)
                            )
                            rel_to_repo = os.path.relpath(full_path, repo_path)

                            if (
                                not os.path.exists(full_path)
                                and rel_to_repo not in existing_files
                            ):
                                broken_refs.append(
                                    {
                                        "type": "broken_link",
                                        "reference": link_path,
                                        "link_text": link_text,
                                    }
                                )

                    # Check code block references (```filename or <!-- include: file -->)
                    code_refs = re.findall(r"```(\w+\.\w+)", content)
                    for ref in code_refs:
                        if ref not in existing_files:
                            broken_refs.append(
                                {"type": "code_block_file", "reference": ref}
                            )

                    if broken_refs:
                        stat = os.stat(filepath)
                        drift_issues.append(
                            {
                                "path": rel_path,
                                "broken_references": broken_refs[:5],  # Limit to 5
                                "broken_count": len(broken_refs),
                                "modified": datetime.fromtimestamp(
                                    stat.st_mtime
                                ).strftime("%Y-%m-%d"),
                                "category": "documentation",
                                "category_name": "Documentation (Papers)",
                                "confidence": min(40 + len(broken_refs) * 10, 80),
                                "reason": "documentation_drift",
                                "gratitude": generate_gratitude(
                                    "documentation", rel_path, 0
                                ),
                            }
                        )
                except (IOError, OSError):
                    continue

    return drift_issues


# =============================================================================
# CATEGORY 4: CONFIGURATION & TOOLING (Komono)
# =============================================================================


def find_orphaned_configs(repo_path: str) -> List[Dict]:
    """Find configuration files that may be orphaned or outdated."""
    orphans = []

    config_patterns = [
        # Build tool configs without corresponding tools
        (r"\.babelrc$", "babel", ["package.json"]),
        (r"webpack\.config\.js$", "webpack", ["package.json"]),
        (r"rollup\.config\.js$", "rollup", ["package.json"]),
        (r"jest\.config\.(js|ts|json)$", "jest", ["package.json"]),
        (r"\.eslintrc.*$", "eslint", ["package.json"]),
        (r"\.prettierrc.*$", "prettier", ["package.json"]),
        (r"tsconfig.*\.json$", "typescript", ["package.json"]),
        # Python configs
        (r"setup\.cfg$", "setuptools", ["setup.py", "pyproject.toml"]),
        (r"\.pylintrc$", "pylint", ["requirements.txt", "pyproject.toml"]),
        (r"\.flake8$", "flake8", ["requirements.txt", "pyproject.toml"]),
        (r"mypy\.ini$", "mypy", ["requirements.txt", "pyproject.toml"]),
        # CI/CD configs (check if referenced tools exist)
        (r"\.travis\.yml$", "travis", []),
        (r"\.circleci/config\.yml$", "circleci", []),
        (r"Jenkinsfile$", "jenkins", []),
    ]

    # Get list of installed packages if package.json exists
    installed_packages = set()
    pkg_json_path = os.path.join(repo_path, "package.json")
    if os.path.exists(pkg_json_path):
        try:
            with open(pkg_json_path, "r") as f:
                pkg = json.load(f)
            for dep_type in ["dependencies", "devDependencies"]:
                if dep_type in pkg:
                    installed_packages.update(pkg[dep_type].keys())
        except (IOError, json.JSONDecodeError):
            pass

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]

        for file in files:
            for pattern, tool_name, dep_files in config_patterns:
                if re.match(pattern, file):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, repo_path)

                    # Check if tool is installed
                    tool_installed = tool_name in installed_packages

                    # Check if any dependency files exist
                    has_dep_files = any(
                        os.path.exists(os.path.join(repo_path, df)) for df in dep_files
                    )

                    if not tool_installed and not has_dep_files and dep_files:
                        try:
                            stat = os.stat(filepath)
                            age_days = calculate_age_days(stat.st_mtime)

                            orphans.append(
                                {
                                    "path": rel_path,
                                    "tool": tool_name,
                                    "age_days": age_days,
                                    "category": "configuration",
                                    "category_name": "Configuration (Komono)",
                                    "confidence": 55 + (15 if age_days > 90 else 0),
                                    "reason": "orphaned_config",
                                    "gratitude": generate_gratitude(
                                        "config", tool_name, age_days
                                    ),
                                }
                            )
                        except OSError:
                            continue

    return orphans


# =============================================================================
# CATEGORY 5: LEGACY CODE (Sentimental)
# =============================================================================


def find_legacy_code(repo_path: str) -> List[Dict]:
    """Find potentially legacy code that needs human judgment."""
    legacy_items = []

    # Look for deprecation markers (must be in actual comments, not strings)
    # Pattern: comment character followed by optional whitespace, then marker
    # More specific patterns to avoid false positives from regex patterns and section headers
    comment_deprecation_patterns = [
        (r"@\s*deprecated", "python"),
        (r"//.*@\s*deprecated", "js"),
        (r"/\*.*@\s*deprecated.*\*/", "js"),
        (r"#\s*DEPRECATED[:\s]", "python"),
        (r"//\s*DEPRECATED[:\s]", "js"),
        (r"/\*\s*DEPRECATED[:\s].*\*/", "js"),
        (r"#\s*LEGACY[:\s]", "python"),
        (r"//\s*LEGACY[:\s]", "js"),
        (r"TODO[:\s].*remove", "python"),
        (r"FIXME[:\s].*remove", "python"),
    ]

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]

        for file in files:
            if file.endswith(
                (".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java")
            ):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, repo_path)

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    deprecation_markers = []
                    for pattern, lang in comment_deprecation_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            deprecation_markers.extend(matches[:3])

                    if deprecation_markers:
                        stat = os.stat(filepath)
                        age_days = calculate_age_days(stat.st_mtime)

                        legacy_items.append(
                            {
                                "path": rel_path,
                                "markers": list(set(deprecation_markers))[:5],
                                "marker_count": len(deprecation_markers),
                                "age_days": age_days,
                                "category": "legacy",
                                "category_name": "Legacy Code (Sentimental)",
                                "confidence": 40,  # Low confidence - needs human review
                                "reason": "contains_deprecation_markers",
                                "gratitude": generate_gratitude(
                                    "legacy", rel_path, age_days
                                ),
                            }
                        )
                except (IOError, OSError):
                    continue

    return sorted(legacy_items, key=lambda x: x["marker_count"], reverse=True)[:15]


# =============================================================================
# GIT ARCHAEOLOGY
# =============================================================================


def analyze_commits(repo_path: str, days: int = 90) -> Dict:
    """Analyze recent commits for AI-generated patterns."""
    if not is_git_repo(repo_path):
        return {"has_git": False, "ai_commits": [], "ai_signed_commits": []}

    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Get commit log with full message
    log_output = run_git_command(
        [
            "git",
            "log",
            f"--since={since_date}",
            "--pretty=format:%H|%s|%ai|%an|%b<<<END>>>",
        ],
        cwd=repo_path,
    )

    if not log_output:
        return {
            "has_git": True,
            "ai_commits": [],
            "ai_signed_commits": [],
            "total_commits": 0,
        }

    ai_commits = []
    ai_signed_commits = []
    total_commits = 0

    for entry in log_output.split("<<<END>>>"):
        entry = entry.strip()
        if not entry:
            continue

        parts = entry.split("|", 4)
        if len(parts) < 4:
            continue

        total_commits += 1
        commit_hash, subject, date, author = parts[0], parts[1], parts[2], parts[3]
        body = parts[4] if len(parts) > 4 else ""
        full_message = subject + "\n" + body

        # Check for AI tool signatures
        if any(signature in full_message for signature in AI_COMMIT_SIGNATURES):
            ai_signed_commits.append(
                {
                    "hash": commit_hash[:8],
                    "message": subject[:100],
                    "date": date[:10],
                    "author": author,
                    "is_ai_signed": True,
                }
            )
            continue

        # Check for AI patterns
        ai_score = 0
        matched_patterns = []
        for pattern in AI_COMMIT_PATTERNS:
            if re.search(pattern, subject, re.IGNORECASE):
                ai_score += 1
                matched_patterns.append(pattern)

        if ai_score >= 2:  # Require multiple pattern matches
            ai_commits.append(
                {
                    "hash": commit_hash[:8],
                    "message": subject[:100],
                    "date": date[:10],
                    "author": author,
                    "ai_score": ai_score,
                    "patterns": matched_patterns[:3],
                }
            )

    return {
        "has_git": True,
        "total_commits": total_commits,
        "ai_signed_commits": ai_signed_commits[:10],
        "ai_signed_commit_count": len(ai_signed_commits),
        "ai_commits": sorted(ai_commits, key=lambda x: x["ai_score"], reverse=True)[
            :10
        ],
        "ai_commit_count": len(ai_commits),
        "ai_commit_ratio": len(ai_commits) / max(total_commits, 1),
    }


def find_stale_branches(repo_path: str) -> List[Dict]:
    """Find branches that may be stale or experimental."""
    if not is_git_repo(repo_path):
        return []

    stale_patterns = [
        r"^claude-",
        r"^cursor-",
        r"^copilot-",
        r"^codex-",
        r"^attempt-",
        r"^test-",
        r"^wip-",
        r"^experimental-",
        r"^try-",
        r"^debug-",
        r"^feature/wip-",
        r"^hotfix-\d{8}",  # Old dated hotfixes
    ]

    branches_output = run_git_command(["git", "branch", "-a"], cwd=repo_path)
    if not branches_output:
        return []

    stale_branches = []
    for branch in branches_output.split("\n"):
        branch = branch.strip().lstrip("* ").replace("remotes/origin/", "")

        for pattern in stale_patterns:
            if re.match(pattern, branch, re.IGNORECASE):
                stale_branches.append(
                    {
                        "name": branch,
                        "pattern": pattern,
                        "reason": "matches_stale_pattern",
                    }
                )
                break

    return stale_branches[:20]


# =============================================================================
# CONTEXT-HEAVY FILES
# =============================================================================


def find_context_heavy_files(repo_path: str) -> List[Dict]:
    """Find files that may bloat an AI assistant's context window."""
    heavy_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d
            not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
        ]

        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in CONTEXT_HEAVY_EXTENSIONS:
                continue

            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, repo_path)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                lines = content.count("\n") + 1
                tokens = estimate_tokens(content)

                if lines > MAX_RECOMMENDED_LINES or tokens > MAX_RECOMMENDED_TOKENS:
                    heavy_files.append(
                        {
                            "path": rel_path,
                            "lines": lines,
                            "estimated_tokens": tokens,
                            "exceeds_lines": lines > MAX_RECOMMENDED_LINES,
                            "exceeds_tokens": tokens > MAX_RECOMMENDED_TOKENS,
                            "recommendation": "consider_splitting"
                            if lines > 1000
                            else "monitor",
                            "category": "context_heavy",
                            "confidence": 50,  # Not deletions, just recommendations
                        }
                    )
            except (IOError, OSError):
                continue

    return sorted(heavy_files, key=lambda x: x["estimated_tokens"], reverse=True)[:15]


# =============================================================================
# GRATITUDE GENERATION
# =============================================================================


def generate_gratitude(item_type: str, identifier: str, age_days: int) -> str:
    """Generate a gratitude message for a file/item in KonMari spirit."""
    templates = {
        "dead_file": [
            f"Thank you, {identifier}, for being part of this project's journey.",
            f"Thank you for the work you represented. Your purpose has been fulfilled.",
            f"Gratitude for {identifier} - you served your purpose during development.",
        ],
        "duplicate": [
            f"Thank you for preserving a backup of {identifier}. That safety is no longer needed.",
            f"Gratitude for being a safety net. Version control now provides this security.",
        ],
        "dependency": [
            f"Thank you, {identifier}, for the capability you offered, even if unused.",
            f"Gratitude for {identifier} - you taught us about available tools.",
        ],
        "documentation": [
            f"Thank you, documentation, for attempting to guide future developers.",
            f"Gratitude for documenting past understanding, even as the code evolved.",
        ],
        "config": [
            f"Thank you, {identifier} configuration, for the tooling you once enabled.",
            f"Gratitude for the development environment you helped create.",
        ],
        "legacy": [
            f"Deep gratitude to this code for getting the project to where it is today.",
            f"Thank you for the foundation you provided. Your lessons remain even as you go.",
        ],
    }

    import random

    choices = templates.get(item_type, [f"Thank you, {identifier}, for your service."])
    return random.choice(choices)


# =============================================================================
# MONOREPO DETECTION
# =============================================================================


def detect_monorepo(repo_path: str) -> Dict:
    """Detect if this is a monorepo and identify packages."""
    monorepo_markers = {
        "lerna": "lerna.json",
        "pnpm": "pnpm-workspace.yaml",
        "nx": "nx.json",
        "turborepo": "turbo.json",
        "yarn_workspaces": "package.json",  # Check for workspaces field
        "rush": "rush.json",
    }

    detected = None
    packages = []

    for tool, marker in monorepo_markers.items():
        marker_path = os.path.join(repo_path, marker)
        if os.path.exists(marker_path):
            if tool == "yarn_workspaces":
                try:
                    with open(marker_path, "r") as f:
                        pkg = json.load(f)
                    if "workspaces" in pkg:
                        detected = "yarn_workspaces"
                        # Find workspace packages
                        workspaces = pkg["workspaces"]
                        if isinstance(workspaces, dict):
                            workspaces = workspaces.get("packages", [])
                        for ws in workspaces:
                            # Expand glob patterns
                            import glob

                            for match in glob.glob(os.path.join(repo_path, ws)):
                                if os.path.isdir(match):
                                    packages.append(os.path.relpath(match, repo_path))
                except (IOError, json.JSONDecodeError):
                    pass
            else:
                detected = tool

    # Count package.json files as a heuristic
    pkg_count = 0
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in ["node_modules", ".git"]]
        if "package.json" in files:
            pkg_count += 1

    return {
        "is_monorepo": detected is not None or pkg_count > 3,
        "tool": detected,
        "packages": packages[:20],
        "package_json_count": pkg_count,
    }


# =============================================================================
# CELEBRATION FOR CLEAN REPOS
# =============================================================================


def check_cleanliness(summary: Dict) -> Dict:
    """Check if repo is already clean and generate celebration if so."""
    issues = (
        summary.get("dead_files", 0)
        + summary.get("duplicates", 0)
        + summary.get("orphaned_dependencies", 0)
        + summary.get("documentation_drift", 0)
        + summary.get("orphaned_configs", 0)
    )

    if issues == 0:
        return {
            "is_clean": True,
            "message": "Your repository already sparks joy!",
            "details": [
                "No stale backup files detected",
                "Dependencies appear actively used",
                "Documentation references look current",
                "No orphaned configurations found",
            ],
            "celebration": "You've reached your click point. Enjoy the clarity!",
        }
    elif issues < 5:
        return {
            "is_clean": False,
            "nearly_clean": True,
            "message": "Your repository is well-maintained with only minor tidying needed.",
            "issues_count": issues,
        }
    else:
        return {
            "is_clean": False,
            "nearly_clean": False,
            "message": f"Found {issues} items that may benefit from the KonMari treatment.",
            "issues_count": issues,
        }


# =============================================================================
# MAIN ANALYSIS
# =============================================================================


def analyze_repo(path: str = ".", sample_mode: bool = False) -> Dict[str, Any]:
    """
    Main analysis function following KonMari sacred order.

    Categories:
    1. Dead Files (Clothing) - easiest wins
    2. Dependencies (Books) - clear utility
    3. Documentation (Papers) - context awareness
    4. Configuration (Komono) - scattered items
    5. Legacy (Sentimental) - hardest decisions
    """
    repo_path = get_repo_root(os.path.abspath(path))

    # Check repo size for sampling
    file_count = count_files(repo_path)
    is_large_repo = file_count > 10000

    if is_large_repo and not sample_mode:
        sample_mode = True

    # Detect monorepo
    monorepo_info = detect_monorepo(repo_path)

    # Detect ecosystems
    ecosystems = detect_ecosystems(repo_path)

    # Category 1: Dead Files (Clothing)
    dead_files = find_dead_files(repo_path)
    duplicates = find_duplicates(repo_path)

    # Category 2: Dependencies (Books)
    orphaned_deps = find_all_orphaned_deps(repo_path)

    # Category 3: Documentation (Papers)
    doc_drift = find_documentation_drift(repo_path)

    # Category 4: Configuration (Komono)
    orphaned_configs = find_orphaned_configs(repo_path)

    # Category 5: Legacy (Sentimental)
    legacy_code = find_legacy_code(repo_path)

    # Git archaeology
    commit_analysis = analyze_commits(repo_path)
    stale_branches = find_stale_branches(repo_path)

    # Context-heavy files (for awareness, not deletion)
    context_heavy = find_context_heavy_files(repo_path)

    # Build analysis result
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "repo_path": repo_path,
        "file_count": file_count,
        "is_large_repo": is_large_repo,
        "sample_mode": sample_mode,
        "has_git": commit_analysis.get("has_git", False),
        "monorepo": monorepo_info,
        "ecosystems": ecosystems,
        # KonMari Categories
        "categories": {
            "1_dead_files": {
                "name": "Dead Files (Clothing)",
                "description": "Backup files, temp files, duplicates - easiest wins",
                "items": dead_files,
                "duplicates": duplicates,
                "count": len(dead_files) + len(duplicates),
            },
            "2_dependencies": {
                "name": "Dependencies (Books)",
                "description": "Unused packages and orphaned imports",
                "items": orphaned_deps,
                "count": len(orphaned_deps),
            },
            "3_documentation": {
                "name": "Documentation (Papers)",
                "description": "Outdated docs with broken references",
                "items": doc_drift,
                "count": len(doc_drift),
            },
            "4_configuration": {
                "name": "Configuration (Komono)",
                "description": "Orphaned config files and unused tooling",
                "items": orphaned_configs,
                "count": len(orphaned_configs),
            },
            "5_legacy": {
                "name": "Legacy Code (Sentimental)",
                "description": "Deprecated code needing human judgment",
                "items": legacy_code,
                "count": len(legacy_code),
            },
        },
        # Git archaeology
        "git_archaeology": {**commit_analysis, "stale_branches": stale_branches},
        # Context awareness
        "context_heavy_files": context_heavy,
        # Summary
        "summary": {
            "dead_files": len(dead_files),
            "duplicates": len(duplicates),
            "orphaned_dependencies": len(orphaned_deps),
            "documentation_drift": len(doc_drift),
            "orphaned_configs": len(orphaned_configs),
            "legacy_markers": len(legacy_code),
            "context_heavy": len(context_heavy),
            "total_issues": (
                len(dead_files)
                + len(duplicates)
                + len(orphaned_deps)
                + len(doc_drift)
                + len(orphaned_configs)
                + len(legacy_code)
            ),
        },
        # Quick wins vs decisions needed
        "quick_wins": [
            item
            for category in [
                "1_dead_files",
                "2_dependencies",
                "3_documentation",
                "4_configuration",
            ]
            for item in (
                analysis.get("categories", {}).get(category, {}).get("items", [])
                if "analysis" in dir()
                else []
            )
            if item.get("confidence", 0) >= 80
        ],
        # Cleanliness check
        "cleanliness": None,  # Will be filled after full analysis
    }

    # Recalculate quick wins with actual data
    all_items = dead_files + duplicates + orphaned_deps + doc_drift + orphaned_configs
    analysis["quick_wins"] = [
        item for item in all_items if item.get("confidence", 0) >= 80
    ]
    analysis["decisions_needed"] = [
        item for item in all_items + legacy_code if 50 <= item.get("confidence", 0) < 80
    ]

    # Check cleanliness
    analysis["cleanliness"] = check_cleanliness(analysis["summary"])

    return analysis


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = analyze_repo(path)
    print(json.dumps(result, indent=2, default=str))
