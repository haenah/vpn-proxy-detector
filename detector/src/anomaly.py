from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


def get_isolation_forest_anomly(ips):
    clf = IsolationForest()
    clf.fit_predict(ips)


def get_local_outlier_factor_anomly(ips):
    clf = LocalOutlierFactor()
    clf.fit_predict(ips)
