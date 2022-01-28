import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier

df = pd.read_excel('stress_data.xlsx', header=None)

df.columns=['Target', 'ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']
X_train, X_test, y_train, y_test = train_test_split(df[['ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']], df['Target'],
    test_size=0.30, random_state=12345)

# Min-Max Scaling

minmax_scale = preprocessing.MinMaxScaler().fit(df[['ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)', 'RESP(mV)']])
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
model = DecisionTreeClassifier(max_leaf_nodes=3)
fit = model.fit(X_train, y_train)

# on normalized data
model_norm = DecisionTreeClassifier(max_leaf_nodes=3)
fit_norm = model_norm.fit(X_train_norm, y_train)

pred_train = model.predict(X_train)

pred_test = model.predict(X_test)

print('Accuracy measure for dataset')
print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test)))

pred_train_norm = model_norm.predict(X_train_norm)

print('Accuracy measure for normalized dataset')

pred_test_norm = model_norm.predict(X_test_norm)

print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test_norm)))


pred = model.predict([[0.001,0.931,5.91,19.773,99.065,35.59]])
print(pred)
pred = model.predict([[-0.005,0.49,8.257,9.853,66.142,45.998]])
print(pred)

pred = model_norm.predict([[0.001,0.931,5.91,19.773,99.065,35.59]])
print(pred)
pred = model_norm.predict([[0.005,0.49,8.257,5.853,80.142,45.998]])
print(pred)
