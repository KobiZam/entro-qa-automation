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
