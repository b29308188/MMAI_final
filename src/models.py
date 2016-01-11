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
        self.clf = SVC(C = 10,  kernel = "rbf", class_weight = {0:1, 1:100, 2:2})
        #self.clf = RandomForestClassifier(n_estimators=128, criterion="entropy")
        #self.clf = GradientBoostingClassifier(learning_rate=0.2, max_depth=6)
        #self.clf = RandomForestClassifier(n_estimators=128)
        #self.clf = skflow.TensorFlowDNNClassifier(hidden_units=[64, 128, 64, 64, 32, 16], n_classes=3)
        self.scaler = StandardScaler()
        #self.var_threshold = VarianceThreshold(threshold = 0.99)
        #self.feature_selection = SelectKBest(f_classif, k = 20)

    def fit(self, X, Y, sample_weight = None):
        X = self.scaler.fit_transform(X)
        #print X
        #X = self.var_threshold.fit_transform(X)
        #print X.shape
        #X = self.feature_selection.fit_transform(X, Y)
        if sample_weight is None:
            self.clf.fit(X, Y)
        else:
            self.clf.fit(X, Y, sample_weight = sample_weight)
            #self.clf.fit(X, Y)
    
    def predict(self, X):
        X = self.scaler.transform(X)
        # X = self.var_threshold.transform(X)
        # X = self.feature_selection.transform(X)
        Y = self.clf.predict(X)
        return Y
