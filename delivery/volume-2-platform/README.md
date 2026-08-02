# Governed delivery for the Volume 2 platform service

This companion builds one container, records its digest, creates a Cloud Deploy release, deploys it to development, and requires an explicit Cloud Deploy approval before production. Development and production are separate Cloud Run targets and should be separate governed-cell projects.

The example uses the development governed cell as the delivery control project. Configure the production Terraform stack's `cloud_deploy_control_plane` input before registering the cross-project target. This creates the documented IAM relationships; the customer foundation team must separately decide whether to permit cross-project service-account usage through organization policy.

The checked-in templates contain no customer identifiers. Copy `customer.env.example` outside source control, replace every value, and render the Cloud Deploy configuration:

~~~bash
python3 render_config.py --environment-file /secure/path/customer.env --output rendered/clouddeploy.yaml
python3 validate_delivery.py rendered/clouddeploy.yaml service.yaml cloudbuild.yaml
gcloud deploy apply --file=rendered/clouddeploy.yaml --region=DELIVERY_REGION --project=DELIVERY_PROJECT_ID
~~~

Submit a build with the customer build identity. The configuration uses Cloud Logging because Google requires `CLOUD_LOGGING_ONLY` (or a user-owned logs bucket) when a user-specified Cloud Build service account is selected. The image is declared in Cloud Build's top-level `images` field; Google documents that this is required for generated build provenance and that an explicit `docker push` step does not generate that provenance.

~~~bash
gcloud builds submit . \
  --config=delivery/volume-2-platform/cloudbuild.yaml \
  --project=DELIVERY_PROJECT_ID \
  --region=DELIVERY_REGION \
  --substitutions=COMMIT_SHA=FULL_40_CHARACTER_GIT_SHA,_REGION=ARTIFACT_REGION,_REPOSITORY=agent-platform
~~~

Cloud Build pushes and records the image only after all build steps succeed. Retrieve the resulting digest and build ID from that completed build. Wait until Artifact Analysis has a successful discovery occurrence, then submit the separately authorized release gate:

~~~bash
gcloud builds submit . \
  --config=delivery/volume-2-platform/release.yaml \
  --project=DELIVERY_PROJECT_ID \
  --region=DELIVERY_REGION \
  --substitutions=_IMAGE_URI=ARTIFACT_IMAGE_WITHOUT_TAG,_IMAGE_DIGEST=sha256:64_HEX_DIGEST,_SOURCE_BUILD_ID=CLOUD_BUILD_ID,_SOURCE_REVISION=FULL_40_CHARACTER_GIT_SHA,_PIPELINE=platform-admission
~~~

Submit the release from a clean checkout of `_SOURCE_REVISION`; the Skaffold and Cloud Run manifests are release inputs as well as the container. In the customer automation, reject a dirty tree and verify `git rev-parse HEAD` equals `_SOURCE_REVISION` before submitting this configuration.

The release gate fails closed unless scanning completed successfully, matching Cloud Build provenance exists, and no High or Critical vulnerability occurrence exists. A scanner exception needs a separate, expiring customer risk-acceptance process; this baseline does not silently allowlist it.

The Cloud Run manifest enables Binary Authorization with the target project's default policy. Configure that policy before deployment and use organization policy to require Binary Authorization where appropriate. Google's `built-by-cloud-build` attestor is currently documented as Preview for Cloud Run; a customer that cannot accept that maturity must use a qualified custom attestor or another approved supply-chain control.

Production promotion is deliberately separate:

~~~bash
gcloud deploy releases promote \
  --release=RELEASE_ID \
  --delivery-pipeline=platform-admission \
  --region=DELIVERY_REGION \
  --project=DELIVERY_PROJECT_ID
gcloud deploy rollouts approve ROLLOUT_ID \
  --delivery-pipeline=platform-admission \
  --release=RELEASE_ID \
  --region=DELIVERY_REGION \
  --project=DELIVERY_PROJECT_ID
~~~

Approval is a customer change-control decision. Confirm the rendered manifest, artifact digest, test evidence, vulnerability results, data-classification decision, rollback owner, and maintenance window before approval. Cloud Deploy supports only one Cloud Run service, job, or worker pool per target; use another pipeline for another workload.

## Official evidence

- [Deploy Cloud Run services with Cloud Deploy](https://docs.cloud.google.com/deploy/docs/run-targets)
- [Cloud Deploy service accounts and required roles](https://docs.cloud.google.com/deploy/docs/cloud-deploy-service-account)
- [Cloud Deploy deploy parameters](https://docs.cloud.google.com/deploy/docs/parameters)
- [Cloud Run service YAML reference](https://docs.cloud.google.com/run/docs/reference/yaml/v1)
- [User-specified Cloud Build service accounts](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts)
- [Generate and validate Cloud Build provenance](https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance)
- [Artifact Analysis container scanning](https://docs.cloud.google.com/artifact-analysis/docs/container-scanning-overview)
- [Enable Binary Authorization for Cloud Run](https://docs.cloud.google.com/binary-authorization/docs/run/enabling-binauthz-cloud-run)
- [Cloud Build attestor maturity and behavior](https://docs.cloud.google.com/binary-authorization/docs/deploy-cloud-build)
- [Cloud Deploy official samples at reviewed commit](https://github.com/GoogleCloudPlatform/cloud-deploy-samples/tree/3ea194851eaf3451c0d59ca211f5176e4070b3d6)
