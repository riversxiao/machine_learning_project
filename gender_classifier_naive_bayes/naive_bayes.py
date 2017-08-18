import random
from nltk.corpus import names
from nltk import NaiveBayesClassifier
from nltk.classify import accuracy as nltk_accuracy

# Extract features from the input word
def gender_features(word, num_letters=2):
    return {'feature': word[-num_letters:].lower()}

if __name__=='__main__':
    # Extract labeled names
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
            [(name, 'female') for name in names.words('female.txt')])

    random.seed(7)# reproduce the same result each time
    random.shuffle(labeled_names)# shuffle the list
    PROMTS = input()# example "xiao, wen ,hao" seperated with comma
    input_names  = [x.replace(" ","") for x in PROMTS.strip().split(",")]
    # Sweeping the parameter space
    for i in range(1, 5):
        print ('\nNumber of letters:', i)
        featuresets = [(gender_features(n, i), gender) for (n, gender) in labeled_names]
        train_set, test_set = featuresets[500:], featuresets[:500]
        classifier = NaiveBayesClassifier.train(train_set)

        # Print classifier accuracy
        print ('Accuracy ==>', str(100 * nltk_accuracy(classifier, test_set)) + str('%'))

        # Predict outputs for new inputs
        for name in input_names:
            print (name, '==>', classifier.classify(gender_features(name, i)))
