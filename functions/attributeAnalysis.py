import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def attribute_analysis(directory, csv_file_path):

    # Load the dataset
    data = pd.read_csv(csv_file_path)

    # Age Pyramid
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
    data['AgeGroup'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)
    grouped_data = data.groupby(['AgeGroup', 'Gender'], observed=False).size().unstack(fill_value=0)
    age_groups = labels
    group1 = grouped_data['Female'].values
    group2 = grouped_data['Male'].values
    y = np.arange(len(age_groups)) + 0.5
    plt.figure(figsize=(10, 10))
    plt.barh(y, -group1, color=['#fe83cc'], label='Female', align='center')
    plt.barh(y, group2, color=['#069af3'], label='Male', align='center')
    plt.xticks(np.arange(-40, 41, 10), fontsize=12)
    plt.gca().set_xticklabels([abs(x) for x in plt.gca().get_xticks()])
    plt.xlabel('Count', fontsize=14, fontweight='bold', color='black')
    plt.title('Age Pyramid', fontsize=24, fontweight='bold', color='black', pad=20)
    ax = plt.gca()
    ax.spines['left'].set_color('none')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('none')
    ax.set_yticklabels([])
    for i, age_group in enumerate(age_groups):
        plt.text(0, y[i], age_group, ha='center', va='center', fontsize=10)
    plt.text(0, max(y) + 0.4, 'Age Groups', ha='center', va='center', fontsize=14, fontweight='bold', color='black')
    plt.legend(title="Gender", loc="upper right", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'age_pyramid.png'))
    plt.close()

    # Gender Pie Chart
    labels = ['Female', 'Male']
    size = data['Gender'].value_counts()
    colors = ['#fe83cc', '#069af3']
    explode = [0, 0.1]
    plt.figure(figsize=(10, 7))
    plt.pie(size, colors=colors, explode=explode, labels=labels, shadow=False, autopct='%.1f%%', startangle=90, radius=0.8)
    plt.title('Gender', fontsize=24, fontweight='bold', color='black')
    plt.legend(title="Gender", loc="upper right", fontsize=12)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'gender_pie_chart.png'))
    plt.close()

    # Annual Income Bar Chart
    income_bins = pd.interval_range(start=0, freq=10, end=data['Annual Income (k$)'].max() + 10, closed='left')
    data['IncomeGroup'] = pd.cut(data['Annual Income (k$)'], bins=income_bins)
    income_group_counts = data['IncomeGroup'].value_counts().sort_index()
    formatted_labels = [f"{int(interval.left)}-{int(interval.right)}" for interval in income_group_counts.index]
    plt.figure(figsize=(10, 7))
    plt.bar(formatted_labels, income_group_counts.values, color='grey', edgecolor='black', width=0.8, alpha=0.8)
    plt.xlabel('Annual Income (k$)', fontsize=14, fontweight='bold', color='black')
    plt.ylabel('Count', fontsize=14, fontweight='bold', color='black')
    plt.title('Annual Income', fontsize=24, fontweight='bold', color='black', pad=20)
    plt.xticks(fontsize=10, rotation=45, color='black')
    plt.yticks(fontsize=10, color='black')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'annual_income_bar_chart.png'))
    plt.close()

    # Spending Score Bar Chart
    spending_bins = pd.interval_range(start=0, freq=5, end=data['Spending Score (1-100)'].max() + 5, closed='left')
    data['SpendingGroup'] = pd.cut(data['Spending Score (1-100)'], bins=spending_bins)
    spending_group_counts = data['SpendingGroup'].value_counts().sort_index()
    formatted_spending_labels = [f"{int(interval.left)}-{int(interval.right)}" for interval in spending_group_counts.index]
    plt.figure(figsize=(10, 7))
    plt.bar(formatted_spending_labels, spending_group_counts.values, color='grey', edgecolor='black', width=0.8, alpha=0.8)
    plt.xlabel('Spending Score', fontsize=14, fontweight='bold', color='black')
    plt.ylabel('Count', fontsize=14, fontweight='bold', color='black')
    plt.title('Spending Score', fontsize=24, fontweight='bold', color='black', pad=20)
    plt.xticks(fontsize=10, rotation=45, color='black')
    plt.yticks(fontsize=10, color='black')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'spending_score_bar_chart.png'))
    plt.close()


