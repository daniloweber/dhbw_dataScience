
from functions.kMC import kMC
from main import csv_file_path
from list_of_attributes import list_of_attributes

def cluster_analysis ():
    clusters_dict = {}
    cluster_centers_dict = {}

    for attribute in list_of_attributes:
        attribute_name = "_".join([attr.replace(" ", "").replace("(", "").replace(")", "").replace("$", "dollar") for attr in attribute])
        clusters, cluster_centers = kMC('not needed', csv_file_path, attribute)
        clusters_dict[f"{attribute_name}_clusters"] = clusters
        cluster_centers_dict[f"{attribute_name}_clustercenters"] = cluster_centers
    # Ab hier können die Cluster analysiert werden, es muss dafür dann nur dieses File ausgeführt werden


cluster_analysis()