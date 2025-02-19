from functions.kMC import kMC
from listOfAttributes import list_of_attributes
import numpy as np
from pdf import PDF

def analysis_4(csv_file_path):
    # Get the count of every Gender in each cluster
    attribute = list_of_attributes[4]
    data = kMC('not needed', csv_file_path, attribute)

    gender_counts = data.groupby('Cluster')['Gender'].value_counts().unstack(fill_value=0)
    results = []

    for cluster, row in gender_counts.iterrows():
        male_count = row.get(0, 0)
        female_count = row.get(1, 0)
        results.append(f"Cluster {cluster} there are {male_count} Male and {female_count} Female.")

    return results

def analysis_5(csv_file_path):
    # Get the age range, average age, and count of each Gender in the highest spending cluster
    attribute = list_of_attributes[3]
    data = kMC('not needed', csv_file_path, attribute)
    highest_spending_cluster = data.groupby('Cluster')['Spending Score (1-100)'].mean().idxmax()
    highest_spending_cluster_data = data[data['Cluster'] == highest_spending_cluster]
    highest_spending_cluster_male = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 0]
    highest_spending_cluster_female = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 1]

    male_min_age = highest_spending_cluster_male['Age'].min()
    male_max_age = highest_spending_cluster_male['Age'].max()
    male_mean_age = highest_spending_cluster_male['Age'].mean()
    male_count = len(highest_spending_cluster_male)

    female_min_age = highest_spending_cluster_female['Age'].min()
    female_max_age = highest_spending_cluster_female['Age'].max()
    female_mean_age = highest_spending_cluster_female['Age'].mean()
    female_count = len(highest_spending_cluster_female)

    results_analysis_5 = []
    results_analysis_5.append(
        f"Male: Min Age: {male_min_age}, Max Age: {male_max_age}, Avg Age: {male_mean_age}, Count: {male_count}."
    )
    results_analysis_5.append(
        f"Female: Min Age: {female_min_age}, Max Age: {female_max_age}, Avg Age: {female_mean_age}, Count: {female_count}."
    )

    return results_analysis_5

def analysis_6(csv_file_path):
    # Get the cluster with the lowest average age and the average spending score of each Gender in that cluster
    attribute = list_of_attributes[3]
    data = kMC('not needed', csv_file_path, attribute)

    lowest_age_cluster = data.groupby('Cluster')['Age'].mean().idxmin()
    lowest_age_cluster_data = data[data['Cluster'] == lowest_age_cluster]
    lowest_age_cluster_male = lowest_age_cluster_data[lowest_age_cluster_data['Gender'] == 0]
    lowest_age_cluster_female = lowest_age_cluster_data[lowest_age_cluster_data['Gender'] == 1]

    lowest_age_cluster_male_spending = lowest_age_cluster_male['Spending Score (1-100)'].sum() / len(lowest_age_cluster_male)
    lowest_age_cluster_female_spending = lowest_age_cluster_female['Spending Score (1-100)'].sum() / len(lowest_age_cluster_female)

    results_analysis_6 = []
    results_analysis_6.append(f"Lowest Age Cluster: {lowest_age_cluster}, Avg Age: {lowest_age_cluster_data['Age'].mean()}")
    results_analysis_6.append(f"Male Spending: {lowest_age_cluster_male_spending}, Count: {len(lowest_age_cluster_male)}, Total: {lowest_age_cluster_male['Spending Score (1-100)'].sum()}")
    results_analysis_6.append(f"Female Spending: {lowest_age_cluster_female_spending}, Count: {len(lowest_age_cluster_female)}, Total: {lowest_age_cluster_female['Spending Score (1-100)'].sum()}")

    return results_analysis_6

def analysis_7(csv_file_path):
    attribute = list_of_attributes[2]
    data = kMC('not needed', csv_file_path, attribute)
    dataset_mean = float(data['Annual Income (k$)'].mean())
    clusters_higher_than_dataset = []

    for cluster in np.unique(data['Cluster']):
        cluster_data = data[data['Cluster'] == cluster]
        cluster_mean = float(cluster_data['Annual Income (k$)'].mean())

        if cluster_mean > dataset_mean:
            clusters_higher_than_dataset.append((float(cluster), cluster_mean))

    # Sum the spending scores of each cluster by person
    cluster_scores = {}
    for cluster in [1, 2]:
        cluster_data = data[data['Cluster'] == cluster]
        total_spending_score = cluster_data['Spending Score (1-100)'].sum()
        num_persons = cluster_data['Spending Score (1-100)'].count()
        average_spending_score = total_spending_score / num_persons
        cluster_scores[cluster] = average_spending_score

    # Compare the average spending scores of the clusters
    higher_cluster = max(cluster_scores, key=cluster_scores.get)

    # Calculate the sum of spending score divided by count of entries for each gender in the higher cluster
    higher_cluster_data = data[data['Cluster'] == higher_cluster]
    gender_grouped = higher_cluster_data.groupby('Gender')['Spending Score (1-100)'].agg(['sum', 'count'])
    gender_grouped['average_spending_score'] = gender_grouped['sum'] / gender_grouped['count']

    results_analysis_7 = []
    results_analysis_7.append(f"Dataset Mean Annual Income is {dataset_mean:.2f}.")
    if clusters_higher_than_dataset:
        results_analysis_7.append("Clusters with a higher mean annual income than the dataset mean:")
        for c, income in clusters_higher_than_dataset:
            results_analysis_7.append(f"- Cluster {int(c)}: {income:.2f}")
    else:
        results_analysis_7.append("No clusters exceed the dataset mean annual income.")

    results_analysis_7.append(f"The cluster with the highest average spending score is {higher_cluster} with {cluster_scores[higher_cluster]:.2f}.")
    results_analysis_7.append("Spending by gender in this cluster:")

    for gender, row in gender_grouped.iterrows():
        gender_label = "Male" if gender == 0 else "Female"
        results_analysis_7.append(f"Gender {gender_label}")
        results_analysis_7.append(f"Sum: {row['sum']:.1f}")
        results_analysis_7.append(f"Count: {row['count']:.1f}")
        results_analysis_7.append(f"Avg: {row['average_spending_score']:.2f}")

    return results_analysis_7

def analysis_9(csv_file_path):
    # Get the cluster with the highest gap between normalized income and spending score
    attribute = list_of_attributes[0]
    data = kMC('not needed', csv_file_path, attribute)
    max_income_dataset = data['Annual Income (k$)'].max()
    min_income_dataset = data['Annual Income (k$)'].min()

    difference_income_spending = {}
    for cluster in np.unique(data['Cluster']):
        cluster_data = data[data['Cluster'] == cluster]
        cluster_income = cluster_data['Annual Income (k$)'].mean()
        cluster_spending = cluster_data['Spending Score (1-100)'].mean()
        normed_income = (cluster_income - min_income_dataset) / (max_income_dataset - min_income_dataset) * 100
        gap = float(normed_income) - float(cluster_spending)
        difference_income_spending[int(cluster)] = gap
    highest_gap_cluster = max(difference_income_spending, key=difference_income_spending.get)

    results_analysis_9 = []
    results_analysis_9.append(f"Cluster with the highest gap between normalized income and spending score: {highest_gap_cluster}")
    results_analysis_9.append(f"Gap: {difference_income_spending[highest_gap_cluster]:.2f}")

    return results_analysis_9

def analysis_10(csv_file_path):
    # Get the highest spending cluster, separate by Gender, and get the age and income range
    attribute = list_of_attributes[0]
    data = kMC('not needed', csv_file_path, attribute)
    highest_spending_cluster = data.groupby('Cluster')['Spending Score (1-100)'].mean().idxmax()
    highest_spending_cluster_data = data[data['Cluster'] == highest_spending_cluster]
    highest_spending_cluster_male = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 0]
    highest_spending_cluster_female = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 1]

    results_analysis_10 = []
    results_analysis_10.append(f"Highest Spending Cluster: {highest_spending_cluster}")

    results_analysis_10.append(f"Male Count: {len(highest_spending_cluster_male)}")
    results_analysis_10.append(f"Female Count: {len(highest_spending_cluster_female)}")

    results_analysis_10.append(f"Male Age Range: {highest_spending_cluster_male['Age'].min()} - {highest_spending_cluster_male['Age'].max()}")
    results_analysis_10.append(f"Female Age Range: {highest_spending_cluster_female['Age'].min()} - {highest_spending_cluster_female['Age'].max()}")
    results_analysis_10.append(f"Overall Age Range: {highest_spending_cluster_data['Age'].min()} - {highest_spending_cluster_data['Age'].max()}")

    results_analysis_10.append(f"Male Income Range: {highest_spending_cluster_male['Annual Income (k$)'].min()} - {highest_spending_cluster_male['Annual Income (k$)'].max()}")
    results_analysis_10.append(f"Female Income Range: {highest_spending_cluster_female['Annual Income (k$)'].min()} - {highest_spending_cluster_female['Annual Income (k$)'].max()}")
    results_analysis_10.append(f"Overall Income Range: {highest_spending_cluster_data['Annual Income (k$)'].min()} - {highest_spending_cluster_data['Annual Income (k$)'].max()}")

    return results_analysis_10

def cluster_analysis(directory, csv_file_path):
    # Define analysis functions and their titles
    analyses = {
        "Analysis 4": analysis_4,
        "Analysis 5": analysis_5,
        "Analysis 6": analysis_6,
        "Analysis 7": analysis_7,
        "Analysis 9": analysis_9,
        "Analysis 10": analysis_10
    }

    # Create a PDF
    pdf = PDF(title='Analysis Report')
    pdf.add_page()

    # Perform analyses and add results to the PDF
    for title, analysis_func in analyses.items():
        results = analysis_func(csv_file_path)
        pdf.chapter_title(title)
        pdf.chapter_body("\n".join(results))

    # Save the PDF to the given file path
    pdf.output(directory + '/analysis_report.pdf')
