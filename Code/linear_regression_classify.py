
# coding: utf-8

# In[37]:

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import random
from sklearn.externals import joblib
import common_classify


# In[38]:

def build_classifier(train_X, train_Y):
    regr = linear_model.LinearRegression()
    regr.fit(train_X, train_Y)
    return regr


def cross_val_model(scaled_filtered_data, labels, regr_dir_path, numberOfClasses):
    # divide to train and test
    training_size_fraction = .09

    # train and test indexes
    test_idx = np.array(random.sample(xrange(len(labels)), int((1 - training_size_fraction) * len(labels))))
    train_idx = np.array([x for x in xrange(len(labels)) if x not in test_idx])


    # build train and test samples
    test_X=scaled_filtered_data[test_idx]
    train_X=scaled_filtered_data[train_idx]

    # keep train and test labels
    test_Y=labels[test_idx]
    train_Y=labels[train_idx]

    # build classifier
    regr = build_classifier(train_X, train_Y)

    # dump classifier
    joblib.dump(regr, regr_dir_path+"/"+'linearRegression_model.pkl', compress=9)


     # The coefficients
    resultsStr=("Coefficients: {0}\n").format(regr.coef_)+\
               ("Residual sum of squares: %.2f" % (np.mean(regr.predict(test_X) - test_Y) ** 2))+"\n"+\
               ('Variance score: %.2f' % regr.score(test_X,test_Y))+"\n"


    prdarr=regr.predict(test_X)
    succ=0
    for i in range(0,len(prdarr)):
        prdarr[i]=round(prdarr[i])
        if prdarr[i]==test_Y[i]:
            succ+=1

    succ=(float(succ)/len(prdarr))*100
    resultsStr+=("Success: {0}%\n".format(succ))

  # Plot outputs
  #  plt.scatter(test_idx, test_Y,  color='black')
  #  plt.scatter(test_idx, prdarr, color='blue')
  #  plt.xticks(())
  #  plt.yticks(())
  #  plt.show()

    print resultsStr

    # save to file
    with open(regr_dir_path+"/linearRegression_results.txt", 'w') as f2:
        f2.write("Linear Regression:\n")
        f2.write("Number of classes={0}\n\n".format(numberOfClasses))
        f2.write(" -- cross val prediction --\n")
        f2.write(resultsStr)
        f2.write("\n")



# build the classifier
def build_train_model(vec_dir_path, regr_dir_path, numberOfClasses):
    # read the vectors from all data files
    data_vectors = common_classify.read_vectors(vec_dir_path)

    # return vectors in range [0,1] and labels
    (vectors, labels) = common_classify.scale_and_filter_vectors_without_negative(data_vectors)

    # cross val the train set
    cross_val_model(vectors, labels, regr_dir_path, numberOfClasses)


# classify validation vectors
def predict_validation_set(validation_dir_path, regr_dir_path):
    test_X = common_classify.read_vectors(validation_dir_path)
    (test_X, test_Y) = common_classify.scale_and_filter_vectors_without_negative(test_X)

    # load classifier
    regr = joblib.load(regr_dir_path+"/"+'linearRegression_model.pkl')

    # The coefficients
    resultsStr=("Coefficients: {0}\n").format(regr.coef_)+\
               ("Residual sum of squares: %.2f" % (np.mean(regr.predict(test_X) - test_Y) ** 2))+"\n"+\
               ("Variance score: %.2f" % regr.score(test_X,test_Y))+"\n"


    prdarr=regr.predict(test_X)
    succ=0
    for i in range(0,len(prdarr)):
        prdarr[i]=round(prdarr[i])
        if prdarr[i]<0:
            print (prdarr[i])
        if prdarr[i]==test_Y[i]:
            succ+=1

    succ=(float(succ)/len(prdarr))*100
    resultsStr+=("Success: {0}%\n".format(succ))

   # Plot outputs
   # test_idx=[i for i in range (0,len(test_Y))]
   # plt.scatter(test_idx, test_Y,  color='black')
   # plt.scatter(test_idx, prdarr, color='blue')
   # plt.xticks(())
   # plt.yticks(())
   # plt.show()

    print resultsStr

    # save to file
    with open(regr_dir_path+"/linearRegression_results.txt", 'a') as f2:
        f2.write("\n")
        f2.write(" -- validation prediction -- \n")
        f2.write(resultsStr)
        f2.write("\n")