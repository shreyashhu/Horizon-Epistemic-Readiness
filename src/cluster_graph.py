import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain
import collections
import random

# 1. Load Data & Build Undirected Graph (Community detection requires undirected edges)
nodes_df = pd.read_csv('clean_nodes.csv')
edges_df = pd.read_csv('clean_edges.csv')

G = nx.Graph() 
for _, row in nodes_df.iterrows():
    G.add_node(row['id'], title=row['title'])

for _, row in edges_df.iterrows():
    if row['source'] in G.nodes and row['target'] in G.nodes:
        G.add_edge(row['source'], row['target'])

# 2. Isolate the Giant Component (The 353 nodes)
giant_component_nodes = max(nx.connected_components(G), key=len)
G_giant = G.subgraph(giant_component_nodes).copy()

print(f"Running Community Detection on Giant Component ({G_giant.number_of_nodes()} nodes)...\n")

# 3. Run Louvain
partition = community_louvain.best_partition(G_giant, random_state=42)

# 4. Group and Print
communities = collections.defaultdict(list)
for node_id, comm_id in partition.items():
    title = G_giant.nodes[node_id].get('title', 'Unknown')
    if pd.notna(title):
        communities[comm_id].append(title)

sorted_comms = sorted(communities.items(), key=lambda x: len(x[1]), reverse=True)

print(f"Found {len(sorted_comms)} distinct communities.\n")
print("--- TOP 5 LARGEST COMMUNITIES (The Sanity Check) ---")

for i, (comm_id, papers) in enumerate(sorted_comms[:5]):
    print(f"\n[ Community {i+1} ] ({len(papers)} papers)")
    sample = random.sample(papers, min(5, len(papers)))
    for p in sample:
        print(f"  • {p}")