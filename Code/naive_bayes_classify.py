# coding: utf-8


import numpy as np
from sklearn import naive_bayes
import random
from sklearn.externals import joblib
import common_classify


def build_classifier(train_samples, train_out):
    clf = naive_bayes.MultinomialNB()
    clf.fit(train_samples, train_out)
    return clf


def cross_val_model(scaled_filtered_data, labels, naive_bayes_model_dir_path, numberOfClasses):
    # divide to train and test
    training_size_fraction = .09

    # train and test indexes
    test_idx = np.array(random.sample(xrange(len(labels)), int((1 - training_size_fraction) * len(labels))))
    train_idx = np.array([x for x in xrange(len(labels)) if x not in test_idx])

    # build train and test samples
    test_samples = scaled_filtered_data[test_idx]
    train_samples = scaled_filtered_data[train_idx]

    # keep train and test labels
    test_out = labels[test_idx]
    train_out = labels[train_idx]

    # build classifier
    clf = build_classifier(train_samples, train_out)

    # dump classifier
    joblib.dump(clf, naive_bayes_model_dir_path + "/" + 'naive_bayes_model.pkl', compress=9)

    # predict
    a = np.array(clf.predict(test_samples).astype(int))
    c = np.array(a) == np.array(test_out)

    print ("\nCross Validation...\n")

    resultsStr = "Accuracy                                    : " + str(sum(c) * 100.0 / len(a)) + " %" + "\n"

    print resultsStr

    # save to file
    with open(naive_bayes_model_dir_path+ "/naive_bayes_results.txt", 'w') as f2:
        f2.write("NAIVE BAYES model: \n")
        f2.write("Number of classes={0}\n\n".format(numberOfClasses))
        f2.write(" -- cross val prediction --\n")
        f2.write(resultsStr)
        f2.write("\n")


# build the SVM classifier
def build_train_model(vec_dir_path, naive_bayes_model_dir_path, numberOfClasses):
    # read the vectors from all data files
    data_vectors = common_classify.read_vectors(vec_dir_path)

    # return vectors in range [0,1] and labels
    (vectors, labels) = common_classify.scale_and_filter_vectors_without_negative(data_vectors)

    # cross val the train set
    cross_val_model(vectors, labels, naive_bayes_model_dir_path, numberOfClasses)


# classify validation vectors
def predict_validation_set(validation_dir_path, naive_bayes_model_dir_path):
    validation_vectors = common_classify.read_vectors(validation_dir_path)
    (validation_vectors, validation_labels) = common_classify.scale_and_filter_vectors_without_negative(validation_vectors)

    # load classifier
    clf = joblib.load(naive_bayes_model_dir_path + "/" + 'naive_bayes_model.pkl')

    a = np.array(clf.predict(validation_vectors).astype(int))
    c = np.array(a) == np.array(validation_labels)

    print ("\nClassify Validation Data...\n")

    resultsStr = "Accuracy                                    : " + str(sum(c) * 100.0 / len(a)) + " %" + "\n"

    print resultsStr

    # save to file
    with open(naive_bayes_model_dir_path + "/naive_bayes_results.txt", 'a') as f2:
        f2.write("\n")
        f2.write(" -- validation prediction -- \n")
        f2.write(resultsStr)
        f2.write("\n")