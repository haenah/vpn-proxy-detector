from abc import ABCMeta, abstractmethod
from ipaddress import ip_address
from typing import List, Tuple

import pandas as pd


def ipv4_to_int(ip) -> int:
    return int(ip_address(ip))


class Record(metaclass=ABCMeta):
    @abstractmethod
    def ipv4(self) -> str | int:
        """Returns an IPv4 address in the record."""


class PacketRecord(Record):
    def __init__(self, packet):
        self.packet = packet

    def __str__(self) -> str:
        return self.packet["dst_ip"]

    def __format__(self, __format_spec: str) -> str:
        return format(self.packet["dst_ip"], __format_spec)

    def ipv4(self) -> str | int:
        return self.packet["dst_ip"]


class DefaultRecord(Record):
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def __str__(self) -> str:
        return str(self.ip)

    def __format__(self, __format_spec: str) -> str:
        return format(self.ip, __format_spec)

    def ipv4(self) -> str | int:
        return self.ip


class Clusterer:
    def __init__(self, file_name: str):
        self.__ranges: List[Tuple[int, int, str]] = []  # inclusive for both side
        self.__clusters: List[List[Record]] = []
        self.__remainders: List[Record] = []

        isp_ipv4_assignment = pd.read_csv(
            file_name, names=["ISP", "ISP_Eng", "Start_IP", "End_IP", "Size", "Date"]
        )
        for _, row in isp_ipv4_assignment.iterrows():
            start = ipv4_to_int(row["Start_IP"])
            end = ipv4_to_int(row["End_IP"])
            isp = row["ISP_Eng"]
            self.__ranges.append((start, end, isp))
            self.__clusters.append([])

        self.__ranges.sort()

    def add_records(self, records: List[Record]):
        for record in records:
            self.add_record(record)

    def add_record(self, record: Record):
        idx = self.__bsearch(ipv4_to_int(record.ipv4()))
        if idx is None:
            self.__remainders.append(record)
        else:
            self.__clusters[idx].append(record)

    def get_clusters(self):
        clusters = self.__clusters.copy()
        clusters.append(self.__remainders)
        # filter empty clusters
        clusters = list(filter(lambda cluster: len(cluster) > 0, clusters))
        return clusters

    def __bsearch(self, target: int) -> int | None:
        start = int(0)
        end = len(self.__ranges) - 1
        if start > end:
            return None

        start_test = Clusterer.__range_test(self.__ranges[start], target)
        end_test = Clusterer.__range_test(self.__ranges[end], target)
        if start_test < 0 or end_test > 0:
            return None
        if start_test == 0:
            return start
        if end_test == 0:
            return end

        while start < end - 1:
            mid = (start + end) // 2
            mid_test = Clusterer.__range_test(self.__ranges[mid], target)
            if mid_test < 0:
                end = mid
            elif mid_test > 0:
                start = mid
            else:
                return mid

        return None

    @staticmethod
    def __range_test(range: Tuple[int, int, str], target: int) -> int:
        if target < range[0]:
            return -1
        elif target > range[1]:
            return 1
        return 0

    def debug(self):
        for (start, end, isp), cluster in zip(self.__ranges, self.__clusters):
            if len(cluster) == 0:
                continue

            print(
                f"===== ISP: {isp} / IP Range {ip_address(start)} ~ {ip_address(end)} ====="
            )
            for record in cluster:
                print(record)

        if len(self.__remainders) == 0:
            return

        print(f"===== Remainders =====")
        for record in self.__remainders:
            print(record)

    def export(self, output_dir: str):
        for (start, end, isp), cluster in zip(self.__ranges, self.__clusters):
            if len(cluster) == 0:
                continue

            with open(
                f"{output_dir}/{isp}_{ip_address(start)}_{ip_address(end)}.csv", "w"
            ) as f:
                for record in cluster:
                    print(record, file=f)

        if len(self.__remainders) == 0:
            return

        with open(f"{output_dir}/remainders.csv", "w") as f:
            for record in self.__remainders:
                print(record, file=f)


def main():
    clusterer = Clusterer("src/assets/ipv4_ko_kr.csv")

    # Example Data (IP Addresses)
    data = ["101.79.48.0", "101.79.72.0", "203.238.128.0", "210.98.224.0", "127.0.0.1"]
    records = list(DefaultRecord(ip) for ip in data)

    clusterer.add_records(records)
    clusterer.debug()
    clusterer.export(output_dir="src/assets")


if __name__ == "__main__":
    main()
