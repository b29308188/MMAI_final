import sys
import numpy as np
from sklearn.cross_validation import KFold, LabelKFold
from utils import weighted_precision_recall, read_training_data
from models import Model
sys.path.append(".")

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
    for train_index, test_index in kf:
        trainX, testX = X[train_index], X[test_index]
        trainY, testY = Y[train_index], Y[test_index]
        
        #fit data
        model.fit(trainX, trainY, sample_weight = sample_weights[train_index])
        #make prediction
        predY = model.predict(testX)
        
        #evaluation
        scores = weighted_precision_recall(testY, predY, sample_weight = sample_weights[test_index])
        print "(Precision/Recall) T: (%.3f,%.3f) / F: (%.3f,%.3f) / N:(%.3f,%.3f)" %(scores[0][0], scores[0][1], scores[1][0], scores[1][1], scores[2][0], scores[2][1])

