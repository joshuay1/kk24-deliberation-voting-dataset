"""
KK24 Radial Clustering Visualization

This script implements the Radial Clustering method described in the paper
"Bridging Voting and Deliberation with Algorithms: Field Insights from vTaiwan and Kultur Komitee".

The algorithm projects participant preferences into a two-dimensional space using PCA,
then partitions them into balanced groups by dividing the space into "pizza slices"
based on angular positions around a central point.

Author: [Your Name]
License: [License Type]
"""

import matplotlib.cm as cm
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

# Configuration
NUM_CLUSTERS = 6  # Number of deliberation groups to create
OUTPUT_FILENAME = 'radial_clustering_visualization.pdf'
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Custom color palette for visualization
CLUSTER_COLORS = {
    'A': '#264653',  # Dark blue
    'B': '#e76f51',  # Coral
    'C': '#2a9d8f',  # Teal
    'D': '#e9c46a',  # Yellow
    'E': '#f4a261',  # Orange
    'F': '#00b4d8'   # Light blue
}

def load_and_preprocess_data(filepath):
    """
    Load voter preference data and preprocess for PCA.
    
    Args:
        filepath: Path to the voting data CSV file
        
    Returns:
        DataFrame with preprocessed data
    """
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Convert voting options to numeric values
    # The CSV contains 'yes', 'no', or empty cells (abstain/skip)
    for col in df.columns[1:]:  # Skip participant ID column
        df[col] = df[col].map({'yes': 1, 'no': 0, np.nan: 0.5})
    
    # Handle missing values
    df.fillna(0.5, inplace=True)  # Treat missing votes as abstain
    
    return df

def apply_pca(df):
    """
    Apply PCA to reduce data dimensionality to 2 components.
    
    Args:
        df: DataFrame with preprocessed voting data
        
    Returns:
        DataFrame with PCA components and participant IDs
    """
    # Extract participant IDs
    participant_ids = df['pid'].copy()
    
    # Standardize the data (only numeric columns, skip participant ID)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df.iloc[:, 1:])  # Exclude participant ID column
    
    # Apply PCA
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(scaled_data)
    
    # Create DataFrame with PCA results
    pca_df = pd.DataFrame(pca_components, columns=['PC1', 'PC2'])
    pca_df['pid'] = participant_ids
    
    # Display variance explained
    explained_variance = pca.explained_variance_ratio_
    print("\nExplained Variance Ratio:")
    for i, var in enumerate(explained_variance):
        print(f"PC{i+1}: {var:.4f}")
    print(f"Total: {sum(explained_variance):.4f}")
    
    return pca_df

def find_optimal_clustering(pca_df, num_clusters=6):
    """
    Find the optimal angular offset for radial clustering to create balanced groups.
    
    Args:
        pca_df: DataFrame with PCA components
        num_clusters: Number of clusters to create
        
    Returns:
        DataFrame with cluster assignments, optimal angle offset
    """
    print("\nFinding optimal cluster arrangement...")
    total_participants = len(pca_df)
    
    # Calculate how many clusters need extra participants for even distribution
    participants_per_cluster = total_participants // num_clusters
    clusters_with_extra = total_participants % num_clusters
    
    # Generate cluster labels (A-F)
    cluster_labels = list('ABCDEF')[:num_clusters]
    
    # Try different angle offsets to find optimal grouping
    for initial_angle_offset in range(0, 360, 1):
        # Calculate central point and angles
        central_point = [pca_df['PC1'].mean(), pca_df['PC2'].mean()]
        angles = -np.arctan2(pca_df['PC2'] - central_point[1], pca_df['PC1'] - central_point[0])
        angles_degrees = (np.degrees(angles) + initial_angle_offset + 360) % 360
        
        # Sort participants by angle
        temp_df = pca_df.copy()
        temp_df['Angle'] = angles_degrees
        temp_df_sorted = temp_df.sort_values('Angle')
        
        # Distribute participants to clusters
        assignments = []
        current_label = 0
        
        # Assign participants_per_cluster to each group
        for i in range(num_clusters):
            if i < clusters_with_extra:
                # These clusters get an extra participant
                assignments += [cluster_labels[i]] * (participants_per_cluster + 1)
            else:
                assignments += [cluster_labels[i]] * participants_per_cluster
        
        # Ensure we don't exceed the number of participants
        assignments = assignments[:total_participants]
        
        # Apply assignments to sorted DataFrame
        temp_df_sorted['Cluster'] = assignments
        
        # Map assignments back to original DataFrame
        cluster_mapping = dict(zip(temp_df_sorted.index, temp_df_sorted['Cluster']))
        temp_df['Cluster'] = temp_df.index.map(cluster_mapping)
        
        # Check if we have balanced clusters (6-7 participants each)
        cluster_sizes = temp_df.groupby('Cluster').size()
        if cluster_sizes.min() >= participants_per_cluster and cluster_sizes.max() <= participants_per_cluster + 1:
            print(f"Optimal arrangement found with angle offset: {initial_angle_offset}°")
            print("Cluster sizes:", dict(cluster_sizes))
            return temp_df, initial_angle_offset
    
    print("Warning: Could not find optimal arrangement")
    return None, None

def visualize_clusters(df_with_clusters, central_point):
    """
    Create visualization of the radial clustering results.
    
    Args:
        df_with_clusters: DataFrame with cluster assignments
        central_point: [x, y] coordinates of the central point
    """
    print("\nGenerating visualization...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Add color information
    df_with_clusters['Color'] = df_with_clusters['Cluster'].map(CLUSTER_COLORS)
    
    # Calculate and draw boundary lines between clusters
    cluster_labels = sorted(df_with_clusters['Cluster'].unique(), 
                           key=lambda x: df_with_clusters[df_with_clusters['Cluster'] == x]['Angle'].min())
    
    boundary_angles = []
    for i in range(len(cluster_labels)):
        current_cluster = cluster_labels[i]
        next_cluster = cluster_labels[(i + 1) % len(cluster_labels)]
        
        max_angle_current = df_with_clusters[df_with_clusters['Cluster'] == current_cluster]['Angle'].max()
        min_angle_next = df_with_clusters[df_with_clusters['Cluster'] == next_cluster]['Angle'].min()
        
        # Handle wrap-around at 360 degrees
        if min_angle_next < max_angle_current:
            min_angle_next += 360
            
        boundary_angle = (max_angle_current + min_angle_next) / 2 % 360
        boundary_angles.append(-boundary_angle + 30)
    
    # Draw boundary lines
    boundary_angles = sorted(boundary_angles)
    for boundary in boundary_angles:
        rad = np.radians(boundary)
        ax.plot(
            [central_point[0], central_point[0] + 5 * np.cos(rad)],
            [central_point[1], central_point[1] + 5 * np.sin(rad)],
            color='black', linestyle='--', linewidth=1, alpha=0.7
        )
    
    # Fill cluster areas with transparent colors
    for cluster_label, color in CLUSTER_COLORS.items():
        cluster_points = df_with_clusters[df_with_clusters['Cluster'] == cluster_label][['PC1', 'PC2']].values
        if len(cluster_points) > 2:
            hull = ConvexHull(cluster_points)
            for simplex in hull.simplices:
                plt.fill(cluster_points[simplex, 0], cluster_points[simplex, 1], color=color, alpha=0.2)
    
    # Plot participants
    ax.scatter(df_with_clusters['PC1'], df_with_clusters['PC2'], 
               c=df_with_clusters['Color'], s=100)
    
    # Plot central point
    ax.scatter(*central_point, color='red', s=200, label='Center Point')
    
    # Add legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=f'Group {label}', 
                          markersize=10, markerfacecolor=color) 
               for label, color in CLUSTER_COLORS.items()]
    handles.append(plt.Line2D([0], [0], marker='o', color='red', label='Center Point', markersize=10))
    ax.legend(handles=handles, fontsize='13', loc='upper right')
    
    # Add labels and title
    ax.set_xlabel('Principal Component 1', fontsize='13')
    ax.set_ylabel('Principal Component 2', fontsize='13')
    plt.title('Radial Clustering for Deliberation Group Formation', fontsize='15')
    
    # Save figure
    plt.savefig(OUTPUT_FILENAME, format='pdf', bbox_inches='tight')
    print(f"Visualization saved as {OUTPUT_FILENAME}")
    
    plt.show()

def main():
    """
    Main function to run the Radial Clustering algorithm and visualization.
    """
    # Load and preprocess data
    df = load_and_preprocess_data('voter_pre_voting.csv')
    
    # Apply PCA
    pca_df = apply_pca(df)
    
    # Calculate central point
    central_point = np.array([pca_df['PC1'].mean(), pca_df['PC2'].mean()])
    
    # Find optimal clustering
    optimal_grouping, angle_offset = find_optimal_clustering(pca_df, NUM_CLUSTERS)
    
    if optimal_grouping is not None:
        # Visualize the results
        visualize_clusters(optimal_grouping, central_point)
        
        # Save cluster assignments
        output_file = 'radial_clustering_assignments.csv'
        optimal_grouping[['pid', 'Cluster']].to_csv(output_file, index=False)
        print(f"Cluster assignments saved to {output_file}")
        
        # For debug: Verify cluster sizes
        print("\nCluster sizes:")
        print(optimal_grouping.groupby('Cluster').size())
    else:
        print("Error: Could not find suitable clustering arrangement")

if __name__ == "__main__":
    main()