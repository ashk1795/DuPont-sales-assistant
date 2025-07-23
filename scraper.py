from playwright.sync_api import sync_playwright

def scrape_exhibitors_mys():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("🔄 Navigating to exhibitor page...")
        page.goto("https://isasignexpo2026.mapyourshow.com/8_0/exh/exhibitor-alphalist.cfm?alpha=*")

        # ✅ Wait until Vue mounts first card
        try:
            page.wait_for_selector("li.js-Card", timeout=30000)
            print("✅ Exhibitor cards found.")
        except:
            print("❌ Timed out waiting for exhibitor cards.")
            browser.close()
            return []

        # ✅ Scroll to bottom repeatedly to trigger lazy load
        print("🔽 Scrolling to load all exhibitors...")
        previous_count = 0
        scroll_attempts = 0
        while scroll_attempts < 10:
            try:
                page.mouse.wheel(0, 5000)
                page.wait_for_timeout(2000)
                cards = page.query_selector_all("li.js-Card")
                current_count = len(cards)
            except:
                print("⚠️ DOM error — retrying scroll...")
                continue

            if current_count == previous_count:
                break
            previous_count = current_count
            scroll_attempts += 1
            print(f"🔄 Scrolled — now found {current_count} exhibitors")

        # 📝 Save full HTML snapshot for debugging
        html = page.content()
        with open("debug_snapshot.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("📝 Saved debug_snapshot.html")

        # ✅ Try primary and fallback selectors
        try:
            cards = page.query_selector_all("li.js-Card")
            print(f"🔍 Found {len(cards)} using li.js-Card selector.")
            if len(cards) == 0:
                print("🧪 Trying fallback selector: div[class*=card]")
                cards = page.query_selector_all("div[class*=card]")
                print(f"🔍 Fallback found {len(cards)} card-like divs.")
        except Exception as e:
            print(f"❌ Failed to query cards: {e}")
            browser.close()
            return []

        exhibitors = []

        for card in cards:
            try:
                print("------ CARD START ------")
                print(card.inner_html())  # 🔍 Show full card HTML
                print("------ CARD END ------")

                name_el = card.query_selector("h3.card-Title") or card.query_selector("h3") or card.query_selector("span")
                name = name_el.inner_text().strip() if name_el else None

                link_el = card.query_selector("a")
                href = link_el.get_attribute("href") if link_el else None
                full_url = "https://isasignexpo2026.mapyourshow.com" + href if href else None

                if name:
                    exhibitors.append({
                        "name": name,
                        "profile_url": full_url
                    })
            except Exception as e:
                print(f"⚠️ Error parsing card: {e}")
                continue

        print(f"✅ Scraped {len(exhibitors)} exhibitors")
        browser.close()
        return exhibitors

def scrape_event_companies(event_url):
    """
    Given an event URL, return a list of dicts with company info.
    """
    exhibitors = scrape_exhibitors_mys()
    # Convert to the expected format for the dashboard
    return [{"company": ex["name"], "profile_url": ex.get("profile_url")} for ex in exhibitors if ex.get("name")]