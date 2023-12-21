import pandas as pd
from nfstream import NFStreamer
import os
from nfs_attributes import csv_attributes
import data
import sys


def load_dataframe(service_names=None, version=1):
    totalSize = 0
    services = data.services if version == 1 else data.services_v2
    if service_names is None:
        service_names = services.keys()
    if isinstance(service_names, str):
        service_names = [service_names]
    dataframes = []
    for service_name in service_names:
        output_path = os.path.join(
            os.path.dirname(__file__),
            f"../preprocessed/nfs/v{version}/{service_name}.csv",
        )
        # If exists in preprocessed, load from there
        if os.path.exists(output_path):
            dataframe = pd.read_csv(output_path)
        else:
            data_dict = {k: [] for k in csv_attributes}
            data_dict["label"] = []
            for file_name in services[service_name]:
                is_vpn = file_name.startswith("vpn")
                # input_path = f"../data/{'vpn' if is_vpn else 'nvpn'}_pcap{'_v2' if version == 2 else ''}/{file_name}"
                input_path = os.path.join(
                    os.path.dirname(__file__),
                    f"../data/{'vpn' if is_vpn else 'nvpn'}_pcap{'_v2' if version == 2 else ''}/{file_name}",
                )
                streamer = NFStreamer(source=input_path, statistical_analysis=True)

                for flow in streamer:
                    for k in csv_attributes:
                        data_dict[k].append(getattr(flow, k))
                    data_dict["label"].append(1 if is_vpn else 0)

            dataframe = pd.DataFrame(data_dict)
        totalSize += len(dataframe)
        dataframes.append(dataframe)
    return pd.concat(dataframes, ignore_index=True)


if __name__ == "__main__":
    totalSize = 0
    version = int(sys.argv[1])
    os.makedirs(
        os.path.join(os.path.dirname(__file__), f"../preprocessed/nfs/v{version}/"),
        exist_ok=True,
    )
    services = (
        data.services if version == 1 else data.services_v2 if version == 2 else None
    )
    for service_name in services.keys():
        dataframe = load_dataframe(service_name, version=version)
        totalSize += len(dataframe)
        dataframe.to_csv(
            os.path.join(
                os.path.dirname(__file__),
                f"../preprocessed/nfs/v{version}/{service_name}.csv",
            ),
            index=False,
        )
