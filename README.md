# KK24: Kultur Komitee Winterthur Budgeting Assembly Dataset

## Description
This repository contains comprehensive data and analysis code from the Kultur Komitee Winterthur 2024 (KK24) participatory budgeting process, as described in the research paper "Bridging Voting and Deliberation with Algorithms: Field Insights from vTaiwan and Kultur Komitee" (Yang & Bachmann, 2024).

KK24 represents an innovative democratic format combining elements of participatory budgeting and citizens' assemblies to allocate cultural funding in Winterthur, Switzerland. In this process, 35 randomly selected citizens allocated CHF 381,500 to cultural projects through a hybrid approach integrating algorithmic voting aggregation (Method of Equal Shares) with face-to-face deliberation in both homogeneous and heterogeneous groups.

The repository includes the complete dataset, from initial voting preferences to final funding decisions, along with the implementation of novel algorithms for group formation and voting aggregation.

## Theoretical Background
Traditional deliberative processes typically treat voting and deliberation as separate mechanisms rather than complementary parts of a unified decision-making system. The Preference-based Clustering for Deliberation (PCD) framework bridges this gap by using voting data to create more effective deliberation groups.
Group deliberation often leads to middle-ground solutions that fail to address niche interests, such as local or specific community needs. The theoretical foundations for our approach draw from key concepts in deliberative democracy, including Fraser's (1990) emphasis on creating spaces for marginalized groups to deliberate autonomously, Mansbridge's (1994) "enclaves of protected discourse," and Sunstein's (2017) "Enclave Deliberation" concept, which acknowledges both the potential to address inequalities and the risks of group polarization.

Our PCD approach implements these ideas through a structured process:

- All participants cast their votes on the projects under consideration
- Participants with similar voting patterns are grouped together for homogeneous deliberation, creating spaces where niche interests can be fully explored
- Participants are then reconfigured into diverse groups for heterogeneous deliberation, building broader consensus while ensuring minority viewpoints have already been developed

## Dataset Files

### Voting Data
- **pre_voting.pb**: Original participatory budgeting data in PB format, containing project details, costs, and individual approval votes from 38 participants across 56 cultural project proposals.
- **voter_pre_voting.csv**: Processed CSV format of the voting data where each column represents a project ID and each row represents a participant's votes ('yes', 'no', or blank).

### Deliberation Data
- **deliberation_outcomes.csv**: Complete outcomes from the deliberation process, including:
  - Points assigned by each homogeneous group (A-F) and heterogeneous group (1-6)
  - Aggregated points from homogeneous vs. heterogeneous rounds
  - Project costs and vote counts
  - Comparison with algorithmic outcomes (MES/Greedy)
  - Final selection decisions

- **grouping.csv**: Participant group assignments showing which homogeneous (A-F) and heterogeneous (1-6) groups each participant was placed in, along with attendance information.

### Project Outcomes and Reasoning
- **outcomes.csv**: Final project outcomes including vote counts, costs, and funding decisions under different scenarios:
  - MES with 190,000 CHF budget (mes190k)
  - Greedy with 190,000 CHF budget (grdy190k)
  - MES with 380,000 CHF budget (mes380k)
  - Greedy with 380,000 CHF budget (grdy380k)
  - Final allocation decisions (final)

- **reasons_all.csv**: Qualitative data capturing deliberation group reasoning, including:
  - Group identifier and points assigned
  - Project details
  - Justifications in German (reason_de) and English (reason_en)
  - Budget proposals and adjustments

### Code and Algorithms
- **radial_clustering.py**: Implementation of the Preference-based Clustering for Deliberation method using Principal Component Analysis (PCA) and the proposed Radial Clustering algorithm. This script creates balanced deliberation groups based on voting preferences and generates visualizations of the clustering results.

## Methods and Algorithms

### Radial Clustering for Group Formation
While the PCD framework can be implemented using various clustering algorithms, for the KK24 case study we employed a Radial Clustering method. Most standard clustering algorithms like k-Means create uneven groups or exclude outliers. The Radial Clustering method addresses these challenges by projecting participants into a two-dimensional opinion space and dividing it into "pizza slice" sectors, with each sector containing an equal number of participants.

The `radial_clustering.py` script implements the novel approach described in the paper for creating balanced deliberation groups based on participant preferences. The algorithm:

1. Applies Principal Component Analysis (PCA) to reduce the high-dimensional voting data to a 2D representation
2. Places participants in this 2D space based on their preference similarities
3. Divides the space radially into equal "pizza slices" to create balanced groups
4. Produces visual representations and group assignments for both homogeneous and heterogeneous deliberation rounds

### Human-in-the-Loop Method of Equal Shares (MES)
The dataset includes outcomes from the Human-in-the-Loop MES approach, which:

1. Uses the Method of Equal Shares algorithm to provide proportional representation in project selection
2. Allows participants to adjust the amount of budget allocated to algorithmic decision-making vs. deliberation
3. Provides a mechanism for participants to modify algorithmic decisions during the deliberation phase

## Citation
If you use this data in your research, please cite:
```
Yang, J. C., & Bachmann, F. (2024). Bridging Voting and Deliberation with Algorithms: Field Insights from vTaiwan and Kultur Komitee. [Publication details]
```

## Acknowledgments
We thank the entire KK24 committee and all participating Winterthur citizens and residents for their contributions to this research and to participatory democracy. Special thanks to Noemi Scheurer and Mia Odermatt, the main organizers of Kultur Komitee Winterthur, for their openness to experimenting with innovative methods.
