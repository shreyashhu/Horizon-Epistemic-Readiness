import requests
import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain
import collections
import random
import time

# 1. Fetch OpenAlex Data (1000 Most Cited DL Papers 2012-2017)
EMAIL = "shreyash2672009@gmail.com" # Put your email here for the polite pool
BASE_URL = "https://api.openalex.org/works"

params = {
    "filter": "concepts.id:C154945302,publication_year:2012-2017",
    "sort": "cited_by_count:desc", 
    "select": "id,doi,title,publication_year,referenced_works,cited_by_count",
    "per_page": 200,
    "cursor": "*",
    "mailto": EMAIL
}

papers = []
next_cursor = "*"
pages_to_fetch = 5 

print("Fetching 1000 most cited Deep Learning papers (2012-2017)...")
for i in range(pages_to_fetch):
    params["cursor"] = next_cursor
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200: break
    data = response.json()
    results = data.get('results', [])
    if not results: break
    papers.extend(results)
    next_cursor = data.get('meta', {}).get('next_cursor')
    print(f"  Page {i+1} fetched. Total: {len(papers)}")
    time.sleep(0.1)

# 2. Build Graph and Save to CSV
valid_ids = {p['id'] for p in papers}
G = nx.DiGraph()

nodes_list = []
edges_list = []

for p in papers:
    nodes_list.append({'id': p['id'], 'title': p.get('title'), 'year': p.get('publication_year')})
    for ref in p.get('referenced_works', []):
        if ref in valid_ids:
            edges_list.append({'source': p['id'], 'target': ref})

nodes_df = pd.DataFrame(nodes_list)
edges_df = pd.DataFrame(edges_list)

nodes_df.to_csv('openalex_nodes.csv', index=False)
edges_df.to_csv('openalex_edges.csv', index=False)
print(f"\nSaved {len(nodes_df)} nodes and {len(edges_df)} edges to CSV.")

# 3. Isolate Giant Component & Cluster
G_undirected = G.to_undirected()
giant_nodes = max(nx.connected_components(G_undirected), key=len)
G_giant = G_undirected.subgraph(giant_nodes).copy()

print(f"Running Louvain on Giant Component ({G_giant.number_of_nodes()} nodes, {G_giant.number_of_edges()} edges)...\n")
partition = community_louvain.best_partition(G_giant, random_state=42)

communities = collections.defaultdict(list)
for node_id, comm_id in partition.items():
    title = G_giant.nodes[node_id].get('title', 'Unknown')
    if pd.notna(title):
        communities[comm_id].append(title)

sorted_comms = sorted(communities.items(), key=lambda x: len(x[1]), reverse=True)

print("--- TOP 5 LARGEST COMMUNITIES (The 2012-2017 AI Boom) ---")
for i, (comm_id, comm_papers) in enumerate(sorted_comms[:5]):
    print(f"\n[ Plate {i+1} ] ({len(comm_papers)} papers)")
    sample = random.sample(comm_papers, min(5, len(comm_papers)))
    for p in sample:
        print(f"  • {p}")