# -*- coding: utf-8 -*-
"""Capstone_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dqRJstSlZJ9TOXWD-26dmEzHcEp1LlWZ
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns
import tensorflow as tf
from sklearn import preprocessing, svm
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostRegressor ,RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense ,LSTM, Normalization
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.optimizers import Adam

url = '/content/drive/MyDrive/Dataset/Training_capstone_1.csv'
data = pd.read_csv(url)

data.head()

data.info()

data.isnull().sum()

data = data.drop(columns=['nan'])
data.head()

data.describe()

z = data.drop(["prognosis"],axis =1)
a = data['prognosis'].unique()

# sns.pairplot(data, diag_kind = 'kde')

plt.figure(figsize=(100, 90))
correlation_matrix = data.corr().round(2)
 
# Untuk menge-print nilai di dalam kotak, gunakan parameter anot=True
sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

category = pd.get_dummies(data.prognosis)
category

data = pd.concat([data, category], axis=1)
data = data.drop(columns='prognosis')
data.head()

data_1 = data.values
data_1

X = data_1[:,0:132]
y = data_1[:,132:173]

# Normalize
min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)
X_scale

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 123)

print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in test dataset: {len(X_test)}')

models = pd.DataFrame(index=['train_mse', 'test_mse'], 
                      columns=['KNN', 'RandomForest'])

knn = KNeighborsRegressor(n_neighbors=300)
knn.fit(X_train, y_train)
 
models.loc['train_mse','knn'] = mean_squared_error(y_pred = knn.predict(X_train), y_true=y_train)

RF = RandomForestRegressor(n_estimators=150, max_depth=16, random_state=55, n_jobs=-1)
RF.fit(X_train, y_train)
 
models.loc['train_mse','RandomForest'] = mean_squared_error(y_pred=RF.predict(X_train), y_true=y_train)

mse = pd.DataFrame(columns=['train', 'test'], index=['KNN','RF'])
 
model_dict = {'KNN': knn, 'RF': RF}
 
for name, model in model_dict.items():
    mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))
    mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))
 
mse

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

prediksi = z.iloc[:1].copy()
prediksi
print(type(z))

pred_dict = {'y_true':y_test[:1]}
pred_dict
print(type(y_test))

y_test = pd.DataFrame(y_test, columns =a)
y_test

prediksi = z.iloc[:1].copy()
pred_dict = {'y_true':y_test[:1]}
for name, model in model_dict.items():
    pred_dict['prediksi_'+name] = model.predict(prediksi).round(1)
 
pd.DataFrame(pred_dict)

"""Sekuensial Multiclass target"""

#Cara 1 Multiclass
tf.random.set_seed(42)
model_s = tf.keras.models.Sequential([
      tf.keras.layers.Dense(128,input_shape=(132,)),
      tf.keras.layers.Dense(64, activation='relu'),
      tf.keras.layers.Dense(41,activation ='softmax')
])

model_s.compile(optimizer='Adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.9):
      print("\nAkurasi telah mencapai >90%!")
      self.model.stop_training = True
callbacks = myCallback()

model_s.summary()

history = model_s.fit(X_train,y_train, epochs=5000, verbose=1 ,callbacks = [callbacks] )

model_s.evaluate(X_test, y_test)

# Membuat plot akurasi model
plt.figure(figsize=(10,4))
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.grid(True)
plt.show()

print()

# Membuat plot loss model
plt.figure(figsize=(10,4))
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.grid(True)
plt.show()

"""Sekuensial single target"""

X = data.drop(["prognosis"],axis =1)
y = data["prognosis"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 123)

tf.random.set_seed(42)
model_s = tf.keras.models.Sequential([
      tf.keras.layers.Dense(128,input_shape=(132,)),
      tf.keras.layers.Dense(64, activation='relu'),
      tf.keras.layers.Dense(54, activation='relu'),
      tf.keras.layers.Dense(1,activation ='softmax')
])

model_s.compile(optimizer='Adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.9):
      print("\nAkurasi telah mencapai >90%!")
      self.model.stop_training = True
callbacks = myCallback()

model_s.summary()

history = model_s.fit(X_train,y_train, epochs=5000, verbose=1 ,callbacks = [callbacks] )

model_s.evaluate(X_test, y_test)

# Membuat plot akurasi model
plt.figure(figsize=(10,4))
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.grid(True)
plt.show()

print()

# Membuat plot loss model
plt.figure(figsize=(10,4))
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.grid(True)
plt.show()

"""SVM"""

data['prognosis'].value_counts()

classifier_linear = svm.SVC(kernel='linear')
classifier_linear.fit(X_train, y_train)
prediction_linear = classifier_linear.predict(X_test)

target_names = data['prognosis'].unique()
print(classification_report(y_test, prediction_linear, target_names=target_names))

"""Export Model"""

# Menyimpan model dalam format SavedModel
export_dir = 'saved_model/'
tf.saved_model.save(model_s, export_dir)

# Convert SavedModel menjadi vegs.tflite
converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
tflite_model = converter.convert()

import pathlib
tflite_model_file = pathlib.Path('capstone.tflite')
tflite_model_file.write_bytes(tflite_model)