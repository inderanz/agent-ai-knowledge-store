# Governed cell module

This module configures workload resources inside an existing project. It creates no Agent Platform Preview/Pre-GA resource and no secret value.

The runtime identity receives only Firestore access, Secret Manager access to the subject-hash secret, Telemetry trace writing, and Service Usage consumption. Build and deploy identities are separate. Plan/apply roles are caller-supplied and reject primitive Owner/Editor roles at the root boundary.

