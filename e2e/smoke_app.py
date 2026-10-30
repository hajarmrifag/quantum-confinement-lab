"""Playwright smoke and responsive-visual checks for a running local app."""

from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
URL = "http://127.0.0.1:8501"


def assert_healthy(page) -> None:
    expect(page.get_by_role("heading", name="Quantum Confinement Lab")).to_be_visible(timeout=30_000)
    expect(page.locator("[data-testid='stException']")).to_have_count(0)
    expect(page.get_by_text("Ground energy", exact=True)).to_be_visible(timeout=30_000)
    expect(page.locator("[data-testid='stPlotlyChart']").first).to_be_attached(timeout=30_000)
    assert page.locator("[data-testid='stPlotlyChart']").count() >= 2


def main() -> None:
    ARTIFACTS.mkdir(exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        desktop = browser.new_page(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)
        desktop.goto(URL, wait_until="domcontentloaded", timeout=30_000)
        assert_healthy(desktop)
        desktop.screenshot(path=ARTIFACTS / "app-desktop.png", full_page=True)

        # Change a representative physics control and verify a recomputation.
        baseline_energy = desktop.locator("[data-testid='stMetricValue']").nth(1).inner_text()
        desktop.get_by_role("combobox", name="Physical model").click()
        desktop.get_by_role("option", name="Infinite square well").click()
        expect(desktop.locator("[data-testid='stMetricValue']").nth(1)).not_to_have_text(baseline_energy, timeout=30_000)
        expect(desktop.get_by_text("continuum analytical", exact=False).first).to_be_visible()
        expect(desktop.locator("[data-testid='stException']")).to_have_count(0)

        desktop.get_by_role("tab", name="Model comparison").click()
        expect(desktop.get_by_text("Ground-state energy versus confinement width", exact=True)).to_be_visible(timeout=30_000)

        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        mobile.goto(URL, wait_until="domcontentloaded", timeout=30_000)
        assert_healthy(mobile)
        overflow = mobile.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        assert overflow <= 1, f"mobile layout overflows horizontally by {overflow}px"
        mobile.screenshot(path=ARTIFACTS / "app-mobile.png", full_page=True)

        browser.close()
    print("Playwright smoke checks passed; desktop and mobile screenshots written to artifacts/.")


if __name__ == "__main__":
    main()
