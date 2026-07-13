# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

This is the **charter repository** for the Red Hat AI Community Plugins initiative. It is NOT a code project — it is a governance, registry, and catalog repo. It contains:

- The charter and guidelines defining what community plugins are (and aren't) for Red Hat AI Enterprise (RHAIE)
- `plugins.yaml` — the plugin registry (source of truth for available plugins)
- A static GitHub Pages catalog site generated from that registry
- Documentation: plugin spec, Helm requirements, security guidelines

Individual plugins live in their own repositories (see `plugins.yaml` for links). The seed/reference plugin is [hello-world](https://github.com/rh-ai-community-plugins/hello-world).

## Key Terminology

- **RHOAI** = Red Hat OpenShift AI — the product with the dashboard/UI that plugins extend
- **RHAIE** = Red Hat AI Enterprise — a SKU that bundles RHOAI + OpenShift. The charter uses both names; when referring to the dashboard or plugin integration, it means the RHOAI dashboard
- **Community plugin** = a dashboard extension with visible UI in the RHOAI dashboard, deployed via Helm, unsupported by Red Hat
- **Deployment models**: `per-project` (user installs per namespace), `cluster-shared` (admin installs once for all users)
- **Lifecycle states**: experimental → beta → stable-candidate → deprecated → archived

## Common Commands

### Lint markdown

```bash
npm install
npm run lint:md
```

### Validate plugins.yaml

```bash
python3 -c "import yaml; yaml.safe_load(open('plugins.yaml'))"
```

The CI validation logic is inline in `.github/workflows/validate-pr.yml` — it checks required fields (`name`, `repo`, `status`, `maintenance`, `last_updated`), valid enum values, link accessibility, and cross-validates each plugin's own `plugin.yaml` from its repo.

### Build the catalog site

```bash
pip install pyyaml jinja2
python catalog/build.py
```

Output goes to `_site/` (gitignored). The build aggregates metadata by fetching each plugin's `plugin.yaml` from its repo, then renders `catalog/template.html` with the merged data. It also produces `_site/catalog.json` for the future in-product catalog plugin.

## Architecture

### plugins.yaml

Lightweight registry. Each entry has required fields (`name`, `repo`, `status`, `maintenance`, `last_updated`). All other plugin metadata (description, version, compatibility, deployment model, etc.) lives in each plugin's own `plugin.yaml` — single source of truth, no drift. CI enforces this schema on PRs that touch the file.

Valid values:

- `status`: experimental, beta, stable-candidate, deprecated, archived
- `maintenance`: red-hat, community, archived

### Catalog site (catalog/)

- `aggregate.py` — fetches each plugin's `plugin.yaml` from its GitHub repo, validates schema conformance, merges with registry data, auto-discovers screenshots, and produces `_site/catalog.json`
- `build.py` — calls the aggregation pipeline, then renders `template.html` with the merged data, copies screenshots and icon to `_site/`
- `template.html` — single-page HTML using PatternFly 6 CSS (loaded from CDN), with client-side search/filter JS
- `screenshots/` — plugin screenshots auto-discovered by name convention (`{plugin-name}.png`)
- Deployed automatically to GitHub Pages on push to `main` (when `plugins.yaml` or `catalog/**` change)

### CI Workflows (.github/workflows/)

- `validate-pr.yml` — runs on PRs touching `plugins.yaml`: YAML syntax check, required field validation, enum validation, repo link check (non-blocking), cross-validation of each plugin's `plugin.yaml` from its repo
- `deploy-catalog.yml` — runs on push to `main`: aggregates plugin metadata, builds catalog, and deploys to GitHub Pages

### Documentation (docs/)

- `plugin-spec.md` — full `plugin.yaml` schema for plugin authors (different from the registry entry schema in `plugins.yaml`)
- `helm-requirements.md` — Helm chart rules (clean removal, values.yaml configurability, OpenShift security contexts)
- `security-guidelines.md` — container security, namespace isolation, RBAC, data access rules
- `examples/example-plugin.yaml` — starter template for a plugin's own `plugin.yaml`
- `decisions/initial-charter.md` — ADR recording founding decisions and rationale

## Working With This Repo

When adding a plugin entry to `plugins.yaml`, only `name`, `repo`, `status`, `maintenance`, and `last_updated` are needed — all other metadata is fetched from the plugin's own `plugin.yaml` during CI and catalog builds. The PR template at `.github/PULL_REQUEST_TEMPLATE/add-plugin.md` has the submission checklist.

When editing the catalog template, run `python catalog/build.py` and inspect `_site/index.html` to verify rendering.

Container images for plugins are hosted at `quay.io/rh-ai-community-plugins/`.
