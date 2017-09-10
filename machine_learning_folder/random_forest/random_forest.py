#!/usr/bin/python

"""
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project.

    Use a Naive Bayes Classifier to identify emails by their authors

    authors and labels:
    Sara has label 0
    Chris has label 1
"""

import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()

#features_train = features_train[:len(features_train)/100]
#labels_train = labels_train[:len(labels_train)/100]
#########################################################
### your code goes here ###


clf = RandomForestClassifier(max_depth=2, random_state=0)

t0 = time()
clf.fit(features_train,labels_train)
print "training time:", round(time()-t0, 3), "s"
t0 = time()
clf.predict(features_test)
print "predicting time:", round(time()-t0, 3), "s"
clf.score(features_test,labels_test)
print(len(features_train[0]))
print(clf.score(features_test,labels_test))

#########################################################
