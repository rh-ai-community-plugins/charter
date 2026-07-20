#!/usr/bin/env python3
"""Build the plugin catalog static site.

Uses the aggregation pipeline to fetch plugin metadata from individual
repos, then renders the catalog HTML from the merged data.
"""

import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

from aggregate import aggregate, write_catalog_json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT, "_site")


def build():
    plugins, warnings = aggregate()
    write_catalog_json(plugins)

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
