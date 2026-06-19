# Publishing `convex-sdk` to PyPI

Releases publish via **PyPI Trusted Publishing** (OIDC) — no API token or secret is
stored in GitHub. The workflow (`.github/workflows/publish.yml`) is ready but **inert**
until a trusted publisher is configured on PyPI (one-time setup below).

## One-time setup on PyPI

1. Sign in at <https://pypi.org> as a maintainer of the `convex-sdk` project.
2. Go to the project → **Settings → Publishing** (or
   <https://pypi.org/manage/project/convex-sdk/settings/publishing/>).
3. Under **Add a new trusted publisher → GitHub**, fill in:
   - **Owner:** `Convex-Dev`
   - **Repository:** `convex-api-py`
   - **Workflow name:** `publish.yml`
   - **Environment:** `pypi`
4. Save.

> `convex-sdk` is a fresh PyPI project; the trusted publisher above authorises the first
> tagged release to create and populate it — no manual bootstrap publish is needed. (The
> predecessor package `convex-api-py` remains frozen at 0.3.1.)

Optionally protect the `pypi` GitHub environment
(repo **Settings → Environments → pypi**) with required reviewers so a human approves
each release.

## Cutting a release

1. Update `CHANGELOG.md` (promote the `Unreleased` section to the new version).
2. Bump the version and tag in one step:
   ```bash
   bumpversion patch   # or: minor / major
   ```
   `bumpversion` updates `setup.py` + `convex_sdk/__init__.py`, commits, and creates a
   `v{version}` tag (see `.bumpversion.cfg`).
3. Push the tag:
   ```bash
   git push --follow-tags
   ```
4. The `v*` tag triggers `publish.yml`, which builds the sdist + wheel and publishes to
   PyPI via trusted publishing.

## References

- PyPI Trusted Publishing: <https://docs.pypi.org/trusted-publishers/>
- `pypa/gh-action-pypi-publish`: <https://github.com/pypa/gh-action-pypi-publish>
