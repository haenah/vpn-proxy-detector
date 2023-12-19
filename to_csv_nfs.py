import numpy as np
import pandas as pd
import sys
from nfstream import NFStreamer

from filenames import vpn_file_names, nvpn_file_names, file_name_groups


file_names = vpn_file_names + nvpn_file_names
n_vpn = len(vpn_file_names)
n_nvpn = len(nvpn_file_names)

attributes = [
    'expiration_id',
    'src_ip',
    'src_mac',
    'src_oui',
    'src_port',
    'dst_ip',
    'dst_mac',
    'dst_oui',
    'dst_port',
    'protocol',
    'ip_version',
    'vlan_id',
    'tunnel_id',
    'bidirectional_first_seen_ms',
    'bidirectional_last_seen_ms',
    'bidirectional_duration_ms',
    'bidirectional_packets',
    'bidirectional_bytes',
    'src2dst_first_seen_ms',
    'src2dst_last_seen_ms',
    'src2dst_duration_ms',
    'src2dst_packets',
    'src2dst_bytes',
    'dst2src_first_seen_ms',
    'dst2src_last_seen_ms',
    'dst2src_duration_ms',
    'dst2src_packets',
    'dst2src_bytes',
    'application_name',
    'application_category_name',
    'application_is_guessed',
    'application_confidence',
    'requested_server_name',
    'client_fingerprint',
    'server_fingerprint',
    'user_agent',
    'content_type'
]


for file_name, is_vpn in file_name_groups[-1]:
    path = f"./{is_vpn}_pcap/{file_name}"
    streamer = NFStreamer(source=path, statistical_analysis=True)

    data_dict = {k: [] for k in attributes}
    data_dict['label'] = []
    data_dict['file_name'] = []
    for flow in streamer:
        for k in attributes:
            data_dict[k].append(getattr(flow, k))
        data_dict['label'].append(is_vpn)
        data_dict['file_name'].append(file_name)

    df = pd.DataFrame(data_dict)
    df['src_freq'] = df.groupby('src_ip')['src_ip'].transform('count') / len(df)
    key = file_name.split("/")[-1].split(".")[0]
    df.to_csv(f'./nfs/{key}.csv', mode='w')