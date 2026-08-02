# Volume 3 validation and release boundary

The Cloud Build job runs deterministic unit/evaluation gates first, then installs
exactly ADK v2.6.1 to compile the real graph. Its only declared artifact is the
deterministic evaluation report in a build-ID-scoped evidence location. It does
not deploy, modify IAM, or create an Agent Runtime resource.

Run locally:

~~~bash
python3 delivery/volume-3-adk/validate_delivery.py delivery/volume-3-adk/cloudbuild.yaml
python3 -m unittest discover -s delivery/volume-3-adk -p 'test_*.py' -v
~~~

The customer release workflow must add independent approval, source revision,
artifact digest/SBOM/provenance, vulnerability policy, exact target project and
region, runtime identity, and rollback evidence. The guarded sandbox deployment
script is documented with the example application; it is intentionally absent
from this validation build.
