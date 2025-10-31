# Om Gan Ganpataye Namah
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

INPUT_FILE = "input_urls.csv"
OUTPUT_FILE = "playing11.csv"

def clean_name(text: str) -> str:
    """Remove captain (c), keeper † and commas."""
    return text.replace("(c)", "").replace("†", "").replace(",", "").strip()

def scrape_playing11(driver, url):
    """Scrape playing 11 from a single Cricinfo scorecard URL."""
    print(f"\n🔗 Opening URL: {url}")
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.ci-scorecard-table"))
        )
    except Exception:
        print("⚠️ Scorecard not found on page.")
        return []

    time.sleep(1.5)  # safety delay
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    teams = []
    team_names = [t.get_text(strip=True) for t in soup.select("span.ds-text-title-xs.ds-font-bold.ds-capitalize")]
    batting_tables = soup.select("table.ci-scorecard-table")

    for idx, table in enumerate(batting_tables[:2]):  # both teams
        players = []

        # batting order
        for a in table.select("tbody a[href*='/cricketers/']"):
            pname = clean_name(a.get_text(strip=True))
            if pname and pname not in players:
                players.append(pname)

        # Did not bat
        did_not_bat = table.find(string=lambda s: s and "Did not bat" in s)
        if did_not_bat:
            parent_td = did_not_bat.find_parent("td")
            if parent_td:
                for a in parent_td.select("a[href*='/cricketers/']"):
                    pname = clean_name(a.get_text(strip=True))
                    if pname and pname not in players:
                        players.append(pname)

        if idx < len(team_names):
            teams.append({"team": team_names[idx], "players": players})

    return teams


if __name__ == "__main__":
    # read URLs from CSV (one per line)
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"📄 Found {len(urls)} URLs in {INPUT_FILE}")

    options = Options()
    # TIP: keep popup visible locally (comment headless). For CI (Actions), it will run headless.
    # options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    all_rows = []

    for i, url in enumerate(urls, 1):
        print(f"\n===== MATCH {i} of {len(urls)} =====")
        match_data = scrape_playing11(driver, url)
        for t in match_data:
            print(f"\n{t['team']} Playing XI (batting order):")
            for j, p in enumerate(t["players"], 1):
                print(f"{j}. {p}")
                all_rows.append([t["team"], p])

    driver.quit()
    print("\n✅ Chrome closed successfully.")

    # save Team & Player only
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Team", "Player Name"])
        writer.writerows(all_rows)

    print(f"\n✅ Saved Playing XI for {len(urls)} match(es) to {OUTPUT_FILE}")
