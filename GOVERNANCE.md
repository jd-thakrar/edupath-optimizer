# Governance

## Maintainers

Maintainers are repository administrators and designated reviewers in this project.

Current maintainer responsibilities:
- Triage and prioritize issues
- Review and merge pull requests
- Manage releases and security responses
- Maintain documentation and contribution standards

## Decision-Making

- Small/isolated changes: single maintainer approval.
- Medium/high impact changes: at least two maintainer approvals.
- Security-sensitive changes: maintainer review plus passing CI checks.

## Review and Merge Policy

- All PRs must pass required CI checks before merge.
- PRs should be scoped to one concern.
- Backward-incompatible changes must be documented clearly.

## Release Cadence

- Patch releases: as needed for bug/security fixes.
- Minor releases: grouped functional improvements.
- Major releases: planned with migration notes.

## Contribution Scope

In scope:
- Model quality, explainability, and reliability improvements
- API and frontend bug fixes
- Documentation, testing, and deployment reliability improvements

Out of scope unless discussed first:
- Breaking schema/API redesigns
- Large framework rewrites
- Significant scope expansion unrelated to academic risk optimization

## Labels Convention

Recommended labels for issue triage:
- `bug`
- `enhancement`
- `good first issue`
- `help wanted`

## Maintainer Response Policy

- Initial issue response target: **5 business days**
- Initial PR response target: **5 business days**

## Branch Protection Policy

Apply these rules on default branch:
1. Require pull request before merging
2. Require at least one review approval
3. Require status checks to pass (CI workflow)
4. Disallow force pushes
5. Disallow branch deletion
