# AI Context Limits Reference

## Practical Limits

While modern AI context windows can be large, effective working limits are lower:

| Metric | Recommended Max | Hard Limit |
|--------|-----------------|------------|
| Lines per file | 500 | 2000 |
| Tokens per file | 4,000 | 16,000 |
| Total context load | 50,000 tokens | 150,000 tokens |

## Why Lower is Better

Context bloat degrades performance:
- Attention diffuses across more content
- Relevant information gets buried
- Response quality decreases
- Latency increases

## File Organization Heuristics

### Split when:
- File exceeds 500 lines
- File contains multiple distinct topics
- Sections are referenced independently

### Consolidate when:
- Multiple small files on same topic
- Files are always used together
- Fragmentation adds navigation overhead

### Delete when:
- File hasn't been touched in 60+ days AND has stale pattern (backup, old, v1, etc.)
- Duplicate of another file
- Experimental script that was never integrated
- Documentation that's outdated or redundant

## Token Estimation

Rough formula: `tokens ≈ characters / 4`

| Content Type | Chars/Token |
|--------------|-------------|
| Code | ~3.5 |
| Prose | ~4.5 |
| JSON/YAML | ~3 |

---

## AI Assistant Session Patterns

### Common Session Artifacts

These files often accumulate during AI-assisted sessions and may become cruft:

| Pattern | Description | Typical Lifespan |
|---------|-------------|------------------|
| `CLAUDE-CONTEXT.md` | Session context briefing | Single session |
| `AI-CONTEXT.md` | Session context briefing | Single session |
| `PLAN.md` | Implementation planning | Until implemented |
| `DEBUG.md` | Debugging notes | Until bug fixed |
| `TODO-claude.md` | AI-specific todos | Varies |
| `TODO-ai.md` | AI-specific todos | Varies |
| `NOTES.md` | Session notes | Until consolidated |
| `scratch_*.py` | Quick experiments | Single session |
| `debug_*.js` | Debug scripts | Until bug fixed |
| `verify_*.ts` | Verification scripts | Until verified |
| `check_*.py` | Check scripts | Single session |

### Conversation Artifacts in Code

AI assistant sessions may leave these patterns in source files:

```python
# Q: Should this be async?
# A: Yes, because the API call blocks...

# TODO: AI - remove after testing
# FIXME: session artifact
```

These are usually meant to be temporary and can be safely cleaned up after the session.

### Commit Message Patterns

AI-assisted commits often include these signatures:

```
Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: GitHub Copilot <...>
Generated with Codex
```

This makes AI-generated commits identifiable for git archaeology.

### Branch Naming Patterns

Experimental branches from AI sessions often follow:
- `claude-*` - Claude attempts
- `cursor-*` - Cursor attempts
- `copilot-*` - Copilot attempts
- `codex-*` - Codex attempts
- `attempt-*` - Numbered attempts
- `wip-*` - Work in progress
- `test-refactor-*` - Experimental refactors
- `debug-*` - Debugging branches

These may become stale if the experiment concludes or is abandoned.

### Directory Patterns

AI tools may create or populate these directories:
- `.claude/` - Claude Code configuration
- `.cursor/` - Cursor configuration
- `.codex/` - Codex configuration
- `.ai/` - Generic AI tool configuration

### Config File Patterns

| File | Purpose | Clean Up When |
|------|---------|---------------|
| `.claude/settings.json` | Project settings | Usually keep |
| `.claude/settings.local.json` | Local overrides | Keep unless personal |
| `.mcp.json` | MCP server config | Review periodically |
| `CLAUDE-CONTEXT.md` | Session context | After session ends |

## Recommendations

### Start of Session
1. Check for stale session artifacts from previous sessions
2. Review `CLAUDE-CONTEXT.md` if it exists
3. Consider running KonMari cleanup if accumulated cruft

### End of Session
1. Clean up debug/scratch files
2. Update or remove `PLAN.md` if complete
3. Consolidate session notes into permanent docs
4. Consider running `/konmari` as closeout ritual

### Periodic Maintenance
1. Review `.claude/commands/` for experimental commands
2. Check for orphaned branches with AI patterns
3. Audit AI-generated commits for squash opportunities
4. Clean up experimental dependencies that were never used

---

*Context is a public good. Keep it clean for your future self and your AI pair.*
