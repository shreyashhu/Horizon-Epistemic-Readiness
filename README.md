# Horizon: Quantifying Epistemic Readiness in Scientific Citation Networks

<p align="center">
  <img src="outputs/gephi/horizon_map.png" alt="Horizon Topology Map" width="800"/>
  <br>
  <em><strong>Figure 1:</strong> The Tectonic Plates of AI Research (2012–2017). Colors represent distinct sub-disciplines identified via Louvain Community Detection. Node size represents citation impact.</em>
</p>

---

## Research Question

> **Can structural properties of scientific citation networks explain where breakthroughs emerge better than activity-based explanations?**

Instead of asking *"What will be discovered?"*, Horizon asks:

> **"How structurally prepared is the knowledge landscape for a discovery?"**

By modeling scientific citation networks as dynamic topological maps, Horizon attempts to identify **Structural Holes**—regions where distinct scientific sub-disciplines are highly active but remain topologically isolated.

The central hypothesis is that when **Epistemic Readiness** (the pressure to bridge these structural gaps) reaches a critical threshold, the scientific landscape becomes increasingly favorable for paradigm-shifting breakthroughs.

---

## Why Horizon Matters

Most forecasting approaches focus on:

* Publication counts
* Citation accumulation
* Funding intensity
* Research activity

Horizon explores a different possibility:

> The structure of knowledge itself may contain predictive information.

Rather than predicting specific discoveries, Horizon seeks to quantify whether a research landscape is becoming structurally prepared for one.

---

## Empirical Findings (Phase 0.5)

To validate the methodology, Horizon ingested the **1,000 most-cited Deep Learning papers (2012–2017)** through the OpenAlex API and reconstructed the resulting citation topology.

### 1. Topological Mapping

Using the **Louvain Community Detection Algorithm**, the network spontaneously fractured into twelve distinct "tectonic plates" based purely on citation behavior.

Representative examples include:

#### Plate A (Community 7)

Sequence Modeling, NLP, and Relational Learning

Examples:

* Word2Vec
* LSTMs
* Bahdanau Attention

#### Plate B (Community 9)

Algorithmic Control, Reinforcement Learning, and Scientific ML

Examples:

* AlphaGo
* PyTorch
* Quantum Chemistry applications

#### Plate C

Computer Vision and Generative Models

Examples:

* ResNet
* GANs
* YOLO

Notably, these communities emerged without manual labeling and were inferred solely from citation topology.

---

### 2. Measuring Epistemic Readiness

To determine whether the separation between NLP (Plate A) and RL/Scientific ML (Plate B) represented a genuine structural barrier rather than random variation, Horizon generated **100 randomized universes** using a **Degree-Preserving Configuration Model**.

#### Results

| Metric                           | Value       |
| -------------------------------- | ----------- |
| Expected Cross-Edges (Null Mean) | 113.62      |
| Actual Cross-Edges               | 68          |
| Structural Hole Z-Score          | -5.81       |
| Significance                     | p < 0.00001 |

The observed separation was significantly deeper than expected under the null model, suggesting a statistically meaningful structural hole.

---

## Discussion & Limitations

The pilot study demonstrates that:

* Citation topology contains measurable large-scale structure.
* Structural holes can be quantified statistically.
* Degree-preserving null models provide meaningful significance estimates.
* Community boundaries align closely with recognizable scientific sub-disciplines.

However, the pilot does **not** establish predictive power.

Whether structural holes actively precede future breakthroughs remains an open empirical question.

Examples often cited in this context include:

* AlphaFold 2
* Decision Transformers
* Cross-domain foundation models

Phase 2 will rigorously test whether regions exhibiting high Epistemic Readiness subsequently generate a higher rate of breakthrough papers than activity-based baselines.

### Methodological Note

The pilot utilized 100 randomized universes.

Future phases will increase this to 1,000+ null-model iterations to support publication-grade significance estimates.

---

## Current Status

### ✅ Phase 0.5 Complete

Validated:

* OpenAlex data density and coverage
* Citation topology reconstruction
* Louvain community detection
* Structural-hole significance testing
* Gephi visualization workflow

### 🟡 Current Focus

**Phase 1: Temporal Community Tracking (1990–2015)**

Implemented:

* Temporal data collection pipeline

Upcoming:

* Jaccard similarity matching
* Community lineage tracking
* Merge/split detection
* Longitudinal structural-hole analysis

---

## Project Roadmap

| Phase | Objective                               | Status         |
| ----- | --------------------------------------- | -------------- |
| 0.5   | Pilot Study & Reality Audit             | ✅ Complete     |
| 1     | Temporal Community Tracking             | 🟡 In Progress |
| 2     | Historical Backtesting & AUC Evaluation | ⚪ Planned      |
| 3     | Interactive Dashboard                   | ⚪ Planned      |

### Phase 1: Temporal Community Tracking

* Track communities across time
* Detect merges and splits
* Build lineage graphs
* Measure changing epistemic pressure

### Phase 2: Historical Backtesting

Compare:

* H₀: Stochastic Emergence
* H₁: Activity-Based Emergence
* H₂: Epistemic Readiness

Against real historical breakthroughs.

### Phase 3: Interactive Dashboard

Deploy a Streamlit application allowing users to:

* Explore topology maps
* Scrub through time
* Observe community evolution
* Monitor structural holes

---

## 📂 Repository Structure

```text
Horizon-Epistemic-Readiness/
│
├── data/
│   ├── raw/                     # Temporal OpenAlex snapshots
│   └── processed/               # Cleaned node/edge CSVs
│
├── src/
│   │
│   ├── 🟢 ACTIVE PIPELINE (Phase 0.5)
│   │   ├── openalex_cluster.py
│   │   ├── measure_pressure.py
│   │   ├── inspect_plates.py
│   │   └── export_for_gephi.py
│   │
│   ├── 🟡 AUDIT & FUTURE PHASES
│   │   ├── openalex_audit.py
│   │   └── fetch_temporal_data.py
│   │
│   ├── ⚪ LEGACY PIPELINE
│   │   ├── build_graph.py
│   │   ├── cluster_graph.py
│   │   └── cluster_csv.py
│   │
│   └── __init__.py
│
├── outputs/
│   └── gephi/
│
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Script Evolution

Several standalone prototypes were developed during Horizon's early construction to validate graph-building and clustering workflows.

As the project matured, their functionality was consolidated into `openalex_cluster.py`, which now serves as the primary ingestion and community-detection pipeline.

Legacy scripts remain for:

* Reproducibility
* Historical comparison
* Methodological transparency
* Regression testing

---

## Step-by-Step Setup & Execution Guide

### Step 1: Environment Setup

```bash
git clone https://github.com/shreyashhu/Horizon-Epistemic-Readiness.git
cd Horizon-Epistemic-Readiness

python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### Step 2: Configure API Credentials

Create a local `config.py` file:

```python
EMAIL = "your_actual_email@example.com"
```

Verify that `config.py` is listed in `.gitignore`.

---

### Step 3: Run the Phase 0.5 Pipeline

```bash
python src/openalex_cluster.py
python src/measure_pressure.py
python src/inspect_plates.py
python src/export_for_gephi.py
```

Outputs will be generated in:

```text
data/processed/
outputs/gephi/
```

---

### Step 4: Generate Temporal Data (Phase 1)

```bash
python src/fetch_temporal_data.py
```

---

## Visualizing the Topology in Gephi

### 1. Open the Network

Load:

```text
outputs/gephi/horizon_openalex_map.gexf
```

### 2. Run ForceAtlas2

Recommended settings:

* Prevent Overlap: Enabled
* Scaling: 10

Allow the graph to stabilize before stopping the layout.

### 3. Color by Community

Appearance → Nodes → Partition → `community`

### 4. Scale by Impact

Appearance → Nodes → Ranking → Degree

Recommended:

* Min Size: 10
* Max Size: 60

### 5. Enable Labels & Export

* Enable labels
* Scale labels proportionally
* Export a high-resolution PNG

---

## Data Sources & Acknowledgments

### OpenAlex

Provides the citation metadata used throughout Horizon.

### NetworkX

Graph construction and network analysis.

### Python-Louvain

Community detection and modularity optimization.

### Gephi

Topology visualization and ForceAtlas2 layout generation.

---

## License

This project is built for academic research, computational scientometrics, and exploratory network science.

Contributions, critiques, and methodological discussions are welcome.
