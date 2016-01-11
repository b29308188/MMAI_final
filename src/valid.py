import sys
sys.path.append(".")
import numpy as np
from sklearn.cross_validation import KFold, LabelKFold
from utils import weighted_precision_recall, read_training_data, f1_score
from models import Model

if __name__ == "__main__":
    csv_path = sys.argv[1]
    image_prefix = sys.argv[2]
    (X, Y, categories, sample_weights) = read_training_data(csv_path, image_prefix = image_prefix, category = True, sample_weight = True)
    print "#T = %d, #F = %d, #N = %d"%(sum(1 for y in Y if y == 0), sum(1 for y in Y if y == 1), sum(1 for y in Y if y == 2))
    print "X =", X.shape, ", Y =",Y.shape

    # Machine Learning models
    model = Model()
    
    kf = LabelKFold(categories, n_folds = 5) # ***shuffle internally***
    #kf = KFold(len(X), n_folds = 5, shuffle = True, random_state = 123)
    #cross validation
    S = []
    for train_index, test_index in kf:
        trainX, testX = X[train_index], X[test_index]
        trainY, testY = Y[train_index], Y[test_index]
        K = None 
        #fit data
        model.fit(trainX[:K], trainY[:K], sample_weight = sample_weights[train_index][:K])
        #make prediction
        predY = model.predict(testX)
        
        #evaluation
        
        scores = weighted_precision_recall(testY, predY, sample_weight = sample_weights[test_index])
        S.append(scores)
        print "(Precision/Recall) T: (%.3f,%.3f) / F: (%.3f,%.3f) / N:(%.3f,%.3f)" %(scores[0], scores[1], scores[2], scores[3], scores[4], scores[5])
    S = np.array(S)
    Tp = np.mean(S[:,0])
    Tr = np.mean(S[:,1])
    Fp = np.mean(S[:,2])
    Fr = np.mean(S[:,3])
    Np = np.mean(S[:,4])
    Nr = np.mean(S[:,5])
    print "TOTAL (Precision/Recall) T: (%.3f,%.3f) / F: (%.3f,%.3f) / N:(%.3f,%.3f)" %(Tp, Tr, Fp, Fr, Np, Nr)
    print "F1 SCORE T:%.3f / F:%.3f / N:%.3f " %(f1_score(Tp, Tr), f1_score(Fp, Fr), f1_score(Np, Nr))
