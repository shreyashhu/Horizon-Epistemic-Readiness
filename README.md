# Horizon: Quantifying Epistemic Readiness in Scientific Citation Networks

**Horizon** is a computational scientometrics engine designed to measure the structural topology of human knowledge. Instead of asking "What will be discovered?", Horizon asks: *"How structurally prepared is the knowledge landscape for a discovery?"*

## Core Methodology
1. **Data Ingestion:** Pulls dense citation networks from the OpenAlex API.
2. **Topological Mapping:** Uses the Louvain algorithm to identify "tectonic plates" (sub-disciplines) of research.
3. **Epistemic Readiness Metric:** Calculates a Structural Hole Z-Score using a Degree-Preserving Configuration Model (Null Model) to identify regions of high interdisciplinary pressure.

## Current Status
- [x] Phase 0.5: Pilot Study & Reality Audit (OpenAlex API validation)
- [x] Phase 0.5: Static Community Detection & Null Model Math (Z-score validation)
- [ ] Phase 1: Temporal Community Tracking (1990-2015)
- [ ] Phase 2: Historical Backtesting & AUC Evaluation

## Setup
```bash
pip install networkx pandas requests python-louvain numpy