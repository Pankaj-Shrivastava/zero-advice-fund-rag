import os
import json
from bs4 import BeautifulSoup

RAW_HTML_DIR = os.path.join(os.path.dirname(__file__), "../scraper/raw_html")
METADATA_FILE = os.path.join(RAW_HTML_DIR, "scraped_metadata.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "parsed_data.json")

def clean_html(soup):
    # Remove boilerplate elements that add noise to text extraction
    for element in soup.find_all(['nav', 'footer', 'script', 'style', 'svg', 'button', 'iframe', 'noscript', 'header']):
        element.decompose()

def parse_table(table):
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(separator=' ', strip=True) for td in tr.find_all(['td', 'th'])]
        rows.append(" | ".join(cells))
    return "\n".join(rows)

def tag_section(text):
    text_lower = text.lower()
    if "expense ratio" in text_lower: return "expense_ratio"
    if "exit load" in text_lower: return "exit_load"
    if "sip" in text_lower and "minimum" in text_lower: return "sip_details"
    if "risk" in text_lower and "category" in text_lower: return "risk_classification"
    if "benchmark" in text_lower: return "benchmark"
    if "fund manage" in text_lower or "manager" in text_lower: return "fund_manager"
    if "returns" in text_lower and ("1y" in text_lower or "3y" in text_lower or "5y" in text_lower): return "returns_table"
    if "holdings" in text_lower or "portfolio" in text_lower or "sector" in text_lower: return "holdings"
    return "fund_overview"

def parse_file(html_file, metadata):
    filepath = os.path.join(RAW_HTML_DIR, html_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    clean_html(soup)
    
    documents = []
    
    # 1. Extract tables (returns, holdings, etc.)
    tables = soup.find_all('table')
    for table in tables:
        table_text = parse_table(table)
        if len(table_text) > 20: # ignore tiny/empty tables
            documents.append({
                "section": tag_section(table_text),
                "text": table_text,
                **metadata
            })
        # Remove the table so its text isn't duplicated in the next step
        table.decompose()
        
    # 2. Extract remaining text by splitting into lines
    remaining_text = soup.get_text(separator='\n', strip=True)
    lines = [line.strip() for line in remaining_text.split('\n') if line.strip()]
    
    # Group lines by identifying potential section headers or max chunk lengths
    current_text = []
    headers = ["Expense ratio", "Exit load", "Tax implications", "Fund Management", "Pros and Cons", "Risk", "About", "Peers", "Minimum Investment"]
    
    for line in lines:
        is_header = any(h.lower() in line.lower() for h in headers) and len(line) < 60
        
        # If we hit a header and we already have a good amount of text collected, store it
        if is_header and len("\n".join(current_text)) > 100:
            section_text = "\n".join(current_text)
            documents.append({
                "section": tag_section(section_text),
                "text": section_text,
                **metadata
            })
            current_text = []
        
        current_text.append(line)
        
        # Also split if the block gets too large (e.g., > 1000 characters) to avoid massive blobs
        if len("\n".join(current_text)) > 1500:
            section_text = "\n".join(current_text)
            documents.append({
                "section": tag_section(section_text),
                "text": section_text,
                **metadata
            })
            current_text = []
            
    if current_text:
        section_text = "\n".join(current_text)
        if len(section_text) > 20: # skip very small trailing noise
            documents.append({
                "section": tag_section(section_text),
                "text": section_text,
                **metadata
            })
        
    return documents
    
def main():
    if not os.path.exists(METADATA_FILE):
        print(f"Error: Metadata file not found at {METADATA_FILE}")
        return
        
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata_list = json.load(f)
        
    all_documents = []
    for item in metadata_list:
        meta = {k: v for k, v in item.items() if k != "html_file"}
        docs = parse_file(item["html_file"], meta)
        all_documents.extend(docs)
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_documents, f, ensure_ascii=False, indent=2)
        
    print(f"Parsed {len(metadata_list)} files into {len(all_documents)} clean document sections.")
    
    # Print a sample of sections extracted
    section_counts = {}
    for doc in all_documents:
        section_counts[doc['section']] = section_counts.get(doc['section'], 0) + 1
    print("Section counts:", section_counts)

if __name__ == "__main__":
    main()
