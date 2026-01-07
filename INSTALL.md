# KonMari Skill Installation Guide

This guide covers installing the KonMari repository decluttering skill for use with any skill-based AI assistant, plus a standalone tool option.

## System Requirements

### Minimum Requirements
- Python 3.7 or higher
- pip (Python package manager)
- 50MB free disk space

### Optional but Recommended
- Git (for full commit history analysis)
- A git repository to analyze

## Installation Methods

### Method 1: Skill-Based AI Assistant (Recommended)

For users of any AI assistant that supports `.skill` bundles:

#### Step 1: Download the Skill File

Download `konmari.skill` from the repository:
- Via GitHub Releases: Download the latest `.skill` file
- Or build from source (see Method 2)

Note: `konmari.skill` is generated from `skill_package/` and may not be committed in the repo.

#### Step 2: Locate Your Skills Directory

Claude Code/Cursor stores skills in:
```
~/.claude/skills/
```

Codex CLI uses:
```
~/.codex/skills/
```

If this directory doesn't exist, create it:
```bash
mkdir -p ~/.claude/skills
```

For Codex CLI:
```bash
mkdir -p ~/.codex/skills
```

#### Step 3: Install the Skill

Copy or move the `.skill` file to the skills directory:
```bash
cp konmari.skill ~/.claude/skills/
```

Or via the IDE:
1. Open your AI assistant's settings
2. Navigate to Skills
3. Add new skill and select `konmari.skill`

#### Step 4: Verify Installation

Restart your IDE or refresh the skill list. In Claude Code/Cursor, try:
```
/konmari help
```

The skill should trigger with documentation.

### Method 2: Build and Install from Source

If you have this repo cloned, the fastest path is:

```bash
./scripts/install_skill.sh
```

This builds `konmari.skill` and installs it into `~/.claude/skills/` by default.
To install elsewhere, pass a directory or full `.skill` path:

```bash
./scripts/install_skill.sh /path/to/skills
./scripts/install_skill.sh /path/to/skills/konmari.skill
```

### Method 3: Standalone Python Script

Use the analyzer directly as a command-line tool.

#### Step 1: Clone or Download

```bash
# Via git
git clone https://github.com/Hmbown/KonMari.git
cd KonMari

# Or download and extract
unzip konmari.skill -d konmari
cd konmari
```

#### Step 2: Verify Python Version

```bash
python3 --version
```

You should see Python 3.7+. If not, install Python 3:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip

# Windows
# Download from https://www.python.org/downloads/
```

#### Step 3: Make Script Executable (Optional)

```bash
chmod +x analyze_repo.py
```

#### Step 4: Add to PATH (Optional)

For system-wide access:
```bash
# Create symlink
sudo ln -s $(pwd)/analyze_repo.py /usr/local/bin/konmari

# Or add to PATH in ~/.bashrc or ~/.zshrc
echo 'export PATH="$PATH:/path/to/konmari"' >> ~/.bashrc
source ~/.bashrc
```

#### Step 5: Run Analysis

```bash
# Analyze current directory
python3 analyze_repo.py

# Analyze specific directory
python3 analyze_repo.py /path/to/repo

# If in PATH
konmari /path/to/repo
```

### Method 4: Install as Python Package

For users who prefer pip installation:

```bash
# From local directory
cd konmari
pip install -e .

# From PyPI (when published)
pip install konmari-skill

# Run
konmari /path/to/repo
```

## Verification

### Test the Installation

Run the analyzer on the konmari repository itself:
```bash
python3 analyze_repo.py /path/to/konmari
```

Expected output: JSON structure with categories and findings. The repo should show as "already sparks joy" since it's well-maintained.

### Test in IDE

Open a repository in your AI assistant and trigger:
```
clean up this repo
```

Expected behavior:
1. AI asks about your ideal codebase vision
2. Runs `analyze_repo.py` on the repository
3. Presents findings organized by KonMari categories
4. Generates `CLEANUP_PROPOSAL.md`
5. Walks through each item with approval prompts

## Troubleshooting

### Python Not Found

**Error**: `command not found: python3`

**Solution**:
- Install Python 3: [python.org/downloads](https://www.python.org/downloads/)
- Or use `python` instead of `python3` on some systems

### Permission Denied

**Error**: `Permission denied: analyze_repo.py`

**Solution**:
```bash
chmod +x scripts/analyze_repo.py
```

### Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'ast'` (or similar)

**Solution**:
- Python standard library modules should work. Ensure you're using Python 3.7+
- Check for typo: `python3` not `python`

### Git Command Failed

**Error**: Git commands return errors

**Solution**:
- Ensure git is installed: `git --version`
- If analyzing non-git directory, script runs in "limited mode"
- Git is optional; core analysis works without it

### Skill Not Showing in IDE

**Issue**: Your AI assistant doesn't list the skill

**Solution**:
1. Verify `.skill` file is in the correct directory (example: `~/.claude/skills/`)
2. Restart IDE completely (close and reopen)
3. Check file permissions: `ls -la ~/.claude/skills/`
4. Verify `.skill` is a valid ZIP: `unzip -l konmari.skill`

### Analysis Takes Too Long

**Issue**: Analyzer hangs on large repositories

**Solution**:
- Repositories with >10,000 files automatically enable sampling mode
- For manual control, create a `.konmarirc` file:
  ```json
  {
    "sample_mode": true,
    "max_files": 5000
  }
  ```

### False Positives on Active Files

**Issue**: Analyzer proposes deletions for files you're actively using

**Solution**:
- Before analysis, tell the AI about your current work focus
- Mark files you want to keep as exceptions
- Review confidence scores carefully - lower scores require your judgment

## Advanced Configuration

### Custom Gratitude Templates

The skill uses templates in `references/gratitude_templates.md`. Customize by editing this file.

### Adding New Ecosystems

Edit `analyze_repo.py` to add new ecosystem detection:

1. Add marker to `ECOSYSTEM_MARKERS` dictionary
2. Implement `find_orphaned_*_deps()` function
3. Add ecosystem to `find_all_orphaned_deps()` switch

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Uninstallation

### From Claude Code/Cursor

```bash
rm ~/.claude/skills/konmari.skill
```

Restart IDE to refresh skill list.

### Standalone Script

```bash
# Remove symlink if created
sudo rm /usr/local/bin/konmari

# Remove repository
rm -rf /path/to/konmari
```

### Python Package

```bash
pip uninstall konmari-skill
```

## Getting Help

- **Documentation**: [SKILL.md](SKILL.md) - Complete reference
- **Examples**: [examples/](examples/) - Sample outputs and demos
- **Issues**: Report bugs via GitHub Issues
- **Community**: Discuss in GitHub Discussions

## System Compatibility

| Platform | Python 3.7+ | Git | Status |
|-----------|----------------|------|--------|
| macOS 10.15+ | ✓ | ✓ | Fully supported |
| Ubuntu 20.04+ | ✓ | ✓ | Fully supported |
| Debian 11+ | ✓ | ✓ | Fully supported |
| Windows 10/11 | ✓ | ✓ | Fully supported |
| WSL | ✓ | ✓ | Fully supported |

---

Ready to transform your codebase? See [README.md](README.md) for usage guide.
