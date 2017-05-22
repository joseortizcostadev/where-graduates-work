
# Author:      Jose Ortiz Costa
# Date:        April 01, 2017
# File:        k_fold_cross_validation.py
# Description: Evaluates a classification method by implementing a the k-fold-cross-validation algorith.
#
from preprocessor import Dataset
from naive_bayes_classifier import NaiveBayesClassifier
from dataset_metadata import Dataset_Metadata
import prettytable
class KFCV (object):
    NBC = "Naive Bayes Classifier" # naive bayes classifier
    def __init__(self, k, method, dataset_metadata, verbose):
        """
        Class constructor
        :param k: the K value. recomended to be set to 10
        :param method: method descriptor e.g Naive Bayes
        :param dataset_metadata: the metadata
        :param verbose: print out every step if true
        """
        self.k = k
        self.method = method
        self.metadata = dataset_metadata
        self.verbose = verbose

    @property
    def k (self):
        return self._k

    @k.setter
    def k (self, value):
        self._k = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    def run_classifier_method (self, from_index, to_index):
        """
        Runs the classifier to be evaluated
        :param from_index: 
        :param to_index: 
        :return: the measures 
        """
        data = Dataset(self.metadata.path)
        dataset = data.preprocess(from_index, to_index)
        nbc = NaiveBayesClassifier(dataset, self.metadata.index, self.metadata.attr)
        return nbc.measures()

    def run_classifier_method_with_k (self, test_from_index, test_to_index, k):
        """
        Runs the classifier method k times to perform the fold
        :param test_from_index: 
        :param test_to_index: 
        :param k: 
        :return: the measures of the fold
        """
        measurements =  self.run_classifier_method(test_from_index, test_to_index)
        if self.verbose is True:
            print "fold: " + str(k+1) + " accuracy: " + str(measurements['accuracy'])
        return measurements
    def means (self, accuracy, precision, recall, f1, specificty):
        """
        Calculates the mean of the folds measurements
        :param accuracy: 
        :param precision: 
        :param recall: 
        :param f1: 
        :param specificty: 
        :return: the mean of the folds
        """
        accuracy = accuracy / (self.k)
        if self.verbose is True:
            print " mean acuracies for this fold: " + str(accuracy)
        precision = precision / (self.k-1)
        recall = recall / (self.k-1)
        f1 = f1 / (self.k-1)
        specificty = specificty / (self.k-1)
        return [accuracy, precision, recall, f1, specificty]

    def measurements (self, html):
        """
        Computes the general measurements
        :param html: 
        :return: the general measurements
        """
        if self.verbose is True:
            print "Running K-Fold Cross Validation with k= " + str(self.k) + " with " + self.method + ""
        size_partition = self.metadata.dataset_size / self.k
        test_data_from = 0
        test_data_to = size_partition-1
        means = []
        results = {}
        for x in range(0, self.k):
            means.append(self.run_classifier_method_with_k(test_data_from, test_data_to, x))
            test_data_to += size_partition
            test_data_from += size_partition-1
        accuracy = 0.00
        precision = 0.00
        recall = 0.00
        f1 = 0.00
        specificty = 0.00
        for x in range(0, self.k):
            measurements = means[x]
            accuracy += measurements['accuracy']
            precision += measurements['precision']
            recall += measurements['recall']
            f1 += measurements['f1']
            specificty += measurements['specificty']
        results['accuracy'] = accuracy / self.k
        results['precision'] = precision / self.k
        results['recall'] = recall / self.k
        results['f1'] = f1 / self.k
        results['specificty'] = specificty / self.k
        return results

    def print_measurements (self, results):
        """
        Print out in a table the measurements results from this evaluation
        :param results: 
        :return: the table with results
        """
        table = prettytable.PrettyTable(["ACCURACY", "PRECISION", "RECALL", "F1", "SPECIFICTY"])
        table.add_row([results['accuracy'], results['precision'], results['recall'], results['f1'], results['specificty']])
        print table