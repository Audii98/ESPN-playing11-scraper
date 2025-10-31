# 🏏 Playing XI Scraper

Scrapes **Playing XI** (batting order + Did Not Bat) from ESPN Cricinfo **for multiple scorecards in one Chrome session** using Selenium + BeautifulSoup.

## Setup (local)
1. Install Python 3.10+
2. `pip install -r requirements.txt`
3. Put match URLs (one per line) in `input_urls.csv`
4. Run: `python Playing_11.py`

- Chrome window will open once, visit each URL, and save `playing11.csv`.
- CSV columns: **Team, Player Name**

## Notes
- Keep `--headless` commented for a visible popup locally.
- Works best when Cricinfo HTML structure remains consistent.
