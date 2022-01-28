import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from django.conf import settings
filepath = settings.MEDIA_ROOT + "\\" + 'stress_data.xlsx'
df = pd.read_excel(filepath, header=None)

df.columns=['Target', 'ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']
X_train, X_test, y_train, y_test = train_test_split(df[['ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']], df['Target'],
    test_size=0.30, random_state=12345)

# Min-Max Scaling

minmax_scale = preprocessing.MinMaxScaler().fit(df[['ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']])
df_minmax = minmax_scale.transform(df[['ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']])
X_train_norm, X_test_norm, y_train_norm, y_test_norm = train_test_split(df_minmax, df['Target'],
    test_size=0.30, random_state=12345)
def plot():
    plt.figure(figsize=(8,6))

    plt.scatter(df['Hand GSR(mV)'], df['HR(bpm)'],
            color='green', label='input scale', alpha=0.5)

    plt.scatter(df_minmax[:,0], df_minmax[:,1],
            color='blue', label='min-max scaled [min=0, max=1]', alpha=0.3)

    plt.title('Hand GSR and HR content of the physiological dataset')
    plt.xlabel('Hand GSR')
    plt.ylabel('HR')
    plt.legend(loc='upper left')
    plt.grid()

    plt.tight_layout()

class KNNclassifier:
    def getKnnResults(self):
        # filepath = settings.MEDIA_ROOT + "\\" + 'stress_data.xlsx'
        print("Started works")
        knn = KNeighborsClassifier(n_neighbors=5)
        fit = knn.fit(X_train, y_train)

        # on normalized data
        knn_norm = KNeighborsClassifier(n_neighbors=5)
        fit_norm = knn_norm.fit(X_train_norm, y_train)

        pred_train = knn.predict(X_train)
        pred_test = knn.predict(X_test)

        # Accuracy measure for datasets

        print('Accuracy measure for dataset:- ', '{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test)))

        pred_test_norm = knn_norm.predict(X_test_norm)
        print('Accuracy measure for normalized dataset:- ',
              '{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test_norm)))

        # comparing the true and predicted responses

        print('True target values: ', y_test.values[0:25])
        print('Predicted target values: ', pred_test_norm[0:25])

        # Confusion Matrix
        print(metrics.confusion_matrix(y_test, pred_test_norm))
        print('True target values: ', y_test.values[0:25])
        print('Predicted target values: ', pred_test_norm[0:25])
        print()
        confusion = metrics.confusion_matrix(y_test, pred_test_norm)
        TP = confusion[1, 1]
        TN = confusion[0, 0]
        FP = confusion[0, 1]
        FN = confusion[1, 0]

        # Metrics calclulation using confusion matrix

        print()
        # Classsification accuracy:- how often is the classifier correct
        accuracy = metrics.accuracy_score(y_test, pred_test_norm)
        print('Classification Accuracy:- ', accuracy)

        # Classification error/Misclassification rate:- how often is the classifier is incorrect
        classificationerror = 1 - metrics.accuracy_score(y_test, pred_test_norm)
        print('Classification Error:- ',classificationerror )

        # Sensitivity :- when the actual value is positive , how often is the prediction correct?
        sensitivity = metrics.recall_score(y_test, pred_test_norm)
        print('Sensitivity:- ',sensitivity )

        # Specificity:- when the actual value is negative ,how often the prediction is the correct?
        Specificity =  TN / float(TN + FP)
        print('Specificity:- ',Specificity )

        # False positive rate:- when the actual value is negative ,how often the prediction is the incorrect?
        fsp =  FP / float(TN + FP)
        print('False positive rate:- ', fsp)

        # Precision:- when a positive value is predicted , how often is the prediction correct?
        precision = metrics.precision_score(y_test, pred_test_norm)
        print('Precision:- ', precision)

        # Prediction of stress/no stress class on new dataset
        print()
        pred_data_norm = minmax_scale.transform([[-0.005, 0.49, 8.257, 5.853, 66.142, 45.998]])
        pred = knn_norm.predict(pred_data_norm)
        print('Predicted class for dataset [-0.005,0.49,8.257,5.853,66.142,45.998]:- ', pred)

        pred_data_norm = minmax_scale.transform([[0.001, 0.931, 5.91, 19.773, 99.065, 35.59]])
        pred = knn_norm.predict(pred_data_norm)
        print('Predicted class for dataset [0.001,0.931,5.91,19.773,99.065,35.59]:- ', pred)

        return df,accuracy,classificationerror,sensitivity,Specificity,fsp,precision