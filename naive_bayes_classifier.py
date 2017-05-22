# Author:      Jose Ortiz Costa
# Date:        April 01, 2017
# File:        naive_bayes_classifier.py
# Description: The file takes a dataset and pre-process all the attributes values
#              It contains useful methods to remove null or empty attributes values,
#              and handle missing values. In addition, this file transform continuous
#              attributes to categorical.
#

from preprocessor import Dataset
import math
import prettytable
class NaiveBayesClassifier(object):
    PREDICTION = "bachelors degree(ba ab bs)"
    def __init__(self,  data, index_class_label,  conditions):
        """
        Class constructor
        :param data: the dataset preprocesed
        :param index_class_label: the class label to be predicted
        :param conditions: the binary conditions index to be predicted 
        """
        self.data = data
        self.class_label = index_class_label
        self.class_labels_conditions = conditions
        self.prob_list = []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def class_labels(self):
        return self._class_labels

    @class_labels.setter
    def class_labels(self, value):
        self._class_labels = value

    @property
    def class_labels_conditions(self):
        return self._class_labels_conditions

    @class_labels_conditions.setter
    def class_labels_conditions(self, value):
        self._class_labels_conditions = value

    @property
    def prob_list(self):
        return self._prob_list

    @prob_list.setter
    def prob_list(self, value):
        self._prob_list = value

    # is working
    def get_class_label_probabililities (self):
        """
        :return: the probabilities of a the class label
        """
        attr_in_prob1 = 0
        attr_in_prob2 = 0

        for attributes in self.data:
            index = 0

            for attribute in attributes:
                if attribute == self.class_labels_conditions[0] or attribute == self.class_labels_conditions[1]:
                    if attribute == self.class_labels_conditions[0]:
                         attr_in_prob1+=1
                    elif attribute == self.class_labels_conditions[1]:
                         attr_in_prob2+=1
                    index+=1

        total_attr = attr_in_prob1 + attr_in_prob2
        prob1 = float(attr_in_prob1) / total_attr
        prob2 = float(attr_in_prob2) / total_attr
        return prob1, prob2, attr_in_prob1, attr_in_prob2

    def column_index (self):
        """
        Adds up a column index
        :return: 
        """
        column_index = []

        for attributes in self.data:
            index = 0

            for attribute in attributes:
                index_attr = {}
                key = attribute + attributes[self.class_label]
                if len(column_index) < len(attributes):
                    index_attr[key] = 1
                    column_index.append(index_attr)
                else:
                    index_attr = column_index[index]
                    if key in index_attr:
                        index_attr[key] += 1
                    else:
                        index_attr[key] = 1
                index+=1

        return column_index

    def prediction (self, tuple, prob1, prob2, labelcount1, labelcount2, index_table):
        """
        Predicts based on the class label
        :param tuple: the data
        :param prob1: 
        :param prob2: 
        :param labelcount1: 
        :param labelcount2: 
        :param index_table: the index to perform the prediction
        :return: the prediction
        """
        index = 0
        attributes_prob_true = prob1
        attributes_prob_false = prob2
        for attribute in tuple:
           if attribute != self.class_labels_conditions[0] and attribute != self.class_labels_conditions[1]:
                key_true = attribute + self.class_labels_conditions[0]
                key_false = attribute + self.class_labels_conditions[1]
                index_table_attribute = index_table[index]
                if key_true in index_table_attribute:
                   attr_true = index_table_attribute[key_true]
                   tmp_prob1 = float(attr_true) / labelcount1
                else:
                   tmp_prob1 = 0.000001
                if key_false in index_table_attribute:
                   attr_false = index_table_attribute[key_false]
                   tmp_prob2 = float(attr_false) / labelcount2
                else:
                   tmp_prob2 = 0.000001
                attributes_prob_true = attributes_prob_true * tmp_prob1
                attributes_prob_false = attributes_prob_false * tmp_prob2
           index +=1
        if attributes_prob_true > attributes_prob_false and tuple[4] == self.PREDICTION:
            return 'false_positive'
        elif attributes_prob_true < attributes_prob_false and tuple[4] == self.PREDICTION:
            return 'false_negative'
        elif attributes_prob_true < attributes_prob_false and tuple[4] != self.PREDICTION:
            return 'true_negative'
        elif attributes_prob_true > attributes_prob_false and tuple[4] != self.PREDICTION:
            return 'true_positive'


    def confusion_matrix (self):
        """
        :return: the confusion matrix
        """
        confusion_matrix = {'true_positive': 0, 'true_negative': 0, 'false_positive': 0, 'false_negative': 0}
        prob1, prob2, labelcount1, labelcount2 = self.get_class_label_probabililities()
        index_table = self.column_index()
        for classes in self.data:
            prediction = self.prediction(classes,prob1, prob2, labelcount1, labelcount2, index_table)
            if prediction in confusion_matrix:
                confusion_matrix[prediction]+=1
            else:
                confusion_matrix[prediction] = 1
        return  confusion_matrix

    def measures (self):
        """
        Compute the measuremnts
        :return: the measurements
        """
        confusion_matrix = self.confusion_matrix()
        results = {}
        tp = confusion_matrix['true_positive']
        tn = confusion_matrix['true_negative']
        fp = confusion_matrix['false_positive']
        fn = confusion_matrix['false_negative']
        total = tp + tn + fp + fn
        accuracy = float((tp + tn)) / total
        precission = float(tp) / (tp + fp)
        recall =  float(tp) / (tp + fn)
        f1 = float((2*tp)) / (2*tp + fp + fn)
        specificity = float(tn) / (tn + fp)
        results['tp'] = tp
        results['tn'] = tn
        results['fp'] = fp
        results['fn'] = fn
        results['total'] = total
        results['accuracy'] = accuracy
        results['precision'] = precission
        results['recall'] = recall
        results['f1'] = f1
        results['specificty'] = specificity
        return results

    def print_table_confusion_matrix (self, results):
        """
        prints the confusion matrix
        :param results: the results
        :return: the confusion matrix measurements
        """
        print ""
        table = prettytable.PrettyTable( ["TP", "TN", "FP", "FN", 'TOTAL'])
        table.add_row([results['tp'], results['tn'], results['fp'], results['fn'], results['total']])
        print table
        print ""

    def print_measurements (self, results):
        """
        Print measurements conputed from the results
        :param results: the results
        :return: the measurements from the results
        """
        print ""
        table = prettytable.PrettyTable(["ACCURACY", "PRECISION", "RECALL", "F1", "SPECIFICTY"])
        table.add_row([results['accuracy'], results['precision'], results['recall'], results['f1'], results['specificty']])
        print table
        print ""

    def print_absolute_errors_table (self, testing_results, other_results):
        """
        Prints the absolute error from measurements
        :param testing_results: 
        :param other_results: 
        :return: the absolute errors
        """
        print ""
        accuracy_error = math.fabs(testing_results['accuracy'] - other_results['accuracy'])
        precision_error = math.fabs(testing_results['precision'] - other_results['precision'])
        recall_error = math.fabs(testing_results['recall'] - other_results['recall'])
        f1_error = math.fabs(testing_results['f1'] - other_results['f1'])
        specifictly_error = math.fabs(testing_results['specificty'] - other_results['specificty'])
        table = prettytable.PrettyTable(["ACCURACY ABSOLUTE ERROR", "PRECISION ABSOLUTE ERROR", "RECALL ABSOLUTE ERROR", "F1 ABSOLUTE ERROR", "SPECIFICTY ABSOLUTE ERROR"])
        table.add_row(
            [accuracy_error, precision_error, recall_error, f1_error, specifictly_error])
        print table
        print ""


















