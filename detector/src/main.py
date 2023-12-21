import sys
import os
from preprocess import load_dataframe
from anomaly import get_isolation_forest_anomly, get_local_outlier_factor_anomly
import joblib


def main():
    if len(sys.argv <= 1):
        raise Exception("Please specify the pcap file path to the file")
    pcap_path = sys.argv[1]
    if not os.path.exists(pcap_path):
        raise Exception("Pcap file does not exist")
    dataframe = load_dataframe(pcap_path)
    src_ips = dataframe["src_ip"]
    isof_anomalies = get_isolation_forest_anomly(src_ips)
    lof_anomalies = get_local_outlier_factor_anomly(src_ips)
    random_forest_model = joblib.load(
        os.path.join(os.path.dirname(__file__), "../model/random_forest_v1.joblib")
    )
    random_forest_anomalies = random_forest_model.predict(dataframe)
    anomalies = isof_anomalies & lof_anomalies & random_forest_anomalies
    vpn_packets = dataframe[anomalies]
    print(vpn_packets)
