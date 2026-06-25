# Contributing a Community Plugin

Anyone can submit a plugin to the catalog: Red Hat engineers, partners, or individuals.

## Before You Start

Read the [Charter](CHARTER.md) to understand what community plugins are (and aren't). Your plugin must:

- Be open source under the Apache-2.0 license
- Deploy via Helm chart
- Be completely removable without affecting RHAIE core
- Include a README with screenshots and installation guide
- Declare RHAIE version compatibility
- Follow OpenShift best practices (non-root containers, UBI9 base images preferred)

See [docs/plugin-spec.md](docs/plugin-spec.md) for the full technical specification.

## Plugin Repository Structure

See [Plugin Specification — Repository Structure](docs/plugin-spec.md#repository-structure) for the required layout and [docs/examples/example-plugin.yaml](docs/examples/example-plugin.yaml) for a complete `plugin.yaml` template.

## Submission Process

1. **Prepare your plugin repo** with the required structure above
2. **Fork this repo** (`rh-ai-community-plugins/charter`)
3. **Add your plugin** to `plugins.yaml`:

```yaml
  - name: your-plugin-name
    description: Short description of what it does
    repo: https://github.com/your-org/your-plugin
    status: experimental
    maintenance: community
    deployment_model: per-project  # per-project, cluster-shared, or both
    rhoai_versions: ["3.4.0"]      # required — at least one tested RHOAI version
    maintainer: your-github-handle
    last_updated: 2026-06-24
```

> **Note**: `rhoai_versions` must not be empty. Declare at least one RHOAI version your plugin has been tested against. This must match the `rhoai_compatibility.tested_versions` field in your plugin's own `plugin.yaml`. CI will reject PRs with empty version declarations.

4. **Open a pull request** using the PR template
5. **Wait for review** — CI validates your entry, then the Red Hat team reviews for policy compliance

## What Happens After Submission

- **CI checks**: YAML validation, required fields, link checks, security scans
- **Red Hat review**: Policy compliance only — we don't review technical quality or code
- **Merge**: Approved PRs merge and your plugin appears in the catalog
- **First-come, first-served**: Plugin names are unique. If your name conflicts, you'll need to pick a different one

## Plugin Lifecycle

New plugins start as **Experimental**. You can request a status change via PR. See the [Charter — Plugin Lifecycle](CHARTER.md#plugin-lifecycle) for the full progression (Experimental → Beta → Stable-Candidate → Deprecated → Archived).

## Removing Your Plugin

Maintainers can archive their plugin anytime by opening a PR to change the status to `deprecated` (then `archived` after 90 days).

Red Hat may remove plugins that violate security policies, impersonate core features, are abandoned (maintainer stops responding to issues and PRs for 6+ months), or create legal issues.

## Support Model

**Community plugins are not supported by Red Hat.** You are responsible for:

- Responding to issues in your plugin's GitHub repository
- Maintaining compatibility with RHAIE upgrades
- Setting your own response times and fix priorities

## Questions

Open an issue in this repository or join the community discussion.
