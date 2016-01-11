from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import skflow
from sklearn.preprocessing import StandardScaler
class Model:
    """
    Machine learning models for fitting and predicting data
    """
    def __init__(self):
        #self.clf = SVC(C = 10,  kernel = "rbf")
        #self.clf = RandomForestClassifier(n_estimators=128, criterion="entropy")
        #self.clf = GradientBoostingClassifier(learning_rate=0.2, max_depth=6)

        self.clf = RandomForestClassifier(n_estimators=128)
        #self.clf = skflow.TensorFlowDNNClassifier(hidden_units=[64, 128, 64, 64, 32, 16], n_classes=3)
        self.scaler = StandardScaler()
    
    def fit(self, X, Y, sample_weight = None):
        X = self.scaler.fit_transform(X)
        self.clf.fit(X, Y)
        if sample_weight is None:
            self.clf.fit(X, Y)
        else:
            #self.clf.fit(X, Y, sample_weight = sample_weight)
            self.clf.fit(X, Y)
    
    def predict(self, X):
        X = self.scaler.transform(X)
        Y = self.clf.predict(X)
        return Y
