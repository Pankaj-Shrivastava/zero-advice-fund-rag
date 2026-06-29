import json
import os
import hashlib

INPUT_FILE = os.path.join(os.path.dirname(__file__), "parsed_data.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "chunked_data.json")

def generate_chunk_id(scheme, section, index):
    # e.g., iciciprudentiallar-holdings-001
    safe_scheme = "".join(c for c in scheme if c.isalnum()).lower()[:20]
    return f"{safe_scheme}-{section}-{index:03d}"

def split_table(text, chunk_char_limit=1000):
    lines = text.split('\n')
    if len(lines) <= 2:
        return [text]
    
    header = lines[0]
    data_lines = lines[1:]
    
    chunks = []
    current_chunk_lines = [header]
    current_length = len(header)
    
    for line in data_lines:
        if current_length + len(line) > chunk_char_limit and len(current_chunk_lines) > 1:
            chunks.append("\n".join(current_chunk_lines))
            current_chunk_lines = [header, line]
            current_length = len(header) + len(line) + 1 # +1 for newline
        else:
            current_chunk_lines.append(line)
            current_length += len(line) + 1
            
    if len(current_chunk_lines) > 1:
        chunks.append("\n".join(current_chunk_lines))
        
    return chunks

def split_text(text, chunk_char_limit=1000, overlap=100):
    lines = text.split('\n')
    chunks = []
    
    current_chunk = ""
    for line in lines:
        if len(current_chunk) + len(line) > chunk_char_limit and current_chunk:
            chunks.append(current_chunk.strip())
            # For overlap, keep the last line of the current chunk if it's not too long
            current_chunk = line
        else:
            current_chunk += "\n" + line if current_chunk else line
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def chunk_document(doc):
    text = doc['text']
    # Heuristic for detecting tables based on our parser logic
    is_table = ' | ' in text and '\n' in text 
    
    if len(text) <= 1000:
        raw_chunks = [text]
    else:
        if is_table:
            raw_chunks = split_table(text)
        else:
            raw_chunks = split_text(text)
            
    chunks = []
    scheme = doc['scheme']
    section = doc['section']
    
    for i, rc in enumerate(raw_chunks):
        # Metadata Prefixing
        context_prefix = f"[{scheme} - {section.replace('_', ' ').title()}]\n"
        final_text = context_prefix + rc
        
        chunk_doc = {
            "chunk_id": generate_chunk_id(scheme, section, i+1),
            "text": final_text,
            "source_url": doc["source_url"],
            "amc": doc["amc"],
            "scheme": scheme,
            "category": doc["category"],
            "section": section,
            "scraped_at": doc["scraped_at"]
        }
        chunks.append(chunk_doc)
        
    return chunks

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return
        
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    all_chunks = []
    for doc in data:
        all_chunks.extend(chunk_document(doc))
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        
    avg_len = sum(len(c["text"]) for c in all_chunks) / len(all_chunks) if all_chunks else 0
    print(f"Generated {len(all_chunks)} chunks across {len(data)} document sections.")
    print(f"Average chunk size: {avg_len:.0f} characters.")
    
if __name__ == "__main__":
    main()
