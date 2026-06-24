# Community Plugins Project - Progress Notes

**Date**: 2026-06-24  
**Participants**: Erwan Granger, Claude

## Project Overview

This repo will become the **charter** for Red Hat AI Enterprise (RHAIE) Community Plugins initiative. It contains documentation and a registry/catalog that lists available community plugins.

**Purpose**: Create a clear separation between stable, supported RHAIE core features and experimental, high-velocity community plugins. Plugins extend the RHAIE dashboard without destabilizing the core product.

## Key Decisions

### Repo Scope
- **What this repo contains**: Documentation (manifesto, guidelines) + registry/catalog of plugins
- **What lives elsewhere**: 
  - Technical integration layer (how plugins load) → RHAIE core product
  - Shared tooling (templates, CI scripts) → separate `plugin-template` repo
  - Individual plugins → their own repos in `rh-ai-community-plugins` org

### Repo Naming
- Current: `first-repo`
- **Decided**: Rename to `charter`
- URL will be: `github.com/rh-ai-community-plugins/charter`

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
- Dashboard extensions only - no operators, no cluster-level changes without admin approval

## Acceptance Criteria

### Required
- Open source (Apache-2.0/MIT)
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
- Plugins handle their own multi-tenancy (shared vs per-user instances)

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

Field: `deployment_model: per-project | cluster-shared`

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

These will be the first batch to convert/validate the model:

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

## Charter Repo Structure

Agreed structure:
```
charter/
├── README.md (landing page)
├── MANIFESTO.md (the philosophy doc) ✅ DONE
├── CONTRIBUTING.md (how to submit a plugin)
├── plugins.yaml (the registry)
├── docs/
│   ├── plugin-spec.md (plugin.yaml schema)
│   ├── helm-requirements.md
│   ├── security-guidelines.md
│   └── examples/
│       └── example-plugin.yaml
├── .github/
│   ├── workflows/
│   │   └── validate-pr.yml
│   └── PULL_REQUEST_TEMPLATE/
│       └── add-plugin.md
└── site/ (generated GitHub Pages)
```

## MANIFESTO.md

**Status**: ✅ Completed and pushed to GitHub

Covers 8 sections:
1. Why This Exists - philosophy of core vs community separation
2. Principles - velocity, community-driven, clean separation, safe removal, namespace isolation
3. What Is a Community Plugin - 5 defining characteristics
4. What Is NOT a Community Plugin - explicit boundaries
5. Plugin Lifecycle - experimental → beta → stable-candidate → deprecated → archived
6. Support Model - unsupported by Red Hat, maintainer-driven
7. Governance - adding/removing plugins, conflict resolution
8. Adoption Into Core - how plugins graduate (Kubernetes model)
9. Technical Requirements - high-level overview

Key changes made:
- Changed all references from RHOAI to RHAIE
- Added note: "RHAIE is the combination of Red Hat OpenShift AI and OpenShift"
- Tone: practical engineer-to-engineer, 2 pages, scannable

## Next Steps

### Immediate (Not Yet Started)
1. **Technical spec** (`docs/plugin-spec.md`)
   - Define exact `plugin.yaml` schema
   - Helm chart requirements
   - RBAC patterns
   - Dashboard integration contract

2. **Repo scaffolding**
   - Create directory structure
   - Set up CI workflows
   - PR templates
   - GitHub Pages config

3. **Registry file** (`plugins.yaml`)
   - Define schema
   - Add pilot plugins (or start empty)

4. **Contributing guide** (`CONTRIBUTING.md`)
   - Step-by-step submission process
   - Quality checklist
   - PR template usage

### Medium-term
5. **Pilot plugin conversion**
   - Pick Brewet or Sardeenz
   - Convert to validate the model
   - Document conversion process
   - Use as reference implementation

6. **Dashboard integration**
   - Meeting with dashboard specialist scheduled
   - Discuss "hack" approach for demo
   - Plan proper integration path

### Deferred Decisions
- Exact dashboard integration mechanism (waiting on specialist meeting)
- How RHAIE dashboard discovers plugins at runtime (CRDs vs YAML fetch vs static)
- Dashboard "hack" implementation for demos

## Tracking Metrics

Internally, Red Hat will track:
- Plugin utilization/adoption
- Usage patterns
- Feature popularity

Purpose: Inform decisions about which plugins to adopt into core product.

## Important Notes

- RHAIE = Red Hat AI Enterprise = Red Hat OpenShift AI + OpenShift
- First-come, first-served for plugin names
- 90-day deprecation notice required (unless security risk)
- Red Hat can adopt plugins with maintainer agreement
- Plugins remain in community catalog during core integration work
