# Security Guidelines

Community plugins run alongside RHAIE core. These rules protect the platform and its users.

## Container Security

| Requirement | Rule |
|-------------|------|
| Root user | Forbidden. Run as UID 1001+ |
| Privileged mode | Forbidden |
| Privilege escalation | Forbidden (`allowPrivilegeEscalation: false`) |
| Root filesystem | Read-only recommended (`readOnlyRootFilesystem: true`) |
| Base image | UBI9 preferred |
| Ports | Non-privileged only (8080, 8443). Never below 1024 |

## Namespace Isolation

- **Per-project plugins**: Run in the user's namespace with the user's ServiceAccount. Cannot access other namespaces.
- **Cluster-shared plugins**: Run in the dedicated `rhaie-community-plugins` namespace with minimal RBAC.
- Plugins must never access namespaces they don't own.

## RBAC

- Declare all required permissions in `plugin.yaml`. Undeclared permissions will be denied.
- No ClusterRole bindings unless explicitly justified in the PR description. Expect pushback.
- Charter maintainers review all RBAC requirements before approving a plugin.
- Plugins that request excessive permissions will be rejected.

## Data Access

- Plugins **cannot** access RHAIE's internal databases or APIs.
- Plugins **cannot** read or modify other users' projects or data.
- If a plugin needs shared state, it must manage its own storage (e.g., its own database or ConfigMap).

## Network

- Plugins should not require cluster-wide network policies.
- Egress to external services is allowed but must be documented in `plugin.yaml` (e.g., phoning home to a vendor API).
- Ingress is handled through OpenShift Routes created by the Helm chart.

## Secrets

- Never hardcode credentials in container images or Helm templates.
- Use Kubernetes Secrets or external secret management.
- Document any secrets the plugin requires in the installation guide.

## Reporting Vulnerabilities

If you discover a security issue in a community plugin, file a private issue in the plugin's repository or contact the maintainer directly.
