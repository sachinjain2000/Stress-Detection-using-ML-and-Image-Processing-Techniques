import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV



df = pd.read_excel('stress_data.xlsx', header=None)

df.columns=['Target', 'ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']
X_train, X_test, y_train, y_test = train_test_split(df[['ECG(mV)', 'EMG(mV)','Foot GSR(mV)','Hand GSR(mV)', 'HR(bpm)','RESP(mV)']], df['Target'],
    test_size=0.30, random_state=12345)

def create_model(optimizer='rmsprop',init='glorot_uniform'):
    model = Sequential()
    model.add(Dense(6, input_dim=6, kernel_initializer=init, activation='relu'))
    model.add(Dense(3, kernel_initializer=init, activation='relu'))
    model.add(Dense(1, kernel_initializer=init, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

seed = 7
np.random.seed(seed)

model = KerasClassifier(build_fn=create_model,verbose=0)
optimizers = ['rmsprop','adam']
init = ['glorot_uniform','normal','uniform']
epochs = [50,100,150]
batches = [5,10,20]
param_grid = dict(optimizer=optimizers, epochs=epochs, batch_size=batches, init=init)
grid = GridSearchCV(estimator=model,param_grid=param_grid)
grid_result = grid.fit(np.array(X_train),np.array(y_train))

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
for params, mean_score, scores in grid_result.grid_scores_:
    print("%f (%f) with: %r" % (scores.mean(), scores.std(), params))



# Prediction of stress/no stress class on new dataset
print()
pred_data = np.array([[-0.005,0.49,8.257,5.853,66.142,45.998]])
pred = grid_result.predict(pred_data)
print('Predicted class for dataset [-0.005,0.49,8.257,5.853,66.142,45.998]:- ', pred)

pred_data = np.array([[0.001,0.931,5.91,19.773,99.065,35.59]])
pred = grid_result.predict(pred_data)
print('Predicted class for dataset [0.001,0.931,5.91,19.773,99.065,35.59]:- ', pred)
