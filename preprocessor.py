# Author:      Jose Ortiz Costa
# Date:        April 01, 2017
# File:        DatasetPreprocessor.py
# Description: The file takes a dataset and pre-process all the attributes values
#              It contains useful methods to remove null or empty attributes values,
#              and handle missing values. In addition, this file transform continuous
#              attributes to categorical.
#

import csv  # library to read/write csv files.
import codecs  # library to handle asscci values.


class Dataset(object):
    PATH_TO_WRITE_PREPROCESSED_DATASET = 'data/preproccesedDataset.csv'
    KEY_CATEGORYCAL_MISSING_VALUES = "UNKNOWN"
    CATEGORICAL_ATTRIBUTE = "categorical"
    CONTINOUS_ATTRIBUTE = "continuous"
    KEY_CONTINOUS_MISSING_VALUES = 0.0000001

    def __init__(self, path_to_dataset, indexes = 0):
        """
        Class constructor
        :param path_to_dataset: path to the dataset to be processed, static value is set above by default
        """
        self.data = path_to_dataset
        self.class_names = []
        self.class_indexes = []
        self.class_labels = indexes
        self.class_labels_indexes = []
        self.preprocessed_dataset = {}
        self.attributes_classification = []  # can be categorical, or continous
        self.filter_condition = "DEFAULT"
        self.dataset_size = 0
        self.missing_key_categorical_value = "UNKOWN"
        self.missing_key_continous_value = "?"
        # if 0, a probability function method will be applied to determine value by default
        # if 1, the missing value will be replaced by the epsalon value. ( not reconmendable )
        self.method_to_handle_missing_continous_attribute = 0
        self.discretize_num_bins = 0  # set when self.missing_value_continous_method is 1
        self.dataset = []
        self.dataset_size = 0
        self.discretize_cond1 = ""
        self.discretize_cond2 = ""


    #
    # Setters and getters. Self explanatory names
    #
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def class_names(self):
        return self._class_names

    @class_names.setter
    def class_names(self, value):
        self._class_names = value

    @property
    def class_indexes(self):
        return self._class_indexes

    @class_indexes.setter
    def class_indexes(self, value):
        self._class_indexes = value

    @property
    def class_labels(self):
        return self._class_labels

    @class_labels.setter
    def class_labels(self, value):
        self._class_labels = value

    @property
    def class_labels_indexes(self):
        return self._class_labels_indexes

    @class_labels_indexes.setter
    def class_labels_indexes(self, value):
        self._class_labels_indexes = value

    @property
    def preprocessed_dataset(self):
        return self.preprocessed_dataset

    @preprocessed_dataset.setter
    def preprocessed_dataset(self, value):
        self._preprocessed_dataset = value

    @property
    def dataset_size(self):
        return self._dataset_size

    @dataset_size.setter
    def dataset_size(self, value):
        self._dataset_size = value

    @property
    def missing_key_categorical_value(self):
        return self._missing_key_categorical_value

    @missing_key_categorical_value.setter
    def missing_key_categorical_value(self, value):
        self._missing_key_categorical_value = value

    @property
    def attributes_classification(self):
        return self._attributes_classification

    @attributes_classification.setter
    def attributes_classification(self, value):
        self._attributes_classification = value

    @property
    def filter_condition(self):
        return self._filter_condition

    @filter_condition.setter
    def filter_condition(self, value):
        self._filter_condition = value

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        self._dataset = value

    @property
    def dataset_size(self):
        return self._dataset_size

    @dataset_size.setter
    def dataset_size(self, value):
        self._dataset_size = value


    def probability_density_function(self):
        return 0.000001

    def bin_method(self):
        return '1<=10'

    def set_discretize_conditions (self, condition):
        self.discretize_cond1 = condition


    def discretize (self, cont_attribute):
        """
        :param cont_attribute: The continuous attribute to be disctretized
        :return: the attribute discretized
        """
        tmp_attr = int(cont_attribute)
        if tmp_attr < self.discretize_cond1:
            return "<", tmp_attr
        else:
            return ">=", tmp_attr

    def preprocess (self, min_num_classes, max_num_classes, filter_by_attribute = None):
        """
        Starts the preprocess tasks
        :param min_num_classes: 
        :param max_num_classes: 
        :param filter_by_attribute: applies the attribute to be filtered
        :return: the preprocessed data
        """
        pre_dataset = []
        dataset = csv.reader(codecs.open(self.data, 'rU', 'utf-8'))
        index = 0
        for tuple in dataset:
            if index > min_num_classes and index <= max_num_classes:
               preprocesed_tuple = tuple[4].strip().lower()
               if "degree" in preprocesed_tuple:
                   tuple[40] = "yes"
               else:
                   tuple[40] = "no"
               pre_dataset.append(self.handle_categorical_missing_values (tuple, "IGNORE", filter_by_attribute))
            index+=1
        self.dataset_size = index
        return pre_dataset

    def handle_categorical_missing_values (self, class_attributes, missing_value_key, filter_by_attribute):
        """
        Handles missing values in categorical attributes
        :param class_attributes: 
        :param missing_value_key: 
        :param filter_by_attribute: 
        :return: the tuple without missing values or ignored
        """
        index = 0
        class_attr = map(str.strip, class_attributes)
        if filter_by_attribute is None:
            for attribute in class_attr:
                attribute = attribute.lower()
                if 'not in universe' in attribute or attribute == '?':
                    attribute = missing_value_key
                class_attr[index] = attribute
                index+=1
        else:
            if filter_by_attribute in class_attr:
                for attribute in class_attr:
                    attribute = attribute.lower()
                    if 'not in universe' in attribute or attribute == '?':
                        attribute = missing_value_key
                    class_attr[index] = attribute
                    index += 1
        return class_attr

    def get_prepocessed_dataset_by_index_range (self, dataset, min_index, max_index):
        """
        Preprocess the dataset by specifying the index range 
        :param dataset: the data
        :param min_index: from index
        :param max_index: to index
        :return: the preprocessed data
        """
        pre_dataset = []
        index = 0
        for data in dataset:
            if index >=min_index and index <=max_index:
                pre_dataset.append(data)
            index+=1
        return pre_dataset



