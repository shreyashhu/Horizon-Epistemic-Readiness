import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain
import random
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

# 1. Load the OpenAlex Data
nodes_df = pd.read_csv(DATA_PROCESSED_DIR / 'openalex_nodes.csv')
edges_df = pd.read_csv(DATA_PROCESSED_DIR / 'openalex_edges.csv')

G = nx.Graph()
for _, row in nodes_df.iterrows():
    if pd.notna(row['title']):
        G.add_node(str(row['id']), title=row['title'])

for _, row in edges_df.iterrows():
    s, t = str(row['source']), str(row['target'])
    if s in G.nodes and t in G.nodes:
        G.add_edge(s, t)

# Isolate Giant Component
giant_nodes = max(nx.connected_components(G), key=len)
G_giant = G.subgraph(giant_nodes).copy()

# 2. Run Louvain (MUST use random_state=42 to match the exact same clusters as before)
partition = community_louvain.best_partition(G_giant, random_state=42)

# 3. Inspect Communities 7 and 9
target_communities = [7, 9]
for comm_id in target_communities:
    # Find all nodes belonging to this specific community ID
    nodes_in_comm = [node for node, comm in partition.items() if comm == comm_id]
    print(f"\n=== COMMUNITY {comm_id} ({len(nodes_in_comm)} papers) ===")

    if len(nodes_in_comm) > 0:
        # Grab a random sample of 15 papers to see what the "Plate" is about
        sample_nodes = random.sample(nodes_in_comm, min(15, len(nodes_in_comm)))
        for node in sample_nodes:
            title = G_giant.nodes[node].get('title', 'Unknown')
            print(f"  • {title}")
    else:
        print("Community not found.")