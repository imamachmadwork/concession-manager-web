# concession-manager-web

Playwright + pytest (Python) test suite for concession-manager-web, scaffolded
from [playwright-python-template](https://github.com/imamachmadwork/playwright-python-template):
Page Object Model, an API client, Allure reporting, per-team bug reports,
known-bug regression tracking, and a ready-to-go CI workflow.

The example suite ships with a placeholder `HomePage` test pointed at
`https://concessions.roamstay.com` and a backend example pointed at
`https://jsonplaceholder.typicode.com` — replace both with real page objects
and API tests once the app's actual pages/endpoints are mapped out.

## Quickstart

```bash
uv sync
uv run playwright install chromium
uv run pytest
```

`uv` manages its own Python interpreter per `.python-version` /
`requires-python`, so your system Python version doesn't matter. If you
don't have `uv`, install it first: `curl -LsSf https://astral.sh/uv/install.sh | sh`.

## Configuration

Copy `.env.example` to `.env` and fill in whatever you need — every value
has a working default (see `.env.example`), so an empty `.env` is fine to
start.

`PYTEST_BASE_URL` can also be passed on the command line:

```bash
uv run pytest --base-url=http://localhost:3000
```

## Running tests

```bash
uv run pytest                     # run everything: frontend + backend
uv run pytest -m frontend         # UI/E2E tests only (tests/e2e)
uv run pytest -m backend          # API tests only (tests/api)
uv run pytest -m smoke            # only smoke-tagged tests
uv run pytest --headed            # run with a visible browser
uv run pytest --browser=firefox   # run against Firefox instead of Chromium
```

Failed frontend tests automatically save a screenshot, video, and trace under
`test-results/`. View a trace with:

```bash
uv run playwright show-trace test-results/<test-folder>/trace.zip
```

## Project structure

```
pages/           # Page Object Model classes (one per page/component), used by tests/e2e
clients/         # API client wrappers (httpx), used by tests/api
tests/e2e/       # Frontend/UI test specs (Playwright)
tests/api/       # Backend/API test specs (httpx)
scripts/         # generate_bug_report.py — per-team markdown bug reports
conftest.py      # Shared fixtures + auto-tagging of Allure epic/feature labels
credentials.py   # Per-account/org credentials, read from env vars
```

Add new pages under `pages/`, wire them up as fixtures in
`tests/e2e/conftest.py`, and write specs under `tests/e2e/`. Add new API
tests the same way under `tests/api/`, using the `api_client` fixture from
`tests/api/conftest.py`.

## Next steps

1. **Replace the example page/test** — `pages/home_page.py` and
   `tests/e2e/test_home_page.py` are stand-ins; swap in the app's real
   landing page once mapped out. Same for `clients/api_client.py`'s default
   URL and `tests/api/test_example_api.py`.
2. **Wire up authentication, if needed** — `credentials.py` holds one entry
   per account/org, read from env vars. `tests/e2e/conftest.py` and
   `tests/api/conftest.py` each have a commented-out
   session-scoped-login-then-reuse pattern (storage state for the browser,
   a bearer token for the API client) — uncomment and adapt the endpoint/URL
   details to the app's actual login flow, or delete if not needed.
3. **Push to GitHub and set CI variables** — `PYTEST_BASE_URL`, `API_BASE_URL`
   (Settings → Secrets and variables → Actions → Variables) and
   `DEFAULT_EMAIL`/`DEFAULT_PASSWORD` as **secrets** if auth is wired up.

## Reporting (Allure)

Every test run writes [Allure](https://allurereport.org/) results to
`allure-results/`. Each test is auto-tagged (see `conftest.py`) with:

- **epic** — the test suite/module, e.g. `Sign In`, `Home Page`
- **feature** — the layer, `Frontend` or `Backend`

so the same report can be sliced either by suite or by layer, with zero
per-test decorators needed. View it locally (requires the `allure` CLI —
`brew install allure` or `npm i -g allure-commandline`):

```bash
uv run pytest
allure serve allure-results   # generates + opens the HTML report in one step
```

Or generate the static HTML report and serve it yourself:

```bash
uv run pytest || true
allure generate allure-results --clean -o allure-report
python3 -m http.server 4567 --directory allure-report
```

Then open `http://localhost:4567`. Don't open `allure-report/index.html`
directly via `file://` — the report fetches its data over HTTP and won't
render.

`allure-results/` (raw data) and `allure-report/` (generated HTML) are both
gitignored — they're build output, regenerated every run, never committed.

## Bug reports (per team)

After a run, `scripts/generate_bug_report.py` reads `allure-results/` and
writes one markdown doc per Frontend/Backend + suite combination under
`reports/bug-reports/<feature>/<suite>.md` — e.g. a sign-in bug that only
fails on the backend produces `reports/bug-reports/backend/sign-in.md`,
scoped to just what the backend team needs to act on. Run it manually:

```bash
uv run pytest || true
uv run python scripts/generate_bug_report.py
```

## Known-bug tracking

Tests for tracked, pre-existing product bugs can be marked
`@pytest.mark.known_bug` (see `pyproject.toml`). They should assert the
*correct* expected behavior, so they fail until each bug is fixed
upstream — that's the point: once someone fixes the underlying bug, the
test starts passing on its own with no follow-up needed to "remember" to
re-check it. They're excluded from the main `pytest` run
(`pytest -m "not known_bug"`, see CI below) so a tracked issue doesn't fail
every PR check, and instead run on their own via `pytest -m known_bug`.

There are no `known_bug`-marked tests yet — add the first one when there's
an actual tracked bug to pin down, e.g.:

```python
@pytest.mark.known_bug
def test_logout_actually_clears_session(authenticated_page):
    # Bug: logout redirects to /login but the session cookie isn't cleared,
    # so back-button navigation still shows authenticated content.
    # Tracked in JIRA-1234.
    ...
```

## CI

`.github/workflows/playwright.yml` runs the suite on GitHub Actions:

- on push to `main`
- on pull requests targeting `main`
- nightly at 03:00 UTC (catches drift on the live/staging site)
- manually via the "Run workflow" button (`workflow_dispatch`)

It installs dependencies with `uv`, installs Chromium, runs `pytest`
(frontend + backend), generates per-team bug reports, generates the Allure
HTML report, and uploads as build artifacts: screenshots/videos/traces (on
failure), the bug reports (on failure), and the **Allure HTML report**
(always — this is the report document, generated whether the run passed or
failed).

`known_bug`-marked tests run in a separate **`known-bugs`** job, after the
main `test` job, with `continue-on-error: true` so they never block a PR —
its own Allure report and bug-report artifacts (`known-bugs-allure-report`,
`known-bugs-report`) keep them visible without blocking anything. Until a
`known_bug` test is added, that job will show as failed (pytest exits non-zero
on "no tests collected") — harmless, since it's non-blocking; the badge just
won't go green until either a known-bug test is added or the job is removed.

To view a downloaded `allure-report` (or `known-bugs-allure-report`)
artifact: unzip it and serve the folder (its `index.html` won't work opened
directly via `file://` — the report fetches its data over HTTP). E.g.
`python3 -m http.server 4567 --directory allure-report` then open
`http://localhost:4567`.

To point CI at different targets than the defaults, set repository/environment
variables (Settings → Secrets and variables → Actions → Variables):
`PYTEST_BASE_URL`, `API_BASE_URL`. If authentication is wired up, add
`DEFAULT_EMAIL`/`DEFAULT_PASSWORD` as **secrets** (not variables).
