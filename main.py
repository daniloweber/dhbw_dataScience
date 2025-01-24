import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter

dataset = pd.read_csv('kunden_einkaufszentrum.csv')

#check if there are null or empty cells
print(dataset.isnull().sum())

#gender replace male with 0 and female with 1
dataset['Gender'] = dataset['Gender'].map({'Male': 0, 'Female': 1})

#Summary statistics
summary = dataset.describe()
print(summary)

data = dataset[['Gender', 'Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
# k-means clustering

range_n_clusters = range(2,11)
iterations = 100

k_counts = Counter()

#elbow method
for _ in range(iterations):
    sse = []
    for n_clusters in range_n_clusters:
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++')
        kmeans.fit(data)
        sse.append(kmeans.inertia_)

    # Determine the optimal k using the Elbow method
    optimal_k = range_n_clusters[np.argmin(np.diff(sse, 2))]
    k_counts[optimal_k] += 1

# Calculate percentages
total_iterations = sum(k_counts.values())
k_percentages = {k: (count / total_iterations) * 100 for k, count in k_counts.items()}

# Print the results
for k, percentage in k_percentages.items():
    print(f"k={k}: {percentage:.2f}%")

# Plot the results
plt.figure(figsize=(8, 5))
plt.bar(k_percentages.keys(), k_percentages.values())
plt.xlabel("Anzahl Cluster (k)")
plt.ylabel("Prozentsatz der optimalen k")
plt.title("Prozentsatz der optimalen k über 100 Iterationen")
plt.xticks(range_n_clusters)
plt.show()


