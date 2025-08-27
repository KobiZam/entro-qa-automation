import os
from pathlib import Path
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, expect
from pages.login_page import LoginPage

# Load environment
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://qa.entro.security/")
EMAIL = os.getenv("EMAIL") or "user1@qa.interview"
PASSWORD = os.getenv("PASSWORD") or "Entr0T@sk!"
HEADLESS = os.getenv("HEADLESS", "1") == "1"

ARTIFACT_DIR = Path(".test-results")
ARTIFACT_DIR.mkdir(exist_ok=True)

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def storage_state(tmp_path_factory, browser: Browser):
    # Login once per worker and share storage state to speed up tests while keeping them isolated.
    storage = tmp_path_factory.mktemp("state") / "state.json"
    context = browser.new_context()
    page = context.new_page()
    LoginPage(page, BASE_URL).open()
    LoginPage(page, BASE_URL).login(EMAIL, PASSWORD)
    context.storage_state(path=storage)
    context.close()
    return storage

@pytest.fixture()
def context(browser: Browser, storage_state) -> BrowserContext:
    ctx = browser.new_context(storage_state=storage_state)
    yield ctx
    ctx.close()

@pytest.fixture()
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()

# Pytest hook: capture artifacts on failure (no logging)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            test_name = item.name.replace("/", "_")
            Path(".test-results").mkdir(exist_ok=True)
            page.screenshot(path=f".test-results/{test_name}.png", full_page=True)
            html = page.content()
            Path(f".test-results/{test_name}.html").write_text(html)
