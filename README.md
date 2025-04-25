# 2025 Canadian Federal Election Compass

The Compass can be accessed here: https://2025-voting-compass.streamlit.app/

**Author**: Adam Smith-Orlik  
**Version**: 1.0.4
**Last Updated**: April 24, 2025

**Updates**
April 15, 2025

1. Fixed Religious Liberty scale to reflect the correct Left/Right positions
2. Fixed Conservative positions for Military Spending and Foreign Aid
3. Added a legend to visuals
4. Minor aesthetic changes to Radar Plot

April 16, 2025

1. Added GPT-API results with justifications for tranparency
2. Added button before survey to change the party position data
3. GPT responses saved for fact chacking in the GPT-API/data/ folder

April 24, 2025

1. Added updated data based on the 2025 party platforms
2. Refactored the codebase for readability

---

## Overview

The 2025 Canadian Federal Election Compass is a political alignment tool designed to help voters evaluate which major party—**Liberal**, **Conservative**, or **NDP**—most closely aligns with their personal views on key policy issues.

Unlike traditional political quizzes, this app:

- Covers broad politcal values instead of hot-button topics
- Allows users to express **how strongly** they hold a view by weighting their responses importance
- Uses a **Euclidean distance** to measure absolute distance and **cosine similarity** to measure alignment
- Provides clear, interpretable **results** and **visualizations** including tables, number lines, a radar plot, and principle component analysis plots

The project is built in Python using Streamlit and is fully open source.

---

## Key Features

- **Survey-Based Input**: Rate your stance from -1 (strong opposition) to +1 (strong support) across a curated set of political topics
- **Importance Weighting**: Assign relative importance to each issue (0 to 1 scale)
- **Alignment Metrics**:
  - **Weighted Euclidean Distance** (closeness in policy space)
  - **Weighted Cosine Similarity** (directional agreement)
- **Visualizations**:
  - Number line plots per topic
  - Radar plots by dimension
  - 2D and 3D PCA ideological projections
- **Detailed Results Tables**:
  - Per-topic alignment with each party
  - Summary of closest/furthest matches
- Session-safe: Survey inputs persist within a session for analysis across tabs

---

## Topics Covered

The compass evaluates alignment across 8 broad dimensions and over 30 subtopics, including:

- Economic Policy (taxation, fiscal discipline, minimum wage)
- Social Reforms (healthcare, education, immigration, housing)
- Environment (carbon pricing, green investment, fossil fuel stance)
- Science and Technology (AI, research funding, internet access)
- Governance and Institutions (transparency, federalism, electoral reform)
- Foreign Policy and Defense (military spending, trade, global conflicts)
- Justice and Civil Liberties (free speech, privacy, police reform, religious liberty)
- Cultural and Social Topics (curriculum control, DEI, refugee policy)

All party positions are approximated based on public statements, platforms, and cross-referenced summaries derived using multiple LLMs and media sources.

---
