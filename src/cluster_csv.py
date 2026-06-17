import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain
import collections
import random

# 1. Load the CSVs you just generated
print("Loading data from CSVs...")
nodes_df = pd.read_csv('openalex_nodes.csv')
edges_df = pd.read_csv('openalex_edges.csv')

# 2. Build the NetworkX Graph (Properly this time!)
G = nx.Graph() # Undirected is best for Louvain

for _, row in nodes_df.iterrows():
    node_id = str(row['id'])
    title = row['title'] if pd.notna(row['title']) else 'Unknown'
    G.add_node(node_id, title=title)

for _, row in edges_df.iterrows():
    source = str(row['source'])
    target = str(row['target'])
    if source in G.nodes and target in G.nodes:
        G.add_edge(source, target)

print(f"Graph built successfully: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.\n")

# 3. Isolate Giant Component
if G.number_of_nodes() == 0:
    print("Graph is empty! Check CSVs.")
else:
    giant_nodes = max(nx.connected_components(G), key=len)
    G_giant = G.subgraph(giant_nodes).copy()
    
    print(f"Isolated Giant Component: {G_giant.number_of_nodes()} nodes, {G_giant.number_of_edges()} edges.")
    print("Running Louvain Community Detection...\n")
    
    # 4. Run Louvain
    partition = community_louvain.best_partition(G_giant, random_state=42)
    
    # 5. Group and Print
    communities = collections.defaultdict(list)
    for node_id, comm_id in partition.items():
        title = G_giant.nodes[node_id].get('title', 'Unknown')
        communities[comm_id].append(title)
        
    sorted_comms = sorted(communities.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"Found {len(sorted_comms)} distinct tectonic plates.\n")
    print("--- TOP 5 LARGEST COMMUNITIES (The 2012-2017 AI Boom) ---")
    
    for i, (comm_id, comm_papers) in enumerate(sorted_comms[:5]):
        print(f"\n[ Plate {i+1} ] ({len(comm_papers)} papers)")
        sample = random.sample(comm_papers, min(5, len(comm_papers)))
        for p in sample:
            print(f"  • {p}")
# Export to Gephi with Community Colors
nx.set_node_attributes(G_giant, partition, 'community')
nx.write_gexf(G_giant, "horizon_openalex_map.gexf")
print("\n✅ Successfully exported to horizon_openalex_map.gexf")
print("Download Gephi (gephi.org), open this file, and run 'ForceAtlas 2' to see the 12 plates.")