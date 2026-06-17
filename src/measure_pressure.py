import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain
import itertools
import os
from pathlib import Path
import numpy as np

# Dynamically find the project root (MIT 2027 IG/)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Define target directories
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_GEPHI_DIR = PROJECT_ROOT / "outputs" / "gephi"

# Ensure these directories exist before saving
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_GEPHI_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load Data and Build Graph
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

# 2. Get Communities
partition = community_louvain.best_partition(G_giant, random_state=42)
nx.set_node_attributes(G_giant, partition, 'community')

# 3. Measure Cross-Community Pressure
# Let's find the two largest communities (e.g., Vision and NLP/RL)
communities = {}
for node, comm_id in partition.items():
    communities.setdefault(comm_id, []).append(node)

sorted_comms = sorted(communities.items(), key=lambda x: len(x[1]), reverse=True)

# Grab the top 2 largest plates
plate_A_id, plate_A_nodes = sorted_comms[0]
plate_B_id, plate_B_nodes = sorted_comms[1]

print(f"Measuring pressure between Plate {plate_A_id} ({len(plate_A_nodes)} nodes) and Plate {plate_B_id} ({len(plate_B_nodes)} nodes)...\n")

# Count actual edges crossing the boundary
cross_edges = 0
for u in plate_A_nodes:
    for v in plate_B_nodes:
        if G_giant.has_edge(u, v):
            cross_edges += 1

# Calculate maximum possible edges (Density baseline)
max_possible_edges = len(plate_A_nodes) * len(plate_B_nodes)
actual_density = cross_edges / max_possible_edges if max_possible_edges > 0 else 0

print(f"--- RAW TOPOLOGY METRICS ---")
print(f"Actual Cross-Edges: {cross_edges}")
print(f"Max Possible Edges: {max_possible_edges}")
print(f"Cross-Density: {actual_density:.6f}")

# 4. The "Super-Hub" Check
# Let's see how many of those cross edges are just papers citing a massive hub like AlexNet
hub_citations = 0
# (Assuming AlexNet is in one of the plates, let's find the top 3 most connected nodes in the combined set)
combined_nodes = set(plate_A_nodes).union(set(plate_B_nodes))
subgraph = G_giant.subgraph(combined_nodes)
degrees = dict(subgraph.degree())
top_hubs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:3]

print(f"\n--- TOP 3 HUBS IN THIS INTERFACE ---")
for hub_id, degree in top_hubs:
    title = G_giant.nodes[hub_id].get('title', 'Unknown')
    print(f"Hub: {title} (Degree: {degree})")
    
    # Check if this hub is responsible for the cross-edges
    hub_cross_edges = 0
    for neighbor in G_giant.neighbors(hub_id):
        if (hub_id in plate_A_nodes and neighbor in plate_B_nodes) or \
           (hub_id in plate_B_nodes and neighbor in plate_A_nodes):
            hub_cross_edges += 1
            
    print(f"  -> {hub_cross_edges} of the {cross_edges} cross-edges are just connections to this hub.")

def count_cross_edges(G, nodes_A, nodes_B):
    count = 0
    for u in nodes_A:
        for v in nodes_B:
            if G.has_edge(u, v):
                count += 1
    return count

actual_cross = count_cross_edges(G_giant, plate_A_nodes, plate_B_nodes)

# ---------------------------------------------------------
# THE NULL MODEL (Degree-Preserving Randomization)
# ---------------------------------------------------------
null_cross_edges = []
n_iterations = 100  # 100 randomized universes (increase to 500 for final paper)
swaps_per_iter = G_giant.number_of_edges() * 2  # Enough swaps to thoroughly shuffle

print(f"\nGenerating null distribution ({n_iterations} randomized graphs)...")
print("This proves whether the structural hole is statistically significant...\n")

for i in range(n_iterations):
    # Copy graph to avoid altering the original
    G_rand = G_giant.copy()
    
    # Rewire the graph while preserving the exact degree of every node
    # (This simulates a universe where researchers cite randomly, but maintain their overall activity levels)
    nx.connected_double_edge_swap(G_rand, nswap=swaps_per_iter)
    
    # Count cross edges in the randomized graph
    rand_cross = count_cross_edges(G_rand, plate_A_nodes, plate_B_nodes)
    null_cross_edges.append(rand_cross)

# ---------------------------------------------------------
# THE EPISTEMIC READINESS METRIC (Z-Score)
# ---------------------------------------------------------
mean_null = np.mean(null_cross_edges)
std_null = np.std(null_cross_edges)

if std_null > 0:
    z_score = (actual_cross - mean_null) / std_null
else:
    z_score = 0

print("--- EPISTEMIC READINESS (STRUCTURAL HOLE Z-SCORE) ---")
print(f"Actual Cross-Edges: {actual_cross}")
print(f"Expected Cross-Edges (Null Mean): {mean_null:.2f}")
print(f"Standard Deviation: {std_null:.2f}")
print(f"Z-Score: {z_score:.2f}")

# ---------------------------------------------------------
# THE VERDICT
# ---------------------------------------------------------
if z_score < -2.0:
    print("\n🚨 HIGH EPISTEMIC READINESS DETECTED! ")
    print("The gap between these two fields is statistically massive. ")
    print("Despite high activity on both sides, an invisible barrier keeps them apart. ")
    print("The pressure for a paradigm-shifting bridge is extremely high. ")
elif z_score > 2.0:
    print("\n⚠️ FIELDS ARE OVER-INTEGRATED. ")
    print("These communities are already heavily merged. No structural hole exists. ")
else:
    print("\n➖ NORMAL TOPOLOGY. ")
    print("The connection between these fields is exactly what random chance would predict. ")