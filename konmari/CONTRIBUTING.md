# Contributing to KonMari Skill

Thank you for your interest in contributing to the KonMari repository decluttering skill! This document provides guidelines for participating in the project.

## Code of Conduct

- Be respectful and inclusive
- Assume good intentions
- Focus on what is best for the community
- Constructive feedback is always welcome

## How to Contribute

### Reporting Bugs

Before reporting a bug, please:

1. **Search existing issues** - Check if the bug has already been reported
2. **Check the latest version** - Ensure you're using the current version
3. **Reproduce the issue** - Provide steps to reproduce the bug

#### Bug Report Template

```markdown
**Description**: Brief description of the bug

**Steps to reproduce**:
1. Run analyzer on: `[repository path or type]`
2. `[next step]`
3. `[next step]`

**Expected behavior**: What should happen

**Actual behavior**: What actually happens

**Environment**:
- Python version: `python3 --version`
- OS: `[your OS]`
- Git version: `git --version` (if applicable)

**Additional context**: Stack traces, error messages, screenshots, etc.
```

### Suggesting Enhancements

We welcome ideas for improving the skill! Please:

1. **Search existing issues and discussions** - Check for duplicate suggestions
2. **Consider the philosophy** - Does it align with KonMari principles?
3. **Be specific** - Provide concrete use cases and examples

#### Enhancement Request Template

```markdown
**Title**: One-line summary of enhancement

**Problem**: What problem does this solve?

**Proposed solution**: How should it work?

**Alternatives considered**: What other approaches did you think about?

**Additional context**: Screenshots, examples, references to similar tools
```

### Code Contributions

We welcome code contributions! Follow this process:

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/your-username/konmari.git
cd konmari
```

#### 2. Set Up Development Environment

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No dependencies required! The script uses only Python standard library
```

#### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# Or for bug fix:
git checkout -b fix/issue-number
```

#### 4. Make Changes

Follow these guidelines:

**Code Style**:
- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings to functions
- Keep functions focused and single-purpose

**Testing**:
- Test on multiple repository types (Python, JS, Go, Rust repos)
- Test with and without git history
- Test edge cases (empty repos, large repos, monorepos)
- Verify JSON output is valid: `python3 -m json.tool output.json > /dev/null`

**Documentation**:
- Update inline docstrings if behavior changes
- Update this CONTRIBUTING.md if process changes
- Update SKILL.md if user-facing behavior changes
- Add example to examples/ if it demonstrates new feature

#### 5. Commit Changes

Use clear, descriptive commit messages:

```bash
git commit -m "feat: Add support for Dart ecosystem"
# or
git commit -m "fix: Handle null values in confidence calculation"
# or
git commit -m "docs: Update CONTRIBUTING.md with new guidelines"
```

Commit message prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code restructuring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

#### Skill Bundle Updates

When you change `skill_package/`, rebuild the bundle:

```bash
scripts/build_skill.sh
```

Optional: enable the local git hook to auto-rebuild on commit:

```bash
git config core.hooksPath .githooks
```

#### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title based on your commit message
- Description of what changed and why
- Reference any related issues
- Screenshots or examples if applicable

## Adding New Ecosystem Support

KonMari supports multiple dependency ecosystems. Adding a new one involves:

### Step 1: Add Ecosystem Marker

Edit `ECOSYSTEM_MARKERS` in `analyze_repo.py`:

```python
ECOSYSTEM_MARKERS = {
    "python": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
    "javascript": ["package.json"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "dart": ["pubspec.yaml"],  # NEW: Add this
}
```

### Step 2: Implement Detection Function

Create `find_orphaned_{ecosystem}_deps()` function:

```python
def find_orphaned_dart_deps(repo_path: str) -> List[Dict]:
    """Find Dart packages in pubspec.yaml that are never used."""
    orphans = []

    pubspec_path = os.path.join(repo_path, "pubspec.yaml")
    if not os.path.exists(pubspec_path):
        return orphans

    # Parse pubspec.yaml (implement parsing logic)
    # ...

    # Find orphaned packages
    for pkg in declared_deps:
        if pkg not in all_imports:
            orphans.append({
                "package": pkg,
                "source": "pubspec.yaml",
                "ecosystem": "dart",
                "category": "dependencies",
                "category_name": "Dependencies (Books)",
                "confidence": 65,
                "reason": "package_not_imported",
                "gratitude": generate_gratitude("dependency", pkg, 0),
            })

    return orphans
```

### Step 3: Register in Main Analysis

Add your function to `find_all_orphaned_deps()`:

```python
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
    if "dart" in ecosystems:  # NEW: Add this
        all_orphans.extend(find_orphaned_dart_deps(repo_path))

    return all_orphans
```

### Step 4: Test

Create test repository with dependencies from new ecosystem and verify:
- Detection works
- Orphan detection is accurate
- Gratitude messages generate
- Confidence scores are appropriate

### Step 5: Document

Update documentation:
- Add ecosystem to [SKILL.md](SKILL.md) under "Ecosystem Support"
- Update [README.md](README.md) supported ecosystems list
- Add example to [examples/](examples/) showing the new ecosystem

## Documentation Contributions

Documentation is critical for user experience. When contributing docs:

1. **Keep the KonMari voice** - Maintain the philosophical, ceremonial tone
2. **Be specific** - Include concrete examples
3. **Stay aligned** - Docs should match current implementation
4. **Test instructions** - Follow your own docs as a new user

### Updating Gratitude Templates

Gratitude templates live in `references/gratitude_templates.md`. When adding new templates:

1. **Maintain the KonMari spirit** - Express thankfulness, acknowledge service
2. **Be category-specific** - Different tone for different file types
3. **Use respectful language** - Honor the code's purpose
4. **Add variety** - Multiple templates per category for variety

Example addition:

```markdown
### Category 2: Dependencies (Books)

### Ruby Gems
- "Thank you, [gem], for capabilities you offered even if unused. You showed us what's possible in Ruby ecosystem."
```

## Development Guidelines

### Philosophy Alignment

All contributions should respect the KonMari philosophy:

1. **Never auto-delete** - Always require user approval
2. **Follow sacred order** - Don't skip categories or reorder them
3. **Express gratitude** - Every proposed deletion should include acknowledgment
4. **Honor user agency** - User makes all final decisions
5. **Celebrate completion** - Acknowledge when click point is reached

### Technical Considerations

- **Performance** - Handle large repos efficiently (>10,000 files)
- **Safety** - Don't break git history or delete protected files
- **Accuracy** - Confidence scores should be meaningful, not arbitrary
- **Graceful degradation** - Work without git, handle non-repos gracefully

### Testing Strategy

Before submitting code:

1. **Unit test confidence calculation** - Verify score makes sense
2. **Integration test on real repos** - Test on Python, JS, Go, Rust projects
3. **Edge case testing** - Empty repos, no git, nested structures
4. **Documentation test** - Follow your own instructions

## Release Process

Releases are managed by maintainers. For contributors wanting to drive a release:

1. Ensure all tests pass
2. Update [CHANGELOG.md](CHANGELOG.md) with new features and fixes
3. Update version in skill metadata if applicable
4. Tag release in git: `git tag -a v1.1.0 -m "Release v1.1.0"`
5. Push tag: `git push origin v1.1.0`

## Community

### Discussion

- Use GitHub Issues for bug reports and feature requests
- Use GitHub Discussions for questions, ideas, and general conversation
- Be patient - Maintainers contribute voluntarily

### Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes in CHANGELOG.md
- Special thanks in skill documentation

## Getting Help

If you need help contributing:

1. **Read the docs** - [SKILL.md](SKILL.md), [README.md](README.md), [INSTALL.md](INSTALL.md)
2. **Review examples** - [examples/](examples/) show how features work
3. **Ask in discussions** - GitHub Discussions is open to all
4. **Draft PR early** - Open PR as "Draft" to get feedback before polishing

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see [LICENSE](LICENSE)).

---

Thank you for helping make KonMari better for everyone!

*"The objective of tidying is not just to clean, but to feel clarity working within that environment."*
