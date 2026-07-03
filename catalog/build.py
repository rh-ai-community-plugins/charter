#!/usr/bin/env python3
"""Build the plugin catalog static site from plugins.yaml."""

import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

STATUS_ORDER = {
    "stable-candidate": 0,
    "beta": 1,
    "experimental": 2,
    "deprecated": 3,
    "archived": 4,
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT, "_site")


def load_plugins():
    with open(os.path.join(ROOT, "plugins.yaml")) as f:
        data = yaml.safe_load(f)
    plugins = data.get("plugins", [])
    plugins.sort(key=lambda p: (STATUS_ORDER.get(p.get("status", ""), 99), p.get("name", "")))
    return plugins


def build():
    plugins = load_plugins()
    env = Environment(loader=FileSystemLoader(CATALOG_DIR), autoescape=True)
    template = env.get_template("template.html")
    html = template.render(plugins=plugins, plugin_count=len(plugins))
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w") as f:
        f.write(html)
    icon_src = os.path.join(CATALOG_DIR, "icon.png")
    if os.path.exists(icon_src):
        shutil.copy2(icon_src, os.path.join(OUTPUT_DIR, "icon.png"))
    screenshots_src = os.path.join(CATALOG_DIR, "screenshots")
    if os.path.isdir(screenshots_src):
        screenshots_dst = os.path.join(OUTPUT_DIR, "screenshots")
        if os.path.exists(screenshots_dst):
            shutil.rmtree(screenshots_dst)
        shutil.copytree(screenshots_src, screenshots_dst)
    print(f"Built catalog with {len(plugins)} plugins -> {out_path}")


if __name__ == "__main__":
    build()
