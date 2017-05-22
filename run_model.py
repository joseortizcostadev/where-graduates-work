# Author:      Jose Ortiz Costa
# Date:        April 01, 2017
# File:        run_model.py
# Description: This file is the entry execution point of the program and performs all the computations, measurements and
#              predictions performed by the program. Also, it prints out the results.
#

from decision_tree import DecisionTree
from preprocessor import Dataset
from naive_bayes_classifier import NaiveBayesClassifier
from dataset_metadata import Dataset_Metadata
from k_fold_cross_validation import KFCV
from clustering import Clustering
import prettytable

#constants
RACE_INDEX = 10
GENDER_INDEX = 12
EDUCATION_INDEX = 4
OCCUPATION_FIELD_INDEX = 8

# Construct the decision trees for stem datasets
woman = DecisionTree("data/stem-dataset-woman.csv", "Woman")
men = DecisionTree("data/stem-dataset-men.csv", "Men")
white = DecisionTree("data/stem-dataset-white.csv", "White")
hispanic_latino = DecisionTree("data/stem-dataset-hispanic-latino.csv", "Hispanic-Latino")
asian = DecisionTree("data/stem-dataset-asian.csv", "Asian")
african_american = DecisionTree("data/stem-dataset-african-american.csv", "African-American")

def predict_gender_study_field (gender, occupation_field):
    """
    Predicts the field of study from a decision tree given a gender value 
    :param gender: male or female
    :param occupation_field: see list in dataset
    :return: the predicted field of study e.g: engineering
    """
    if gender == "male":
        return men.decision(occupation_field)
    elif gender == "female":
        return woman.decision(occupation_field)


def predict_race_study_field(race, occupation_field):
    """
    Predicts the field of study from a decision tree given a race value 
    Note: American indian race is not included since there is not enough data to make a prediction.
    :param race: white, hispanic-latino, asian and african american.
    :param occupation_field: see list in dataset
    :return: the predicted field of study e.g: engineering
    """
    if race == "white":
        return white.decision(occupation_field)
    elif race == "black":
        return african_american.decision(occupation_field)
    elif race == "asian or pacific islander":
        return asian.decision(occupation_field)
    else:
        return hispanic_latino.decision(occupation_field)

# Prepossess dataset
print "************************** THIS PROGAM FIND CAUSES ABOUT WHY RECENT GRADUATES CANNOT FIND A JOB IN THEIR AREA " \
      "OF STUDY RIGHT AFTER THEIR GRADUATION ****************************************************************************"
print ""
print "KDD STEPS PERFORMED"
print ""
print "1.SELECTION_____________________________________________________________________________________________________: "
print "stem-dataset-african-american.csv"
print "stem-dataset-asian.csv"
print "stem-dataset-hispanic-latino.csv"
print "stem-dataset-men.csv"
print "stem-dataset-white.csv"
print "stem-dataset-woman.csv"
print "unemployment-by-major.csv"
print "census-income.csv"
print ""
print "2. DATA CLEANING AND PREPROCESING_______________________________________________________________________________",
#######################################################################################################################
#                                               Preprocessing
#######################################################################################################################
MIN_DATA = 0
MAX_DATA = 199523
TRAINING_DATA = 0.75 * MAX_DATA
EVALUATION_DATA = 0.15 * MAX_DATA
TESTING_DATA = 0.15 * MAX_DATA

data = Dataset("data/census-income.csv")
data.set_discretize_conditions(30)
dataset = data.preprocess(MIN_DATA, MAX_DATA)
print " Done.", MAX_DATA, " records preproccesed"

#######################################################################################################################
#               MINING: Naive Bayes Classifier Predict Which Record Has a bachelor degree from the census dataset
#######################################################################################################################
print ""
print "2. MINING_______________________________________________________________________________________________________:"
print ""
print "Using training Data: 75 % of", MAX_DATA , "=", TRAINING_DATA
print ""
print "Naives Bayes Classifier is mining the dataset to predict the people on the census that have a bachellor degree using training data of size: ", TRAINING_DATA
bachelor_degree = "yes" # has a bachelor degree
other_education = "no" # does not have a bachelor degree
dataset_training = data.get_prepocessed_dataset_by_index_range(dataset, MIN_DATA, TRAINING_DATA);
nbc = NaiveBayesClassifier(dataset_training, 40, [bachelor_degree, other_education])
measurements = nbc.measures()
nbc.print_table_confusion_matrix(measurements)
nbc.print_measurements(measurements)
print "Preparing testing data............"
training_results = nbc.measures()
print ""
print "Using testing Data: 15 % of", MAX_DATA , "=", TESTING_DATA
print ""
print "Naives Bayes Classifier is mining the dataset to predict the people on the census that have a bachellor degree using testing data of size: ", TESTING_DATA
bachelor_degree = "yes" # has a bachelor degree
other_education = "no" # does not have a bachelor degree
MIN_DATA = TRAINING_DATA
TESTING_DATA = TRAINING_DATA + TESTING_DATA
dataset_testing = data.get_prepocessed_dataset_by_index_range(dataset, MIN_DATA, TESTING_DATA);
nbc = NaiveBayesClassifier(dataset_testing, 40, [bachelor_degree, other_education])
measurements = nbc.measures()
nbc.print_table_confusion_matrix(measurements)
nbc.print_measurements(measurements)
testing_results = nbc.measures()
print ""
print "Absolute errors table between training and testing measures........."
nbc.print_absolute_errors_table(training_results, testing_results)

#######################################################################################################################
#               MINING: Validate our data using K-FOLD-CROSS-VALIDATION with K = 10
#######################################################################################################################

print "--------------Validating erformance of the classifier with K-FOLD-CROSS-VALIDATION WITH K=10 WITH EVALUATION DATA SIZE: -----------", EVALUATION_DATA
print ""
print "Using evaluation Data: 15 % of", MAX_DATA , "=", EVALUATION_DATA
k = 10
metadata = Dataset_Metadata('data/census-income.csv', EVALUATION_DATA, 40, [bachelor_degree, other_education])
validation = KFCV(k, KFCV.NBC, metadata, True)
measurements = validation.measurements(True)
print ""
validation.print_measurements(measurements)
print ""

#######################################################################################################################
#               MINING: Decision tree to establish which of those bachelors are in the following fields
#                       'Computers, Mathematics, and Statistics', 'Engineering', 'Science Related'
#######################################################################################################################
print "---------------- Predicting Bachelor's field of study using Decision Tree method -------------------------------"
# from the data predict the field of study of all the people on the census
# this is accomplished by making a decision for every decision tree by race and gender.
# For expample if the tuple has attribute male, and gender white, and its degree is a bachelor degree,
# it will predict the field of study for that degree based on the decision tree male and gender.
# the prediction with more weight will be the predicted field of study for that bachelor.
# Note that predictions are independent of the age.
number_of_bachelors_degree_predicted = 0
dataset_predicted = []
for attributes in dataset_testing:
    education = attributes[EDUCATION_INDEX]
    if education == "bachelors degree(ba ab bs)":
        race = attributes[RACE_INDEX]
        gender = attributes[GENDER_INDEX]
        study_field_by_gender = predict_gender_study_field(gender, attributes[OCCUPATION_FIELD_INDEX])
        study_field_by_race = predict_race_study_field(race, attributes[OCCUPATION_FIELD_INDEX])
        study_field_description_by_gender = study_field_by_gender['prediction']
        study_field_description_by_race = study_field_by_race['prediction']
        study_weight_by_gender = study_field_by_gender['weight']
        study_weight_by_race = study_field_by_race['weight']
        if study_weight_by_gender > study_weight_by_race:
            attributes[EDUCATION_INDEX] = study_field_description_by_gender
        else:
            attributes[EDUCATION_INDEX] = study_field_description_by_race
        number_of_bachelors_degree_predicted+=1
        dataset_predicted.append(attributes)
        if attributes[EDUCATION_INDEX] == "computers, mathematics, and statistics" or \
           attributes[EDUCATION_INDEX] == "engineering" or \
           attributes[EDUCATION_INDEX] == "science- and engineering-related":
           dataset_predicted.append(attributes)


percent_predicted = float(number_of_bachelors_degree_predicted) / MAX_DATA
print "Predicted as bachelor degree for the following areas of study 'Computer Science and Mathematics', 'Engineering', or 'Science Related' bachelors degrees in people with a different occupational area than their area of study"
print number_of_bachelors_degree_predicted, "of", EVALUATION_DATA, ",", percent_predicted * 100, "% of the data"

# outputs descriptives tables about how the decision trees performed the calcutions
woman.prediction_table(number_of_bachelors_degree_predicted)
men.prediction_table(number_of_bachelors_degree_predicted)
white.prediction_table(number_of_bachelors_degree_predicted)
hispanic_latino.prediction_table(number_of_bachelors_degree_predicted)
african_american.prediction_table(number_of_bachelors_degree_predicted)
asian.prediction_table(number_of_bachelors_degree_predicted)
impurity_woman = woman.impurity()
impurity_men = men.impurity()
impurity_white = white.impurity()
impurity_hispanic_latino = hispanic_latino.impurity()
impurity_african_american = african_american.impurity()
impurity_asian = asian.impurity()
print ""
print "TABLE OF IMPURITIES"
print "---------------------------------------------------------------------------------------"
table = prettytable.PrettyTable(["","WOMAN", "MEN", "WHITE", "HISPANIC_LATINO", "AFRICAN_AMERICAN", "ASIAN"])
entropies = ["ENTROPY", str(impurity_woman['entropy']), str(impurity_men['entropy']), str(impurity_white['entropy']),
            str(impurity_hispanic_latino['entropy']), str(impurity_african_american['entropy']), str(impurity_asian['entropy'])]
gini_indexes = ["GINI_INDEXES", str(impurity_woman['gini_index']), str(impurity_men['gini_index']), str(impurity_white['gini_index']),
               str(impurity_hispanic_latino['gini_index']), str(impurity_african_american['gini_index']), str(impurity_asian['gini_index'])]
classification_error = ["CLASSIFICATION_ERROR", impurity_woman['classification_error'], impurity_men['classification_error'],
                        impurity_white['classification_error'], impurity_hispanic_latino['classification_error'],
                        impurity_african_american['classification_error'], impurity_asian['classification_error']]
table.add_row(entropies)
table.add_row(gini_indexes)
table.add_row(classification_error)
print table
print ""
#######################################################################################################################
#   EVALUATION: Clustering data to determine patterns why people with a bachelor degree in
#               'Computer Science and Mathematics', 'Engineering', or 'Science Related' are working in their area of
#                study
#######################################################################################################################

print "--------------------- Clustering data to determine patterns about people with a bachelor degree in 'Computer Science and Mathematics', 'Engineering', or 'Science Related' that are not working in their area of study ---------------"
print ""
clusters = Clustering(dataset_predicted)

# occupational field
computer_science_cluster = clusters.computer_science_field_cluster()
engineering_cluster = clusters.engineering_field_cluster()
science_related_cluster = clusters.science_related_field_cluster()
print "------------------ CLUSTERS OF PEOPLE PREDICTED WITH BACHELOR IN COMPUTER SCIENCE, MATHEMATICS, AND STATISTICS CLUSTERED  ---------------------------"
print ""
occupational_field = clusters.ocupational_fields_measures(computer_science_cluster)
print "Table Clusters Occupational Area Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(occupational_field)
# race
race = clusters.race_measures(computer_science_cluster)
print "Table Clusters Gender Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(race)

# working-partime or fulltime
citizen_status = clusters.citizenship_status(computer_science_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(citizen_status)

# working-partime or fulltime
employment = clusters.unemployment_measures(computer_science_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(employment)

# working-partime or fulltime
age = clusters.age_measures(computer_science_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(age)

# working-partime or fulltime
gender = clusters.gender_measures(computer_science_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(gender)


print "------------------ CLUSTERS OF PEOPLE PREDICTED WITH BACHELOR IN ENGINEERING  ---------------------------"
print ""
occupational_field = clusters.ocupational_fields_measures(engineering_cluster)
print "Table Clusters Occupational Area Percentage for People with a Bachelor in Engineering"
clusters.table_clusters(occupational_field)
# race
race = clusters.race_measures(engineering_cluster)
print "Table Clusters Gender Percentage for People with a Bachelor in Engineering"
clusters.table_clusters(race)

# working-partime or fulltime
citizen_status = clusters.citizenship_status(engineering_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(citizen_status)

# working-partime or fulltime
employment = clusters.unemployment_measures(engineering_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Engineering"
clusters.table_clusters(employment)

# working-partime or fulltime
age = clusters.age_measures(engineering_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(age)

# working-partime or fulltime
gender = clusters.gender_measures(engineering_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(gender)

print "------------------ CLUSTERS OF PEOPLE PREDICTED WITH BACHELOR IN SCIENCE RELATED FIELDS ( HEALTH SERVICES NOT INCLUDED )  ---------------------------"

print ""
occupational_field = clusters.ocupational_fields_measures(science_related_cluster)
print "Table Clusters Occupational Area Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(occupational_field)
# race
race = clusters.race_measures(science_related_cluster)
print "Table Clusters Gender Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(race)

# working-partime or fulltime
employment = clusters.unemployment_measures(science_related_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(employment)

# working-partime or fulltime
age = clusters.age_measures(science_related_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(age)

# working-partime or fulltime
gender = clusters.gender_measures(science_related_cluster)
print "Table Clusters Employment Percentage for People with a Bachelor in Computer Science, Mathematics and Statistics"
clusters.table_clusters(gender)

print ""

print "---------------- PATTERNS PROFILES FROM RESULTS (HIGHEST, AVERAGE, LOWER ) --------------------------------------"
print ""
clusters.profile(computer_science_cluster, "Conputer Science, Mathematics and Statistics")
clusters.profile(engineering_cluster, "Engineering")
