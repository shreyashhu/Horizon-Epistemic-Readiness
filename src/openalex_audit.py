import requests
import pandas as pd
import networkx as nx
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

EMAIL = "shreyash2672009@gmail.com" # Keep your email here for the polite pool!
BASE_URL = "https://api.openalex.org/works"

# THE FIX: We sort by citation count descending.
# This guarantees we download the "Core" of the field, not random noise.
params = {
    "filter": "concepts.id:C154945302,publication_year:2012-2017",
    "select": "id,doi,title,publication_year,referenced_works,cited_by_count",
    "sort": "cited_by_count:desc",  #  <--- THE MAGIC LINE
    "per_page": 200,
    "cursor": "*",
    "mailto": EMAIL
}

papers = []
next_cursor = "*"
pages_to_fetch = 5 # 1000 papers

print("Fetching the 1000 MOST CITED Deep Learning papers (2012-2017)...")
for i in range(pages_to_fetch):
    params["cursor"] = next_cursor
    response = requests.get(BASE_URL, params=params, timeout=15)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break
        
    data = response.json()
    results = data.get('results', [])
    if not results:
        break
        
    papers.extend(results)
    next_cursor = data.get('meta', {}).get('next_cursor')
    print(f"  Page {i+1} fetched. Total papers: {len(papers)}")
    time.sleep(0.1) 

print(f"\nTotal core papers downloaded: {len(papers)}")

# ---------------------------------------------------------
# Build the Internal Graph (The Core Density Audit)
# ---------------------------------------------------------
valid_ids = {p['id'] for p in papers}
G = nx.DiGraph()

for p in papers:
    G.add_node(p['id'], title=p.get('title'), year=p.get('publication_year'))

internal_edges = 0
for p in papers:
    source = p['id']
    refs = p.get('referenced_works', [])
    for ref in refs:
        if ref in valid_ids:
            G.add_edge(source, ref)
            internal_edges += 1

print(f"Internal lateral edges found: {internal_edges}")

# ---------------------------------------------------------
# The Audit Metrics
# ---------------------------------------------------------
print("\n--- OPENALEX CORE DENSITY AUDIT ---")
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

if G.number_of_nodes() > 0:
    avg_degree = G.number_of_edges() / G.number_of_nodes()
    print(f"Average Degree (Edges per node): {avg_degree:.2f}")

    weakly_connected = list(nx.weakly_connected_components(G))
    giant_component = max(weakly_connected, key=len)

    print(f"Total Disconnected Islands: {len(weakly_connected)}")
    print(f"Size of Giant Component: {len(giant_component)} nodes")

    # The new threshold for a "Core" graph
    if avg_degree > 3.0 and len(giant_component) > (G.number_of_nodes() * 0.70):
        print("\n✅ AUDIT PASSED: The core is dense and highly interconnected.")
        print("We have successfully captured the 'Rich Club' of the field.")
    else:
        print("\n❌ AUDIT FAILED: The core is still too fragmented.")