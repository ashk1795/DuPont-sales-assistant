from scraper import scrape_exhibitors_mys

if __name__ == "__main__":
    results = scrape_exhibitors_mys()
    print(f"Total exhibitors found: {len(results)}\n")  # <- ADD THIS LINE
    for exhibitor in results:
        print(exhibitor)
