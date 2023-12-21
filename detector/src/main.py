import sys
import os
from preprocess import load_dataframe
from anomaly import get_isolation_forest_anomly, get_local_outlier_factor_anomly
import joblib
import pandas as pd
from clusterer import Clusterer, PacketRecord
import numpy as np
from collections import Counter
from nfs_attributes import train_attributes


def main():
    if len(sys.argv) <= 1:
        raise Exception("Please specify the pcap file path to the file")
    pcap_path = sys.argv[1]
    if not os.path.exists(pcap_path):
        raise Exception("Pcap file does not exist")
    dataframe = load_dataframe(pcap_path)
    # cluster ips
    records = [PacketRecord(row) for _, row in dataframe.iterrows()]
    cluster_file = os.path.join(os.path.dirname(__file__), "assets/ipv4_ko_kr.csv")
    clusterer = Clusterer(cluster_file)
    clusterer.add_records(records)
    cluster_output_dir = os.path.join(os.path.dirname(__file__), "../cluster")
    os.makedirs(cluster_output_dir, exist_ok=True)
    clusters = clusterer.get_clusters()

    # Anomaly detection
    anomaly_ips = []
    for cluster in clusters:
        dst_ips = [record.packet.dst_ip for record in cluster]
        # Aggregate by count
        dict = {}
        for ip in dst_ips:
            if ip in dict:
                dict[ip] += 1
            else:
                dict[ip] = 1
        items = list(dict.items())
        ips = np.array([item[0] for item in items])
        freqs = np.array([item[1] for item in items]).reshape(-1, 1)

        isof_anomalies = get_isolation_forest_anomly(freqs)
        lof_anomalies = get_local_outlier_factor_anomly(freqs)
        anomaly_ips.extend(
            ips[np.logical_and(isof_anomalies == -1, lof_anomalies == -1)]
        )

    print(anomaly_ips)

    random_forest_model = joblib.load(
        os.path.join(os.path.dirname(__file__), "../model/random_forest_v1.joblib")
    )
    random_forest_anomalies = random_forest_model.predict(dataframe[train_attributes])
    anomaly_ips_forest = dataframe[random_forest_anomalies == 1]["dst_ip"].unique()
    # intersection
    anomaly_ips_forest = set(anomaly_ips_forest)
    anomaly_ips = set(anomaly_ips)
    intersection = anomaly_ips_forest.intersection(anomaly_ips)
    print(intersection)


if __name__ == "__main__":
    main()
