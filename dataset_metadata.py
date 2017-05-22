# Author:      Jose Ortiz Costa
# Date:        May 01, 2017
# File:        dataset_metadata.py
# Description: Contains all the metadata information from the dataset

class Dataset_Metadata (object):

    def __init__(self, dataset_path, dataset_size, class_label_index, class_label_attributes):
        """
        Class constructor
        :param dataset_path: the path to the dataset
        :param dataset_size: the size of the data
        :param class_label_index: the class label
        :param class_label_attributes: the index of the class label
        """
        self.path = dataset_path
        self.index = class_label_index
        self.attr = class_label_attributes
        self.dataset_size = dataset_size
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def attr(self):
        return self._attr

    @attr.setter
    def attr(self, value):
        self._attr = value

    @property
    def dataset_size(self):
        return self._dataset_size

    @dataset_size.setter
    def dataset_size(self, value):
        self._dataset_size = value