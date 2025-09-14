import argparse
import os
import re
import sys
from contextlib import suppress
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HOME = "https://digianchorz.com/"

# ---------- Utilities ----------

def wait(driver, timeout=12):
    return WebDriverWait(driver, timeout)

def safe_text(el):
    with suppress(Exception):
        return (el.text or "").strip()
    return ""

def log(ok, name, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}{' — ' + detail if detail else ''}")

def snap_on_fail(driver, name):
    os.makedirs("screens", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join("screens", f"{name}_{ts}.png")
    with suppress(Exception):
        driver.save_screenshot(path)
        print(f"[INFO] Saved screenshot: {path}")

def open_menu_if_needed(driver):
    """
    If a hamburger menu exists on small screens, click it to reveal nav links.
    """
    with suppress(Exception):
        burger = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='menu' i], .navbar-toggler, .menu-toggle, .hamburger")
        if burger:
            burger[0].click()

# ---------- Tests ----------

def test_1_about_nav(driver):
    """Header → About Us navigation."""
    driver.get(HOME)
    try:
        open_menu_if_needed(driver)
        # Try a few locators
        with suppress(Exception):
            wait(driver).until(EC.element_to_be_clickable((By.LINK_TEXT, "About Us"))).click()
        if driver.current_url == HOME:
            with suppress(Exception):
                driver.find_element(By.PARTIAL_LINK_TEXT, "About").click()

        wait(driver).until(lambda d: d.current_url != HOME)
        url = driver.current_url.lower()

        # Validate by URL slug or heading text
        about_like = any(s in url for s in ["/about", "about-us", "aboutus"])
        if not about_like:
            heads = driver.find_elements(By.XPATH, "//h1|//h2|//h3")
            about_in_head = any("about" in safe_text(h).lower() for h in heads)
            log(about_in_head, "About Us navigation", detail=driver.current_url)
            if not about_in_head:
                snap_on_fail(driver, "about_nav")
        else:
            log(True, "About Us navigation", detail=url)
    except Exception as e:
        log(False, "About Us navigation", detail=str(e))
        snap_on_fail(driver, "about_nav")

def test_2_services_seo_page(driver):
    """Open Services → Search Engine Optimization page."""
    driver.get(HOME)
    actions = ActionChains(driver)

    try:
        open_menu_if_needed(driver)

        # Hover/Click "Services"
        services = wait(driver).until(
            EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Services' or contains(.,'Services')]"))
        )
        with suppress(Exception):
            actions.move_to_element(services).pause(0.3).perform()
        with suppress(Exception):
            services.click()  # some menus require click to open

        # Click "Search Engine Optimization"
        with suppress(Exception):
            wait(driver, 6).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Search Engine Optimization"))
            ).click()
        if driver.current_url == HOME:
            with suppress(Exception):
                driver.find_element(By.PARTIAL_LINK_TEXT, "Search Engine Opt").click()

        wait(driver).until(lambda d: d.current_url != HOME)
        url = driver.current_url.lower()

        # Validate page by URL or heading
        ok = ("search" in url and "opt" in url) or any(
            "search engine optimization" in safe_text(h).lower()
            for h in driver.find_elements(By.XPATH, "//h1|//h2")
        )
        log(ok, "Services → Search Engine Optimization", detail=url)
        if not ok:
            snap_on_fail(driver, "services_seo")
    except Exception as e:
        log(False, "Services → Search Engine Optimization", detail=str(e))
        snap_on_fail(driver, "services_seo")

def test_3_carousel_next(driver):
    """Hero carousel 'Next' changes the active slide headline."""
    driver.get(HOME)

    def get_active_heading():
        # Try common carousel libs; fallbacks included
        selectors_css = [
            ".swiper-slide.swiper-slide-active h1, .swiper-slide.swiper-slide-active h2",
            ".slick-slide.slick-active h1, .slick-slide.slick-active h2",
            ".owl-item.active h1, .owl-item.active h2",
            "section header h1, section header h2",
        ]
        for s in selectors_css:
            els = driver.find_elements(By.CSS_SELECTOR, s)
            if els:
                return els[0].text.strip()
        # final fallback: first visible h1/h2
        return driver.find_element(By.XPATH, "(//h1|//h2)[1]").text.strip()

    try:
        before = get_active_heading()

        # Find a "next" control by common selectors or aria-label
        next_selectors = [
            ".swiper-button-next", ".slick-next", ".owl-next",
            "button[aria-label*='next' i]", "a[aria-label*='next' i]",
            "button:contains('Next')", "a:contains('Next')"
        ]
        clicked = False
        for sel in next_selectors:
            # CSS :contains isn't supported; skip those two
            if "contains(" in sel:
                continue
            btns = driver.find_elements(By.CSS_SELECTOR, sel)
            if btns:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btns[0])
                btns[0].click()
                clicked = True
                break
        # Fallback: look for any arrow-like control
        if not clicked:
            with suppress(Exception):
                arrow = driver.find_element(By.XPATH, "//*[contains(@class,'next') or contains(@class,'arrow')][1]")
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", arrow)
                arrow.click()

        # Wait for headline to change and be non-empty
        wait(driver, 10).until(lambda d: (h := get_active_heading()) and h != before)
        after = get_active_heading()
        log(True, "Carousel Next changes headline", detail=f"'{before}' → '{after}'")
    except Exception as e:
        log(False, "Carousel Next changes headline", detail=str(e))
        snap_on_fail(driver, "carousel_next")

def test_4_contact_form(driver):
    """Contact Us page has form inputs and submit button."""
    driver.get(HOME)
    try:
        open_menu_if_needed(driver)
        with suppress(Exception):
            wait(driver).until(EC.element_to_be_clickable((By.LINK_TEXT, "Contact Us"))).click()
        if driver.current_url == HOME:
            with suppress(Exception):
                driver.find_element(By.PARTIAL_LINK_TEXT, "Contact").click()

        wait(driver).until(lambda d: d.current_url != HOME)

        inputs = driver.find_elements(By.XPATH, "//input[not(@type='hidden')]")
        textarea = driver.find_elements(By.TAG_NAME, "textarea")
        submit = driver.find_elements(By.XPATH, "//button[@type='submit' or contains(.,'Submit') or contains(.,'Send')]")

        ok = len(inputs) >= 2 and len(textarea) >= 1 and len(submit) >= 1
        log(ok, "Contact Us form present", detail=f"inputs={len(inputs)}, textarea={len(textarea)}, submit={len(submit)}")
        if not ok:
            snap_on_fail(driver, "contact_form")
    except Exception as e:
        log(False, "Contact Us form present", detail=str(e))
        snap_on_fail(driver, "contact_form")

def test_5_footer_contact_info(driver):
    """Footer contains a phone (tel:) and an email (mailto:), with regex fallback."""
    driver.get(HOME)
    try:
        # Scroll to bottom; allow rendering
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait(driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")

        # Footer element or last main container
        footer = None
        candidates = driver.find_elements(By.TAG_NAME, "footer")
        if candidates:
            footer = candidates[0]
        else:
            blocks = driver.find_elements(By.CSS_SELECTOR, "footer, .site-footer, .footer, body > div:last-of-type, body > section:last-of-type")
            footer = blocks[0] if blocks else driver.find_element(By.TAG_NAME, "body")

        # Prefer tel:/mailto:
        tel_links = footer.find_elements(By.CSS_SELECTOR, "a[href^='tel:']")
        mail_links = footer.find_elements(By.CSS_SELECTOR, "a[href^='mailto:']")

        tel_display = [t.text.strip() or t.get_attribute("href") for t in tel_links]
        mail_display = [m.text.strip() or m.get_attribute("href") for m in mail_links]

        ok = bool(tel_links) and bool(mail_links)

        # Fallback to regex on footer text
        if not ok:
            text = footer.text
            phone_match = re.search(r"\+?\d[\d\-\s()]{7,}", text)
            email_match = re.search(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", text)
            ok = bool(phone_match) and bool(email_match)
            if phone_match: tel_display = [phone_match.group(0)]
            if email_match: mail_display = [email_match.group(0)]

        detail_parts = []
        if tel_display:  detail_parts.append(f"phone={tel_display[0]}")
        if mail_display: detail_parts.append(f"email={mail_display[0]}")
        log(ok, "Footer shows phone & email", detail=", ".join(detail_parts) if detail_parts else "")
        if not ok:
            snap_on_fail(driver, "footer_contact")
    except Exception as e:
        log(False, "Footer shows phone & email", detail=str(e))
        snap_on_fail(driver, "footer_contact")

# ---------- Runner ----------

def build_driver(headless=False):
    options = webdriver.ChromeOptions()
    # Make runs quiet:
    options.add_argument("--log-level=3")  # 0=INFO,1=WARNING,2=ERROR,3=FATAL
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    if headless:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install(), log_path="chromedriver.log")
    return webdriver.Chrome(service=service, options=options)

def main():
    parser = argparse.ArgumentParser(description="Selenium tests for digianchorz.com")
    parser.add_argument("--headless", action="store_true", help="Run Chrome headless")
    args = parser.parse_args()

    driver = build_driver(headless=args.headless)
    try:
        test_1_about_nav(driver)
        test_2_services_seo_page(driver)
        test_3_carousel_next(driver)
        test_4_contact_form(driver)
        test_5_footer_contact_info(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    sys.exit(main() or 0)
