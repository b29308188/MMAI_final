from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import skflow
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
class Model:
    """
    Machine learning models for fitting and predicting data
    """
    def __init__(self):
        self.clf = SVC(C = 10,  kernel = "rbf", decision_function_shape = "ovr")
        self.scaler = StandardScaler()

    def fit(self, X, Y, sample_weight = None):
        X = self.scaler.fit_transform(X)
        if sample_weight is None:
            self.clf.fit(X, Y)
        else:
            self.clf.fit(X, Y, sample_weight = sample_weight)
    
    def predict(self, X):
        X = self.scaler.transform(X)
        Y = self.clf.predict(X)
        return Y
