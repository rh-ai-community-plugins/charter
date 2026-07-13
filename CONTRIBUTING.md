# Contributing a Community Plugin

Anyone can submit a plugin to the catalog: Red Hat engineers, partners, or individuals.

## Before You Start

Read the [Charter](CHARTER.md) to understand what community plugins are (and aren't). Your plugin must:

- Be open source under the Apache-2.0 license
- Deploy via Helm chart
- Be completely removable without affecting RHAIE core
- Include a README with screenshots and installation guide
- Have a `plugin.yaml` at the repo root with all required metadata (see [plugin spec](docs/plugin-spec.md))
- Declare RHAIE version compatibility in `plugin.yaml`
- Follow OpenShift best practices (non-root containers, UBI9 base images preferred)

See [docs/plugin-spec.md](docs/plugin-spec.md) for the full technical specification and [docs/examples/example-plugin.yaml](docs/examples/example-plugin.yaml) for a starter template.

## Submission Process

1. **Prepare your plugin repo** with the required structure (see [plugin spec](docs/plugin-spec.md#repository-structure))
2. **Fork this repo** (`rh-ai-community-plugins/charter`)
3. **Add your plugin** to `plugins.yaml`:

```yaml
  - name: your-plugin-name
    repo: https://github.com/your-org/your-plugin
    status: experimental
    maintenance: community
    last_updated: 2026-07-13
```

All other metadata (description, version, compatibility, deployment model, etc.) is read from your plugin's own `plugin.yaml` — no need to duplicate it here. CI will fetch and validate your `plugin.yaml` automatically.

1. **Open a pull request** using the PR template
1. **Wait for review** — CI validates your entry and cross-validates your plugin.yaml, then the Red Hat team reviews for policy compliance

## What Happens After Submission

- **CI checks**: YAML validation, required fields, link checks, plugin.yaml cross-validation
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
