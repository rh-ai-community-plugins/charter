#!/usr/bin/env python3
"""Aggregate plugin metadata from individual plugin repos.

Reads the lightweight plugins.yaml registry, fetches each plugin's own
plugin.yaml from its GitHub repo, validates schema conformance, and
produces a merged catalog.json suitable for the catalog site and the
future in-product catalog plugin.
"""

import json
import os
import re
import urllib.request
import urllib.error
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT, "_site")

REQUIRED_PLUGIN_FIELDS = [
    "name", "displayName", "description", "version", "maintainer",
    "rhoai_compatibility", "deployment_model", "install", "remote", "rbac",
]

VALID_DEPLOYMENT_MODELS = ["per-project", "cluster-shared", "both"]
VALID_INSTALL_METHODS = ["automatic", "assisted", "manual"]

STATUS_ORDER = {
    "stable-candidate": 0,
    "beta": 1,
    "experimental": 2,
    "deprecated": 3,
    "archived": 4,
}


def load_registry():
    """Load the lightweight plugins.yaml registry."""
    with open(os.path.join(ROOT, "plugins.yaml")) as f:
        data = yaml.safe_load(f)
    return data.get("plugins", [])


def github_raw_url(repo_url, branch="main", path="plugin.yaml"):
    """Convert a GitHub repo URL to a raw content URL."""
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/?", repo_url)
    if not match:
        return None
    return f"https://raw.githubusercontent.com/{match.group(1)}/{branch}/{path}"


def fetch_plugin_yaml(repo_url):
    """Fetch and parse plugin.yaml from a plugin's GitHub repo."""
    url = github_raw_url(repo_url)
    if not url:
        return None, f"Cannot parse GitHub URL: {repo_url}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "rh-ai-catalog-builder"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return yaml.safe_load(resp.read()), None
    except (urllib.error.URLError, urllib.error.HTTPError, yaml.YAMLError) as e:
        return None, str(e)


def validate_plugin_yaml(plugin_data, name):
    """Validate a plugin's plugin.yaml has required fields and valid values."""
    errors = []
    for field in REQUIRED_PLUGIN_FIELDS:
        if field not in plugin_data:
            errors.append(f"missing required field '{field}'")

    dm = plugin_data.get("deployment_model")
    if dm and dm not in VALID_DEPLOYMENT_MODELS:
        errors.append(f"invalid deployment_model '{dm}'")

    install = plugin_data.get("install", {})
    method = install.get("method")
    if method and method not in VALID_INSTALL_METHODS:
        errors.append(f"invalid install.method '{method}'")

    if method == "manual" and not install.get("instructions"):
        errors.append("install.instructions is required when method is 'manual'")

    helm = install.get("helm", {})
    if install and not helm.get("chart_path"):
        errors.append("install.helm.chart_path is required")
    if install and not helm.get("registry"):
        errors.append("install.helm.registry is required")

    compat = plugin_data.get("rhoai_compatibility", {})
    tested = compat.get("tested_versions", [])
    if not tested:
        errors.append("rhoai_compatibility.tested_versions must not be empty")

    return errors


def discover_screenshot(name):
    """Check if a screenshot exists for this plugin in catalog/screenshots/."""
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        path = os.path.join(CATALOG_DIR, "screenshots", f"{name}{ext}")
        if os.path.exists(path):
            return f"screenshots/{name}{ext}"
    return None


def build_helm_install(plugin_data):
    """Build a helm install command from the install block."""
    install = plugin_data.get("install", {})
    helm = install.get("helm", {})
    registry = helm.get("registry")
    name = plugin_data.get("name", "")
    if registry:
        return f"helm install {name} {registry}"
    return None


def aggregate():
    """Aggregate registry entries with fetched plugin metadata."""
    registry = load_registry()
    catalog = []
    warnings = []

    for entry in registry:
        name = entry.get("name", "unknown")
        repo = entry.get("repo", "")

        merged = {
            "name": name,
            "repo": repo,
            "status": entry.get("status", "experimental"),
            "maintenance": entry.get("maintenance", "community"),
            "last_updated": entry.get("last_updated", ""),
        }

        plugin_data, err = fetch_plugin_yaml(repo)
        if err:
            warnings.append(f"{name}: could not fetch plugin.yaml ({err})")
            merged["_fetch_error"] = True
        else:
            errors = validate_plugin_yaml(plugin_data, name)
            if errors:
                for e in errors:
                    warnings.append(f"{name}: {e}")

            merged["displayName"] = plugin_data.get("displayName", name)
            merged["description"] = plugin_data.get("description", "")
            merged["version"] = plugin_data.get("version", "")
            merged["deployment_model"] = plugin_data.get("deployment_model", "")

            maintainer = plugin_data.get("maintainer", {})
            merged["maintainer_name"] = maintainer.get("name", "")
            merged["maintainer_github"] = maintainer.get("github", "")

            compat = plugin_data.get("rhoai_compatibility", {})
            merged["rhoai_versions"] = compat.get("tested_versions", [])

            merged["install"] = plugin_data.get("install", {})
            merged["remote"] = plugin_data.get("remote", {})
            merged["rbac"] = plugin_data.get("rbac", {})
            merged["support"] = plugin_data.get("support", {})

            merged["helm_install"] = build_helm_install(plugin_data)

        screenshot = discover_screenshot(name)
        if screenshot:
            merged["screenshot_url"] = screenshot

        catalog.append(merged)

    catalog.sort(key=lambda p: (
        STATUS_ORDER.get(p.get("status", ""), 99),
        p.get("name", ""),
    ))

    if warnings:
        print("Aggregation warnings:")
        for w in warnings:
            print(f"  - {w}")

    return catalog, warnings


def write_catalog_json(catalog):
    """Write the aggregated catalog to _site/catalog.json."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "catalog.json")
    with open(out_path, "w") as f:
        json.dump({"plugins": catalog}, f, indent=2, default=str)
    print(f"Wrote catalog.json with {len(catalog)} plugins -> {out_path}")
    return out_path


if __name__ == "__main__":
    catalog, warnings = aggregate()
    write_catalog_json(catalog)
