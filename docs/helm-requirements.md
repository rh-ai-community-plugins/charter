# Helm Chart Requirements

Community plugins must deploy via Helm. No exceptions.

## Rules

- **Helm only**. No Kustomize, no custom scripts, no Makefiles.
- **Clean removal**: `helm uninstall` must remove all resources created by the chart. No orphaned ConfigMaps, Secrets, PVCs, or CRDs.
- **Configurable via `values.yaml`**: All environment-specific settings (image tags, resource limits, replicas, namespace) must be configurable through Helm values.
- **No hooks that create persistent state**: Helm hooks for Jobs are fine, but don't create resources that survive uninstall.

## Container Images

Plugin images are hosted at `quay.io/rh-ai-community-plugins/`. Use your plugin name as the image repository:

```yaml
image:
  repository: quay.io/rh-ai-community-plugins/my-plugin
  tag: "0.1.0"
```

## OpenShift Best Practices

- **Non-root containers**: Run as UID 1001+. Never use `runAsUser: 0`.
- **UBI9 base images**: Preferred. If not UBI9, document why.
- **Security context**:
  ```yaml
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
  ```
- **Resource limits**: Always set requests and limits in `values.yaml`.
- **Port 8080**: Use non-privileged ports (8080, 8443). Never bind to ports below 1024.

## Chart Structure

```
chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── route.yaml          # OpenShift Route for external access
│   ├── rbac.yaml           # ServiceAccount, Role, RoleBinding
│   └── _helpers.tpl
└── README.md               # Chart-specific documentation
```

## Testing

Before submitting, verify:
1. `helm template . | oc apply --dry-run=client -f -` succeeds
2. `helm install` and `helm uninstall` leave no orphaned resources
3. The plugin works with every version listed in `rhoai_compatibility.tested_versions`

### Ongoing Compatibility

When RHOAI release candidates are announced:
1. Run your Helm chart validation against the RC
2. Test the plugin UI in the RHOAI dashboard
3. Update `tested_versions` in your `plugin.yaml` and `rhoai_versions` in `plugins.yaml` via PR
