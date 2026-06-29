import json
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

URLS_FILE = os.path.join(os.path.dirname(__file__), "urls.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "raw_html")
METADATA_FILE = os.path.join(OUTPUT_DIR, "scraped_metadata.json")

def sanitize_filename(url):
    return url.strip("/").split("/")[-1] + ".html"

def scrape_pages():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(URLS_FILE, "r", encoding="utf-8") as f:
        urls_data = json.load(f)

    success_count = 0
    total = len(urls_data)
    metadata_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        for index, item in enumerate(urls_data):
            page = context.new_page()
            url = item["source_url"]
            print(f"[{index+1}/{total}] Scraping: {url}")
            
            try:
                # Groww pages might be slow or JS heavy
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                
                # Wait for main content to load (give it some time to fetch API data)
                page.wait_for_timeout(3000)
                
                # Scroll a bit to trigger lazy loading if necessary
                page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
                page.wait_for_timeout(2000)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)
                
                html_content = page.content()
                
                if not html_content or len(html_content) < 5000:
                    print(f"Error: Empty or suspiciously small HTML returned for {url}")
                    continue
                
                filename = sanitize_filename(url)
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, "w", encoding="utf-8") as out_f:
                    out_f.write(html_content)
                
                metadata_list.append({
                    "html_file": filename,
                    "source_url": url,
                    "amc": item["amc"],
                    "scheme": item["scheme"],
                    "category": item["category"],
                    "scraped_at": datetime.utcnow().isoformat() + "Z"
                })
                
                success_count += 1
                
            except PlaywrightTimeoutError:
                print(f"Timeout error while scraping: {url}")
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
            finally:
                page.close()
                time.sleep(2) # Polite delay
                
        browser.close()
    
    with open(METADATA_FILE, "w", encoding="utf-8") as meta_f:
        json.dump(metadata_list, meta_f, ensure_ascii=False, indent=2)

    print(f"Scraped {success_count}/{total} pages successfully")

if __name__ == "__main__":
    scrape_pages()
