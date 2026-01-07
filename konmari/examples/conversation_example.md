# Full KonMari Ceremony Dialogue Example

This is an annotated example of a complete KonMari cleanup ceremony between a developer and Claude Code/Cursor with the KonMari skill installed.

## Setup

**Context**: Developer has been working on a web authentication project for several months. The repository has accumulated some cruft from experimentation, debugging sessions, and old refactors.

**Trigger**: User types `clean up this repo` in Claude Code/Cursor

---

## Ceremony Begins

### Phase 1: Commitment Ritual

**AI**:
> I'm ready to transform this repository.
>
> Let me ask a few questions before we begin the analysis:
>
> **What does your ideal codebase look like?**

**User**:
> I want it to be clean and focused. Just the authentication module and API endpoints. No experimental leftovers, no debug scripts lying around, and all documentation should be accurate.

**AI**:
> Understood. Clean, focused authentication system with accurate docs.
>
> **Are there any files that must stay regardless of what we find?**

**User**:
> The `src/auth/` directory and `src/api/` directory are critical. Don't touch those. Everything else is fair game.

**AI**:
> Noted. I'll respect `src/auth/` and `src/api/` as protected areas. Everything else is open to the KonMari process.
>
> I commit to following the sacred KonMari order: Clothing → Books → Papers → Komono → Sentimental.
>
> Running analysis now...

*[AI runs `python3 scripts/analyze_repo.py` and processes the output]*

---

### Phase 2: Category 1 - Dead Files (Clothing)

**AI**:
> Let's begin with Category 1: Dead Files (Clothing).
>
> This is the easiest category - backup files, temp files, and duplicates. Quick wins to build momentum.
>
> I found 5 items that no longer spark clarity:
>
> **Quick Wins** (high confidence):
>
> 1. `src/utils_old_backup.py` (95% confidence)
>    - 143 days untouched
>    - Matches backup pattern
>    - Size: 4.5 KB
>
> 2. `temp_debug.js` (88% confidence)
>    - 289 days old
>    - Temporary debug script
>    - Size: 0.9 KB
>
> 3. `CLAUDE-CONTEXT.md` (92% confidence)
>    - Claude Code session artifact
>    - Created Dec 20, 17 days ago
>    - Session notes that are now implemented
>
> 4. `verify_auth_2025-10-15.py` (85% confidence)
>    - Verification script from October
>    - Not part of current codebase
>    - 82 days old
>
> 5. `auth_migration_v1.sql` (90% confidence)
>    - Database migration backup
>    - 156 days old
>    - Migration completed long ago
>
> **Decisions Needed**:
>
> - `config.json` duplicates (70% confidence)
>   - 3 versions exist: `config.json`, `config_copy.json`, `config (1).json`
>   - Can you identify which is the source?
>
> Before we let these go, let's express gratitude...

**AI**:
> "Thank you, `src/utils_old_backup.py`, for the safety you provided during refactoring. Version control now serves this purpose. Your work is complete."
>
> "Thank you, `temp_debug.js`, for helping us diagnose the authentication bug. The bug is fixed; your purpose is fulfilled."
>
> "Thank you, session notes, for documenting our conversation with Claude Code. Those decisions are now implemented."
>
> "Thank you, `verify_auth.py`, for confirming the migration worked. Your verification job is done."
>
> "Thank you, `auth_migration_v1.sql`, for bridging our data to the new schema. The bridge is no longer needed."
>
> *[AI pauses]*
>
> Shall I remove these 5 Quick Win files?

**User**:
> Yes, go ahead.

**AI**:
> *[Files deleted with explicit permission]*
>
> Five files released. Space recovered: 18.7 KB
>
> ✓ Deleted: `src/utils_old_backup.py`
> ✓ Deleted: `temp_debug.js`
> ✓ Deleted: `CLAUDE-CONTEXT.md`
> ✓ Deleted: `verify_auth_2025-10-15.py`
> ✓ Deleted: `auth_migration_v1.sql`
>
> Regarding the config duplicates: Which of the three config files is your current source?

**User**:
> `config.json` is the real one. The others can go.

**AI**:
> Got it. Let's express gratitude before letting go...
>
> "Thank you, `config_copy.json`, for preserving redundancy during uncertain times. We now trust our version control."
>
> "Thank you, `config (1).json`, for the backup you provided. That caution is no longer needed."
>
> *[AI deletes the duplicate config files]*
>
> ✓ Deleted: `config_copy.json`
> ✓ Deleted: `config (1).json`
>
> Category 1 complete! 7 files released. Feeling lighter?

---

### Phase 3: Category 2 - Dependencies (Books)

**AI**:
> Now Category 2: Dependencies (Books).
>
> This category requires clear utility judgment. Unused packages clutter your mental model of available tools.
>
> I found 2 packages that appear unused:
>
> 1. `lodash` (60% confidence)
>    - Declared in package.json
>    - Not imported in any source files
>    - Common utility library
>
> 2. `axios` (55% confidence)
>    - Declared in package.json
>    - Not directly imported in source
>    - HTTP client - possibly used by build tools
>
> Both have low-to-medium confidence because package.json dependencies don't always appear directly in code (build tools, dev scripts may use them).
>
> Let's express gratitude first...
>
> "Thank you, `lodash`, for the rich utility functions you offered, even if unused. You taught us what's possible."
>
> "Thank you, `axios`, for being available when we needed HTTP capabilities. Sometimes knowing an option exists is enough."

**AI**:
> Hold these dependencies in your mind. Does `lodash` spark clarity for you? Is it imported in build scripts or is it truly unused? What about `axios` - is it needed by your bundler or dev server?

**User**:
> Lodash isn't used anywhere. Can remove it. But axios is used by the API client library, even though it's not directly in our code. Keep axios.

**AI**:
> Understood. Letting go of lodash with gratitude...
>
> "Thank you, `lodash`, for waiting patiently. We've decided to go a different direction."
>
> *[AI removes lodash from package.json]*
>
> ✓ Removed: `lodash` from dependencies
> ✓ Kept: `axios` (used by API client library)
>
> Category 2 complete! Your dependencies are now leaner and clearer.

---

### Phase 4: Category 3 - Documentation (Papers)

**AI**:
> Category 3: Documentation (Papers).
>
> This requires context awareness. Documentation that has drifted from reality can mislead future developers.
>
> I found 1 issue:
>
> **Decisions Needed**:
>
> 1. `README.md` (55% confidence)
>    - Contains 2 broken references:
>      - Link to `./docs/getting-started.md` (file doesn't exist)
>      - Code block reference to `setup.sh` (not in repo)
>    - Modified today
>    - The rest of the README appears current
>
> Let's express gratitude for the attempt...

**AI**:
> "Thank you, `README.md`, for welcoming newcomers with guidance. You've evolved, and the docs must evolve too."
>
> The question is: Should we fix these broken references, or is it time to update the README entirely?

**User**:
> Fix the references. The README is mostly good, just those two links are stale.

**AI**:
> Got it. I'll update the broken links to point to current documentation or remove them if the content is elsewhere.
>
> *[AI updates README.md]*
>
> ✓ Fixed: Link to `./docs/api-reference.md` (current documentation)
> ✓ Removed: Stale code block reference to `setup.sh`
>
> Category 3 complete! Your documentation now accurately represents reality.

---

### Phase 5: Category 4 - Configuration (Komono)

**AI**:
> Category 4: Configuration (Komono).
>
> Scattered configuration files that may be orphaned from tools you no longer use.
>
> I found 2 orphaned configs:
>
> 1. `.babelrc` (55% confidence)
>    - 456 days old
>    - babel not in dependencies
>    - Your build setup has changed since then
>
> 2. `jest.config.js` (55% confidence)
>    - 312 days old
>    - jest not in devDependencies
>    - Test config from old setup
>
> Both have medium-low confidence. Config files sometimes serve as documentation or are referenced by tool chains in non-obvious ways.
>
> Let's express gratitude...

**AI**:
> "Thank you, `.babelrc`, for transforming our code for the browser. We've moved to a different build system."
>
> "Thank you, `jest.config.js`, for the test environment you helped create. We've migrated testing approaches."

**AI**:
> Hold these in your mind. Does `.babelrc` still serve any purpose - perhaps as reference for the old build? What about `jest.config.js` - could it be useful if you ever need to configure testing differently?

**User**:
> No, both are old configs. The project switched to Vite months ago. Safe to delete.

**AI**:
> Got it. Releasing both with gratitude...
>
> *[AI deletes both config files]*
>
> ✓ Deleted: `.babelrc`
> ✓ Deleted: `jest.config.js`
>
> Category 4 complete! Your configuration is now streamlined to your current tools.

---

### Phase 6: Category 5 - Legacy Code (Sentimental)

**AI**:
> Final category: Category 5 - Legacy Code (Sentimental).
>
> This is the hardest category. These items require careful, honed judgment. They may hold sentimental value or represent significant past work.
>
> I found 1 item:
>
> 1. `src/legacy/AuthManager.js` (40% confidence)
>    - Contains deprecation markers: `// @deprecated`, `TODO: remove after migration`
>    - 234 days old
>    - Note: This is NOT in your protected `src/auth/` directory, but is in the general `src/` area
>    - Very low confidence - this is legacy code that got you to where you are today
>
> Let's express deep gratitude for this foundational code...

**AI**:
> "Deep gratitude to this code for getting the project to where it is today. You were the first authentication implementation. You handled OAuth, JWT, session management - everything. The new auth system stands on your foundation. Your lessons remain even as you go."

**AI**:
> Hold this in your mind. This is the sentimental category. Before we decide, ask:
>
> - Does this code still serve a purpose as reference?
> - Could there be future features where this design would help?
> - Is it truly no longer referenced anywhere?
> - What did you learn from this implementation that's still valuable?
>
> This code has served you well. It's okay to let it go, and it's okay to keep it if it still sparks joy.

**User**:
> *[User pauses, thinks for a moment]*
>
> You know what... it taught us a lot about JWT handling and session management. But the new auth system handles all that. It's not referenced anywhere. Let it go.

**AI**:
> A brave decision. Releasing with gratitude...
>
> "Thank you, `AuthManager.js`, for every authentication flow you handled. Your patterns and approaches live on in the new system. Rest knowing you were essential to getting here."
>
> *[AI deletes the legacy file]*
>
> ✓ Deleted: `src/legacy/AuthManager.js`
>
> Category 5 complete! The sentimental decisions are often the hardest, but also the most meaningful.

---

### Phase 7: Celebration

**AI**:
> All categories complete! Let me generate your cleanup proposal and summarize what was accomplished.
>
> *[AI creates CLEANUP_PROPOSAL.md with full summary]*
>
> **Summary:**
>
> - **Total items addressed**: 11
> - **Files deleted**: 10
> - **Dependencies removed**: 1
> - **Documentation fixed**: 2 references
> - **Space recovered**: 28.4 KB
>
> **Click Point Progress**: 100%
>
> ---

**AI**:
> Your repository has been transformed.
>
> You went from a codebase with accumulated cruft to a focused authentication system where every file serves a clear purpose.
>
> The sacred order has been followed:
> ✓ Clothing (Dead Files) - 7 items released
> ✓ Books (Dependencies) - 1 package removed
> ✓ Papers (Documentation) - 2 references fixed
> ✓ Komono (Configuration) - 2 orphaned configs removed
> ✓ Sentimental (Legacy) - 1 foundational piece released
>
> **You've reached your click point.**

**AI**:
> *[AI pauses for a moment of completion]*
>
> "Life truly begins only after you have put your codebase in order."
>
> Enjoy the clarity! Every remaining file in this repository sparks joy.

**User**:
> Thank you! That was... actually kind of beautiful. I feel lighter.

**AI**:
> The ceremony is complete whenever you're ready. Until next time, keep tidying by category, hold each item in your mind, and ask: does this spark clarity?
>
> *[End of ceremony]*

---

## Key Patterns in This Example

### 1. User Controls the Process
- User sets ideal codebase vision
- User protects critical directories
- User makes all deletion decisions
- AI never acts without explicit permission

### 2. Sacred Order is Maintained
- Each category is completed before moving to next
- Builds decision skill progressively
- Easier categories first, harder ones later

### 3. Gratitude is Not Optional
- Every item (even low confidence) gets gratitude message
- Gratitude is read aloud before action
- This creates psychological closure

### 4. Confidence Levels Guide Behavior
- ≥80%: Presented as Quick Wins, user simply approves
- 50-79%: Presented as "Decisions Needed" with questions
- <50%: Presented as contemplation, especially for sentimental items

### 5. Celebration is Essential
- Ending acknowledges the transformation
- "Click Point" language reinforces completion
- User's choice is validated

---

## Why This Works

### Psychological Benefits
- **Reduces guilt** - Code served a purpose; you acknowledge it before letting go
- **Builds confidence** - Starting with easy wins builds momentum
- **Avoids overwhelm** - One category at a time is manageable
- **Provides closure** - The ceremony has clear beginning and end

### Practical Benefits
- **Systematic** - Sacred order prevents cherry-picking easy stuff only
- **Safe** - Never auto-deletes, git preserves history
- **Adaptable** - User can override at any point
- **Educational** - Learn about what tools/dependencies exist

---

## Tips for Your Own Ceremony

1. **Be honest about your vision** - What do you actually want?
2. **Protect what's important** - Identify must-keep files upfront
3. **Take your time on sentimental items** - Category 5 deserves reflection
4. **Let the AI handle gratitude** - It's harder to express after deciding to delete
5. **Celebrate completion** - You reached your click point!

---

For more examples and documentation:
- [sample_output.json](sample_output.json) - Raw analysis JSON
- [sample_cleanup_proposal.md](sample_cleanup_proposal.md) - Generated proposal
- [README.md](../README.md) - User-facing guide
- [SKILL.md](../SKILL.md) - Complete reference

