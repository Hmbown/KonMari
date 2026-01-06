# Changelog

All notable changes to KonMari repository decluttering skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Planned
- Potential future features and enhancements
- Community-driven improvements

## [1.0.0] - 2026-01-06

### Added
- Initial release of KonMari repository decluttering skill
- Full implementation of KonMari sacred order analysis:
  - Category 1: Dead Files (Clothing) - Backup, temp, duplicate detection
  - Category 2: Dependencies (Books) - Orphaned package detection
  - Category 3: Documentation (Papers) - Broken reference detection
  - Category 4: Configuration (Komono) - Orphaned config detection
  - Category 5: Legacy Code (Sentimental) - Deprecation marker detection
- Support for multiple ecosystems:
  - Python (requirements.txt, pyproject.toml, setup.py, Pipfile)
  - JavaScript/TypeScript (package.json)
  - Go (go.mod)
  - Rust (Cargo.toml)
- Git archaeology features:
  - AI-generated commit detection
  - Claude Code signature identification
  - Stale branch pattern detection
- Confidence scoring system (0-100) with configurable thresholds
- Context-heavy file detection (>500 lines, >4K tokens)
- Monorepo detection and per-package analysis
- Gratitude message generation with customizable templates
- Celebration system for clean repositories

### Documentation
- [SKILL.md](SKILL.md) - Complete reference documentation with philosophy and workflow
- [README.md](README.md) - User-facing quick start guide
- [INSTALL.md](INSTALL.md) - Detailed installation instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history (this file)
- [examples/README.md](examples/README.md) - Example showcase and guide
- [examples/sample_output.json](examples/sample_output.json) - Example analysis JSON
- [examples/sample_cleanup_proposal.md](examples/sample_cleanup_proposal.md) - Example generated proposal
- [examples/conversation_example.md](examples/conversation_example.md) - Full dialogue example
- [references/gratitude_templates.md](references/gratitude_templates.md) - Gratitude template collection
- [references/context_limits.md](references/context_limits.md) - Context window guidelines

### Features
- Automatic .skill ZIP packaging structure
- Command-line interface for standalone use
- JSON output format for programmatic integration
- Claude Code skill integration triggers:
  - "clean up this repo"
  - "what files can I delete"
  - "reduce context bloat"
  - "find stale files"
  - "what doesn't spark joy"
  - "wrap up", "done for today", "close out session", "end of task"
  - "tidy up", "declutter"
  - "/konmari"

### Technical Implementation
- Pattern-based detection for 40+ stale file patterns
- AST-based import detection for Python ecosystem
- Regex-based import detection for JavaScript ecosystem
- Regex-based import detection for Go ecosystem
- Regex-based use detection for Rust ecosystem
- Markdown link validation for documentation drift
- Git history analysis via subprocess (90-day window)
- Large repository sampling mode (>10,000 files)
- No-git fallback mode for non-version-controlled repos

### Safety Features
- Never auto-deletes - all actions require explicit user approval
- Git history preservation reminder
- User-protected files support
- Confidence score transparency
- Age-based heuristics (14, 30, 60, 90, 180 day thresholds)
- Import reference checking (prevents false positives)

### Philosophical Features
- KonMari sacred order enforcement (Clothing → Books → Papers → Komono → Sentimental)
- Gratitude ritual for each proposed deletion
- "Click Point" completion celebration
- User agency preservation
- Ceremony-based workflow (commitment → analysis → presentation → gratitude → action → celebration)

### Platform Support
- macOS 10.15+ (fully supported)
- Ubuntu 20.04+ (fully supported)
- Debian 11+ (fully supported)
- Windows 10/11 (fully supported)
- WSL (fully supported)

### Installation
- Claude Code/Cursor skill installation via .skill ZIP
- Standalone Python script execution
- Symlink support for system-wide access
- No external dependencies (Python standard library only)
- MIT License for maximum compatibility

### Quality
- Linting guidelines for code contributions
- PEP 8 compliance for Python code
- Comprehensive docstrings and inline comments
- Error handling for edge cases
- Graceful degradation without git

### Community
- [CONTRIBUTING.md](CONTRIBUTING.md) with detailed contribution guidelines
- Bug report templates
- Enhancement request templates
- Code of conduct guidelines
- Ecosystem addition guidelines

## Development Roadmap

### Future Enhancements (Unplanned)

Potential features for future versions:

#### Version 1.1.0 (Potential)
- [ ] Web UI for visual repository exploration
- [ ] Interactive mode with immediate feedback
- [ ] Custom pattern configuration file
- [ ] Integration with popular IDEs beyond Claude Code/Cursor
- [ ] Docker container for consistent analysis environment

#### Version 1.2.0 (Potential)
- [ ] Additional ecosystem support (PHP, Java, C#, Swift, Kotlin)
- [ ] Smart duplicate content detection (hash-based)
- [ ] Automated PR generation for cleanup actions
- [ ] Repository health scoring over time
- [ ] Integration with CI/CD pipelines

#### Version 2.0.0 (Potential)
- [ ] Machine learning for better confidence scoring
- [ ] Repository transformation suggestions (not just deletion)
- [ ] Cross-repository cleanup coordination
- [ ] Team collaboration features
- [ ] Analytics and reporting dashboard

### Known Limitations

#### Version 1.0.0
- Confidence scores are heuristics, not deterministic
- Duplicate detection is filename-based (not content-based)
- Deprecation markers require human review
- Git analysis limited to last 90 days
- Large repos use sampling mode
- Context-heavy file recommendations are manual (not auto-delete)

## Migration Guide

### Upgrading from Previous Versions

This is the initial release (1.0.0). No migration required.

### Upgrading from Pre-Releases

If you used early versions:
- Update .skill file from latest release
- Re-run analyzer to benefit from new features
- Review CHANGELOG.md for new capabilities

## Credits

### Inspiration
- Marie Kondo's *The Life-Changing Magic of Tidying Up*
- KonMari Method adapted for software development

### Contributors
- Claude Code Community - Initial concept and implementation
- All future contributors will be credited in future releases

## Support

### Getting Help
- [SKILL.md](SKILL.md) - Complete reference
- [README.md](README.md) - User guide
- [INSTALL.md](INSTALL.md) - Installation guide
- [examples/](examples/) - Usage examples
- GitHub Issues - Bug reports and feature requests
- GitHub Discussions - Community conversation

### Reporting Issues
Include:
- Python version (`python3 --version`)
- Operating system
- Repository type (Python, JS, Go, Rust, monorepo)
- Steps to reproduce
- Error messages or unexpected behavior

---

## Links

- [Repository Home](https://github.com/Hmbown/KonMari)
- [Documentation](SKILL.md)
- [Installation Guide](INSTALL.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Examples](examples/)
- [License](LICENSE)

---

*"The question of what to keep is the question of how you want to develop."* — Adapted from Marie Kondo

