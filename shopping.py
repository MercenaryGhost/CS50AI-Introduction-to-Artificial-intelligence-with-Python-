import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    import csv
    import calendar
    
    def month_to_index(a):
        dic = {
            'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'June' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9, 
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
        }
        return dic[a]
    
    evidence = []
    labels = []
    with open('shopping.csv','r') as csvfile:
        csv = csv.reader(csvfile)
        fields = next(csv)
        for row in csv:
            if row[15] == 'Returning_Visitor':
                ret = 1
            else:
                ret = 0
            if row[16] == 'FALSE':
                week = 0
            else:
                week = 1
            temp = [int(row[0]), float(row[1]), int(row[2]), float(row[3]), int(row[4]), float(row[5]), float(row[6]), float(row[7]), 
                    float(row[8]), float(row[9]), month_to_index(row[10]) - 1, int(row[11]), int(row[12]), int(row[13]), int(row[14]),
                    int(ret), week]
            evidence.append(temp)
            if row[-1] == 'FALSE':
                purchase = 0
            else:
                purchase = 1
            labels.append(purchase)
    tup = (evidence,labels)
    return tup
    #raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(evidence, labels)
    return classifier
    #raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_pos = { 'labels':0, 'predictions':0 }
    true_neg = { 'labels':0, 'predictions':0 }
    for i in range(len(labels)):
        if labels[i] == 1:
            true_pos['labels'] += 1
            true_pos['predictions'] += predictions[i]
        else:
            true_neg['labels'] += 1
            true_neg['predictions'] += 1 - predictions[i]
    
    sensitivity = true_pos['predictions']/true_pos['labels']
    specificity = true_neg['predictions']/true_neg['labels']
    return (sensitivity,specificity)
    #raise NotImplementedError


if __name__ == "__main__":
    main()
