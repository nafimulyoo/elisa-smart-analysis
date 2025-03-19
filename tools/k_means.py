import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from metagpt.tools.tool_registry import register_tool
import matplotlib.pyplot as plt

@register_tool()
def kmeans_clustering_auto(dataframe: pd.DataFrame, max_clusters: int = 10, random_state: int = 42) -> pd.DataFrame:
    """
    Perform KMeans clustering on the input DataFrame with automatic determination of the optimal number of clusters.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing numerical data for clustering.
        max_clusters (int): The maximum number of clusters to consider. Default is 10.
        random_state (int): Random seed for reproducibility. Default is 42.

    Returns:
        pd.DataFrame: The input DataFrame with an additional column 'cluster' for cluster labels.
    """
    # Select only numerical columns for clustering
    X = dataframe.select_dtypes(include=['number'])

    # Calculate Within-Cluster-Sum of Squared Errors (WCSS) for different numbers of clusters
    wcss = []
    silhouette_scores = []
    cluster_range = range(2, max_clusters + 1)

    for n in cluster_range:
        kmeans = KMeans(n_clusters=n, random_state=random_state)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))

    # Determine the optimal number of clusters using the Elbow Method
    optimal_clusters = _find_optimal_clusters(wcss, cluster_range)

    # Perform KMeans clustering with the optimal number of clusters
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(X)

    # Add cluster labels to the DataFrame
    dataframe['cluster'] = clusters

    return dataframe

def _find_optimal_clusters(wcss: list, cluster_range: range) -> int:
    """
    Determine the optimal number of clusters using the Elbow Method.

    Args:
        wcss (list): List of Within-Cluster-Sum of Squared Errors (WCSS) for each number of clusters.
        cluster_range (range): Range of cluster numbers considered.

    Returns:
        int: The optimal number of clusters.
    """
    # Calculate the differences in WCSS
    wcss_diff = np.diff(wcss)
    wcss_diff_ratio = wcss_diff[:-1] / wcss_diff[1:]

    # Find the "elbow" point (where the change in WCSS starts to level off)
    optimal_clusters = cluster_range[np.argmax(wcss_diff_ratio) + 1]
    return optimal_clusters
