![Figure 1: The Tectonic Plates of AI Research (2012–2017)](outputs/gephi/horizon_map.png)
*Figure 1: Topological map of the 2012-2017 Deep Learning boom. Colors represent distinct sub-disciplines identified via Louvain Community Detection. Node size represents citation impact. The visual gap between the NLP and RL clusters represents the structural hole quantified in the pilot study.*

# Horizon: Epistemic Readiness in Scientific Networks

Conventional scientometrics measures velocity: who is publishing, how fast, and who is citing whom. 

Horizon asks a different question: **How structurally prepared is the knowledge landscape for a discovery?**

By modeling scientific citation networks as dynamic topological maps, Horizon identifies "Structural Holes"—regions where distinct sub-disciplines are highly active but artificially isolated. The core hypothesis is that when the "Epistemic Readiness" (the pressure to bridge these gaps) reaches a critical threshold, the landscape **may become increasingly favorable for a paradigm-shifting breakthrough.**

---

## The Pilot Study: The 2012–2017 Deep Learning Boom

To validate the methodology, Horizon ingested the **1,000 most-cited Deep Learning papers (2012–2017)** via the OpenAlex API and mapped the citation topology.

Using the **Louvain Community Detection Algorithm**, the network spontaneously fractured into distinct "tectonic plates" based purely on lateral citation behavior, including:
- **Plate A (Community 7):** Sequence Modeling, NLP, and Relational Learning (e.g., Word2Vec, LSTMs, Bahdanau Attention).
- **Plate B (Community 9):** Algorithmic Control, Reinforcement Learning, and Scientific ML (e.g., AlphaGo, PyTorch, Quantum Chemistry).
- **Plate C:** Core Computer Vision and Generative Models (e.g., ResNet, GANs, YOLO).

To determine if the gap between NLP and RL/Scientific ML was a true structural barrier or just random noise, Horizon generated **100 randomized universes** of the citation graph using a **Degree-Preserving Configuration Model**.

- **Expected Cross-Edges (Null Mean):** 113.62
- **Actual Cross-Edges:** 68
- **Structural Hole Z-Score:** `-5.81` (p < 0.00001)

**The Finding:** The observed separation between these specific sub-disciplines during the 2012–2017 window was **significantly deeper than expected under the null model.**

### What is Proven
- Community structure exists in the citation network.
- A structural hole exists between NLP and RL/Scientific ML.
- The null model confirms this separation is statistically significant.

### What is NOT Proven (The Open Question)
- **Structural holes predict breakthroughs.**

We demonstrated that the topological gap was real. We have *not* yet demonstrated that this topological gap actively predicts the emergence of cross-domain breakthroughs (like AlphaFold 2 or Decision Transformers). Phase 2 is designed specifically to test this causal link against historical baselines.

---

## Repository Structure & Script Status

The `/src` directory contains the pipeline scripts. They are divided into **Pilot Scripts** (used to generate the current findings) and **Future Phase Scripts** (built but not yet executed, awaiting the next research phase).

### Pilot Scripts (Completed)
These scripts were used to generate the pilot findings:
- `openalex_audit.py`: Phase 0.5 audit. Validates OpenAlex API data density and lateral citation topology to ensure the "Rich Club" was captured.
- `openalex_cluster.py` / `cluster_csv.py` / `cluster_graph.py`: Ingests data, builds the citation graph, and applies Louvain community detection to identify sub-disciplines.
- `measure_pressure.py`: Calculates the Epistemic Readiness Z-Score using the degree-preserving null model.
- `inspect_plates.py`: Semantic sampling script to manually inspect and label the discovered communities (e.g., NLP vs. RL).
- `export_for_gephi.py`: Exports the clustered graph to `.gexf` for topological visualization in Gephi.
- `build_graph.py`: Utility to parse raw API JSON/CSV dumps into clean node/edge lists.

### Future Phase Scripts (Ready for Next Steps)
These scripts are written and ready to be executed for the upcoming research phases:
- `fetch_temporal_data.py`: **(For Phase 1)** Fetches a broader temporal slice (1990–2015) from OpenAlex. 
  - *Why it's not used yet:* The pilot only required a static 2012-2017 window to prove the topological concept. This script is queued to build the year-over-year snapshots needed for temporal lineage tracking in Phase 1.

---

## Roadmap

- [x] **Phase 0.5: Pilot Study & Reality Audit**
  - Validated OpenAlex API data density.
  - Proved Louvain clustering successfully isolates semantic sub-disciplines.
  - Validated the Null Model Z-Score math against Super-Hub noise.
- [ ] **Phase 1: Temporal Community Tracking (1990-2015)**
  - Execute `fetch_temporal_data.py`.
  - Implement Jaccard Similarity to track how communities merge, split, and evolve year-over-year.
- [ ] **Phase 2: Historical Backtesting & AUC Evaluation**
  - Test H₀ (Stochastic), H₁ (Activity/Rich-get-richer), and H₂ (Epistemic Readiness) against actual historical breakthroughs.
- [ ] **Phase 3: Interactive Web Dashboard**
  - Deploy a Streamlit application allowing users to scrub through time and watch Epistemic Pressure build in real-time.

---

## Setup & Usage

### Requirements
- **Python 3.9+**
- An email address (OpenAlex provides a significantly faster "polite pool" API rate limit if you include your email in the request headers).

### Installation
```bash
# Clone the repository
git clone https://github.com/shreyashhu/Horizon-Epistemic-Readiness.git
cd Horizon-Epistemic-Readiness

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
OpenAlex requires an email for the polite pool. To protect your privacy, use a local config file:
1. Create a file named `config.py` in the root directory.
2. Add your email:
   ```python
   # config.py
   EMAIL = "your_actual_email@example.com"
   ```
3. Verify that `config.py` is listed in `.gitignore`.

### Execution (Pilot Pipeline)
Run these scripts sequentially from the root directory to replicate the pilot study:
```bash
python src/openalex_audit.py
python src/openalex_cluster.py
python src/measure_pressure.py
python src/inspect_plates.py
python src/export_for_gephi.py
```

### Visualizing the Topology (Gephi)
1. Download and install [Gephi](https://gephi.org/).
2. Open Gephi and import `outputs/gephi/horizon_openalex_map.gexf`.
3. In the **Layout** panel, select `ForceAtlas 2`.
   - ✅ Check `Prevent Overlap`
   - Change `Scaling` to `10.0`
   - Click `Run`, wait 10-15 seconds, then click `Stop`.
4. In the **Appearance** panel (Nodes > Palette), partition by `community`.
5. In the **Appearance** panel (Nodes > Size > Ranking), rank by `Degree` (Min: 10, Max: 60).
6. Export as PNG to `outputs/gephi/horizon_map.png`.

---

## Acknowledgments
- **OpenAlex:** For providing an open, comprehensive catalog of the global research system.
- **NetworkX & Python-Louvain:** For graph construction and modularity-based community detection.
- **Gephi:** For high-resolution topological rendering.

*This project is built for academic research and computational scientometrics exploration.*
```