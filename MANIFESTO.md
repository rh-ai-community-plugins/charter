# Red Hat AI Community Plugins Charter

## Why This Exists

AI moves fast. Enterprise platforms need stability. These forces create tension.

Red Hat AI Enterprise (RHAIE) solves this by separating concerns:

- **Core product**: Stable ML platform primitives with support SLAs. Workbenches, pipelines, model serving, data science projects. The foundation Red Hat supports and maintains.
- **Community plugins**: Everything else. Integrations, experiments, vendor tools, utilities. High velocity, short-lived when needed, no support burden on the core.

Community plugins let us deliver the speed AI demands while protecting the stability enterprises require. They extend RHAIE without destabilizing it.

> **Note**: Red Hat AI Enterprise (RHAIE) is the combination of Red Hat OpenShift AI and OpenShift platform capabilities.

## Principles

**Velocity over perfection.** Plugins can be experimental, exploratory, even temporary. If something stops being useful, it can be deprecated cleanly.

**Community-driven.** Anyone can contribute a plugin: Red Hat engineers, partners, individuals. The barrier to entry is low. Quality comes from transparency and user choice, not gatekeeping.

**Clean separation.** Plugins are clearly marked in the dashboard. Users know what's supported and what isn't. Admins can enable/disable plugins without touching core functionality.

**Safe to remove.** Plugins must be completely removable without affecting RHAIE core. No database migrations, no leftover state, no dependencies that break core features.

**Namespace isolation.** Plugins run with minimal permissions and cannot access other users' data or compromise cluster security.

## What Is a Community Plugin?

A community plugin is a dashboard extension that:

1. **Integrates cleanly** - Appears in the RHAIE dashboard left nav with a clear "Community Plugin" tag
2. **Respects RBAC** - Admins control which users/groups see which plugins
3. **Deploys via Helm** - Standard installation, upgrade, and removal
4. **Declares its scope** - Either per-project (user provisions instances) or cluster-shared (admin provisions once, users share)
5. **Is self-contained** - Can be completely removed without affecting core RHAIE

### Examples of Community Plugins

- **Brewet** (ODH TEC): Technical enablement catalog and demos
- **Sardeenz**: Specialized visualization tools
- **Hermes**: OpenShift integration utilities  
- **GPU Booking App**: Resource scheduling and calendar
- **OpenShift Skills**: AI-powered cluster operations
- **Quickstart Launcher**: One-click deployment of quickstart templates

## What Is NOT a Community Plugin

Plugins **cannot**:

- Replace or override core RHAIE features
- Require cluster-admin privileges to use (installation is different - admins install, users use)
- Access RHAIE's internal databases or APIs directly
- Modify other users' projects or data
- Run privileged containers or bypass security policies
- Create dependencies that would break core features if the plugin is removed

If it needs to be in core to work, it's not a community plugin.

## Plugin Lifecycle

Plugins progress through these states:

### Experimental
New plugins start here. Expect breaking changes, incomplete features, possible deprecation. Use at your own risk.

### Beta
Stabilizing. API may still change, but maintainers commit to migration paths. Suitable for non-critical workloads.

### Stable
Production-ready. Maintainers commit to backward compatibility and deprecation notices. Suitable for critical workloads if you accept the community support model.

### Deprecated
No longer recommended. Security fixes only. Maintainers must give 90 days notice before moving to archived.

### Archived
No longer maintained. Remains in catalog for historical reference but is not installable. No support, no updates.

## Support Model

**Community plugins are unsupported by Red Hat.**

- Users file issues in the plugin's GitHub repository
- Plugin maintainers decide response times and fix priorities
- Red Hat may track adoption metrics internally but provides no SLAs
- Plugins may break with RHAIE upgrades; maintainers are responsible for compatibility
- Use community forums, Slack channels, or plugin-specific support channels

If you need Red Hat support, use core RHAIE features only.

## Governance

### Adding a Plugin

Anyone can submit a plugin to the catalog:

1. Create a plugin repository with required structure (see technical requirements)
2. Open a PR adding your plugin to `plugins.yaml`
3. Automated CI validates schema, checks links, runs security scans
4. Red Hat team reviews for policy compliance (not technical quality)
5. Approved PRs merge and appear in the catalog

First-come, first-served. Later plugins with similar functionality must differentiate clearly.

### Removing a Plugin

Maintainers can archive their plugin anytime. Red Hat can remove plugins that:

- Violate security policies
- Impersonate core features
- Are abandoned (no maintainer response for 6+ months)
- Create legal or compliance issues

Removed plugins get 90-day deprecation notice unless they pose immediate security risk.

### Conflict Resolution

If two plugins provide overlapping functionality:
- Both can coexist if clearly differentiated
- Users and admins choose which to use
- Red Hat does not pick winners; market adoption decides

If technical conflicts arise (port collisions, resource names, etc.), later plugin must adapt.

## Adoption Into Core

Red Hat may adopt community plugins into the core product. This requires:

- Maintainer agreement
- Code/license review and transfer
- Red Hat QE validation
- Full support commitment from Red Hat engineering

Adoption follows the Kubernetes graduation model: incubating → graduated. Plugins don't disappear from the community catalog when adopted; they remain available while the core integration is built.

Internally, Red Hat tracks plugin adoption metrics to inform these decisions.

## Technical Requirements

All plugins must:

1. **Have a `plugin.yaml` manifest** - Declares metadata, dashboard integration, deployment model
2. **Deploy via Helm chart** - Standard installation method, no custom scripts or Makefiles
3. **Follow OpenShift best practices** - Non-root containers (UID 1001+), UBI9 base images preferred
4. **Include documentation** - README with screenshots, installation guide, RHAIE version compatibility
5. **Declare RBAC requirements** - What permissions the plugin needs
6. **Support clean removal** - Uninstalling the Helm release removes all resources

See `docs/plugin-spec.md` for detailed technical requirements.

## Getting Started

- **For plugin users**: Browse the catalog, talk to your admin about enabling plugins
- **For admins**: See installation guides in each plugin's repository
- **For plugin authors**: Read `CONTRIBUTING.md` to submit your plugin

Questions? Open an issue in this repository or join the community discussion.

---

*This is a living document. Propose changes via pull request.*
