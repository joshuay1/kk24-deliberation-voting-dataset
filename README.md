# KK24: Kultur Komitee Winterthur Budgeting Assembly Dataset

## Description
This repository contains comprehensive data and analysis code from the Kultur Komitee Winterthur 2024 (KK24) participatory budgeting process, as described in the research paper "Bridging Voting and Deliberation with Algorithms: Field Insights from vTaiwan and Kultur Komitee" (Yang & Bachmann, 2024).

KK24 represents an innovative democratic format combining elements of participatory budgeting and citizens' assemblies to allocate cultural funding in Winterthur, Switzerland. In this process, 35 randomly selected citizens allocated CHF 381,500 to cultural projects through a hybrid approach integrating algorithmic voting aggregation (Method of Equal Shares) with face-to-face deliberation in both homogeneous and heterogeneous groups.

The repository includes the complete dataset, from initial voting preferences to final funding decisions, along with the implementation of novel algorithms for group formation and voting aggregation.

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

## Research Applications
This dataset is valuable for researchers studying:
- Democratic innovations combining voting and deliberation
- Algorithmic fairness in resource allocation
- Group composition effects on deliberation outcomes
- Human-algorithm interaction in collective decision-making
- Participatory budgeting methodologies
- Preference clustering for deliberation
- Decision-making transparency and justification

## Usage Examples
```python
# Example 1: Analyze voting patterns and project popularity
import pandas as pd

# Load voting data and count approvals per project
voting = pd.read_csv('voter_pre_voting.csv')
project_votes = {col: voting[col].value_counts().get('yes', 0) for col in voting.columns[1:]}
sorted_projects = sorted(project_votes.items(), key=lambda x: x[1], reverse=True)
print("Top 5 most popular projects:")
for project_id, votes in sorted_projects[:5]:
    print(f"Project {project_id}: {votes} votes")

# Example 2: Compare deliberation outcomes between group types
delib = pd.read_csv('deliberation_outcomes.csv')
print("\nHomogeneous vs. Heterogeneous Deliberation:")
print(delib[['project_id', 'Homogeneous_points', 'Heterogeneous_points']].head(10))

# Example 3: Run the radial clustering algorithm
# python radial_clustering.py
```

## Citation
If you use this data in your research, please cite:
```
Yang, J. C., & Bachmann, F. (2024). Bridging Voting and Deliberation with Algorithms: Field Insights from vTaiwan and Kultur Komitee. [Publication details]
```

## License
[Specify license type]

## Acknowledgments
We thank the entire KK24 committee and all participating citizens for their contributions to this research and to participatory democracy. Special thanks to Noemi Scheurer and Mia Odermatt, the main organizers of Kultur Komitee Winterthur, for their openness to experimenting with innovative methods.
