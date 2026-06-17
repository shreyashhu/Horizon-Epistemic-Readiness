import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain

# 1. Rebuild the graph
nodes_df = pd.read_csv('clean_nodes.csv')
edges_df = pd.read_csv('clean_edges.csv')

G = nx.Graph()
for _, row in nodes_df.iterrows():
    if pd.notna(row['title']):
        G.add_node(row['id'], title=row['title'], label=row['title'][:30]) # Truncate label for readability

for _, row in edges_df.iterrows():
    if row['source'] in G.nodes and row['target'] in G.nodes:
        G.add_edge(row['source'], row['target'])

# 2. Isolate Giant Component
giant_nodes = max(nx.connected_components(G), key=len)
G_giant = G.subgraph(giant_nodes).copy()

# 3. Calculate Communities and attach as metadata
partition = community_louvain.best_partition(G_giant, random_state=42)
nx.set_node_attributes(G_giant, partition, 'community')

# 4. Export to GEXF (Gephi's native format)
nx.write_gexf(G_giant, "horizon_pilot_map.gexf")
print("Successfully exported to horizon_pilot_map.gexf")
print("Download Gephi (gephi.org) and open this file to see the map.")