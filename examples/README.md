# KonMari Skill Examples

This directory contains example outputs and usage demonstrations for the KonMari repository decluttering skill.

## Examples Overview

- [`sample_output.json`](sample_output.json) - Full analysis output from a typical repository
- [`sample_cleanup_proposal.md`](sample_cleanup_proposal.md) - Example cleanup proposal as presented to user
- [`conversation_example.md`](conversation_example.md) - Full dialogue example of a KonMari ceremony

## Understanding the Output

### Analysis JSON Structure

The `analyze_repo.py` script outputs structured JSON with these sections:

```json
{
  "timestamp": "2026-01-06T...",
  "repo_path": "/path/to/repo",
  "file_count": 1247,
  "is_large_repo": false,
  "has_git": true,
  "monorepo": {...},
  "ecosystems": {...},
  "categories": {
    "1_dead_files": {...},
    "2_dependencies": {...},
    "3_documentation": {...},
    "4_configuration": {...},
    "5_legacy": {...}
  },
  "git_archaeology": {...},
  "context_heavy_files": [...],
  "summary": {...},
  "quick_wins": [...],
  "decisions_needed": [...],
  "cleanliness": {...}
}
```

### Key Fields

#### Categories (Sacred Order)

Each category follows the KonMari method:
1. **1_dead_files** - Dead Files (Clothing) - easiest wins
2. **2_dependencies** - Dependencies (Books) - clear utility
3. **3_documentation** - Documentation (Papers) - context awareness
4. **4_configuration** - Configuration (Komono) - scattered items
5. **5_legacy** - Legacy Code (Sentimental) - hardest decisions

Each category contains:
- `name` - Display name
- `description` - What this category represents
- `items` - Array of findings with metadata
- `count` - Number of items found

#### Item Structure

Each item includes:
- `path` or `package` - Identifier
- `confidence` - 0-100, where ≥80 is Quick Win, 50-79 needs decision
- `reason` - Why it was flagged
- `gratitude` - Gratitude message to read before deletion
- `category` - Which KonMari category it belongs to
- Additional metadata (age, size, markers, etc.)

#### Cleanliness Assessment

- `is_clean` - Boolean, true if no issues found
- `nearly_clean` - Boolean, true if <5 minor issues
- `celebration` - Message for reaching click point

## Sample Scenarios

### Scenario 1: Well-Maintained Repository

**Input**: Repository with no dead files, active dependencies, current docs

**Output**:
- `cleanliness.is_clean: true`
- Celebration message: "Your repository already sparks joy!"
- Empty item lists across all categories
- AI presents congratulatory message instead of cleanup proposal

### Scenario 2: Typical Development Repository

**Input**: Repository with some accumulated cruft

**Output**:
- Several items in "Dead Files" (backups, temp files)
- A few orphaned dependencies in "Dependencies"
- Maybe a broken link in "Documentation"
- Confidence scores vary (high for clear patterns, lower for judgment calls)
- Mix of "Quick Wins" and "Decisions Needed"

### Scenario 3: Legacy Project

**Input**: Old project with deprecation markers, abandoned branches

**Output**:
- Many items in "Legacy Code" (sentimental category)
- Stale branches in git_archaeology
- Multiple AI-generated commits detected
- Low confidence scores requiring human judgment
- Emphasis on gratitude and careful consideration

### Scenario 4: Claude Code Session Repository

**Input**: Repository used primarily with Claude Code

**Output**:
- Claude Code session artifacts (CLAUDE-CONTEXT.md, PLAN.md, etc.)
- Experimental branches (claude-*, attempt-*, wip-*)
- Debug and verify scripts
- High confidence for session artifacts (meant to be temporary)
- AI commits identified in git_archaeology

## Running the Examples

### View Sample Output

```bash
cat examples/sample_output.json | python3 -m json.tool
```

### Test with Sample Repository

```bash
# Create test repo structure
mkdir test_repo && cd test_repo

# Add some test files
echo "# Old backup" > old_utils_backup.py
echo "# Temp file" > temp_debug.py
echo "{'dependencies': {}}" > package.json

# Run analyzer
python3 ../scripts/analyze_repo.py

# Clean up
cd .. && rm -rf test_repo
```

### Generate Your Own Examples

```bash
# Run on a real repository
python3 scripts/analyze_repo.py /path/to/real/repo > my_output.json

# Format for viewing
python3 -m json.tool my_output.json > my_output_pretty.json
```

## Confidence Score Interpretation

| Confidence Range | Meaning | Action |
|-----------------|-----------|---------|
| 0-49% | Low confidence, likely needed | Keep or investigate |
| 50-79% | Medium confidence, ambiguous | Present to user for decision |
| 80-100% | High confidence, safe to remove | Present as Quick Win |

### High Confidence Indicators

- Matches stale pattern (_old, _backup, temp, etc.)
- Is Claude Code session artifact
- Is duplicate of another file
- Age > 180 days with stale pattern
- Age > 90 days with multiple indicators

### Low Confidence Indicators

- Modified in last 14 days
- Imported by other code
- Active work focus file
- User explicitly marked to keep
- Part of essential project structure

## Gratitude Messages

Each item includes a `gratitude` field with a message to read aloud before deletion. Example:

```json
{
  "path": "old_utils_backup.py",
  "gratitude": "Thank you, old_utils_backup.py, for the safety you provided during refactoring. Version control now serves this purpose. Your work is complete."
}
```

These messages are randomly selected from templates in `references/gratitude_templates.md` based on item category.

## Integration with AI Workflow

The skill is designed to integrate seamlessly into Claude Code/Cursor conversations:

1. **User triggers skill**: "clean up this repo"
2. **AI runs analysis**: Executes `analyze_repo.py` silently
3. **AI presents results**: Walks through each category in sacred order
4. **User approves**: "Yes, delete those"
5. **AI expresses gratitude**: Reads the gratitude message aloud
6. **AI executes deletion**: Removes files with user's explicit permission
7. **AI celebrates**: Acknowledges reaching click point

See [`conversation_example.md`](conversation_example.md) for a full annotated dialogue.

## Tips for Best Results

### Before Running Analysis

1. **State your work focus** - Tell AI what you're actively working on
2. **Identify must-keep files** - Any files that should never be considered
3. **Define your ideal codebase** - What do you want this repository to be like?

### During Analysis

1. **Ask questions** - If you're unsure about a recommendation, ask why
2. **Consider the category** - Remember the sacred order builds decision skill
3. **Hold each item in mind** - "Does this spark clarity?"

### After Cleanup

1. **Verify nothing broke** - Run tests, check functionality
2. **Review git history** - Deleted files are preserved there
3. **Celebrate your click point** - Enjoy the clarity!

## Troubleshooting Examples

If examples don't work as expected:

### Python JSON parsing error

```bash
# Ensure python3 is available
python3 -m json.tool sample_output.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

### Permission denied on examples directory

```bash
chmod -R 755 examples/
```

### Can't find sample files

```bash
# Verify you're in examples directory
pwd  # Should be .../konmari/examples
ls -la
```

---

For more information, see the main documentation:
- [SKILL.md](../SKILL.md) - Complete reference
- [README.md](../README.md) - User guide
- [INSTALL.md](../INSTALL.md) - Installation

