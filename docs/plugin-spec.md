# Plugin Specification

This document defines the technical requirements for building a community plugin for Red Hat AI Enterprise (RHAIE). Every plugin must have a visible UI presence in the RHAIE dashboard — backend-only services are out of scope.

## plugin.yaml Schema

Every plugin repo must include a `plugin.yaml` at the root. This file declares metadata, dashboard integration, and deployment configuration.

### Required Fields

```yaml
name: my-plugin
version: 0.1.0
description: Short description of what this plugin does

maintainer:
  name: Your Name
  email: you@example.com
  github: your-github-handle

rhaie_compatibility:
  min_version: "2.14"
  tested_versions: ["2.14", "2.15"]

helm:
  chart_path: chart/

nav:
  label: My Plugin
  icon: puzzle-piece
  url_pattern: /community/my-plugin

deployment_model: per-project  # per-project, cluster-shared, or both

rbac:
  required_roles: []
  cluster_roles: false
```

### Optional Fields

```yaml
dependencies:
  - name: postgresql
    version: ">=14"
    required: true

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

telemetry:
  opt_in: true
  metrics_endpoint: /metrics

support:
  docs: https://github.com/your-org/your-plugin/docs
  issues: https://github.com/your-org/your-plugin/issues
  slack: https://slack.example.com/channel

screenshots:
  - path: docs/screenshots/overview.png
    caption: Plugin overview page
```

## Deployment Models

Plugins declare their deployment model in `plugin.yaml`. A plugin can support one or both models — if both are supported, the admin or user chooses which to use at install time.

### Per-Project (`per-project`)

User clicks "Add to project" in the dashboard. The dashboard triggers a Helm install into the user's namespace. Multiple instances can exist across different projects.

**Examples**: Quickstart Launcher, Hermes, OpenShift Skills

**Characteristics**:
- Runs in user's namespace with user's ServiceAccount
- User provisions and manages their own instances
- Each project can have its own instance

### Cluster-Shared (`cluster-shared`)

Admin runs Helm install once. The plugin appears in the left nav for all authorized users. A single deployment serves multiple users.

**Examples**: Brewet, GPU Booking, LibreChat

**Characteristics**:
- Runs in dedicated `rhaie-community-plugins` namespace
- Admin provisions once, users share
- Multi-tenancy approach is up to the plugin author (TBD — best practices will be defined as the ecosystem matures)

### Both (`both`)

Plugin supports either deployment model. The Helm chart accepts a value to switch between per-project and cluster-shared modes. Use this when the plugin can reasonably work both ways.

## Repository Structure

```
your-plugin/
├── plugin.yaml           # Required: metadata and configuration
├── chart/                # Required: Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── rbac.yaml
├── deploy/
│   ├── instance.yaml     # What gets created when user "adds" plugin
│   └── rbac.yaml         # Permissions plugin needs
├── docs/
│   ├── README.md         # Required: with screenshots and install guide
│   └── screenshots/
└── src/                  # Plugin UI code if applicable
```

## Container Images

Plugin images are hosted at [`quay.io/rh-ai-community-plugins`](https://quay.io/organization/rh-ai-community-plugins). Use your plugin name as the image repository:

```
quay.io/rh-ai-community-plugins/<your-plugin-name>:<version>
```

## Helm Chart Requirements

- **Helm only**. No Kustomize, no custom scripts, no Makefiles.
- **Clean removal**: Uninstalling the Helm release must remove all resources. No orphaned ConfigMaps, Secrets, PVCs, or CRDs.
- **Configurable via values.yaml**: All environment-specific settings must be configurable through Helm values, not hardcoded.
- See [helm-requirements.md](helm-requirements.md) for detailed Helm guidelines.

## Security & Isolation

### Container Security
- **Non-root**: Containers must run as non-root user (UID 1001+)
- **UBI9 base images**: Preferred but not required
- **Read-only rootfs**: Recommended
- **No privileged mode**: Containers must not run privileged

### Namespace Isolation
- Per-project plugins run in the user's namespace
- Cluster-shared plugins run in `rhaie-community-plugins` namespace with minimal RBAC
- Plugins cannot access RHAIE internal databases or APIs directly

### RBAC
- All required permissions must be declared in `plugin.yaml`
- No ClusterRole bindings unless explicitly justified and documented
- Admin reviews RBAC requirements before approving the plugin
- Dashboard filters left nav visibility based on user's RBAC permissions

See [security-guidelines.md](security-guidelines.md) for the full security policy.

## RBAC Model

Access control uses OpenShift RBAC:

1. Admin installs the plugin cluster-wide (or user installs per-project)
2. Admin grants access to specific users/groups
3. Dashboard filters left nav based on user's permissions
4. For cluster-shared plugins, multi-tenancy is the plugin author's responsibility — the approach is not prescribed

## Plugin Lifecycle

See the [Charter — Plugin Lifecycle](../CHARTER.md#plugin-lifecycle) for the full progression and stability guarantees. To change status, open a PR updating your entry in `plugins.yaml`.

## Forward Compatibility

Plugins declare which RHAIE versions they have been tested against. Authors are responsible for testing against new releases and updating `rhaie_compatibility.tested_versions`. See the [Charter — Forward Compatibility](../CHARTER.md#forward-compatibility) for more detail.

### CI Validation (Recommended)

Add this to your plugin's CI to validate against declared RHAIE versions:

```bash
# For each declared version, verify Helm chart renders cleanly
for version in $(yq '.rhaie_compatibility.tested_versions[]' plugin.yaml); do
  helm template . | oc apply --dry-run=client -f -
done
```

## What Plugins Cannot Do

See the [Charter — What Is NOT a Community Plugin](../CHARTER.md#what-is-not-a-community-plugin) for the full list of restrictions.
