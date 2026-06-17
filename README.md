#  Horizon: Quantifying Epistemic Readiness in Scientific Citation Networks

<p align="center">
  <img src="outputs/gephi/horizon_map.png" alt="Horizon Topology Map" width="800"/>
  <br>
  <em><strong>Figure 1:</strong> The Tectonic Plates of AI Research (2012–2017). Colors represent distinct sub-disciplines identified via Louvain Community Detection. Node size represents citation impact.</em>
</p>

**Horizon** is a computational scientometrics engine designed to measure the structural topology of human knowledge. 

Instead of asking *"What will be discovered?"*, Horizon asks: **"How structurally prepared is the knowledge landscape for a discovery?"**

By modeling scientific citation networks as dynamic topological maps, Horizon identifies "Structural Holes"—regions where distinct sub-disciplines are highly active but artificially isolated. When the "Epistemic Readiness" (the pressure to bridge these gaps) reaches a critical threshold, the landscape is primed for a paradigm-shifting breakthrough.

---

##  Phase 0.5 Results: The Pilot Study

To validate the methodology, Horizon ingested the **1,000 most-cited Deep Learning papers (2012–2017)** via the OpenAlex API and mapped the citation topology.

### 1. Topological Mapping
Using the **Louvain Community Detection Algorithm**, the network spontaneously fractured into 12 distinct "tectonic plates" based purely on lateral citation behavior, including:
*   **Plate A:** Sequence Modeling, NLP, and Relational Learning (e.g., Word2Vec, LSTMs, Attention).
*   **Plate B:** Algorithmic Control, Reinforcement Learning, and Scientific ML (e.g., AlphaGo, PyTorch, Quantum Chemistry).
*   **Plate C:** Core Computer Vision and Generative Models (e.g., ResNet, GANs).

### 2. Measuring Epistemic Readiness (The Null Model)
To determine if the gap between NLP (Plate A) and RL/Scientific ML (Plate B) was a true structural barrier or just random noise, Horizon generated **100 randomized universes** of the citation graph using a **Degree-Preserving Configuration Model**.

*   **Expected Cross-Edges (Null Mean):** 113.62
*   **Actual Cross-Edges:** 68
*   **Structural Hole Z-Score:** `-5.81` (p < 0.00001)

**Conclusion:** Despite massive research volume on both sides, an invisible epistemic barrier kept Sequence Modeling and Algorithmic Control isolated. This mathematically quantified the "readiness" of the field for a bridge. Within three years, that exact structural hole was collapsed by breakthroughs like **AlphaFold 2** and **Decision Transformers**, which fused sequence attention with scientific and control environments.

---

##  Project Roadmap

- [x] **Phase 0.5: Pilot Study & Reality Audit** 
  - Validated OpenAlex API data density and lateral citation topology.
  - Proved Louvain clustering successfully isolates semantic sub-disciplines.
  - Validated the Null Model Z-Score math against Super-Hub noise.
- [ ] **Phase 1: Temporal Community Tracking (1990-2015)**
  - Implement Jaccard Similarity to track how communities merge, split, and evolve year-over-year.
- [ ] **Phase 2: Historical Backtesting & AUC Evaluation**
  - Test H₀ (Stochastic), H₁ (Activity/Rich-get-richer), and H₂ (Epistemic Readiness) against actual historical breakthroughs.
- [ ] **Phase 3: Interactive Web Dashboard**
  - Deploy a Streamlit application allowing users to scrub through time and watch Epistemic Pressure build in real-time.

---

## 📂 Repository Structure

```text
Horizon-Epistemic-Readiness/
│
├── data/
│   └── processed/       # Cleaned openalex_nodes.csv and openalex_edges.csv
│
├── src/                 # Core scientific logic and API ingestion scripts
│
├── outputs/             
│   └── gephi/           # .gexf files and topology screenshots
│
├── .gitignore
└── README.md
```

---

##  Setup & Installation

### 1. Prerequisites
*   **Python 3.9+**
*   An email address (OpenAlex provides a significantly faster "polite pool" API rate limit if you include your email in the request headers).

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Horizon-Epistemic-Readiness.git
cd Horizon-Epistemic-Readiness

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install networkx pandas requests python-louvain numpy pyvis
```

---

##  Data Sources & Acknowledgments

*   **OpenAlex:** Horizon relies entirely on the [OpenAlex](https://openalex.org/) index, which provides a fully open, comprehensive, and un-embargoed catalog of the global research system.
*   **NetworkX & Python-Louvain:** For graph construction and modularity-based community detection.
*   **Gephi:** For high-resolution topological rendering and ForceAtlas2 layout generation.

---

##  License
This project is built for academic research and computational scientometrics exploration.
```
