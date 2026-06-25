# ADR: Initial Charter Decisions

**Date**: 2026-06-24
**Status**: Accepted

This document records the founding decisions for the Red Hat AI Community Plugins initiative. It captures the rationale behind the project scope, technical standards, and governance model established in the [Charter](../../CHARTER.md).

---

## Project Overview

The `charter` repo is the home for the Red Hat AI Enterprise (RHAIE) Community Plugins initiative. It contains documentation (charter, guidelines) and a registry/catalog that lists available community plugins.

**Purpose**: Create a clear separation between stable, supported RHAIE core features and experimental, high-velocity community plugins. Plugins extend the RHAIE dashboard without destabilizing the core product.

## Key Decisions

### Repo Scope
- **What this repo contains**: Documentation (charter, guidelines) + registry/catalog of plugins
- **What lives elsewhere**:
  - Technical integration layer (how plugins load) → RHAIE core product
  - Shared tooling (templates, CI scripts) → separate `plugin-template` repo
  - Individual plugins → their own repos in `rh-ai-community-plugins` org

### Registry Format
**Decision**: Structured YAML + auto-generated GitHub Pages site
- `plugins.yaml` contains structured data (name, repo, description, icon, version, status)
- CI auto-generates a GitHub Pages site from the YAML
- Both humans (browse site) and potentially RHAIE dashboard (consume YAML) can use it

### Plugin Discovery (deferred)
Dashboard integration mechanism to be discussed with dashboard specialist later. For now, will "hack" the dashboard to demo plugins before proper integration exists.

## Core vs Community Boundaries

### Core RHAIE Keeps
- Stable AI platform primitives with support SLAs
- Workbenches, pipelines, model serving, MaaS
- Foundation Red Hat supports, tests, documents, and maintains

### Community Plugins Are
- Integrations (LLM playgrounds, vector DBs, monitoring dashboards)
- Experiments (new notebook types, custom accelerators)
- Vendor plugins (W&B, MLflow UI)
- Utilities (cost calculators, resource cleaners)
- Dashboard extensions only — every plugin must have a visible UI. No operators, no cluster-level changes without admin approval

## Audience & Framing

This charter is primarily a leadership proposal — designed to get formal backing and resources from Red Hat leadership. Once approved, it becomes the contributor-facing governance document.

**Success criteria (6-month horizon)**:
- Leadership approval and formal backing
- 3+ community plugins live and usable on a real RHAIE instance
- Compelling demo at a Red Hat event or customer meeting

## Acceptance Criteria

### Required
- Open source under the Apache-2.0 license
- Basic docs (README with screenshots + install YAML)
- Declared RHAIE version compatibility
- Maintainer contact

### Strongly Recommended
- Security scanned
- Non-root containers
- UBI9 base images (OpenShift best practices)

### Allowed
- Anyone can submit (Red Hat, partners, individuals)
- Commercial plugins allowed if source is open (can phone home to vendor services)

## Technical Standards

### Plugin Metadata
Track in catalog:
- Status (experimental/beta/stable-candidate/deprecated/archived)
- RHAIE version compatibility
- Maintenance level (red-hat/community/archived)
- Last updated date

Example:
```yaml
- name: brewet
  status: beta
  maintenance: red-hat
  rhaie_versions: ["2.14+", "2.15+"]
  last_updated: 2026-06-01
```

### RBAC Model
**Decision**: User/group-based via OpenShift RBAC
- Admin installs plugin cluster-wide
- Grants access to specific users/groups
- Dashboard filters left nav based on user's permissions
- Plugins handle their own multi-tenancy (approach TBD — not prescribed; best practices will emerge as the ecosystem matures)

### Contribution Workflow
**Decision**: Self-service PR with approval
- Plugin maintainer opens PR adding entry to `plugins.yaml`
- PR template enforces required fields
- CI validates schema, checks links, runs security scans
- Red Hat team reviews for policy compliance (not technical quality)
- Approved PRs auto-deploy to GitHub Pages catalog

### Required Repo Structure
Each plugin repo must have:
```
plugin-repo/
├── plugin.yaml           # Metadata: name, icon, description, nav config
├── deploy/
│   ├── operator.yaml     # Optional: if plugin includes operator
│   ├── instance.yaml     # What gets created when user "adds" plugin
│   └── rbac.yaml         # Permissions plugin needs
├── docs/
│   ├── README.md
│   └── screenshots/
└── src/                  # Plugin UI code if applicable
```

**Critical requirement**: Helm only for installation. No Kustomize, no fancy scripts, no Makefiles.

### plugin.yaml Fields

**Required**:
- name, version, description
- maintainer (email/GitHub)
- RHAIE compatibility
- Helm chart path
- Nav config (label, icon, URL pattern)
- Scoping (project-scoped vs cluster-scoped)

**Optional**:
- Dependencies
- Resource limits
- Telemetry opt-in
- Support links
- Screenshots

### Deployment Model
**Decision**: Plugin declares its deployment model in `plugin.yaml`

Field: `deployment_model: per-project | cluster-shared | both`

A single plugin can support both models. When set to `both`, the Helm chart accepts a value to switch modes.

- **Per-project plugins**: User clicks "Add to project" → dashboard triggers Helm install into user's namespace
- **Cluster-shared plugins**: Admin runs Helm install once → plugin appears in left nav for authorized users

Examples:
- OpenShell: per-project (3 instances in different projects)
- LibreChat: cluster-shared (single pod for 124 users)

### Security & Isolation
**Decision**: Strict namespace isolation + no elevated privileges

- Per-project plugins run in user's namespace with user's ServiceAccount
- Cluster-shared plugins run in dedicated `rhaie-community-plugins` namespace with minimal RBAC
- Plugin must declare required RBAC in `plugin.yaml` (admin reviews before approving)
- No ClusterRole bindings unless explicitly justified
- Container security: non-root (UID 1001+), read-only rootfs, no privileged mode
- Plugins cannot access RHAIE database or internal APIs directly

## Pilot Plugins

These are the first batch to validate the model:

1. **Brewet** (formerly ODH TEC)
   - Repo: https://github.com/rh-aiservices-bu/odh-tec
   - Will be renamed to "brewet"
   - Owner: rh-aiservices-bu

2. **Sardeenz**
   - Repo: https://github.com/rh-aiservices-bu/sardeenz
   - Owner: rh-aiservices-bu

3. **Hermes**
   - Repo: https://github.com/aicatalyst-team/hermes-openshift
   - Owner: aicatalyst-team

4. **GPU Booking App**
   - Repo: https://github.com/rhai-code/gpu-booking-app-plugin
   - Owner: rhai-code

5. **OpenShift Skills**
   - Repo: https://github.com/rhai-code/rhai-openshift-skills-plugin
   - Owner: rhai-code

6. **Quickstart Launcher** (new)
   - Will deploy quickstarts from: https://github.com/rh-ai-quickstart/
   - Deploys into user-level project
   - Needs to be built from scratch

### Conversion Ownership
- **Erwan's team converts**: Brewet, Sardeenz (direct control, use as reference implementations)
- **Build from scratch**: Quickstart Launcher (3rd reference implementation)
- **External teams convert**: Hermes (aicatalyst-team), GPU Booking + Skills (rhai-code)
  - Provide them with documentation and reference implementations first

## Tracking Metrics

Internally, Red Hat will track:
- Plugin utilization/adoption
- Usage patterns
- Feature popularity

Purpose: Inform decisions about which plugins to adopt into core product.

## Key Rules

- RHAIE = Red Hat AI Enterprise = Red Hat OpenShift AI + OpenShift
- First-come, first-served for plugin names
- 90-day deprecation notice required (unless security risk)
- Red Hat can adopt plugins with maintainer agreement
- Plugins remain in community catalog during core integration work

## Decisions from Charter Review (2026-06-24)

- **UI requirement**: Every plugin must have a visible dashboard presence. Backend-only services are out of scope.
- **Abandonment**: Defined as maintainer non-responsiveness to issues/PRs for 6+ months (not commit inactivity).
- **Graduation to core**: Possible but rare. Lifecycle states signal maturity, not a pipeline to product inclusion.
- **Forward compatibility**: No commitments from RHAIE team yet. Plugins declare tested versions; RC access and CI templates are future goals.
- **Licensing**: Apache-2.0 required for all plugins.
- **Dual deployment**: A plugin can support both per-project and cluster-shared modes.
- **Multi-tenancy**: No prescribed approach for cluster-shared plugins — left to plugin authors.
- **Security review**: Charter maintainers review RBAC justifications, not a formal security team.
- **Quay org**: `quay.io/rh-ai-community-plugins` exists and is controlled by the initiative owner.
- **Marketplace vision**: Long-term goal is an in-product catalog for plugin discovery and installation.
- **Initiative ownership**: Driven by Erwan Granger / Customer Adoption and Innovation team. Not co-owned with RHAIE product team.
- **Demo approach**: Standalone demo cluster with plugins installed. Dashboard integration can be hacked (iframe or DevTools) if needed.

## Deferred Decisions

- Exact dashboard integration mechanism (TBD with RHAIE dashboard team)
- How RHAIE dashboard discovers plugins at runtime (CRDs vs YAML fetch vs static)
- Multi-tenancy best practices for cluster-shared plugins
- In-product plugin catalog UX
