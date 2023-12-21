import pandas as pd
from nfstream import NFStreamer
import os
from nfs_attributes import csv_attributes

from filenames import vpn_file_names, nvpn_file_names, file_name_groups


file_names = vpn_file_names + nvpn_file_names
n_vpn = len(vpn_file_names)
n_nvpn = len(nvpn_file_names)

os.makedirs("./preprocessed/nfs", exist_ok=True)

for file_name, is_vpn in file_name_groups[-1]:
    path = f"./data/{is_vpn}_pcap/{file_name}"
    streamer = NFStreamer(source=path, statistical_analysis=True)

    data_dict = {k: [] for k in csv_attributes}
    data_dict["label"] = []
    data_dict["file_name"] = []
    for flow in streamer:
        for k in csv_attributes:
            data_dict[k].append(getattr(flow, k))
        data_dict["label"].append(is_vpn)
        data_dict["file_name"].append(file_name)

    df = pd.DataFrame(data_dict)
    df["src_freq"] = df.groupby("dst_ip")["dst_ip"].transform("count") / len(df)
    key = file_name.split("/")[-1].split(".")[0]
    df.to_csv(f"./preprocessed/nfs/{key}.csv", mode="w")
