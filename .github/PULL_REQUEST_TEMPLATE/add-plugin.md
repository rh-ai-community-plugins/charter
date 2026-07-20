## New Plugin Submission

**Plugin name**:
**Plugin repo**:

### Checklist

- [ ] Added entry to `plugins.yaml` with all required fields (name, repo, status, maintenance, last_updated)
- [ ] Plugin repo has required structure (`plugin.yaml`, `chart/`, `docs/`)
- [ ] `plugin.yaml` has all required fields (see [plugin spec](../../docs/plugin-spec.md))
- [ ] README exists with screenshots and installation guide
- [ ] RHOAI version compatibility declared in `plugin.yaml` (`rhoai_compatibility.tested_versions` is non-empty)
- [ ] `remote` section present in `plugin.yaml` for dashboard integration
- [ ] `install` section present in `plugin.yaml` with `method`, `helm.chart_path`, and `helm.registry`
- [ ] Helm chart included and `helm template` succeeds
- [ ] RBAC requirements declared in `plugin.yaml`
- [ ] Maintainer contact provided in `plugin.yaml`
- [ ] License is Apache-2.0
- [ ] Containers run as non-root (UID 1001+)
- [ ] No ClusterRole bindings (or justification provided below)

### ClusterRole Justification (if applicable)

_Explain why your plugin needs ClusterRole bindings._

### Additional Notes

_Anything reviewers should know about this plugin._
