import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from preprocess import load_dataframe_from_services
from nfs_attributes import train_attributes
import data
import sys
import os
import joblib


def fit(X, y, version=1):
    clf = RandomForestClassifier()
    clf.fit(X, y)
    output_dir = os.path.join(os.path.dirname(__file__), "../model")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"random_forest_v{version}.joblib")
    if os.path.exists(output_file):
        return joblib.load(output_file)
    else:
        joblib.dump(clf, output_file)
        return clf


def test(clf, X, y):
    prediction = clf.predict(X)
    return f1_score(y, prediction)


def split_train_test(df):
    X = df[train_attributes]
    y = df["label"]
    dataset_size = len(df)
    train_mask = np.random.rand(dataset_size) < 0.7
    X_train = X[train_mask]
    y_train = y[train_mask]
    X_test = X[~train_mask]
    y_test = y[~train_mask]
    return X_train, y_train, X_test, y_test


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":

        def fit_test(df, version=1):
            X_train, y_train, X_test, y_test = split_train_test(df)
            clf = fit(X=X_train, y=y_train, version=version)
            return test(clf, X=X_test, y=y_test)

        # version 1
        print("===============VPN/NonVPN===============")
        for service in data.services:
            df = load_dataframe_from_services(service, version=1)
            if len(df[df["label"] == 1]) == 0:
                print(f"no vpn packet for {service}")
                continue
            f1 = fit_test(df, version=1)
            print(f"f1 score for {service} is {f1}")
        df = load_dataframe_from_services(version=1)
        f1 = fit_test(df, version=1)
        print(f"f1 score for all is {f1}")

        # version 2
        print("===============VNAT===============")
        for service in data.services_v2:
            df = load_dataframe_from_services(service, version=2)
            if len(df[df["label"] == 1]) == 0:
                print(f"no vpn packet for {service}")
                continue
            f1 = fit_test(df, version=2)
            print(f"f1 score for {service} is {f1}")
        df = load_dataframe_from_services(version=2)
        f1 = fit_test(df, version=2)
        print(f"f1 score for all is {f1}")
    else:
        # Save the model
        df = load_dataframe_from_services(version=1)
        X = df[train_attributes]
        y = df["label"]
        clf = fit(X, y)
