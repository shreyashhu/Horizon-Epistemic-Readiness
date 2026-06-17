import requests
import pandas as pd
import time
import os
from pathlib import Path

# Dynamically find the project root (MIT 2027 IG/)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Define target directories
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_GEPHI_DIR = PROJECT_ROOT / "outputs" / "gephi"

# Ensure these directories exist before saving
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_GEPHI_DIR.mkdir(parents=True, exist_ok=True)

# Load email from config
try:
    from config import EMAIL
except ImportError:
    # Replace with your actual email to access the OpenAlex polite pool (faster rate limits)
    EMAIL = "your_email@example.com"

BASE_URL = "https://api.openalex.org/works"

# We want a broader net for temporal tracking, not just the top 1000.
# We will pull papers from 2010 to 2016 (The build-up to the Transformer)
params = {
    "filter": "concepts.id:C154945302,publication_year:2010-2016",
    "select": "id,doi,title,publication_year,referenced_works,cited_by_count",
    "per_page": 200,
    "cursor": "*",
    "mailto": EMAIL
}

papers = []
next_cursor = "*"

# Let's pull 25 pages (up to 5,000 papers). This gives us a dense, evolving graph.
pages_to_fetch = 25

print("Fetching up to 5,000 Deep Learning papers (2010-2016) for Temporal Tracking...")
for i in range(pages_to_fetch):
    params["cursor"] = next_cursor
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Request failed on page {i+1}: {e}")
        break
        
    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code} on page {i+1}")
        break
        
    data = response.json()
    results = data.get('results', [])
    
    if not results:
        print("No more results found. Stopping pagination.")
        break
        
    papers.extend(results)
    next_cursor = data.get('meta', {}).get('next_cursor')
    print(f"  Page {i+1}/{pages_to_fetch} fetched. Total papers so far: {len(papers)}")
    time.sleep(0.1) # Polite pool delay

# Save the raw temporal data
if papers:
    df = pd.DataFrame(papers)
    # Ensure the directory exists
    os.makedirs(PROJECT_ROOT / 'data' / 'raw', exist_ok=True)
    output_path = PROJECT_ROOT / 'data' / 'raw' / 'temporal_core_2010_2016.csv'
    
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ SUCCESS: Saved {len(df)} papers to {output_path}")
    print("We now have the raw material to build the year-by-year snapshots.")
else:
    print("\n❌ No papers were fetched. Please check your network connection, email configuration, or API parameters.")