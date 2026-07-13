# Plugin Specification

This document defines the technical requirements for building a community plugin for Red Hat AI Enterprise (RHAIE). Every plugin must have a visible UI presence in the RHAIE dashboard — backend-only services are out of scope.

## plugin.yaml Schema

Every plugin repo must include a `plugin.yaml` at the root. This is a flat YAML file (not a Kubernetes resource — do not wrap it in `apiVersion`/`kind`/`metadata`). It declares metadata, dashboard integration, and deployment configuration.

### Required Fields

```yaml
name: my-plugin                    # unique plugin identifier (kebab-case)
displayName: My Plugin             # human-readable name for dashboard sidebar and catalog
description: Short description of what this plugin does
version: 0.1.0

maintainer:
  name: Your Name
  github: your-github-handle

rhoai_compatibility:
  min_version: "3.4.0"
  tested_versions: ["3.4.0"]

deployment_model: per-project      # per-project, cluster-shared, or both

image:
  repository: quay.io/rh-ai-community-plugins/my-plugin
  tag: "0.1.0"

install:
  method: automatic                # automatic | assisted | manual
  helm:
    chart_path: chart/                                          # where the chart source lives in the repo
    registry: oci://quay.io/rh-ai-community-plugins/my-plugin  # published OCI chart
  prerequisites: []                # optional: things that must exist before install
  instructions: https://github.com/your-org/my-plugin/docs/INSTALL.md  # optional for automatic, required for manual

remote:
  type: module-federation
  spec:
    name: myPlugin                 # Module Federation container name (camelCase)
    scope: myPlugin                # must match name above
    remoteEntry: https://<your-openshift-route>/remoteEntry.js
    paths:
      - type: route
        path: /my-plugin           # must match route prefix in extensions.ts
        extensions:
          - myPlugin/extensions    # {scope}/extensions
      - type: icon
        path: myPlugin/Icon        # {scope}/Icon

rbac:
  required_roles: []
  cluster_roles: false             # set to true only if absolutely necessary
```

### Optional Fields

```yaml
bff_image:                         # only if using Backend-For-Frontend pattern
  repository: quay.io/rh-ai-community-plugins/my-plugin-bff
  tag: "0.1.0"

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
  repo: https://github.com/your-org/your-plugin
  docs: https://github.com/your-org/your-plugin/docs
  issues: https://github.com/your-org/your-plugin/issues

screenshots:
  - path: docs/screenshots/overview.png
    caption: Plugin overview page
```

## Install Methods

The `install.method` field determines how the catalog UI handles installation:

| Method | Behavior in catalog UI |
|--------|----------------------|
| `automatic` | Catalog plugin runs `helm install` with defaults. One-click install. |
| `assisted` | Catalog shows a configuration form (driven by `install.helm.values_schema` if provided), then runs `helm install` with user-provided values. |
| `manual` | Catalog shows a link to `install.instructions` — no install button. For plugins requiring operators, CRDs, external dependencies, etc. |

### Prerequisites

Optional list of requirements the catalog plugin can check before enabling the install button:

```yaml
install:
  prerequisites:
    - type: api
      name: kueue.x-k8s.io/v1beta1
      description: Kueue operator must be installed
    - type: secret
      name: my-credentials
      namespace: my-plugin
      description: API credentials for the external service
```

### Values Schema

For `assisted` installs, provide a JSON Schema that drives the configuration form:

```yaml
install:
  method: assisted
  helm:
    chart_path: chart/
    registry: oci://quay.io/rh-ai-community-plugins/my-plugin
    values_schema: chart/values.schema.json
```

## Dashboard Integration (remote)

The `remote` section configures Module Federation so the RHOAI dashboard can load the plugin at runtime. Every community plugin needs this.

- **`name` / `scope`**: Must match (camelCase). This is the Module Federation container name used in the dashboard's dynamic remote loading.
- **`remoteEntry`**: URL to the plugin's `remoteEntry.js`. This is cluster-specific — it depends on the OpenShift route created by the Helm chart.
- **`paths`**: Declares what the plugin exposes:
  - `type: route` — a page route in the dashboard. `path` must match the route prefix in your `extensions.ts`. `extensions` lists the Module Federation exposed modules.
  - `type: icon` — the plugin's navigation icon, loaded via Module Federation from the plugin itself.

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

- Runs in dedicated `rhoai-community-plugins` namespace
- Admin provisions once, users share
- Multi-tenancy approach is up to the plugin author (TBD — best practices will be defined as the ecosystem matures)

### Both (`both`)

Plugin supports either deployment model. The Helm chart accepts a value to switch between per-project and cluster-shared modes. Use this when the plugin can reasonably work both ways.

## Repository Structure

```text
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

```text
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
- Cluster-shared plugins run in `rhoai-community-plugins` namespace with minimal RBAC
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

Plugins declare which RHOAI versions they have been tested against. Authors are responsible for testing against new releases and updating `rhoai_compatibility.tested_versions`. See the [Charter — Forward Compatibility](../CHARTER.md#forward-compatibility) for more detail.

### CI Validation (Recommended)

Add this to your plugin's CI to validate against declared RHAIE versions:

```bash
# For each declared version, verify Helm chart renders cleanly
for version in $(yq '.rhoai_compatibility.tested_versions[]' plugin.yaml); do
  helm template . | oc apply --dry-run=client -f -
done
```

## What Plugins Cannot Do

See the [Charter — What Is NOT a Community Plugin](../CHARTER.md#what-is-not-a-community-plugin) for the full list of restrictions.
