import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
from sklearn.pipeline import Pipeline
from sklearn import svm

if __name__ == "__main__":
    df = pd.read_excel('stress_data.xlsx', header=0)
    df.columns = ['Target', 'ECG(mV)', 'EMG(mV)', 'Foot GSR(mV)', 'Hand GSR(mV)', 'HR(bpm)', 'RESP(mV)']
    X_train, X_test, y_train, y_test = train_test_split(
        df[['ECG(mV)', 'EMG(mV)', 'Foot GSR(mV)', 'Hand GSR(mV)', 'HR(bpm)', 'RESP(mV)']], df['Target'],
        test_size=0.30, random_state=12345)

    # Min-Max Scaling

    minmax_scale = preprocessing.MinMaxScaler().fit(
        df[['ECG(mV)', 'EMG(mV)', 'Foot GSR(mV)', 'Hand GSR(mV)', 'HR(bpm)', 'RESP(mV)']])
    df_minmax = minmax_scale.transform(
        df[['ECG(mV)', 'EMG(mV)', 'Foot GSR(mV)', 'Hand GSR(mV)', 'HR(bpm)', 'RESP(mV)']])
    X_train_norm, X_test_norm, y_train_norm, y_test_norm = train_test_split(df_minmax, df['Target'],
                                                                            test_size=0.30, random_state=12345)


    pipeline = Pipeline([
        ('clf', DecisionTreeClassifier(criterion='entropy'))
    ])

    parameters = {
        'clf__max_depth': (150, 155, 160),
        'clf__min_samples_split': (1, 2, 3),
        'clf__min_samples_leaf': (1, 2, 3)
    }

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy')
    grid_search.fit(X_train_norm, y_train_norm.values.ravel())
    print('Best Score:- %0.3f' % grid_search.best_score_)
    print('Best paramaters set:- ')
    best_paramaters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print('\t%s %r' % (param_name, best_paramaters[param_name]))

    predictions = grid_search.predict(X_test_norm)
    print(classification_report(y_test_norm, predictions))


    parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                         'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]





    grid_search = GridSearchCV(svm.SVC(C=1), parameters, n_jobs=-1, verbose=1, scoring='accuracy')
    grid_search.fit(X_train_norm, y_train_norm.values.ravel())
    print('Best Score:- %0.3f' % grid_search.best_score_)
    print("Best parameters set found on development set:")
    print()
    print(grid_search.best_params_)
    print()
    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, grid_search.predict(X_test_norm)
    print(classification_report(y_true, y_pred))
    print()

    # Prediction of stress/no stress class on new dataset

    print()
    print('Prediction using Decision Tree Classifier')
    pred_data_norm = minmax_scale.transform([[-0.005, 0.49, 8.257, 5.853, 66.142, 45.998]])
    pred = grid_search.predict(pred_data_norm)
    print('Predicted class for dataset [-0.005,0.49,8.257,5.853,66.142,45.998]:- ', pred)

    pred_data_norm = minmax_scale.transform([[0.001, 0.931, 5.91, 19.773, 99.065, 35.59]])
    pred = grid_search.predict(pred_data_norm)
    print('Predicted class for dataset [0.001,0.931,5.91,19.773,99.065,35.59]:- ', pred)

    print()
    print('Prediction using SVM')
    pred_data_norm = minmax_scale.transform([[-0.005, 0.49, 8.257, 5.853, 66.142, 45.998]])
    pred = grid_search.predict(pred_data_norm)
    print('Predicted class for dataset [-0.005,0.49,8.257,5.853,66.142,45.998]:- ', pred)

    pred_data_norm = minmax_scale.transform([[0.001, 0.931, 5.91, 19.773, 99.065, 35.59]])
    pred = grid_search.predict(pred_data_norm)
    print('Predicted class for dataset [0.001,0.931,5.91,19.773,99.065,35.59]:- ', pred)

