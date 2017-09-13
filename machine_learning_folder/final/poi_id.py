#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import cross_val_score

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

features_list = ['poi',
                 'total_payments',
                 'total_stock_value',
                 'expenses',
                 'to_poi_rate']


 # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

data_dict.pop("TOTAL") # excel quirk
data_dict.pop("THE TRAVEL AGENCY IN THE PARK") # company not POI
data_dict.pop("LOCKHART EUGENE E")
my_dataset = {}
for key in data_dict.keys():
    my_dataset[key] = data_dict[key]
    try:
        from_poi_rate = 1.0 * data_dict[key]['from_poi_to_this_person'] / \
        data_dict[key]['to_messages']
    except:
        from_poi_rate = "NaN"
    my_dataset[key]['from_poi_rate'] = from_poi_rate
    try:
        to_poi_rate = 1.0 * data_dict[key]['from_this_person_to_poi'] / \
        data_dict[key]['from_messages']
    except:
        to_poi_rate = "NaN"
    my_dataset[key]['to_poi_rate'] = to_poi_rate



### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


# Shuffle and split the dataset into training and testing set.
features_train, features_test, labels_train, labels_test = train_test_split(features, labels,
                                                    test_size=0.2,
                                                    random_state = 4)
### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html


# Provided to give you a starting point. Try a variety of classifiers.

# Initially I used cross_val_score as cross validation mehtod
# GaussianNB classifiers
clf = GaussianNB()
clf.fit(features_train, labels_train)
scores = cross_val_score(clf, features_train, labels_train, cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
pred = clf.predict(features_test)
acc= accuracy_score(pred, labels_test)
recall = metrics.recall_score(pred,labels_test)
precision = metrics.precision_score(pred,labels_test)
print ("the GaussianNB method accuracy is {}, recall is {}, precision is {}".format(acc, recall, precision))

#DecisionTreeClassifier
clf = DecisionTreeClassifier(min_samples_leaf=7,min_samples_split=20)
clf.fit(features_train, labels_train)
scores = cross_val_score(clf, features_train, labels_train, cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
pred = clf.predict(features_test)
acc= accuracy_score(pred, labels_test)
recall = metrics.recall_score(pred,labels_test)
precision = metrics.precision_score(pred,labels_test)
print ("the DecisionTreeClassifier method accuracy is {}, recall is {}, precision is {}".format(acc, recall, precision))

#KNeighborsClassifier
clf = KNeighborsClassifier()
clf.fit(features_train, labels_train)
scores = cross_val_score(clf, features_train, labels_train, cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
pred = clf.predict(features_test)
acc= accuracy_score(pred, labels_test)
recall = metrics.recall_score(pred,labels_test)
precision = metrics.precision_score(pred,labels_test)
print ("the KNeighborsClassifier method accuracy is {}, recall is {}, precision is {}".format(acc, recall, precision))

# Due to the class imbalance problem,
# it is preferred to use a stratified shuffle split instead.
# This ensures that an equal ratio of POIs to non-POIs are found in the training and test sets.
# Here I decide to use stratified shuffle split and DecisionTreeClassifier to find the best parameters

from sklearn.model_selection import GridSearchCV

cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=4)
# add pipeline to Standard Scaler
#clf = make_pipeline(StandardScaler(),
#                     finalmodel)
clf = DecisionTreeClassifier()
min_samples_leaf  = [5,7,9,11,13,15,17,19,21]
min_samples_split = [5,7,9,11,13,15,17,19,21]
param_grid = {'min_samples_leaf': min_samples_leaf, 'min_samples_split' : min_samples_split}
grid = GridSearchCV(clf, param_grid=param_grid, cv=cv)
grid.fit(features, labels)

print("The best parameters for DecisionTreeClassifier are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html



# Example starting point. Try investigating other evaluation techniques!

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
#min_samples_leaf=7,min_samples_split=20
clf = make_pipeline(StandardScaler(),
                     DecisionTreeClassifier(min_samples_split=7, min_samples_leaf= 15))

dump_classifier_and_data(clf, my_dataset, features_list)
