import sys
sys.path.append(".")
import cPickle
import numpy as np
from models import Model
from utils import weighted_precision_recall, read_training_data

if __name__ == "__main__":
    csv_path = sys.argv[1]
    image_prefix = sys.argv[2]
    model_path = sys.argv[3]
    (X, Y, categories, sample_weights) = read_training_data(csv_path, image_prefix = image_prefix, category = True, sample_weight = True)
    print "#T = %d, #F = %d, #N = %d"%(sum(1 for y in Y if y == 0), sum(1 for y in Y if y == 1), sum(1 for y in Y if y == 2))
    print "X =", X.shape, ", Y =",Y.shape
    # Machine Learning models
    model = Model()

    #fit data
    model.fit(X, Y, sample_weight = sample_weights)
    #make prediction
    predY = model.predict(X)
    #evaluation
    scores = weighted_precision_recall(Y, predY, sample_weight = sample_weights)
    print "IN SAMPLE -- (Precision/Recall) T: (%.3f,%.3f) / F: (%.3f,%.3f) / N:(%.3f,%.3f)" %(scores[0][0], scores[0][1], scores[1][0], scores[1][1], scores[2][0], scores[2][1])

    #save model
    with open(model_path, "wb") as f:
        cPickle.dump(model, f, cPickle.HIGHEST_PROTOCOL)
