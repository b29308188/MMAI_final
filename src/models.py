from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
class Model:
    """
    Machine learning models for fitting and predicting data
    """
    def __init__(self):
        self.clf = SVC(C = 10, kernel = "rbf")
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
