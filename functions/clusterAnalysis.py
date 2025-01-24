
from functions.kMC import kMC
from main import csv_file_path

def cluster_analysis ():
    clusters, cluster_centers = kMC('not needed', csv_file_path)

    # Ab hier können die Cluster analysiert werden, es muss dafür dann nur dieses File ausgeführt werden

cluster_analysis()