# Entro Security — QA Automation (Playwright + Python)

A production‑grade automation framework for Entro's management console, covering:
- Login/Logout
- Navigation
- Accounts (add form validation, change environment, filtering)
- Exposed Inventory (filtering, drawers, bulk operations)
- Vaulted Secrets (filtering, export, drawers)
- Risks (load, severity filter)
- Settings (load)

> **No logs policy**: This project intentionally avoids Python logging and console prints.

## 🏁 Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
playwright install chromium
cp .env.example .env   # Or set env vars in CI
pytest -n auto --maxfail=1
```

### Environment variables
- `BASE_URL` (default: `https://qa.entro.security/`)
- `EMAIL` (default: `user1@qa.interview`)
- `PASSWORD` (default: `Entr0T@sk!`)
- `HEADLESS` (1/0, default 1)

## 🧱 Architecture
- **Pytest** for test orchestration and markers
- **Playwright (sync)** for resilient web automation
- **Page Objects** under `pages/` for maintainability
- **Selectors utils** to concentrate selector strategy
- **Shared storage state** to login once per worker → fast & isolated tests
- **Artifacts on failure** (screenshot + HTML) saved to `.test-results/` (no logs)
- **Parallel** via `pytest-xdist` ensures one failing test doesn’t block others

## 🧪 Running specific suites
```bash
pytest -m smoke
pytest -m accounts -n 4
pytest tests/test_vaulted_secrets_export.py -q
```

## 📦 CI (GitHub Actions)
- Securely provide `EMAIL` and `PASSWORD` using repository **Secrets**.
- See `.github/workflows/ci.yml`.

## ➕ Adding new tests
1. Create a Page Object in `pages/` if a new screen.
2. Use role‑based selectors (`get_by_role`) and text; avoid brittle CSS.
3. Add tests under `tests/` with meaningful markers.
4. Keep tests idempotent; prefer read‑only validations for shared QA envs.

## ♻️ Stability tips
- Wrap navigation clicks with `expect_navigation(wait_until="networkidle")`.
- Prefer `expect(locator).to_be_visible()` over arbitrary waits.
- Keep each test independent (no cross‑test data dependencies).
