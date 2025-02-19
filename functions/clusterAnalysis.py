from functions.kMC import kMC
from main import csv_file_path
from list_of_attributes import list_of_attributes
import numpy as np


def analysis_4():
    attribute = list_of_attributes[4]
    data = kMC('not needed', csv_file_path, attribute)
    gender_count = []
    # count the gender in each cluster
    for cluster in np.unique(data['Cluster']):
        cluster_data = data[data['Cluster'] == cluster]
        gender_counts = cluster_data['Gender'].value_counts()
        print(f"Gender counts in Cluster {cluster}:")
        gender_count.append(gender_counts)
    print(gender_count)

def analysis_5():
    attribute = list_of_attributes[3]
    data = kMC('not needed', csv_file_path, attribute)
    highest_spending_cluster = data.groupby('Cluster')['Spending Score (1-100)'].mean().idxmax()
    highest_spending_cluster_data = data[data['Cluster'] == highest_spending_cluster]
    highest_spending_cluster_male = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 0]
    highest_spending_cluster_female = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 1]

    print(highest_spending_cluster_male['Age'].min(), highest_spending_cluster_male['Age'].max(), highest_spending_cluster_male['Age'].mean(),len(highest_spending_cluster_male))
    print(highest_spending_cluster_female['Age'].min(), highest_spending_cluster_female['Age'].max(), highest_spending_cluster_female['Age'].mean(), len(highest_spending_cluster_female))

def analysis_6():
    attribute = list_of_attributes[3]
    data = kMC('not needed', csv_file_path, attribute)

    lowest_age_cluster = data.groupby('Cluster')['Age'].mean().idxmin()
    lowest_age_cluster_data = data[data['Cluster'] == lowest_age_cluster]

    lowest_age_cluster_male = lowest_age_cluster_data[lowest_age_cluster_data['Gender'] == 0]
    lowest_age_cluster_male_spending = lowest_age_cluster_male['Spending Score (1-100)'].sum() / len(lowest_age_cluster_male)
    lowest_age_cluster_female = lowest_age_cluster_data[lowest_age_cluster_data['Gender'] == 1]
    lowest_age_cluster_female_spending = lowest_age_cluster_female['Spending Score (1-100)'].sum() / len(lowest_age_cluster_female)

    print(lowest_age_cluster, lowest_age_cluster_data['Age'].mean())
    print(lowest_age_cluster_male_spending, len(lowest_age_cluster_male), lowest_age_cluster_male['Spending Score (1-100)'].sum())
    print(lowest_age_cluster_female_spending, len(lowest_age_cluster_female), lowest_age_cluster_female['Spending Score (1-100)'].sum())

def analysis_7():
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

    print(dataset_mean)
    # annual income
    print(clusters_higher_than_dataset)
    # spending score
    print(higher_cluster)
    print(cluster_scores[higher_cluster])
    # spending by gender in the higher cluster
    print(gender_grouped)

def analysis_9():
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

    print(highest_gap_cluster, difference_income_spending[highest_gap_cluster])

def analysis_10():
    # cluster 3, dann gender count, range income und age für beide gender und für das gesamte cluster
    attribute = list_of_attributes[0]
    data = kMC('not needed', csv_file_path, attribute)
    highest_spending_cluster = data.groupby('Cluster')['Spending Score (1-100)'].mean().idxmax()
    highest_spending_cluster_data = data[data['Cluster'] == highest_spending_cluster]
    highest_spending_cluster_male = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 0]
    highest_spending_cluster_female = highest_spending_cluster_data[highest_spending_cluster_data['Gender'] == 1]

    print(highest_spending_cluster_male['Age'].min(), highest_spending_cluster_male['Age'].max(), highest_spending_cluster_male['Age'].mean(), highest_spending_cluster_male['Annual Income (k$)'].min(), highest_spending_cluster_male['Annual Income (k$)'].max(), highest_spending_cluster_male['Annual Income (k$)'].mean(), highest_spending_cluster_male['Spending Score (1-100)'].mean())
    print(highest_spending_cluster_female['Age'].min(), highest_spending_cluster_female['Age'].max(), highest_spending_cluster_female['Age'].mean(), highest_spending_cluster_female['Annual Income (k$)'].min(), highest_spending_cluster_female['Annual Income (k$)'].max(), highest_spending_cluster_female['Annual Income (k$)'].mean(), highest_spending_cluster_female['Spending Score (1-100)'].mean())
    print(highest_spending_cluster_data['Age'].min(), highest_spending_cluster_data['Age'].max(), highest_spending_cluster_data['Age'].mean(), highest_spending_cluster_data['Annual Income (k$)'].min(), highest_spending_cluster_data['Annual Income (k$)'].max(), highest_spending_cluster_data['Annual Income (k$)'].mean())

def cluster_analysis ():
    # analysis_4()
    # analysis_5()
    analysis_6()
    # analysis_7()
    # analysis_9()
    # analysis_10()

cluster_analysis()