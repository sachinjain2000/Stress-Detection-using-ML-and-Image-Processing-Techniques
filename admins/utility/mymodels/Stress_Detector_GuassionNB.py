import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

df = pd.read_excel('stress_data.xlsx', header=None)

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

plot()
plt.show()

# on non-normalized data
gnb = GaussianNB()
fit = gnb.fit(X_train, y_train)

# on normalized data
gnb_norm = GaussianNB()
fit_norm = gnb_norm.fit(X_train_norm, y_train)

pred_train = gnb.predict(X_train)
pred_test = gnb.predict(X_test)

# Accuracy measure for datasets

print('Accuracy measure for dataset')
print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test)))

print('Accuracy measure for normalized dataset')
pred_test_norm = gnb_norm.predict(X_test_norm)
print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test_norm)))


# comparing the true and predicted responses

print('True target values: ',y_test.values[0:25])
print('Predicted target values: ',pred_test_norm[0:25])

# Confusion Matrix
print(metrics.confusion_matrix(y_test,pred_test_norm))
print('True: ',y_test.values[0:25])
print('Pred: ',pred_test_norm[0:25])
print()
confusion = metrics.confusion_matrix(y_test,pred_test_norm)
TP = confusion[1,1]
TN = confusion[0,0]
FP = confusion[0,1]
FN = confusion[1,0]

# Metrics calclulation using confusion matrix

print()
# Classsification accuracy:- how often is the classifier correct
print('Classification Accuracy:- ' , metrics.accuracy_score(y_test,pred_test_norm))

# Classification error/Misclassification rate:- how often is the classifier is incorrect
print('Classification Error:- ' , 1-metrics.accuracy_score(y_test,pred_test_norm))

# Sensitivity :- when the actual value is positive , how often is the prediction correct?
print('Sensitivity:- ' , metrics.recall_score(y_test,pred_test_norm))

# Specificity:- when the actual value is negative ,how often the prediction is the correct?
print('Specificity:- ' , TN/float(TN+FP))

# False positive rate:- when the actual value is negative ,how often the prediction is the incorrect?
print('False positive rate:- ' , FP/float(TN+FP))


# Precision:- when a positive value is predicted , how often is the prediction correct?
print('Precision:- ' , metrics.precision_score(y_test,pred_test_norm))

# Prediction of stress/no stress class on new dataset
print()
pred_data_norm = minmax_scale.transform([[-0.005,0.49,8.257,5.853,66.142,45.998]])
pred = gnb_norm.predict(pred_data_norm)
print('Predicted class for dataset [-0.005,0.49,8.257,5.853,66.142,45.998]:- ', pred)

pred_data_norm = minmax_scale.transform([[0.001,0.931,5.91,19.773,99.065,35.59]])
pred = gnb_norm.predict(pred_data_norm)
print('Predicted class for dataset [0.001,0.931,5.91,19.773,99.065,35.59]:- ', pred)

