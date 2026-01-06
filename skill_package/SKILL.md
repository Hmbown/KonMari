---
name: konmari
description: Repository hygiene skill inspired by Marie Kondo's KonMari Method. An end-of-session closeout ritual for AI-assisted development. Triggers on "clean up this repo", "what files can I delete", "reduce context bloat", "find stale files", "what doesn't spark joy", "wrap up", "done for today", "close out session", "end of task", "tidy up", "declutter", "/konmari".
---

# KonMari Repository Decluttering

*"The question of what code to keep is the question of how you want to develop."*

A repository cleanup ceremony inspired by Marie Kondo's KonMari Method. Not just cleanup - transformation.

## Philosophy

### The KonMari Approach to Code

Marie Kondo teaches that tidying is not about discarding - it's about choosing what to keep. The same applies to codebases.

**Core Principles:**

1. **Commit to Transformation** - This is not a quick cleanup. It's a deliberate choice to create a codebase that sparks clarity.

2. **Envision Your Ideal** - Before touching anything, ask: "What does my ideal codebase look like? How do I want to feel when working here?"

3. **Follow the Sacred Order** - Categories must be addressed in sequence, building decision-making skill progressively.

4. **Ask: Does This Spark Clarity?** - The code equivalent of "Does this spark joy?" Hold each file/module in your mind. Does maintaining it feel energizing or draining?

5. **Express Gratitude** - Before discarding, thank the code for its service. This reduces guilt and acknowledges that all code once served a purpose.

6. **Reach Your Click Point** - The moment when your codebase feels "right" - neither too much nor too little.

### The Five Categories (Sacred Order)

The order is mandatory. Start with easy wins to build confidence before tackling harder decisions.

| # | Category | Code Equivalent | Why This Order |
|---|----------|-----------------|----------------|
| 1 | Clothing | **Dead Files** - backups, temps, duplicates | Easiest wins, visible improvement |
| 2 | Books | **Dependencies** - unused packages, orphaned imports | Clear utility judgment |
| 3 | Papers | **Documentation** - outdated docs, drifted READMEs | Requires context awareness |
| 4 | Komono | **Configuration** - orphaned configs, debug artifacts | Scattered, needs attention |
| 5 | Sentimental | **Legacy Code** - original architecture, founder code | Hardest, requires honed judgment |

## Workflow

### 1. Commitment Ritual

Before analysis, establish the session:

```
I'm ready to transform this repository.
My ideal codebase is: [describe]
I commit to following the KonMari order.
```

Ask the user:
- "What does your ideal codebase look like?"
- "Are there any files that must stay regardless of what we find?"
- "What's your current work focus?" (to avoid flagging active work)

### 2. Run the Analysis

Execute the analyzer following the sacred order:

```bash
python3 analyze_repo.py /path/to/repo
```

The script outputs structured JSON with:
- Categories organized in KonMari order
- Confidence scores (0-100) for each recommendation
- Gratitude messages for items proposed for deletion
- Quick wins vs decisions needed
- Celebration if already clean

### 3. Generate the Cleanup Proposal

Create `CLEANUP_PROPOSAL.md` in the repo root:

```markdown
# KonMari Cleanup Ceremony

Generated: [timestamp]
Repository: [path]

## Your Ideal Codebase Vision
[User's stated goals]

---

## Summary by Category

| Category | Items Found | Quick Wins | Decisions Needed |
|----------|-------------|------------|------------------|
| 1. Dead Files (Clothing) | X | Y | Z |
| 2. Dependencies (Books) | X | Y | Z |
| 3. Documentation (Papers) | X | Y | Z |
| 4. Configuration (Komono) | X | Y | Z |
| 5. Legacy (Sentimental) | X | Y | Z |

**Click Point Progress**: [percentage]%

---

## Quick Wins (Confidence >= 80%)

High-confidence items safe to remove. These clearly no longer spark clarity.

| File | Category | Confidence | Reason |
|------|----------|------------|--------|
| `old_utils_backup.py` | Dead Files | 95% | Backup pattern, 180 days old |
| `debug_test.js` | Dead Files | 88% | Debug script, never integrated |

## Decisions Needed (Confidence 50-79%)

Medium-confidence items requiring your judgment. Hold each in your mind.

| File | Category | Confidence | Question to Consider |
|------|----------|------------|---------------------|
| `legacy_auth.py` | Legacy | 55% | Original auth - still referenced? |
| `unused-lib` | Dependencies | 65% | Was this for a feature not yet built? |

## Gratitude Corner

*These files served their purpose. Thank them before letting go.*

| File | Service Provided | Gratitude |
|------|------------------|-----------|
| `old_parser.py` | Processed v1 data format | Thank you for handling our early data needs. |
| `debug_api.js` | Helped diagnose auth bug | Gratitude for revealing the logging gap. |

## Already Sparking Joy

Files that are active, well-maintained, and aligned with your vision.

[List of recently active, essential files - celebrate these!]

## Git Archaeology

- Claude Code commits (last 90 days): X
- AI-pattern commits: Y
- Potentially stale branches: [list]
- Consider: `git gc` if history is cluttered

---

## Next Steps

1. **Review Quick Wins** - These are safe to delete
2. **Contemplate Decisions Needed** - Hold each in your mind
3. **Express Gratitude** - Thank files before removal
4. **Execute with Approval** - Only act with explicit permission
5. **Celebrate Your Click Point** - Enjoy the clarity!

*This is a proposal. No changes without your explicit approval.*
```

### 4. Present and Execute

After generating the report:

1. **Summarize findings** - Present the high-level view
2. **Walk through categories** - Follow the sacred order
3. **For each item**: Present the recommendation, ask for approval
4. **Before deletion**: Read the gratitude message aloud
5. **After completion**: Celebrate reaching the click point

**Example dialogue:**

```
Let's begin with Category 1: Dead Files.

I found 3 backup files that no longer spark clarity:
- old_utils_backup.py (95% confidence) - 180 days untouched
- config_copy.json (88% confidence) - Duplicate of config.json
- temp_debug.py (92% confidence) - Debug script from March

Before we let these go, let's express gratitude:
"Thank you, old_utils_backup.py, for the safety you provided during refactoring.
 Version control now serves this purpose. Your work is complete."

Shall I remove these files?
```

### 5. Log Actions

After execution, append to CLEANUP_PROPOSAL.md:

```markdown
---

## Actions Taken

| Action | File | Timestamp |
|--------|------|-----------|
| Deleted | old_utils_backup.py | 2025-01-15 14:30 |
| Kept | legacy_auth.py | User decided to keep |
| Deleted | temp_debug.py | 2025-01-15 14:31 |

**Click Point Reached**: Yes
**Files Removed**: 5
**Space Recovered**: 12.4 KB

*"Life truly begins only after you have put your codebase in order."*
```

## Decision Heuristics

### Sparks Clarity = Keep
- Modified in last 14 days
- Referenced by active code paths
- Part of current work focus
- User explicitly wants to keep
- Has clear purpose in project structure

### Doesn't Spark Clarity = Propose Deletion
- Matches stale patterns (_backup, _old, _copy, temp_)
- Not modified in 60+ days AND matches cruft pattern
- Never integrated into main codebase
- Duplicate of another file
- Claude Code session artifact no longer needed

### Confidence Scoring

| Signal | Confidence Impact |
|--------|-------------------|
| Matches stale pattern | +20 |
| Claude Code artifact | +15 |
| Duplicate detected | +15 |
| Age > 180 days | +15 |
| Age > 90 days | +10 |
| Age > 60 days | +5 |
| Modified < 14 days | -35 |
| Modified < 30 days | -20 |
| Imported elsewhere | -40 |

## Claude Code Integration

This skill detects Claude Code-specific patterns:

- **Commit signatures**: `Generated with Claude Code`, `Co-Authored-By: Claude`
- **Session artifacts**: `CLAUDE-CONTEXT.md`, `PLAN.md`, `DEBUG.md`
- **Conversation artifacts**: Q&A comments, debug scripts, verify files
- **Experimental branches**: `claude-*`, `attempt-*`, `wip-*`

## Ecosystem Support

Orphaned dependency detection for:
- **Python**: requirements.txt, pyproject.toml, setup.py
- **JavaScript/TypeScript**: package.json
- **Go**: go.mod
- **Rust**: Cargo.toml

## Edge Cases

### Monorepos
- Detected automatically (lerna, pnpm, Nx, Turborepo, Yarn workspaces)
- Analyzed per-package with aggregate report

### No Git History
- Switches to "limited analysis mode"
- Relies on file timestamps
- Still detects patterns and duplicates

### Large Repos (>10,000 files)
- Enables sampling mode automatically
- Focuses on recently modified areas
- Reports as "sampled analysis"

### Already Clean Repos
If no issues found, celebrate:

```markdown
## Congratulations!

Your repository already sparks joy!

**Signs of a well-maintained codebase:**
- No stale backup files detected
- Dependencies are actively used
- Documentation appears current
- No orphaned configurations found

*You've reached your click point. Enjoy the clarity!*
```

## Important Notes

- **Never auto-delete**: Always present proposals and wait for explicit approval
- **Git safety**: Remind user that git history preserves deleted files
- **Respect user overrides**: If user says "keep X", respect it regardless of patterns
- **Sacred order matters**: Don't skip categories or jump ahead
- **Gratitude is not optional**: The ritual matters for psychological closure

## Authentic KonMari Language

Use these phrases naturally:

- "Does this spark clarity?" (not just "is this useful?")
- "Thank you for your service" (before deletion)
- "Your click point" (the moment of completion)
- "Tidy by category, not by folder"
- "The question of what to keep is the question of how you want to develop"
- "Let go with gratitude"

---

*"The objective of tidying is not just to clean, but to feel clarity working within that environment."*
