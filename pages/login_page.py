from typing import Union, List
from playwright.sync_api import Page, Frame, expect
import re, time

Ctx = Union[Page, Frame]

def _exists(ctx: Ctx, css: str) -> bool:
    try:
        return ctx.locator(css).count() > 0
    except Exception:
        return False

def _first_css(ctx: Ctx, *csses: str):
    for css in csses:
        loc = ctx.locator(css)
        try:
            if loc.count() > 0:
                return loc.first
        except Exception:
            pass
    return None

def _all_visible(ctx: Ctx, *csses: str) -> List:
    out = []
    for css in csses:
        loc = ctx.locator(css)
        try:
            n = loc.count()
            for i in range(n):
                cand = loc.nth(i)
                try:
                    if cand.is_visible():
                        out.append(cand)
                except Exception:
                    continue
        except Exception:
            continue
    return out

def _click_if_any(ctx: Ctx, *locs) -> bool:
    for loc in locs:
        try:
            if loc and loc.count() > 0:
                loc.first.click()
                return True
        except Exception:
            pass
    return False

def _auth_ctx(page: Page) -> Ctx:
    # main page quick check
    quick = [
        'vaadin-email-field input[slot="input"]', 'descope-email-field input[slot="input"]',
        'input[type="email"]', 'input[autocomplete="username"]', 'input[placeholder="Email"]',
        'vaadin-password-field input[slot="input"]', 'descope-password-field input[slot="input"]',
        'input[type="password"]', 'input[autocomplete="current-password"]',
    ]
    if any(_exists(page, s) for s in quick):
        return page
    # prioritize likely auth frames
    frames = sorted(
        page.frames,
        key=lambda f: 0 if re.search(r'(auth|login|sign[- ]?in|descope)', (f.url or '') + (f.name or ''), re.I) else 1
    )
    for f in frames:
        if any(_exists(f, s) for s in quick) or f.get_by_role("textbox", name=re.compile("email", re.I)).count():
            return f
    # fallback
    for f in page.frames:
        if f.get_by_role("textbox", name=re.compile("email|password", re.I)).count():
            return f
    raise AssertionError("Auth context not found (no email/password inputs detected).")

def _fill_email(ctx: Ctx, email: str):
    email_input = (
        _first_css(ctx, 'vaadin-email-field input[slot="input"]')
        or _first_css(ctx, 'descope-email-field input[slot="input"]')
        or _first_css(ctx, 'input[type="email"]', 'input[autocomplete="username"]', 'input[placeholder="Email"]', 'input[name="email"]')
        or (ctx.get_by_role("textbox", name=re.compile("email", re.I)).first if ctx.get_by_role("textbox", name=re.compile("email", re.I)).count() else None)
    )
    if not email_input:
        raise AssertionError("Email input not found")
    email_input.fill(email)
    return email_input

def _find_password(ctx: Ctx):
    # Return a **visible** password input if possible
    cands = _all_visible(
        ctx, 'vaadin-password-field input[slot="input"]',
             'descope-password-field input[slot="input"]',
             'input[type="password"]', 'input[autocomplete="current-password"]',
             'input[placeholder="Password"]', 'input[name="password"]',
             'input[aria-label*="Password" i"]',
    )
    if cands:
        return cands[0]
    # role fallback
    role = ctx.get_by_role("textbox", name=re.compile("password", re.I))
    return role.first if role.count() > 0 else None

class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url, wait_until="load")
        # Launcher button sometimes reveals widget
        launcher = self.page.get_by_role("button", name=re.compile(r"(sign in|log in)", re.I))
        if launcher.count():
            try:
                launcher.first.click()
            except Exception:
                pass
        self.page.wait_for_load_state("networkidle", timeout=120000)  # was default; now 120s

    def login(self, email: str, password: str):
        # Step 1 — email
        ctx = _auth_ctx(self.page)
        email_input = _fill_email(ctx, email)

        # Progress to step 2
        progressed = False
        try:
            email_input.press("Enter"); progressed = True
        except Exception:
            pass
        self.page.wait_for_load_state("networkidle")

        # Buttons like Continue/Next/Verify
        ctx = _auth_ctx(self.page)
        if not _find_password(ctx):
            progressed = _click_if_any(
                ctx.get_by_role("button", name=re.compile(r"(continue|next|verify|submit|proceed)", re.I)),
                ctx.get_by_text(re.compile(r"(continue|next|verify|submit|proceed)", re.I)).first,
                ctx.locator("button:has-text('Continue')"),
                ctx.locator("vaadin-button:has-text('Continue')"),
                ctx.locator("button[type='submit']")
            ) or progressed
            self.page.wait_for_load_state("networkidle")
            ctx = _auth_ctx(self.page)

        # If widget defaults to OTP/magic link, switch to password mode
        if not _find_password(ctx):
            _click_if_any(
                ctx.get_by_role("button", name=re.compile(r"(use password|password)", re.I)),
                ctx.get_by_role("link",   name=re.compile(r"(use password|password)", re.I)),
                ctx.get_by_text(re.compile(r"(use password|password)", re.I)).first
            )
            self.page.wait_for_load_state("networkidle")
            ctx = _auth_ctx(self.page)

        # Step 2 — password (visible)
        pwd = _find_password(ctx)
        if not pwd:
            try:
                email_input.press("Tab"); time.sleep(0.2)
            except Exception:
                pass
            self.page.wait_for_load_state("networkidle")
            ctx = _auth_ctx(self.page)
            pwd = _find_password(ctx)
        if not pwd:
            raise AssertionError("Password input not found after email step")

        # Fill **all** visible password fields to avoid hidden/decoy issues
        for cand in _all_visible(
            ctx, 'vaadin-password-field input[slot="input"]',
                 'descope-password-field input[slot="input"]',
                 'input[type="password"]', 'input[autocomplete="current-password"]',
                 'input[placeholder="Password"]', 'input[name="password"]',
        ) or [pwd]:
            try:
                cand.fill(password)
            except Exception:
                pass

        # Submit
        if not _click_if_any(
            ctx.get_by_role("button", name=re.compile(r"(sign in|log in|continue|submit)", re.I)),
            ctx.locator("button[type='submit']"),
            ctx.get_by_text(re.compile(r"(sign in|log in|continue|submit)", re.I)).first
        ):
            pwd.press("Enter")

        # Success = navigated away from auth/login
        expect(self.page).to_have_url(
    lambda u: not re.search(r"/auth|login|sign[- ]?in", u, re.I),
    timeout=120000,    # was 30s; now 120s
)

    def logout(self):
        logout_btn = self.page.get_by_role("button", name=re.compile("logout", re.I))
        if logout_btn.count():
            logout_btn.first.click()
        else:
            self.page.get_by_role("button", name=re.compile("(profile|account|user)", re.I)).first.click(timeout=5000)
            self.page.get_by_role("menuitem", name=re.compile("logout", re.I)).first.click()
        expect(self.page).to_have_url(lambda u: re.search(r"(auth|login|sign[- ]?in)", u, re.I), timeout=15000)
