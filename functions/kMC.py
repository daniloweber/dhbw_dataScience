import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from PIL import Image

# Set the LOKY_MAX_CPU_COUNT environment variable
os.environ['LOKY_MAX_CPU_COUNT'] = '4'  # Adjust the number as needed

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 10, "kMC-Clustering", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Helvetica", size=10)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, dataframe):
        self.set_font("Helvetica", size=10)
        col_width = self.w / (len(dataframe.columns) + 1)
        row_height = self.font_size * 1.5

        # Add column headers
        for col in dataframe.columns:
            self.cell(col_width, row_height, str(col), border=1)
        self.ln(row_height)

        # Add rows
        for row in dataframe.itertuples():
            for item in row[1:]:
                # Format numbers to fit within the cell
                if isinstance(item, (int, float)):
                    item = f"{item:.2f}"
                self.cell(col_width, row_height, str(item), border=1)
            self.ln(row_height)

    def chapter_image(self, image_path, width=180):
        self.add_page()  # Start a new page
        with Image.open(image_path) as img:
            aspect_ratio = img.height / img.width
            height = width * aspect_ratio

        current_y = self.get_y()
        self.image(image_path, x=10, y=current_y, w=width)
        self.ln(height + 10)

def kMC(file_path, csv_file_path, attribute):

    # Load the dataset
    dataset = pd.read_csv(csv_file_path)

    # Check if there are null or empty cells
    empty_cell_summary = dataset.isnull().sum().to_string()

    # Gender replace male with 0 and female with 1
    dataset['Gender'] = dataset['Gender'].map({'Male': 0, 'Female': 1})

    # Select relevant columns for clustering
    data = dataset[attribute].copy()

    # Define the stability analysis function
    def stability_analysis(X, range_n_clusters):
        optimal_k_counts = Counter()
        for _ in range(100):  # 100 iterations
            silhouette_avgs = []
            for n_clusters in range_n_clusters:
                kmeans = KMeans(n_clusters=n_clusters, random_state=None).fit(X)
                silhouette_avgs.append(silhouette_score(X, kmeans.labels_))
            optimal_k = range_n_clusters[np.argmax(silhouette_avgs)]
            optimal_k_counts[optimal_k] += 1
        return optimal_k_counts

    # Define the range of clusters
    range_n_clusters = range(2, 12)

    # Perform stability analysis
    optimal_k_counts = stability_analysis(data.values, range_n_clusters)

    # Calculate percentages
    total_iterations = sum(optimal_k_counts.values())
    k_percentages = {k: (count / total_iterations) * 100 for k, count in optimal_k_counts.items()}

    result_possible_k = []
    # Print the results
    for k, percentage in k_percentages.items():
        result_possible_k.append(f"k={k}: {percentage:.2f}%")

    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.bar(k_percentages.keys(), k_percentages.values())
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Percentage of Optimal k")
    plt.title("Percentage of Optimal k over 100 Iterations")
    plt.xticks(range_n_clusters)
    plt.savefig('kMC.png')

    # Select the optimal number of clusters
    optimal_k = max(k_percentages, key=k_percentages.get)

    # Initialize variables
    n_init = 100
    best_inertia = float('inf')
    best_seed = None

    # Perform K-Means with different random seeds
    for i in range(n_init):
        kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=i)
        kmeans.fit(data)

        # Compare inertia
        if kmeans.inertia_ < best_inertia:
            best_inertia = kmeans.inertia_
            best_seed = i

    # Perform clustering with the optimal number of clusters using the best seed
    kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=best_seed).fit(data)

    # Add cluster labels to the dataset
    data['Cluster'] = kmeans.labels_

    # Function to calculate descriptive statistics for each cluster
    def descriptive_statistics(data):
        cluster_stats = {}
        for cluster in np.unique(data['Cluster']):
            cluster_data = data[data['Cluster'] == cluster]
            stats = cluster_data.describe().T
            stats['sum'] = cluster_data.sum()
            stats['percentage'] = (cluster_data.sum() / data.sum()) * 100
            cluster_stats[cluster] = stats
        return cluster_stats

    # Calculate descriptive statistics for each cluster
    cluster_stats = descriptive_statistics(data)

    if len(attribute) <= 3:
        fig = plt.figure(figsize=(10, 8))
        if len(attribute) == 2:
            plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=kmeans.labels_, cmap='viridis')
            plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red', marker='x')
            plt.xlabel(data.columns[0])
            plt.ylabel(data.columns[1])
        elif len(attribute) == 3:
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(data.iloc[:, 0], data.iloc[:, 1], data.iloc[:, 2], c=kmeans.labels_, cmap='viridis')
            ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], s=300, c='red', marker='x')
            ax.set_xlabel(data.columns[0])
            ax.set_ylabel(data.columns[1])
            ax.set_zlabel(data.columns[2])
        plt.title('Cluster Analysis')
        plt.savefig('kMC_Cluster.png')

    if file_path != 'not needed':

        # Create PDF
        pdf = PDF()
        pdf.add_page()

        # PDF content
        pdf.chapter_title("Anzahl der Nullen im Datensatz:")
        pdf.chapter_body(empty_cell_summary)
        pdf.chapter_title("Verteilung auf die möglichen K nach dem Silhouette-Verfahren:")
        pdf.chapter_body("\n".join(result_possible_k))
        pdf.chapter_image('kMC.png', width=180)
        pdf.chapter_title("Optimales K:")
        pdf.chapter_body(str(optimal_k))
        pdf.chapter_title("Bester Startwert:")
        pdf.chapter_body(str(best_seed))
        pdf.chapter_title("Clusterzentren:")
        cluster_centers_formatted = []
        for i, center in enumerate(kmeans.cluster_centers_):
            center_str = " / ".join(map(str, center))
            cluster_centers_formatted.append(f"Clusterzentrum {i + 1}: {center_str}")

        pdf.chapter_body("\n".join(cluster_centers_formatted))
        pdf.chapter_title("Inertia:")
        pdf.chapter_body(str(kmeans.inertia_))

        if len(attribute) <= 3:
            pdf.chapter_title("Cluster-Verteilung:")
            pdf.chapter_image('kMC_Cluster.png', width=180)


        # Add descriptive statistics for each cluster
        for cluster, stats in cluster_stats.items():
            pdf.chapter_title(f"Descriptive statistics for Cluster {cluster}:")
            pdf.add_table(stats)

        # Save the PDF
        pdf.output(os.path.join(file_path, f'kMC_report_{attribute}.pdf'))

    os.remove('kMC.png')
    if len(attribute) <= 3:
        os.remove('kMC_Cluster.png')

    return data['Cluster'], kmeans.cluster_centers_

