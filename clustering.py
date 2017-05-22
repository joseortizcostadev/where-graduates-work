# Author:      Jose Ortiz Costa
# Date:        April 01, 2017
# File:        clustering.py
# Description: This class takes a mined data and create unsupervising learning clusters to determine common patterns on
#              about the data mined. It also print tables containing higher and lower profiles predictions.
#
import prettytable
class Clustering(object):
    # constants
    COMPUTER_SCIENCE_AND_MATHEMATICS = "computers, mathematics, and statistics"
    ENGINEERING = "engineering"
    SCIENCE_RELATED = "science- and engineering-related"
    AGE = 0
    OCUPATION_LABEL = 9
    RACE = 10
    GENDER = 12
    EMPLOYED = 15
    CITIZENSHIP = 35

    def __init__(self, results):
        """
        Class constructor
        :param results: the predicted results from the mined data
        """
        self.results = results
        self.computer_science_cluster = []
        self.engineering_cluster = []
        self.science_related_cluster = []
        self.cluster_by_field_of_study()

    def cluster_by_field_of_study(self):
        """
        Create clusters groups using the area of study label
        :return: 
        """
        for data in self.results:
            if data[4] == self.COMPUTER_SCIENCE_AND_MATHEMATICS:
                self.computer_science_cluster.append(data)
            elif data[4] == self.ENGINEERING:
                self.engineering_cluster.append(data)
            elif data[4] == self.SCIENCE_RELATED:
                self.science_related_cluster.append(data)
    #
    # The next functions create clusters and assign labels to clusters
    #
    def computer_science_field_cluster(self):
        return self.computer_science_cluster

    def engineering_field_cluster(self):
        return self.engineering_cluster

    def science_related_field_cluster(self):
        return self.science_related_cluster

    def assign_labels_to_clusters (self, attribute):
        attr = int(attribute)
        if attr < 25:
            return "<25"
        elif attr > 25 and attr <= 35:
            return ">25 and <=35"
        elif attr > 35 and attr <=45:
            return ">25 and <=35"
        else:
            return ">35"

    def get_cluster_label_measures(self, cluster, field_index):
        """
        Get measures from the clusters
        :param cluster: 
        :param field_index: 
        :return: 
        """
        ocuppational_field = {}
        total = len(cluster)
        for label in cluster:
            attribute = label[field_index]
            if field_index == self.AGE:
                attribute = self.assign_labels_to_clusters(label[self.AGE])
            if attribute in ocuppational_field:
                ocuppational_field[attribute] += 1
            else:
                ocuppational_field[attribute] = 1
        for key,value in ocuppational_field.items():
            tmp_val = float(value) / total
            value_percent = tmp_val * 100
            ocuppational_field[key] = value_percent
        return ocuppational_field

    #
    # Individual measures functions
    #
    def ocupational_fields_measures(self, cluster):
        return self.get_cluster_label_measures(cluster, self.OCUPATION_LABEL)

    def race_measures(self, cluster):
        return self.get_cluster_label_measures(cluster, self.RACE)

    def age_measures (self, cluster):
        return self.get_cluster_label_measures(cluster, self.AGE)

    def unemployment_measures (self, cluster):
        return self.get_cluster_label_measures(cluster, self.EMPLOYED)

    def gender_measures(self, cluster):
        return self.get_cluster_label_measures(cluster, self.GENDER)

    def citizenship_status(self, cluster):
        return self.get_cluster_label_measures(cluster, self.CITIZENSHIP)


    def table_clusters (self, cluster):
        """
        Print table of clusters
        :param cluster: 
        :return: 
        """
        print ""
        clusters_labels = []
        cluster_values = []
        for key, value in cluster.items():
            clusters_labels.append(key)
            cluster_values.append(value)
        if len(clusters_labels) == 0:
            clusters_labels.append("DATA CLUSTERED")
            cluster_values.append("NO CLUSTERS FOUND")
        table = prettytable.PrettyTable(clusters_labels)
        table.add_row(cluster_values)
        print table
        print ""

    def profile (self, cluster, label):
        """
        Prints higher and lower profiles predicted in a table
        :param cluster: 
        :param label: 
        :return: 
        """
        print ""
        gender = self.gender_measures(cluster)
        race = self.race_measures(cluster)
        ocuppation = self.ocupational_fields_measures(cluster)
        age = self.age_measures(cluster)
        unemployment = self.unemployment_measures(cluster)
        citizenship_status = self.citizenship_status(cluster)
        maximum_gender = max(gender, key=gender.get)  # Just use 'min' instead of 'max' for minimum.
        maximum_race = max(race, key=race.get)  # Just use 'min' instead of 'max' for minimum.
        maximum_ocupational_field = max(ocuppation, key=ocuppation.get)
        maximum_age = max(age, key=age.get)
        maximum_citizenship_status = max(citizenship_status, key=citizenship_status.get)
        maximum_unemployment = max(unemployment, key=unemployment.get)
        minimum_gender = min(gender, key=gender.get)  # Just use 'min' instead of 'max' for minimum.
        minimum_race = min(race, key=race.get)  # Just use 'min' instead of 'max' for minimum.
        minimum_ocupational_field = min(ocuppation, key=ocuppation.get)
        minimum_age = min(age, key=age.get)
        minimum_unemployment = min(unemployment, key=unemployment.get)
        minimum_citizenship = min(citizenship_status, key=citizenship_status.get)
        # just to be more formal with races names and taking into account the sensivility of some people about those terms
        # I am going to change black race to african-american although in my data it is listed as black
        if (minimum_race == "black"):
            minimum_race = "African-american"
        if (maximum_race == "black"):
            maximum_race = "African-american"
        table = prettytable.PrettyTable(["", "LOWEST PROFILE PREDICTION FOR BACHELOR DEGRESS IN " + label, "HIGHEST PROFILE PREDICTION FOR BACHELOR DEGRESS IN " + label])
        table.add_row(["GENDER", minimum_gender, maximum_gender])
        table.add_row(["RACE", minimum_race,  maximum_race])
        table.add_row(["OCUPPATION", minimum_ocupational_field, maximum_ocupational_field])
        table.add_row(["CITIZENSHIP_STATUS", minimum_citizenship, maximum_citizenship_status])
        table.add_row(["AGE", minimum_age, maximum_age])
        #table.add_row(["EMPLOYMENT STATUS", maximum_unemployment])
        print table
        print ""





