## New Plugin Submission

**Plugin name**: 
**Plugin repo**: 
**Deployment model**: per-project / cluster-shared

### Checklist

- [ ] Added entry to `plugins.yaml` with all required fields
- [ ] Plugin repo has required structure (`plugin.yaml`, `chart/`, `docs/`)
- [ ] README exists with screenshots and installation guide
- [ ] RHOAI version compatibility declared in `plugin.yaml` (`rhoai_compatibility.tested_versions` is non-empty)
- [ ] `rhoai_versions` in `plugins.yaml` matches `tested_versions` in `plugin.yaml`
- [ ] Helm chart included and `helm template` succeeds
- [ ] RBAC requirements declared in `plugin.yaml`
- [ ] Maintainer contact provided
- [ ] License is Apache-2.0
- [ ] Containers run as non-root (UID 1001+)
- [ ] No ClusterRole bindings (or justification provided below)

### ClusterRole Justification (if applicable)

_Explain why your plugin needs ClusterRole bindings._

### Additional Notes

_Anything reviewers should know about this plugin._
