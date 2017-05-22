# Author:      Jose Ortiz Costa
# Date:        April 01, 2017
# File:        decision_tree.py
# Description: Built a decision tree based on the predictions from the other datasets
#

import csv  # library to read/write csv files.
import codecs  # library to handle asscci values.
import prettytable
import math

class DecisionTree(object):
    # fields of study to be applied to this decision tree
    COMPUTER_SCIENCE_AND_MATHEMATICS = 0
    ENGINEERING = 1
    PHYSICAL_SCIENCES = 2
    BIOLOGICAL_ENVIRONMENTAL_AGRICULTURAL = 3
    PSYCHOLOGY = 4
    SOCIAL_SCIENCES = 5
    MULTIDISCIPLINARY_STUDIES = 6
    SCIENCE_RELATED = 7
    BUSSINES = 8
    EDUCATION = 9
    LITERATURE = 10
    LIBERAL_ARTS = 11
    VISUAL_AND_PERFORMING_ARTS = 12
    COMMUNICATION = 13
    OTHERS = 14

    def __init__(self, data, descriptor):
        """
        Class constructor
        :param data: the data preprocesed
        :param descriptor: the descriptor of the data
        """
        self.data = data
        self.fields = []
        self.attributes = {}
        self.population_total = []
        self.build() # build the decision tree. Prepocessing tasks take effect in this function too
        self.computer_science = 0
        self.engineering = 0
        self.science_related = 0
        self.descriptor = descriptor
        self.accuracy = 0.0
        self.precision = 0.0
        self.recall = 0.0
        self.f1 = 0.0
        self.specificity = 0.0
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0
        self.entropy = 0.0
        self.gini_index = 0.0
        self.classification_error = 0.0
        self.prob_cs_and_math = 0.0
        self.prob_engineering = 0.0
        self.prob_science_related = 0.0
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, value):
        self._condition = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        self._fields = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def class_label(self):
        return self._class_label

    @class_label.setter
    def class_label(self, value):
        self._class_label = value

    @property
    def population_total(self):
        return self._population_total

    @population_total.setter
    def population_total(self, value):
        self._population_total = value

    def build_field_of_work_tree (self):
        """
        prepare the field of work labels before building the tree
        :return: all the prepared labels
        """
        field_of_work = {}
        field_of_work['production'] = ["mining", "retail trade"]
        field_of_work['construction'] = ["construction"]
        field_of_work['agriculture'] = ["agriculture"]
        field_of_work['social services'] = ["social services", "private household services", "armed forces"]
        field_of_work['office support'] = ["other professional services"]
        field_of_work['sales'] = ["wholesale trade"]
        field_of_work['service'] = ["transportation"]
        field_of_work['arts and entertainment'] = ["entertainment", "communications"]
        field_of_work['education'] = ["education"]
        field_of_work['legal'] = ["public administration"]
        field_of_work['business and financial'] = ["business and repair services"]
        field_of_work['health care'] = ["utilities and sanitary services", "hospital services"]
        field_of_work['architects'] = ["personal services except private HH"]
        field_of_work['life scientists'] = ["medical except hospital"]
        field_of_work["production"] = ["finance insurance and real estate","forestry and fisheries",
                                       "manufacturing-durable goods", "manufacturing-", "manufacturing-nondurable goods"]
        return field_of_work

    def preprocess (self, class_label):
        """
        Does some extra pre-procesess tasks to the predictions
        :param class_label: 
        :return: the preprocessed class label
        """
        class_label = class_label.lower()
        field_of_work = self.build_field_of_work_tree()
        for field, occupation in field_of_work.items():
            if class_label in occupation:
                return field
        return "other"

    def load_data (self):
        """
        Loads all the data from the datasets
        :return: the loaded data
        """
        dataset = csv.reader(codecs.open(self.data, 'rU', 'utf-8'))
        index = 0
        for classes in dataset:
            if index == 0:
                self.fields = [x.replace("'", "").lower() for x in classes]
            else:
                key_field = classes[0].replace('.', '').lower()
                index_attribute = 0
                tmp_attributes = []
                for attribute in classes:
                    if index_attribute > 0:
                      tmp_attributes.append(int(attribute.replace(",", "").strip()))
                    index_attribute += 1
                self.attributes[key_field] = tmp_attributes
            index+=1

    def load_full_population_data_per_field_of_study(self):
        """
        Creates the inner branches of the tree
        :return: the inner branches
        """
        data_population = [0,0,0]
        for field, classes in self.attributes.items():
            data_population[0] += classes[self.COMPUTER_SCIENCE_AND_MATHEMATICS]
            data_population[1] += classes[self.ENGINEERING]
            data_population[2] += classes[self.SCIENCE_RELATED]
        return data_population

    def build (self):
        """
        Build the decision tree with the dataset provided. 
        Prepossessing tasks take effect in this function
        :return: 
        """
        self.build_field_of_work_tree()
        self.load_data()
        self.population_total = self.load_full_population_data_per_field_of_study()

    def prediction_table (self, total_predicted):
        """
        Prints out a prediction table with the predictions found
        :param total_predicted: 
        :return: the prediction table
        """
        self.compute_purity(total_predicted)
        print ""
        print "Table bachelor predictions for", self.descriptor
        print"-------------------------------------------------------------------------------------"
        table = prettytable.PrettyTable(["         ", "Computer Science, Mathematics and Statistics", "Engineering", "Science Related"])
        cs_percent = float(self.computer_science) / total_predicted
        eng_percent = float(self.engineering) / total_predicted
        science_related_percent = float(self.science_related) / total_predicted
        table.add_row(["Predicted area of study", "%.2f" % (cs_percent * 100), "%.2f" % (eng_percent * 100),  "%.2f" % (science_related_percent * 100)])
        print table
        print ""

    def compute_measurements (self):
        """
        Computes measurements for decision tree
        :return: the measuremets computed
        """
        self.accuracy = float((self.tp + self.tn)) / (self.tp + self.fp + self.tn + self.fn)
        self.precision = float(self.tp) / (self.tp + self.fp)
        self.recall = float(self.tp) / (self.tp + self.fn)
        self.f1 = float((2 * self.tp)) / (2 * self.tp + self.fp + self.fn)
        self.specificity = float(self.tn) / (self.tn + self.fp)

    def compute_purity (self, total_class_label):
        """
        Computes purity of predictions
        :param total_class_label: 
        :return: the purity measurements of the data
        """
        self.prob_cs_and_math = float(self.computer_science) / total_class_label
        self.prob_engineering = float(self.engineering) / total_class_label
        self.prob_science_related = float(self.science_related) / total_class_label
        self.entropy = self.get_entropy(self.prob_cs_and_math, self.prob_engineering, self.prob_science_related)
        self.gini_index = self.get_gin_index(self.prob_cs_and_math, self.prob_engineering, self.prob_science_related)
        self.classification_error = self.get_classification_error(self.prob_cs_and_math, self.prob_engineering, self.prob_science_related)

    def impurity (self):

        measures = {}
        measures['entropy'] = self.entropy
        measures['gini_index'] = self.gini_index
        measures['classification_error'] = self.classification_error
        return measures

    def get_entropy (self, prob1, prob2, prob3):
        """
        Caculates entropy measure
        :param prob1: 
        :param prob2: 
        :param prob3: 
        :return: the entropy
        """
        if prob1 == 0:
            prob1 == 1
        elif prob2 == 0:
            prob2 == 1
        elif prob3 == 0:
            prob3 == 100 - (prob1 - prob2)
        return  ((1 * prob1) * math.log(prob1, 2.0) * (1 * prob2) * math.log(prob2, 2.0))

    def get_gin_index (self, prob1, prob2, prob3):
        """
        Calculates the gin index
        :param prob1: 
        :param prob2: 
        :param prob3: 
        :return: the gin index
        """
        return 1 - (math.pow(prob1, 2) + math.pow(prob2,2) + math.pow(prob3,2))

    def get_classification_error (self, prob1, prob2, prob3):
        """
        Calculates the classification error of the class labels
        :param prob1: 
        :param prob2: 
        :param prob3: 
        :return: 
        """
        prob_list = [prob1, prob2, prob3]
        return 1 - max(prob_list)

    def decision (self, class_label):
        """
        Predicts a decision based on the data
        :param class_label: 
        :return: the prediction
        """
        prediction = {}
        self.class_label = self.preprocess(class_label)
        if self.class_label in self.attributes:
            label_true = 100 / (len(self.fields)-1)
            label_false = 100 - label_true
            total = sum(self.attributes[self.class_label])
            decision_label = ""
            decision_value = 0
            index_field = 1
            attributes = self.attributes[self.class_label]
            for attribute in attributes:
                tmp_decision_value = (label_true*attribute)+(label_false*(total - attribute))
                if decision_value < tmp_decision_value:
                    decision_value = tmp_decision_value
                    decision_label = self.fields[index_field]
                    if index_field == self.COMPUTER_SCIENCE_AND_MATHEMATICS + 1:
                        self.computer_science += 1
                        self.tp+=1
                    elif index_field == self.ENGINEERING + 1:
                        self.engineering += 1
                        self.tp+=1
                    elif index_field == self.SCIENCE_RELATED + 1:
                        self.science_related += 1
                        self.tp+=1
                    else:
                        self.tn+=1
                else:
                    if index_field == self.COMPUTER_SCIENCE_AND_MATHEMATICS + 1:
                        self.fp+=1
                    elif index_field == self.ENGINEERING + 1:
                        self.fp+=1
                    elif index_field == self.SCIENCE_RELATED + 1:
                        self.fp+=1
                    else:
                        self.fn+=1
                index_field+=1
            prediction['prediction'] = decision_label
            prediction['weight'] = decision_value

        else:
            prediction['prediction'] = self.fields[self.OTHERS + 1]
            prediction['weight'] = 0
        #self.compute_measurements()
        return prediction
