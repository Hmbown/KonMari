# KonMari Repository Decluttering Skill

*"The question of what code to keep is the question of how you want to develop."*

A repository cleanup ceremony inspired by Marie Kondo's KonMari Method for AI-assisted development. Not just cleanup - transformation.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Maintained](https://img.shields.io/badge/maintained-active-green.svg)](https://github.com/Hmbown/KonMari)

## What is KonMari?

KonMari is a skill that performs end-of-session closeout rituals for development workflows. It analyzes repositories following a sacred order to help you identify files, dependencies, and code that no longer spark clarity.

### The Core Philosophy

1. **Tidy by Category, Not by Folder** - Follow a deliberate order (Clothing → Books → Papers → Komono → Sentimental)
2. **Ask: Does This Spark Clarity?** - Evaluate each item with a clear question in mind
3. **Express Gratitude** - Thank code for its service before letting go
4. **Reach Your Click Point** - The moment when your codebase feels "right"

## Quick Start

### Prerequisites
- Python 3.7 or higher
- A git repository (optional but recommended for full analysis)

### Installation (Pick One)

#### For Skill-Based AI Assistants

If you already have `konmari.skill`, just copy it into your assistant’s skills folder and refresh.

If you do not have `konmari.skill`, download it from the GitHub Releases assets or build it from the repo.

Note: `konmari.skill` is generated from `skill_package/` and may not be committed in the repo.

#### Common Skills Folders

Use the folder that matches your tool:
- Claude Code / Cursor: `~/.claude/skills/`
- Codex CLI: `$CODEX_HOME/skills` (default is `~/.codex/skills/`)
- Other assistants: use their skills directory and copy `konmari.skill` there

#### If You Cloned the Repo

The repo includes helper scripts to build and install:

```bash
./scripts/install_skill.sh
make install
```

These scripts live in the repository, not inside the `.skill` bundle.

#### For Claude Code / Cursor Users (Manual)

1. Download the `konmari.skill` file from this repository
2. Install it in your Claude Code skills directory:
   ```
   ~/.claude/skills/konmari.skill
   ```
3. Restart your IDE or refresh your skill list

#### Manual Installation

1. Clone this repository
2. Ensure `analyze_repo.py` is executable
3. Add the script to your PATH or run directly:
   ```bash
   python3 /path/to/analyze_repo.py /path/to/repo
   ```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

### Compatibility Notes

- Works with any AI assistant that can load `.skill` bundles or execute the analyzer script.
- If your AI tool does not support scripts, you can still use the workflow in `SKILL.md` and manually gather the repo facts.
- Expand AI artifact detection by editing `AI_TOOL_ARTIFACTS` and `AI_COMMIT_SIGNATURES` in `analyze_repo.py`.

### FAQ

**Where is `konmari.skill`?**
- It is generated from `skill_package/` and may not be committed.
- Download it from the GitHub Releases assets, or build it locally from the repo.

## Usage

### Trigger the Skill

In your AI assistant, use any of these commands to start the KonMari ceremony:

- `clean up this repo`
- `what files can I delete`
- `reduce context bloat`
- `find stale files`
- `what doesn't spark joy`
- `wrap up`
- `done for today`
- `close out session`
- `end of task`
- `tidy up`
- `declutter`
- `/konmari`

### What to Expect

The skill will:

1. **Ask Your Vision** - What does your ideal codebase look like? Are there any files that must stay?

2. **Analyze Categories in Sacred Order**
   - **Category 1: Dead Files (Clothing)** - Backups, temps, duplicates
   - **Category 2: Dependencies (Books)** - Unused packages, orphaned imports
   - **Category 3: Documentation (Papers)** - Outdated docs with broken references
   - **Category 4: Configuration (Komono)** - Orphaned configs, debug artifacts
   - **Category 5: Legacy Code (Sentimental)** - Deprecated code needing judgment

3. **Generate a Cleanup Proposal** - Creates `CLEANUP_PROPOSAL.md` with:
   - Quick Wins (confidence ≥80%)
   - Decisions Needed (confidence 50-79%)
   - Gratitude messages for each item
   - Celebration if already clean

4. **Walk Through with You** - Presents each recommendation and asks for approval
5. **Express Gratitude** - Reads gratitude messages before deletion
6. **Celebrate Your Click Point** - Acknowledges when you reach completion

## Example Experience

```
You: "clean up this repo"

AI: I'm ready to transform this repository.
    What does your ideal codebase look like?
    Are there any files that must stay regardless of what we find?

[Analyzes repository...]

AI: Let's begin with Category 1: Dead Files.

    I found 3 backup files that no longer spark clarity:
    - old_utils_backup.py (95% confidence) - 180 days untouched
    - config_copy.json (88% confidence) - Duplicate of config.json
    - temp_debug.py (92% confidence) - Debug script from March

    Before we let these go, let's express gratitude:
    "Thank you, old_utils_backup.py, for the safety you provided
    during refactoring. Version control now serves this purpose. Your work is complete."

    Shall I remove these files?

You: "Yes"

AI: [Removes files with gratitude]
    Three files released. Space recovered: 12.4 KB

    Ready for Category 2: Dependencies...
```

## Supported Ecosystems

KonMari detects and analyzes dependencies for:

- **Python** - requirements.txt, pyproject.toml, setup.py, Pipfile
- **JavaScript/TypeScript** - package.json
- **Go** - go.mod
- **Rust** - Cargo.toml

## Features

### Smart Analysis
- Confidence scoring (0-100) for each recommendation
- AI session artifact detection (expandable)
- Git archaeology (AI-generated commits, stale branches)
- Monorepo support (lerna, pnpm, Nx, Turborepo)
- Context-heavy file detection (>500 lines or >4K tokens)

### Safe Defaults
- Never auto-deletes without approval
- Git history preserves deleted files
- Respects user overrides
- Sacred order is mandatory

### The Gratitude Ritual
Each proposed deletion includes a gratitude message acknowledging the item's service. This psychological closure reduces guilt and honors the code's purpose.

## Documentation

- [SKILL.md](SKILL.md) - Complete documentation with workflow and philosophy
- [INSTALL.md](INSTALL.md) - Detailed installation instructions
- [examples/](examples/) - Sample outputs and usage demos
- [CHANGELOG.md](CHANGELOG.md) - Version history and release notes

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Bug reports
- Feature requests
- Code contributions
- Adding new ecosystem support

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Inspired by Marie Kondo's *The Life-Changing Magic of Tidying Up* and adapted for software development by the community.

---

*"Life truly begins only after you have put your codebase in order."* — Marie Kondo (adapted)
