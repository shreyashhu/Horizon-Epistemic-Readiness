import pandas as pd
import json
import networkx as nx
import ast
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

# 1. Load the messy CSV
# (We use ast.literal_eval to safely parse the stringified Python lists back into actual lists)
df = pd.read_csv(DATA_PROCESSED_DIR / 'pilot_search_raw.csv')
nodes = []
edges = []

print("Parsing raw data into Nodes and Edges...")
for index, row in df.iterrows():
    source_id = row['paperId']
    # Add the main paper to our nodes list
    nodes.append({
        'id': source_id,
        'title': row['title'],
        'year': row['year'],
        'citationCount': row['citationCount']
    })
    
    # Parse the references
    refs_raw = row['references']
    if pd.notna(refs_raw):
        # Convert the string "[{'paperId':...}]" back into a Python list of dicts
        try:
            refs_list = ast.literal_eval(refs_raw)
            for ref in refs_list:
                target_id = ref.get('paperId')
                if target_id:
                    # Add the edge
                    edges.append({'source': source_id, 'target': target_id})
                    
                    # Add the referenced paper to nodes (if we have its title)
                    if ref.get('title'):
                        nodes.append({
                            'id': target_id,
                            'title': ref['title'],
                            'year': None, # We don't have the year from the reference object alone
                            'citationCount': 0
                        })
        except Exception as e:
            pass # Skip malformed rows

# 2. Save clean, flat CSVs (OpenOffice will love these)
nodes_df = pd.DataFrame(nodes).drop_duplicates(subset=['id'])
edges_df = pd.DataFrame(edges).drop_duplicates()

nodes_df.to_csv(DATA_PROCESSED_DIR / 'clean_nodes.csv', index=False)
edges_df.to_csv(DATA_PROCESSED_DIR / 'clean_edges.csv', index=False)

print(f"Successfully extracted {len(nodes_df)} unique nodes and {len(edges_df)} edges.")

# 3. Build the NetworkX Graph (The Machinery)
G = nx.DiGraph() # Directed Graph (Citations go from source -> target)
for _, row in nodes_df.iterrows():
    G.add_node(row['id'], title=row['title'], year=row['year'])

for _, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'])

print(f"\nGraph built successfully!")
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

# 4. The First Reality Check: Are there disconnected islands?
print(f"Connected Components (Islands): {nx.number_weakly_connected_components(G)}")

# Find the largest connected subgraph (The core knowledge cluster)
largest_cc = max(nx.weakly_connected_components(G), key=len)
print(f"Size of largest knowledge cluster: {len(largest_cc)} nodes")