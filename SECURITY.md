# Security Policy

## Supported Versions

Security updates are applied only to the latest release.

## Reporting a Vulnerability

If you discover a security vulnerability in KonMari, please report it to us responsibly. We take security vulnerabilities seriously.

**How to Report:**

1. **Do not** create a public GitHub issue
2. **Do** use [GitHub's private vulnerability reporting](https://github.com/Hmbown/KonMari/security/advisories/new)
   - Include a detailed description of the vulnerability
   - Include steps to reproduce the vulnerability
   - Include any potential impact or exploit

**What Happens Next:**

- We will acknowledge receipt of your report within 48 hours
- We will provide a detailed response within 7 days
- We will provide regular updates on our progress towards a fix
- We will notify you when a fix is released

## Security Best Practices for Users

### File Deletion

KonMari is designed to be safe, but users should:

- **Review before deleting** - Always review the cleanup proposal before approving deletions
- **Check confidence scores** - Higher confidence (≥80%) indicates safer deletions
- **Keep git history** - Deleted files remain in git history for recovery
- **Test after cleanup** - Verify functionality after any major deletions

### Repository Privacy

- The tool analyzes local file systems only
- No data is transmitted externally
- Analysis runs locally on your machine
- No cloud services or external APIs are contacted

### Permissions

The tool requires:
- Read access to files in your repository
- Execute access to git commands (if repository is version-controlled)
- File system write permissions for creating CLEANUP_PROPOSAL.md
- Write access to delete files (only with explicit approval)

## Known Security Considerations

### Confidence Scoring

The confidence scoring system (0-100) is based on heuristics:
- Not deterministic or foolproof
- Users should always review recommendations
- Lower confidence scores (<70%) require human judgment

### File Pattern Matching

Pattern-based detection may have false positives:
- Experimental branches or WIP files may be flagged
- Recently modified files with stale patterns are deprioritized
- Users can explicitly mark files to keep

### Session Artifacts

Claude Code session artifacts are detected:
- These are intentionally temporary files
- Designed for single-session use
- Safe to delete when session concludes

## Dependencies

KonMari uses only Python standard library:
- No external dependencies
- No pip packages required
- Reduces supply chain attack surface

## Security Updates

We will:
- Publicly announce security vulnerabilities
- Provide clear remediation guidance
- Release security fixes promptly
- Update CHANGELOG.md with security notes

## Contact

For security questions or concerns:
- Security: [Report a vulnerability](https://github.com/Hmbown/KonMari/security/advisories/new)
- GitHub Issues: Use "security" label for non-critical concerns
- Repository: https://github.com/Hmbown/KonMari

---

Thank you for helping keep KonMari and its users safe!

