import requests
import json
import pandas as pd

# ---------------------------------------------------------
# TEST 1: Direct Fetch (Guaranteed to work)
# Fetching "Attention Is All You Need" (2017) by its exact ID
# ---------------------------------------------------------
paper_id = "204e3073870fae3d05bcbc2f6a8e263d9b72e776"
url_details = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"

params = {"fields": "paperId,title,abstract,year,venue,references,citationCount"}

print(f"Fetching landmark paper: {paper_id}...\n")
res = requests.get(url_details, params=params, timeout=10)

if res.status_code == 200:
    paper = res.json()
    print("--- RAW JSON (First 1500 chars) ---")
    print(json.dumps(paper, indent=2)[:1500])
    
    refs = paper.get('references', [])
    print(f"\n[SUCCESS] Found {len(refs)} references.")
    if refs and len(refs) > 0:
        print("\n--- STRUCTURE OF ONE REFERENCE ---")
        print(json.dumps(refs[0], indent=2))
else:
    print(f"[FAILED] API returned {res.status_code}: {res.text}")

print("\n" + "="*50 + "\n")

# ---------------------------------------------------------
# TEST 2: Broad Search (No venue filter, just looking for shape)
# ---------------------------------------------------------
url_search = "https://api.semanticscholar.org/graph/v1/paper/search"
params_search = {
    "query": "transformer attention mechanism", 
    "fields": "paperId,title,abstract,year,venue,references,citationCount",
    "limit": 20
}

print("Fetching broad search (20 papers)...")
res_search = requests.get(url_search, params=params_search, timeout=10)

if res_search.status_code == 200:
    data = res_search.json().get('data', [])
    print(f"[SUCCESS] Downloaded {len(data)} papers.\n")
    
    if data:
        df = pd.DataFrame(data)
        print(f"Missing abstracts: {df['abstract'].isna().sum()} out of {len(df)}")
        print(f"Missing references: {df['references'].isna().sum()} out of {len(df)}")
        df.to_csv('pilot_search_raw.csv', index=False)
        print("Saved to pilot_search_raw.csv")
else:
    print(f"[FAILED] API returned {res_search.status_code}: {res_search.text}")