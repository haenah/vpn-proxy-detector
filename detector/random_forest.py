import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from to_csv_nfs_v2 import load_dataframe
from nfs_attributes import train_attributes
import data


def fit_test(df):
    X = df[train_attributes]
    y = df["label"]
    dataset_size = len(X)
    train_mask = np.random.rand(dataset_size) < 0.7
    X_train = X[train_mask]
    y_train = y[train_mask]
    X_test = X[~train_mask]
    y_test = y[~train_mask]
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    prediction = clf.predict(X_test)
    return f1_score(y_test, prediction)


# version 1
print("===============VPN/NonVPN===============")
for service in data.services:
    df = load_dataframe(service, version=1)
    if len(df[df["label"] == 1]) == 0:
        print(f"no vpn packet for {service}")
        continue
    f1 = fit_test(df)
    print(f"f1 score for {service} is {f1}")
df = load_dataframe(version=1)
f1 = fit_test(df)
print(f"f1 score for all is {f1}")


# version 2
print("===============VNAT===============")
for service in data.services_v2:
    df = load_dataframe(service, version=2)
    if len(df[df["label"] == 1]) == 0:
        print(f"no vpn packet for {service}")
        continue
    print(len(df[df["label"] == 1]))
    f1 = fit_test(df)
    print(f"f1 score for {service} is {f1}")
df = load_dataframe(version=2)
f1 = fit_test(df)
print(f"f1 score for all is {f1}")
